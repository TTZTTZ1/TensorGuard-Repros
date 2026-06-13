#!/usr/bin/env python3
"""
Generate an API-grouped review report for TitanFuzz result sources.

This script does not execute PyTorch programs. It scans the generated source
files and their embedded TitanFuzz result metadata, then separates:

- focus candidates that deserve manual review, grouped by API;
- excluded generated-code/common-user-error/tool-limit cases;
- per-API summaries and root-cause clusters.

Run from the TitanFuzz root on the server:

  python TensorGuard-Repros/scripts/generate_api_cluster_review.py \
    --results-dir Results/torch \
    --repo-dir TensorGuard-Repros
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


STRONG_PATTERNS = [
    r"INTERNAL ASSERT FAILED",
    r"please report a bug",
    r"Segmentation fault",
    r"Floating point exception",
    r"double free",
    r"corruption",
    r"free\(\):",
    r"invalid pointer",
    r"invalid next size",
    r"Check failed",
    r"FATAL",
    r"Aborted",
    r"returncode=-11",
    r"returncode=-8",
    r"returncode=-6",
    r"returncode=139",
    r"returncode=136",
    r"returncode=134",
]

CUDA_ASSERT_PATTERNS = [
    r"device-side assert",
    r"cudaErrorAssert",
    r"AcceleratorError CUDA error",
]

LOGIC_CATCH_PATTERNS = [
    r"VarInconsistentCatch",
    r"ComparisonFail",
]

GENERATED_CODE_PATTERNS = [
    r"unterminated triple-quoted string literal",
    r"expected an indented block",
    r"invalid syntax",
    r"NameError",
    r"name '.*' is not defined",
    r"kwargs' is not defined",
    r"device' is not defined",
    r"module '.*' has no attribute",
    r"No module named",
]

TOOL_OR_ENV_PATTERNS = [
    r"invalid device ordinal",
    r"unsupported tensor layout: SparseCsr",
    r"trying to initialize the default process group twice",
]

COMMON_USER_ERROR_PATTERNS = [
    r"shape .* is invalid",
    r"invalid shape",
    r"size mismatch",
    r"sizes? of tensors? must match",
    r"must match the size",
    r"expected .* got",
    r"expected .* but got",
    r"takes .* positional argument",
    r"takes .* arguments?",
    r"missing .* required",
    r"required positional argument",
    r"got an unexpected keyword",
    r"not implemented for",
    r"doesn't apply to",
    r"must be Tensor",
    r"must be .*Tensor",
    r"must be in the range",
    r"out of range",
    r"Class values must be non-negative",
    r"all elements of input should be between 0 and 1",
    r"invalid multinomial distribution",
    r"invalid Poisson rate",
]

NOISE_PATTERNS = [
    r"\bout\s*=",
    r"\.resize_?\(",
    r"\.numpy\(",
    r"\.data\b",
    r"torch\.empty",
    r"empty_like",
    r"Generator\(",
    r"\.seed\(",
    r"manual_seed",
    r"max_unpool",
    r"MaxUnpool",
    r"allow_tf32",
    r"torch\.log",
    r"torch\.sqrt",
    r"\.sqrt\(",
    r"\.log\(",
    r"\.pow\(",
    r"pow\(",
    r"nan",
    r"inf",
    r"float16",
    r"bfloat16",
]

STATUS_DIRS = {"valid", "exception", "crash", "notarget"}


@dataclass
class SourceRecord:
    api: str
    label: str
    status: str
    path: str
    decision: str
    category: str
    priority: str
    signal: str
    reason: str
    exception_type: str
    error_message: str
    trigger_line: str
    snippet: str
    cluster_key: str


def log(message: str) -> None:
    print(f"[api-cluster-review] {message}", flush=True)


def has_any(patterns: Iterable[str], text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns)


def matched_patterns(patterns: Iterable[str], text: str, limit: int = 4) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            hits.append(pattern)
        if len(hits) >= limit:
            break
    return hits


def one_line(text: str, limit: int = 260) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:limit]


def label_to_api(label: str) -> str:
    match = re.match(r"(.+)_\d+$", label)
    return match.group(1) if match else label


def split_initial_docstring(text: str) -> tuple[str, str, bool]:
    stripped = text.lstrip()
    leading = len(text) - len(stripped)
    if not (stripped.startswith('"""') or stripped.startswith("'''")):
        return "", text, True
    delim = stripped[:3]
    start = leading + 3
    end = text.find(delim, start)
    if end < 0:
        return text[start:], "", False
    return text[start:end], text[end + 3 :], True


