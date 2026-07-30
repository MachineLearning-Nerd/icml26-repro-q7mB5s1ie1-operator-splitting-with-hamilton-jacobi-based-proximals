import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # When does HJ-Prox splitting help?

    The paper's Section 3.3 compares
    \(J_{f+g}=\exp(2L_{f+g}^2t/\delta)\) with
    \(J_f+J_g\). The reproduction found that splitting helps aligned
    terms but is not uniformly tighter.
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    labels = ["cancelling\n$f=x,g=-x$", "aligned\n$f=g=|x|$"]
    unsplit = [1.0, 2980.9579870417283]
    split = [14.7781121978613, 14.7781121978613]
    x = np.arange(2)
    figure, axis = plt.subplots(figsize=(7, 4))
    axis.bar(x - 0.18, unsplit, 0.36, label="unsplit $J_{f+g}$")
    axis.bar(x + 0.18, split, 0.36, label="split $J_f+J_g$")
    axis.set_yscale("log")
    axis.set_xticks(x, labels)
    axis.set_ylabel("theoretical constant")
    axis.legend(frameon=False)
    axis.set_title("Exact reproduction evidence at $t=\\delta=0.1$")
    figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the cancelling pair, both components are convex and 1-Lipschitz,
    but their sum is zero-Lipschitz. Therefore the unsplit constant is
    \(1\), while the split total is \(2e^2=14.778\). This is an exact
    counterexample to a universal tighter-bound reading.

    The aligned control has \(L_{f+g}=2\), so the unsplit constant is
    \(e^8=2980.958\). Here splitting produces the dramatic reduction the
    paper describes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ratio = mo.ui.slider(
        start=0.02,
        stop=2.0,
        step=0.02,
        value=1.0,
        label=r"$t/\delta$",
    )
    ratio
    return (ratio,)


@app.cell(hide_code=True)
def _(mo, np, ratio):
    c = ratio.value
    aligned_unsplit = np.exp(8 * c)
    aligned_split = 2 * np.exp(2 * c)
    cancelling_unsplit = 1.0
    cancelling_split = aligned_split
    mo.md(
        f"""
        At **t/delta = {c:.2f}**:

        | pair | unsplit | split total | split tighter? |
        |---|---:|---:|---|
        | cancelling | {cancelling_unsplit:.3g} | {cancelling_split:.3g} | no |
        | aligned | {aligned_unsplit:.3g} | {aligned_split:.3g} | {"yes" if aligned_split < aligned_unsplit else "no"} |

        This bounded slider changes only the theoretical ratio; it does not
        rerun any formal experiment.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## What the paper-scale run showed

    The corrected nonnegative-LASSO comparison used five independent
    250×500 data sets with 50 positive nonzeros:

    - hybrid/full exact fixed-point-residual geometric mean ratio:
      **0.251737**;
    - paired bootstrap 95% log-ratio interval:
      **[-1.40152, -1.35715]**;
    - the hybrid objective gap was smaller on all five seeds.

    So the practical hybrid hierarchy is supported even though the broad
    theoretical comparison needs an alignment condition. Claims 2–4 have
    the same two-layer interpretation: their printed statements omit a
    minimizer-existence premise and are falsified by exact constructions,
    while paper-scale runs corroborate the likely intended corrected
    setting.
    """)
    return


if __name__ == "__main__":
    app.run()
