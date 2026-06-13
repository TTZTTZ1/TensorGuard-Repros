#!/usr/bin/env python3
"""
Generate the next TitanFuzz manual-audit queues.

Run from /workspace/TitanFuzz after pulling TensorGuard-Repros:

  python TensorGuard-Repros/scripts/generate_next_audit_queue.py \
    --results-dir Results/torch \
    --repo-dir TensorGuard-Repros

The output goes to TensorGuard-Repros/logs/audit_next/queues/.
"""

from __future__ import annotations

import argparse
import csv
import re
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

CUDA_ASSERT_PATTERNS = [
    r"device-side assert",
    r"cudaErrorAssert",
    r"AcceleratorError CUDA error",
]

# These are either already reviewed or are the known disputed alias families.
ALREADY_REVIEWED_LABELS = {
    "torch.is_nonzero_2006",
    "torch.sparse.mm_142",
    "torch.sparse_csr_tensor_516",
    "torch.Tensor.addmm__1173",
    "torch.Tensor.t_407",
    "torch.mean_289",
}

ALREADY_REVIEWED_API_HINTS = {
    "torch.quantile",
    "torch.nanquantile",
    "torch.multinomial",
    "torch.poisson",
    "torch.nn.BCELoss",
    "torch.nn.functional.binary_cross_entropy",
    "torch.nn.functional.embedding_bag",
    "torch.nn.functional.one_hot",
    "torch.nn.MultiMarginLoss",
}

# These patterns are noisy for "real PyTorch bug" auditing unless they also crash hard.
LOGIC_NOISE_PATTERNS = [
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
]