def extract_json_metadata(meta: str) -> tuple[str, str]:
    exception_type = ""
    error_message = ""
    for match in re.finditer(r"\{.*?\}", meta, re.DOTALL):
        raw = match.group(0)
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        exception_type = str(obj.get("exception", exception_type) or "")
        error_message = str(obj.get("msg", error_message) or "")
        if exception_type or error_message:
            break
    if not error_message:
        msg_match = re.search(r"msg['\"]?\s*[:=]\s*['\"]([^'\"]+)", meta)
        if msg_match:
            error_message = msg_match.group(1)
    return exception_type, error_message


def extract_returncode(meta: str) -> str:
    match = re.search(r"returncode\s*=\s*(-?\d+)", meta)
    if match:
        return f"returncode={match.group(1)}"
    return ""


def code_syntax_error(code: str) -> str:
    if not code.strip():
        return ""
    try:
        ast.parse(code)
    except SyntaxError as exc:
        msg = exc.msg or "SyntaxError"
        return f"SyntaxError: {msg} at line {exc.lineno}"
    return ""


def first_code_snippet(code: str, max_lines: int = 8) -> str:
    lines: list[str] = []
    for raw in code.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        lines.append(line.strip())
        if len(lines) >= max_lines:
            break
    return " | ".join(lines)


