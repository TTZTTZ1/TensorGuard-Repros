#!/usr/bin/env python3
"""
Generate a trace-driven review report for TitanFuzz CPU/GPU mismatches.

This script does not execute PyTorch programs. It parses Results/torch/trace.txt,
maps interesting TitanFuzzTestcase entries back to generated source files, and
separates candidates worth manual reproduction from common low-value noise.

Run from /workspace/TitanFuzz on the server:

  python TensorGuard-Repros/scripts/generate_trace_logic_review.py \
    --results-dir Results/torch \
    --repo-dir TensorGuard-Repros
"""

from __future__ import annotations

import argparse
import ast
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


TARGET_CATCHES = {
    "VarInconsistentCatch",
    "ComparisonFail",
    "GpuCrashCatch",
    "FrameworkCrashCatch",
    "GpuExecFail",
    "ExceptMsgCatch",
}

SOURCE_DIRS = ("valid", "exception", "crash", "notarget", "seed")

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
    r"malloc",
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

GENERATED_CODE_PATTERNS = [
    r"unterminated triple-quoted string literal",
    r"expected an indented block",
    r"invalid syntax",
    r"SyntaxError",
    r"NameError",
    r"name '.*' is not defined",
    r"kwargs' is not defined",
    r"device' is not defined",
    r"module '.*' has no attribute",
    r"No module named",
]

ENVIRONMENT_PATTERNS = [
    r"invalid device ordinal",
    r"CUDA-capable device\(s\) is/are busy or unavailable",
    r"no CUDA GPUs are available",
    r"CUDA out of memory",
    r"Default process group has not been initialized",
    r"trying to initialize the default process group twice",
]