BOUNDARY_NUMERIC_PATTERNS = [
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

LABEL_RE = re.compile(r"(torch(?:\.[A-Za-z_][A-Za-z0-9_]*)+_+\d+)")


@dataclass
class Candidate:
    priority: str
    bucket: str
    label: str
    api: str
    source: str
    evidence: str
    reason: str
    score: int


def log(message: str) -> None:
    print(f"[generate-next-audit] {message}", flush=True)


def label_to_api(label: str) -> str:
    match = re.match(r"(.+)_\d+$", label)
    return match.group(1) if match else label


def has_any(patterns: Iterable[str], text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def first_matching_patterns(patterns: Iterable[str], text: str) -> list[str]:
    hits: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(pattern)
    return hits[:4]


def one_line(text: str, limit: int = 240) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:limit]


def score_strong(text: str, path: Path) -> int:
    score = 0
    if re.search(r"INTERNAL ASSERT FAILED|please report a bug", text, re.IGNORECASE):
        score += 100
    if re.search(r"Segmentation fault|returncode=-11|returncode=139", text, re.IGNORECASE):
        score += 95
    if re.search(r"Floating point exception|returncode=-8|returncode=136", text, re.IGNORECASE):
        score += 90
    if re.search(r"double free|free\(\):|invalid pointer|invalid next size|corruption", text, re.IGNORECASE):
        score += 85
    if re.search(r"Check failed|FATAL|Aborted|returncode=-6|returncode=134", text, re.IGNORECASE):
        score += 80
    if "sparse" in str(path):
        score -= 15
    return score


def source_snippet(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('"""') or line.startswith("'''"):
            continue
        if line.startswith("#"):
            continue
        lines.append(line)
        if len(lines) >= 5:
            break
    return " | ".join(lines)


def load_sources(results_dir: Path) -> tuple[dict[str, Path], dict[str, str]]:
    source_by_label: dict[str, Path] = {}
    text_by_label: dict[str, str] = {}
    paths = sorted(results_dir.glob("**/*.py"))
    log(f"indexing source files: {len(paths)} python files")
    for idx, path in enumerate(paths, 1):
        label = path.stem
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        source_by_label[label] = path
        text_by_label[label] = text
        if idx % 2000 == 0:
            log(f"indexed {idx}/{len(paths)} source files")
    log(f"indexed source labels: {len(source_by_label)}")
    return source_by_label, text_by_label


def candidates_from_sources(results_dir: Path) -> list[Candidate]:
    candidates: list[Candidate] = []
    source_by_label, text_by_label = load_sources(results_dir)

    log("scanning source-file embedded evidence")
    for idx, (label, text) in enumerate(text_by_label.items(), 1):
        path = source_by_label[label]
        rel = str(path)
        api = label_to_api(label)
        if has_any(STRONG_PATTERNS, text):
            hits = ", ".join(first_matching_patterns(STRONG_PATTERNS, text))
            candidates.append(
                Candidate(
                    priority="P1",
                    bucket="strong_crash_or_internal_assert",
                    label=label,
                    api=api,
                    source=rel,
                    evidence=hits,
                    reason="matches senior-paper bug style: internal assert / native crash / abort / free() / Check failed",
                    score=score_strong(text, path),
                )
            )
            continue

        if has_any(CUDA_ASSERT_PATTERNS, text):
            hits = ", ".join(first_matching_patterns(CUDA_ASSERT_PATTERNS, text))
            candidates.append(
                Candidate(
                    priority="P2",
                    bucket="cpu_gpu_exception_mismatch",
                    label=label,
                    api=api,
                    source=rel,
                    evidence=hits,
                    reason="CUDA device-side assert or AcceleratorError; audit CPU-vs-GPU error semantics",
                    score=60,
                )
            )
            continue

        if "VarInconsistentCatch" in text or "ComparisonFail" in text:
            if has_any(LOGIC_NOISE_PATTERNS, text):
                continue
            if has_any(BOUNDARY_NUMERIC_PATTERNS, text):
                score = 25
                bucket = "low_numeric_boundary_inconsistency"
                reason = "logic inconsistency, but includes numeric boundary/NaN/Inf pattern; audit after P1/P2"
            else:
                score = 40
                bucket = "clean_logic_inconsistency_candidate"
                reason = "logic inconsistency without obvious alias/numpy/resize/noisy pattern"
            candidates.append(
                Candidate(
                    priority="P3",
                    bucket=bucket,
                    label=label,
                    api=api,
                    source=rel,
                    evidence=source_snippet(text),
                    reason=reason,
                    score=score,
                )
            )
        if idx % 2000 == 0:
            log(f"scanned {idx}/{len(text_by_label)} source files")

    trace = results_dir / "trace.txt"
    if trace.exists():
        log(f"scanning trace evidence: {trace}")
        trace_text = trace.read_text(errors="replace")
        seen_trace_labels: set[str] = set()
        trace_matches = list(LABEL_RE.finditer(trace_text))
        log(f"trace label occurrences: {len(trace_matches)}")
        for idx, match in enumerate(trace_matches, 1):
            label = match.group(1)
            if label in seen_trace_labels:
                continue
            seen_trace_labels.add(label)
            if label not in source_by_label:
                continue
            api = label_to_api(label)
            pos = match.start()
            around = trace_text[max(0, pos - 600) : pos + 1600]
            path = source_by_label[label]
            if has_any(STRONG_PATTERNS, around):
                hits = ", ".join(first_matching_patterns(STRONG_PATTERNS, around))
                candidates.append(
                    Candidate(
                        priority="P1",
                        bucket="trace_strong_crash_or_internal_assert",
                        label=label,
                        api=api,
                        source=str(path),
                        evidence=hits,
                        reason="trace block near label contains strong crash/internal-assert evidence",
                        score=score_strong(around, path) + 5,
                    )
                )
            elif has_any(CUDA_ASSERT_PATTERNS, around):
                hits = ", ".join(first_matching_patterns(CUDA_ASSERT_PATTERNS, around))
                candidates.append(
                    Candidate(
                        priority="P2",
                        bucket="trace_cpu_gpu_exception_mismatch",
                        label=label,
                        api=api,
                        source=str(path),
                        evidence=hits,
                        reason="trace block near label contains CUDA assert evidence",
                        score=62,
                    )
                )
            if idx % 5000 == 0:
                log(f"processed {idx}/{len(trace_matches)} trace label occurrences")

        log(f"trace unique labels seen: {len(seen_trace_labels)}")

    log(f"raw candidates before dedupe: {len(candidates)}")
    return dedupe_candidates(candidates)


def dedupe_candidates(candidates: list[Candidate]) -> list[Candidate]:
    best: dict[str, Candidate] = {}
    for cand in candidates:
        old = best.get(cand.label)
        if old is None or cand.score > old.score:
            best[cand.label] = cand
    return sorted(best.values(), key=lambda c: (-c.score, c.priority, c.api, c.label))


def filter_unreviewed(candidates: list[Candidate]) -> list[Candidate]:
    kept = []
    for cand in candidates:
        if cand.label in ALREADY_REVIEWED_LABELS:
            continue
        if any(cand.api.startswith(api) for api in ALREADY_REVIEWED_API_HINTS):
            continue
        kept.append(cand)
    return kept


def write_tsv(path: Path, candidates: list[Candidate]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["priority", "bucket", "score", "api", "label", "source", "reason", "evidence"])
        for cand in candidates:
            writer.writerow(
                [
                    cand.priority,
                    cand.bucket,
                    cand.score,
                    cand.api,
                    cand.label,
                    cand.source,
                    cand.reason,
                    cand.evidence,
                ]
            )


def write_summary(path: Path, all_candidates: list[Candidate], unreviewed: list[Candidate]) -> None:
    def count_by(items: list[Candidate], attr: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in items:
            key = getattr(item, attr)
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items()))

    p1 = [c for c in unreviewed if c.priority == "P1"]
    p2 = [c for c in unreviewed if c.priority == "P2"]
    p3 = [c for c in unreviewed if c.priority == "P3"]
    lines = [
        "# Next PyTorch Audit Queues",
        "",
        "This queue is generated from TitanFuzz result files and trace evidence.",
        "",
        "Ranking policy:",
        "- P1: internal assert, native crash, abort, `free()`, FPE, segfault, `Check failed`.",
        "- P2: CPU/GPU exception mismatch, especially CUDA device-side assert.",
        "- P3: clean CPU/GPU logic inconsistency after filtering obvious alias/numpy/resize/noisy patterns.",
        "",
        "Known senior-review adjustment:",
        "- Previously collected `out=input`, in-place alias, transpose-view alias, and numpy-view cases are not prioritized as PyTorch bugs.",
        "- Sparse invariant crashes are kept as evidence family, but new sparse candidates need the invariant caveat checked.",
        "",
        f"Total candidates before already-reviewed filtering: {len(all_candidates)}",
        f"Total unreviewed candidates: {len(unreviewed)}",
        "",
        f"Unreviewed by priority: {count_by(unreviewed, 'priority')}",
        f"Unreviewed by bucket: {count_by(unreviewed, 'bucket')}",
        "",
        "## Top P1",
        "",
    ]
    for cand in p1[:30]:
        lines.append(f"- {cand.label} | {cand.source} | {cand.evidence}")
    lines.extend(["", "## Top P2", ""])
    for cand in p2[:30]:
        lines.append(f"- {cand.label} | {cand.source} | {cand.evidence}")
    lines.extend(["", "## Top P3", ""])
    for cand in p3[:30]:
        lines.append(f"- {cand.label} | {cand.source} | {cand.evidence}")
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="Results/torch")
    parser.add_argument("--repo-dir", default="TensorGuard-Repros")
    parser.add_argument("--out-dir", default=None)
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    repo_dir = Path(args.repo_dir)
    out_dir = Path(args.out_dir) if args.out_dir else repo_dir / "logs" / "audit_next" / "queues"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "README.running.txt").write_text(
        "Queue generation started. If this file remains without TSV outputs, the generator is still running or was interrupted.\n"
    )

    if not results_dir.exists():
        raise SystemExit(f"results dir not found: {results_dir}")

    log(f"results dir: {results_dir}")
    log(f"repo dir: {repo_dir}")
    log(f"output dir: {out_dir}")
    all_candidates = candidates_from_sources(results_dir)
    unreviewed = filter_unreviewed(all_candidates)

    p1 = [c for c in unreviewed if c.priority == "P1"]
    p2 = [c for c in unreviewed if c.priority == "P2"]
    p3 = [c for c in unreviewed if c.priority == "P3"]

    write_tsv(out_dir / "p1_strong_crash_or_internal_assert.tsv", p1)
    write_tsv(out_dir / "p2_cpu_gpu_exception_mismatch.tsv", p2)
    write_tsv(out_dir / "p3_clean_logic_candidates.tsv", p3)
    write_tsv(out_dir / "all_unreviewed_candidates.tsv", unreviewed)
    write_summary(out_dir / "README.md", all_candidates, unreviewed)
    running = out_dir / "README.running.txt"
    if running.exists():
        running.unlink()

    log(f"wrote queues to: {out_dir}")
    log(f"P1 strong crash/internal assert: {len(p1)}")
    log(f"P2 exception mismatch: {len(p2)}")
    log(f"P3 clean logic candidates: {len(p3)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