def find_trigger_line(api: str, code: str) -> str:
    api_tail = api.split(".")[-1].rstrip("_")
    for idx, raw in enumerate(code.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if api in line or api_tail and api_tail in line:
            return f"{idx}: {line}"
    for idx, raw in enumerate(code.splitlines(), 1):
        line = raw.strip()
        if line and not line.startswith("#"):
            return f"{idx}: {line}"
    return ""


def normalize_message(text: str) -> str:
    normalized = text.lower()
    normalized = re.sub(r'"/[^"]+"', '"<path>"', normalized)
    normalized = re.sub(r"'/[^']+'", "'<path>'", normalized)
    normalized = re.sub(r"\b0x[0-9a-f]+\b", "<hex>", normalized)
    normalized = re.sub(r"\b\d+(?:\.\d+)?\b", "<num>", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized[:180]


def classify_record(path: Path, text: str) -> SourceRecord:
    label = path.stem
    api = label_to_api(label)
    status = path.parent.name if path.parent.name in STATUS_DIRS else path.parent.name
    meta, code, docstring_closed = split_initial_docstring(text)
    exception_type, json_message = extract_json_metadata(meta)
    syntax_error = code_syntax_error(code) if docstring_closed else "SyntaxError: unclosed initial docstring"
    returncode = extract_returncode(meta)
    evidence_text = "\n".join(part for part in [meta, json_message, syntax_error] if part)
    combined_text = "\n".join(part for part in [meta, json_message, syntax_error, code] if part)
    error_message = one_line(json_message or syntax_error or returncode or meta)
    trigger_line = find_trigger_line(api, code)
    snippet = one_line(first_code_snippet(code), 500)

    if not docstring_closed or syntax_error:
        category = "generated_code_error"
        reason = "源码语法不完整或无法解析，属于生成代码错误，不进入重点人工审核"
        signal = syntax_error or "unclosed initial docstring"
        decision = "exclude"
        priority = "X1"
    elif has_any(TOOL_OR_ENV_PATTERNS, combined_text):
        category = "tool_or_environment_limit"
        reason = "工具或运行环境限制，不作为 PyTorch bug 重点候选"
        signal = ", ".join(matched_patterns(TOOL_OR_ENV_PATTERNS, combined_text))
        decision = "exclude"
        priority = "X2"
    elif has_any(GENERATED_CODE_PATTERNS, combined_text):
        category = "generated_code_error"
        reason = "生成代码引用不存在变量/属性/模块，优先排除"
        signal = ", ".join(matched_patterns(GENERATED_CODE_PATTERNS, combined_text))
        decision = "exclude"
        priority = "X1"
    elif has_any(STRONG_PATTERNS, evidence_text):
        sparse_caveat = "sparse" in api.lower() or "sparse" in str(path).lower()
        category = "strong_backend_failure_sparse_caveat" if sparse_caveat else "strong_backend_failure"
        reason = "匹配论文附录风格的底层失败：internal assert/native crash/FPE/free()/Check failed"
        if sparse_caveat:
            reason += "；但 sparse invariant 需要单独确认"
        signal = ", ".join(matched_patterns(STRONG_PATTERNS, evidence_text))
        decision = "focus"
        priority = "P1"
    elif has_any(CUDA_ASSERT_PATTERNS, evidence_text):
        category = "cpu_gpu_exception_mismatch_candidate"
        reason = "包含 CUDA device-side assert/AcceleratorError，需检查 CPU 是否是正常 RuntimeError"
        signal = ", ".join(matched_patterns(CUDA_ASSERT_PATTERNS, evidence_text))
        decision = "focus"
        priority = "P2"
    elif has_any(LOGIC_CATCH_PATTERNS, evidence_text):
        if has_any(NOISE_PATTERNS, combined_text):
            category = "low_value_logic_noise"
            reason = "逻辑差异疑似由 alias/resize/numpy/TF32/NaN 边界等噪声触发"
            signal = ", ".join(matched_patterns(LOGIC_CATCH_PATTERNS + NOISE_PATTERNS, combined_text))
            decision = "exclude"
            priority = "X4"
        else:
            category = "clean_logic_inconsistency_candidate"
            reason = "存在逻辑/输出不一致信号，且未命中主要噪声模式"
            signal = ", ".join(matched_patterns(LOGIC_CATCH_PATTERNS, evidence_text))
            decision = "focus"
            priority = "P3"
    elif has_any(COMMON_USER_ERROR_PATTERNS, combined_text):
        category = "common_user_or_argument_error"
        reason = "普通参数/shape/dtype/range 错误，不作为底层 bug 重点候选"
        signal = ", ".join(matched_patterns(COMMON_USER_ERROR_PATTERNS, combined_text))
        decision = "exclude"
        priority = "X3"
    elif status in {"exception", "crash", "notarget"} and (exception_type or error_message or returncode):
        category = "low_signal_unclassified_exception"
        reason = "有异常记录但未命中底层 bug/逻辑不一致信号，暂不进入重点审核"
        signal = exception_type or returncode or "exception metadata"
        decision = "exclude"
        priority = "X9"
    else:
        category = "no_embedded_error_signal"
        reason = "未发现嵌入式异常/崩溃信号"
        signal = ""
        decision = "exclude"
        priority = "X0"

    cluster_basis = error_message or signal or category
    cluster_key = f"{api}|{category}|{normalize_message(cluster_basis)}"
    return SourceRecord(
        api=api,
        label=label,
        status=status,
        path=str(path),
        decision=decision,
        category=category,
        priority=priority,
        signal=signal,
        reason=reason,
        exception_type=exception_type,
        error_message=error_message,
        trigger_line=trigger_line,
        snippet=snippet,
        cluster_key=cluster_key,
    )


def iter_source_files(results_dir: Path) -> list[Path]:
    paths = []
    for status in STATUS_DIRS:
        subdir = results_dir / status
        if subdir.exists():
            paths.extend(sorted(subdir.glob("*.py")))
    return sorted(paths)


def write_tsv(path: Path, rows: list[SourceRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "api",
        "label",
        "status",
        "path",
        "decision",
        "category",
        "priority",
        "signal",
        "reason",
        "exception_type",
        "error_message",
        "trigger_line",
        "snippet",
        "cluster_key",
    ]
    with path.open("w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(fields)
        for row in rows:
            writer.writerow([getattr(row, field) for field in fields])


def write_api_summary(path: Path, rows: list[SourceRecord]) -> None:
    by_api: dict[str, list[SourceRecord]] = defaultdict(list)
    for row in rows:
        by_api[row.api].append(row)
    categories = sorted({row.category for row in rows})
    statuses = sorted({row.status for row in rows})
    with path.open("w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(
            ["api", "total", "focus_total", "excluded_total"]
            + [f"category:{category}" for category in categories]
            + [f"status:{status}" for status in statuses]
        )
        for api in sorted(by_api):
            items = by_api[api]
            category_counts = Counter(row.category for row in items)
            status_counts = Counter(row.status for row in items)
            writer.writerow(
                [
                    api,
                    len(items),
                    sum(1 for row in items if row.decision == "focus"),
                    sum(1 for row in items if row.decision == "exclude"),
                ]
                + [category_counts.get(category, 0) for category in categories]
                + [status_counts.get(status, 0) for status in statuses]
            )


def write_cluster_summary(path: Path, rows: list[SourceRecord]) -> None:
    clusters: dict[str, list[SourceRecord]] = defaultdict(list)
    for row in rows:
        clusters[row.cluster_key].append(row)
    with path.open("w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(
            [
                "api",
                "decision",
                "category",
                "priority",
                "count",
                "representative_label",
                "representative_path",
                "representative_message",
                "member_labels",
            ]
        )
        for key, items in sorted(
            clusters.items(),
            key=lambda kv: (kv[1][0].api, kv[1][0].decision != "focus", kv[1][0].category, -len(kv[1])),
        ):
            first = items[0]
            writer.writerow(
                [
                    first.api,
                    first.decision,
                    first.category,
                    first.priority,
                    len(items),
                    first.label,
                    first.path,
                    first.error_message or first.signal,
                    ",".join(item.label for item in items[:50]),
                ]
            )


def write_focus_report(path: Path, focus_rows: list[SourceRecord], all_rows: list[SourceRecord]) -> None:
    by_api: dict[str, list[SourceRecord]] = defaultdict(list)
    for row in focus_rows:
        by_api[row.api].append(row)
    category_counts = Counter(row.category for row in all_rows)
    focus_category_counts = Counter(row.category for row in focus_rows)
    lines = [
        "# API Focus Review Report",
        "",
        "本报告按 API 聚合，只列出需要人工重点考虑的错误源码；生成代码错误和普通参数错误不进入本报告主体，但会在 TSV 中完整记录。",
        "",
        "## Overall",
        "",
        f"- Scanned source files: {len(all_rows)}",
        f"- Focus candidates: {len(focus_rows)}",
        f"- APIs with focus candidates: {len(by_api)}",
        "",
        "Focus categories:",
    ]
    for category, count in sorted(focus_category_counts.items()):
        lines.append(f"- `{category}`: {count}")
    lines.extend(["", "All categories, including excluded ones:"])
    for category, count in sorted(category_counts.items()):
        lines.append(f"- `{category}`: {count}")
    lines.extend(["", "## APIs", ""])

    for api in sorted(by_api):
        items = sorted(by_api[api], key=lambda row: (row.priority, row.category, row.label))
        lines.append(f"### {api}")
        lines.append("")
        lines.append(f"Focus candidates: {len(items)}")
        lines.append("")
        for row in items:
            message = row.error_message or row.signal
            lines.append(f"- `{row.label}` `{row.status}` `{row.category}`")
            lines.append(f"  - path: `{row.path}`")
            lines.append(f"  - signal: {row.signal or 'n/a'}")
            lines.append(f"  - message: {message or 'n/a'}")
            lines.append(f"  - trigger: {row.trigger_line or 'n/a'}")
            lines.append(f"  - snippet: `{row.snippet or 'n/a'}`")
            lines.append(f"  - action: {row.reason}")
        lines.append("")

    path.write_text("\n".join(lines) + "\n")


def write_readme(path: Path, focus_rows: list[SourceRecord], excluded_rows: list[SourceRecord]) -> None:
    lines = [
        "# API Cluster Review",
        "",
        "This directory is generated by `scripts/generate_api_cluster_review.py`.",
        "",
        "Files:",
        "",
        "- `api_focus_report.md`: API-grouped manual review report containing only meaningful bug-like candidates.",
        "- `focus_candidates.tsv`: complete focus candidate table. This is the authoritative all-candidate list.",
        "- `excluded_generated_or_common_errors.tsv`: generated-code errors, common user errors, tool limits, and low-signal exceptions.",
        "- `api_summary.tsv`: per-API counts across focus and excluded categories.",
        "- `cluster_summary.tsv`: root-cause style clusters by API/category/normalized message.",
        "",
        "Interpretation:",
        "",
        "- Focus candidates are not automatically confirmed bugs. They are the cases worth manual reading, reproduction, and minimization.",
        "- Excluded rows are still recorded to show that generated-code and ordinary errors were considered, not ignored.",
        "",
        f"Focus candidates: {len(focus_rows)}",
        f"Excluded rows: {len(excluded_rows)}",
        "",
    ]
    path.write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="Results/torch")
    parser.add_argument("--repo-dir", default="TensorGuard-Repros")
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    repo_dir = Path(args.repo_dir)
    out_dir = Path(args.out_dir) if args.out_dir else repo_dir / "logs" / "api_cluster_review"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not results_dir.exists():
        raise SystemExit(f"results dir not found: {results_dir}")

    source_files = iter_source_files(results_dir)
    log(f"source files: {len(source_files)}")
    rows: list[SourceRecord] = []
    for idx, path in enumerate(source_files, 1):
        try:
            text = path.read_text(errors="replace")
        except OSError as exc:
            log(f"skip unreadable file: {path}: {exc}")
            continue
        rows.append(classify_record(path, text))
        if idx % 5000 == 0:
            log(f"processed {idx}/{len(source_files)}")

    rows = sorted(rows, key=lambda row: (row.api, row.decision != "focus", row.priority, row.category, row.label))
    focus_rows = [row for row in rows if row.decision == "focus"]
    excluded_rows = [row for row in rows if row.decision != "focus"]

    write_tsv(out_dir / "focus_candidates.tsv", focus_rows)
    write_tsv(out_dir / "excluded_generated_or_common_errors.tsv", excluded_rows)
    write_api_summary(out_dir / "api_summary.tsv", rows)
    write_cluster_summary(out_dir / "cluster_summary.tsv", rows)
    write_focus_report(out_dir / "api_focus_report.md", focus_rows, rows)
    write_readme(out_dir / "README.md", focus_rows, excluded_rows)

    log(f"wrote output to: {out_dir}")
    log(f"focus candidates: {len(focus_rows)}")
    log(f"excluded rows: {len(excluded_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
