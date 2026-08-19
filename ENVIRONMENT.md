# Environment and reproduction contract

## Fixed command

```bash
uv sync --frozen
uv run --frozen python -m reproduction.run
```

## Recorded accepted run

The accepted cumulative run used Python `3.12.13` with the locked
dependencies, the `ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim`
container, the Hugging Face `cpu-upgrade` flavor, and no GPU. It reported
`55.064327` seconds of in-program runtime, `1m14s` provider duration, 64 CPUs
visible to the process, and an estimate of eight useful cores. The complete
raw record is
[`run_f4ec095c.json`](.openresearch/artifacts/cumulative/run_f4ec095c.json).

The accepted command, environment, seeds, and per-claim runtimes are also
mirrored under [`space/evidence`](space/evidence). Finite paper-scale runs
are corroboration for the intended nonempty-solution interpretation; they do
not replace the exact printed-statement counterexamples.

This cleanup records and verifies the existing evidence bundle; it does not
silently replace it with an untracked rerun.