COMMON_ARGUMENT_PATTERNS = [
    r"TypeError",
    r"ValueError",
    r"IndexError",
    r"can't index",
    r"not supported",
    r"not a valid",
    r"invalid argument",
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

ALIAS_OR_MUTATION_PATTERNS = [
    r"\bout\s*=",
    r"\.resize_?\(",
    r"\.resize_as_?\(",
    r"\.numpy\(",
    r"\.data\b",
    r"\.set_\(",
    r"as_strided",
]

UNINITIALIZED_PATTERNS = [
    r"torch\.empty",
    r"empty_like",
    r"empty_strided",
    r"resize_",
    r"resize_as_",
    r"uninitialized",
    r"UninitializedBuffer",
    r"UninitializedParameter",
    r"Lazy[A-Z]",
]

NUMERIC_BOUNDARY_PATTERNS = [
    r"torch\.log",
    r"torch\.sqrt",
    r"torch\.rsqrt",
    r"torch\.pow",
    r"\.sqrt\(",
    r"\.rsqrt\(",
    r"\.log\(",
    r"\.pow\(",
    r"nan",
    r"inf",
    r"float16",
    r"bfloat16",
]

METADATA_API_PATTERNS = [
    r"\.get_device$",
    r"\.data_ptr$",
    r"\.is_shared$",
    r"\.share_memory_$",
    r"\.size$",
    r"\.sparse_dim$",
    r"\.dim$",
    r"\.is_set_to$",
    r"Storage$",
]

NUMERIC_API_PATTERNS = [
    r"conv",
    r"matmul",
    r"\.mm$",
    r"\.bmm$",
    r"addmm",
    r"addbmm",
    r"linalg",
    r"\.svd$",
    r"\.eigh$",
    r"\.qr$",
    r"\.fft",
    r"ctc_loss",
    r"det$",
    r"logdet$",
    r"pinverse$",
]

ALREADY_REVIEWED_LABELS = {
    "torch.is_nonzero_2006",
    "torch.sparse.mm_142",
    "torch.sparse_csr_tensor_516",
    "torch.Tensor.addmm__1173",
    "torch.Tensor.t_407",
    "torch.mean_289",
    "torch.Tensor.addcdiv_153",
}


@dataclass
class TraceEntry:
    case_id: str
    api: str
    label: str
    catch: str
    seed: str
    header: str
    block: str


@dataclass
class ReviewRecord:
    decision: str
    priority: str
    category: str
    catch: str
    api: str
    label: str
    source: str
    reason: str
    evidence: str
    snippet: str
    trace_head: str


def log(message: str) -> None:
    print(f"[trace-logic-review] {message}", flush=True)


def has_any(patterns: Iterable[str], text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in patterns)


def matching_patterns(patterns: Iterable[str], text: str, limit: int = 4) -> list[str]:
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


def syntax_error(text: str) -> str:
    if not text.strip():
        return ""
    try:
        ast.parse(text)
    except SyntaxError as exc:
        return f"SyntaxError: {exc.msg} at line {exc.lineno}"
    return ""


def source_snippet(text: str, max_lines: int = 8) -> str:
    _meta, code, _closed = split_initial_docstring(text)
    lines: list[str] = []
    for raw in code.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
        if len(lines) >= max_lines:
            break
    return " | ".join(lines)


def iter_trace_entries(trace_path: Path) -> Iterator[TraceEntry]:
    current: dict[str, str] | None = None
    block_lines: list[str] = []
    block_chars = 0
    max_block_chars = 12000

    def flush() -> TraceEntry | None:
        if current is None:
            return None
        return TraceEntry(
            case_id=current["case_id"],
            api=current["api"],
            label=current["label"],
            catch=current["catch"],
            seed=current["seed"],
            header=current["header"],
            block="\n".join(block_lines),
        )

    with trace_path.open(errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if line.startswith("TitanFuzzTestcase "):
                entry = flush()
                if entry is not None:
                    yield entry
                parts = line.split(maxsplit=6)
                current = None
                block_lines = []
                block_chars = 0
                if len(parts) < 6:
                    continue
                catch = parts[4]
                if catch not in TARGET_CATCHES:
                    continue
                current = {
                    "case_id": parts[1],
                    "api": parts[2],
                    "label": parts[3],
                    "catch": catch,
                    "seed": parts[5],
                    "header": line,
                }
                block_lines = [line]
                block_chars = len(line)
                continue

            if current is not None and block_chars < max_block_chars:
                block_lines.append(line)
                block_chars += len(line) + 1

    entry = flush()
    if entry is not None:
        yield entry


def count_trace_statuses(trace_path: Path) -> tuple[Counter[str], Counter[str]]:
    catch_counts: Counter[str] = Counter()
    logic_api_counts: Counter[str] = Counter()
    with trace_path.open(errors="replace") as handle:
        for raw in handle:
            if not raw.startswith("TitanFuzzTestcase "):
                continue
            parts = raw.split(maxsplit=6)
            if len(parts) < 5:
                continue
            catch_counts[parts[4]] += 1
            if parts[4] in {"VarInconsistentCatch", "ComparisonFail"}:
                logic_api_counts[parts[2]] += 1
    return catch_counts, logic_api_counts


def find_source(results_dir: Path, label: str) -> Path | None:
    for status_dir in SOURCE_DIRS:
        path = results_dir / status_dir / f"{label}.py"
        if path.exists():
            return path
    matches = list(results_dir.glob(f"*/{label}.py"))
    return matches[0] if matches else None


def classify(entry: TraceEntry, source_path: Path | None, source_text: str) -> ReviewRecord:
    source = str(source_path) if source_path is not None else ""
    combined = "\n".join([entry.header, entry.block, source_text])
    snippet = source_snippet(source_text) if source_text else ""
    trace_head = one_line(entry.block, 360)
    syntax = syntax_error(source_text) if source_text else ""

    evidence_hits: list[str] = []

    if source_path is None:
        return ReviewRecord(
            decision="exclude",
            priority="P9",
            category="missing_source",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source="",
            reason="trace entry has no matching generated .py source file",
            evidence="",
            snippet="",
            trace_head=trace_head,
        )

    if entry.label in ALREADY_REVIEWED_LABELS:
        evidence_hits.append("already_reviewed")

    if has_any(STRONG_PATTERNS, combined) or entry.catch in {"FrameworkCrashCatch", "GpuCrashCatch"}:
        evidence_hits.extend(matching_patterns(STRONG_PATTERNS, combined))
        category = "strong_backend_failure"
        reason = "native crash/internal assert style signal; verify with an independent minimal repro"
        if "sparse" in entry.api:
            category = "strong_backend_failure_sparse_caveat"
            reason = "native crash signal in sparse path; check whether invalid sparse invariants make it non-reportable"
        return ReviewRecord(
            decision="focus",
            priority="P1",
            category=category,
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason=reason,
            evidence=", ".join(evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if syntax or has_any(GENERATED_CODE_PATTERNS, combined):
        evidence_hits.extend(matching_patterns(GENERATED_CODE_PATTERNS, combined))
        if syntax:
            evidence_hits.insert(0, syntax)
        return ReviewRecord(
            decision="exclude",
            priority="P8",
            category="generated_code_error",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="generated program is syntactically invalid or references undefined names",
            evidence=", ".join(evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if has_any(ENVIRONMENT_PATTERNS, combined):
        evidence_hits.extend(matching_patterns(ENVIRONMENT_PATTERNS, combined))
        return ReviewRecord(
            decision="exclude",
            priority="P8",
            category="tool_or_environment_limit",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="environment/tooling issue rather than a PyTorch semantic bug",
            evidence=", ".join(evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if entry.catch == "GpuExecFail":
        common = matching_patterns(COMMON_ARGUMENT_PATTERNS, combined)
        cuda_assert = has_any([r"device-side assert", r"cudaErrorAssert", r"AcceleratorError CUDA error"], combined)
        if not cuda_assert:
            return ReviewRecord(
                decision="exclude",
                priority="P6",
                category="gpu_exec_regular_exception",
                catch=entry.catch,
                api=entry.api,
                label=entry.label,
                source=source,
                reason="GPU-only failure has no CUDA assert/native-crash signal; likely generated API misuse or regular exception",
                evidence=", ".join(common),
                snippet=snippet,
                trace_head=trace_head,
            )
        evidence_hits.extend(matching_patterns([r"device-side assert", r"cudaErrorAssert", r"AcceleratorError CUDA error"], combined))
        return ReviewRecord(
            decision="focus",
            priority="P2",
            category="gpu_exec_or_cuda_assert_mismatch",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="CPU/GPU behavior may differ; run CPU and CUDA in independent processes",
            evidence=", ".join(evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if entry.catch == "ExceptMsgCatch":
        common = matching_patterns(COMMON_ARGUMENT_PATTERNS, combined)
        return ReviewRecord(
            decision="exclude",
            priority="P6",
            category="exception_message_difference_low_value",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="exception message differs, but there is no native-crash/CUDA-assert signal; keep out of the main bug queue",
            evidence=", ".join(common),
            snippet=snippet,
            trace_head=trace_head,
        )

    metadata_api = has_any(METADATA_API_PATTERNS, entry.api)
    alias_hits = matching_patterns(ALIAS_OR_MUTATION_PATTERNS, source_text)
    uninit_hits = matching_patterns(UNINITIALIZED_PATTERNS, source_text)
    boundary_hits = matching_patterns(NUMERIC_BOUNDARY_PATTERNS, source_text)

    if metadata_api:
        return ReviewRecord(
            decision="exclude",
            priority="P6",
            category="device_or_metadata_semantics",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="API reports device, pointer, storage, or metadata that naturally differs between CPU and CUDA",
            evidence=", ".join(evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if alias_hits:
        return ReviewRecord(
            decision="exclude",
            priority="P5",
            category="alias_or_mutation_semantics",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="source mutates aliased/out/numpy/resize state; this family was judged low-value unless it crashes hard",
            evidence=", ".join(alias_hits + evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if uninit_hits:
        return ReviewRecord(
            decision="exclude",
            priority="P5",
            category="uninitialized_or_lazy_state",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="source likely reads uninitialized/lazy state, so CPU/GPU contents are not expected to match",
            evidence=", ".join(uninit_hits + evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if boundary_hits:
        return ReviewRecord(
            decision="exclude",
            priority="P5",
            category="nan_inf_or_boundary_numeric",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="mismatch is likely amplified by NaN/Inf/log/sqrt/pow/low-precision boundary behavior",
            evidence=", ".join(boundary_hits + evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if "sparse" in entry.api:
        return ReviewRecord(
            decision="focus",
            priority="P2",
            category="sparse_logic_inconsistency_caveat",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="sparse CPU/GPU inconsistency; verify sparse invariants before treating as reportable",
            evidence=", ".join(evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if re.search(r"max_unpool|MaxUnpool", entry.api):
        return ReviewRecord(
            decision="focus",
            priority="P3",
            category="max_unpool_index_semantics",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="max_unpool index semantics need manual validation; keep as lower-priority trace candidate",
            evidence=", ".join(evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    if has_any(NUMERIC_API_PATTERNS, entry.api):
        return ReviewRecord(
            decision="focus",
            priority="P2",
            category="numeric_consistency_check_needed",
            catch=entry.catch,
            api=entry.api,
            label=entry.label,
            source=source,
            reason="numeric CPU/GPU mismatch; rerun with TF32 disabled and tolerance checks before reporting",
            evidence=", ".join(evidence_hits),
            snippet=snippet,
            trace_head=trace_head,
        )

    category = "final_output_inconsistency" if entry.catch == "ComparisonFail" else "logic_inconsistency_needs_review"
    priority = "P2" if entry.catch == "ComparisonFail" else "P3"
    return ReviewRecord(
        decision="focus",
        priority=priority,
        category=category,
        catch=entry.catch,
        api=entry.api,
        label=entry.label,
        source=source,
        reason="CPU/GPU inconsistency without an obvious low-value pattern",
        evidence=", ".join(evidence_hits),
        snippet=snippet,
        trace_head=trace_head,
    )


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def record_to_row(record: ReviewRecord) -> dict[str, str]:
    return {
        "priority": record.priority,
        "category": record.category,
        "catch": record.catch,
        "api": record.api,
        "label": record.label,
        "source": record.source,
        "reason": record.reason,
        "evidence": record.evidence,
        "snippet": record.snippet,
        "trace_head": record.trace_head,
    }


def write_report(
    out_dir: Path,
    results_dir: Path,
    catch_counts: Counter[str],
    logic_api_counts: Counter[str],
    records: list[ReviewRecord],
) -> None:
    focus = [record for record in records if record.decision == "focus"]
    excluded = [record for record in records if record.decision == "exclude"]
    category_counts = Counter(record.category for record in records)
    focus_api_counts = Counter(record.api for record in focus)

    lines: list[str] = []
    lines.append("# Trace Logic Review")
    lines.append("")
    lines.append(f"- Results dir: `{results_dir}`")
    lines.append(f"- Reviewed trace candidates: `{len(records)}`")
    lines.append(f"- Focus candidates: `{len(focus)}`")
    lines.append(f"- Excluded/noise candidates: `{len(excluded)}`")
    lines.append("")
    lines.append("## Catch Counts")
    lines.append("")
    lines.append("| catch | count |")
    lines.append("| --- | ---: |")
    for catch, count in catch_counts.most_common():
        lines.append(f"| `{catch}` | {count} |")
    lines.append("")
    lines.append("## Focus Categories")
    lines.append("")
    lines.append("| category | count |")
    lines.append("| --- | ---: |")
    for category, count in Counter(record.category for record in focus).most_common():
        lines.append(f"| `{category}` | {count} |")
    lines.append("")
    lines.append("## Excluded Categories")
    lines.append("")
    lines.append("| category | count |")
    lines.append("| --- | ---: |")
    for category, count in Counter(record.category for record in excluded).most_common():
        lines.append(f"| `{category}` | {count} |")
    lines.append("")
    lines.append("## Top Logic APIs In Raw Trace")
    lines.append("")
    lines.append("| api | VarInconsistentCatch + ComparisonFail |")
    lines.append("| --- | ---: |")
    for api, count in logic_api_counts.most_common(40):
        lines.append(f"| `{api}` | {count} |")
    lines.append("")
    lines.append("## Top Focus APIs")
    lines.append("")
    lines.append("| api | focus candidates |")
    lines.append("| --- | ---: |")
    for api, count in focus_api_counts.most_common(60):
        lines.append(f"| `{api}` | {count} |")
    lines.append("")
    lines.append("## First Focus Candidates By Category")
    lines.append("")
    by_category: dict[str, list[ReviewRecord]] = defaultdict(list)
    for record in focus:
        by_category[record.category].append(record)
    for category, _count in Counter(record.category for record in focus).most_common():
        lines.append(f"### {category}")
        lines.append("")
        for record in by_category[category][:20]:
            lines.append(
                f"- `{record.priority}` `{record.catch}` `{record.api}` `{record.label}` "
                f"source=`{record.source}`"
            )
            lines.append(f"  - reason: {record.reason}")
            if record.evidence:
                lines.append(f"  - evidence: `{record.evidence}`")
            if record.snippet:
                lines.append(f"  - snippet: `{record.snippet}`")
        lines.append("")
    lines.append("## Suggested Server Review Command")
    lines.append("")
    lines.append("```bash")
    lines.append("cd /workspace/TitanFuzz")
    lines.append("python TensorGuard-Repros/scripts/generate_trace_logic_review.py \\")
    lines.append("  --results-dir Results/torch \\")
    lines.append("  --repo-dir TensorGuard-Repros")
    lines.append("```")
    lines.append("")
    lines.append("Then start manual reproduction from `logic_focus_candidates.tsv`, P1 first, then P2.")
    lines.append("")

    (out_dir / "logic_focus_report.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", required=True, type=Path)
    parser.add_argument("--repo-dir", required=True, type=Path)
    args = parser.parse_args()

    results_dir = args.results_dir
    trace_path = results_dir / "trace.txt"
    if not trace_path.exists():
        raise SystemExit(f"trace.txt not found: {trace_path}")

    out_dir = args.repo_dir / "logs" / "trace_logic_review"
    queue_dir = out_dir / "queues"
    out_dir.mkdir(parents=True, exist_ok=True)
    queue_dir.mkdir(parents=True, exist_ok=True)

    log(f"trace: {trace_path}")
    log("counting trace statuses")
    catch_counts, logic_api_counts = count_trace_statuses(trace_path)

    log("parsing interesting trace entries and classifying sources")
    source_cache: dict[str, tuple[Path | None, str]] = {}
    records: list[ReviewRecord] = []
    for idx, entry in enumerate(iter_trace_entries(trace_path), 1):
        if entry.label not in source_cache:
            path = find_source(results_dir, entry.label)
            text = ""
            if path is not None:
                try:
                    text = path.read_text(errors="replace")
                except OSError:
                    text = ""
            source_cache[entry.label] = (path, text)
        source_path, source_text = source_cache[entry.label]
        records.append(classify(entry, source_path, source_text))
        if idx % 5000 == 0:
            log(f"classified {idx} trace entries")

    focus = [record for record in records if record.decision == "focus"]
    excluded = [record for record in records if record.decision == "exclude"]
    focus.sort(key=lambda item: (item.priority, item.category, item.api, item.label, item.catch))
    excluded.sort(key=lambda item: (item.category, item.api, item.label, item.catch))

    fieldnames = [
        "priority",
        "category",
        "catch",
        "api",
        "label",
        "source",
        "reason",
        "evidence",
        "snippet",
        "trace_head",
    ]
    write_tsv(out_dir / "logic_focus_candidates.tsv", [record_to_row(record) for record in focus], fieldnames)
    write_tsv(out_dir / "logic_excluded_noise.tsv", [record_to_row(record) for record in excluded], fieldnames)

    api_rows = []
    grouped: dict[str, list[ReviewRecord]] = defaultdict(list)
    for record in records:
        grouped[record.api].append(record)
    for api, api_records in sorted(grouped.items()):
        api_rows.append(
            {
                "api": api,
                "total": str(len(api_records)),
                "focus": str(sum(1 for record in api_records if record.decision == "focus")),
                "excluded": str(sum(1 for record in api_records if record.decision == "exclude")),
                "catches": ";".join(f"{k}:{v}" for k, v in Counter(record.catch for record in api_records).most_common()),
                "categories": ";".join(f"{k}:{v}" for k, v in Counter(record.category for record in api_records).most_common()),
            }
        )
    write_tsv(
        out_dir / "logic_api_summary.tsv",
        api_rows,
        ["api", "total", "focus", "excluded", "catches", "categories"],
    )

    catch_rows = [{"catch": catch, "count": str(count)} for catch, count in catch_counts.most_common()]
    write_tsv(out_dir / "trace_catch_summary.tsv", catch_rows, ["catch", "count"])

    for priority in ("P1", "P2", "P3"):
        with (queue_dir / f"{priority.lower()}_sources.txt").open("w") as handle:
            for record in focus:
                if record.priority == priority and record.source:
                    handle.write(f"{record.source}\n")

    write_report(out_dir, results_dir, catch_counts, logic_api_counts, records)

    readme = [
        "# Trace Logic Review",
        "",
        "Generated from `trace.txt`, not from source-file embedded metadata.",
        "",
        "Files:",
        "",
        "- `logic_focus_report.md`: human-readable summary.",
        "- `logic_focus_candidates.tsv`: candidates to manually reproduce.",
        "- `logic_excluded_noise.tsv`: excluded low-value/generated/environment cases.",
        "- `logic_api_summary.tsv`: per-API totals and categories.",
        "- `trace_catch_summary.tsv`: raw TitanFuzz catch counts.",
        "- `queues/p1_sources.txt`, `queues/p2_sources.txt`, `queues/p3_sources.txt`: source paths for staged review.",
        "",
        "Review order: P1 first, then P2. P3 is useful only after the higher-priority set is exhausted.",
        "",
    ]
    (out_dir / "README.md").write_text("\n".join(readme))

    log(f"records: {len(records)}")
    log(f"focus: {len(focus)}")
    log(f"excluded: {len(excluded)}")
    log(f"wrote: {out_dir}")


if __name__ == "__main__":
    main()
