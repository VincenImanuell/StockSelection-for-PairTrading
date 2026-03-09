import pandas as pd


def _top_row(df, score_col):
    if df is None or df.empty:
        return None
    row = df.iloc[0]
    return {
        "Saham_1": row["Saham_1"],
        "Saham_2": row["Saham_2"],
        score_col: row[score_col],
    }


def select_top_pairs(
    pearson_results,
    spearman_results,
    cointegration_results,
    top_n=5,
):
    """Build selected pair tables from three methods."""
    sectors = sorted(
        set(pearson_results.keys())
        | set(spearman_results.keys())
        | set(cointegration_results.keys())
    )

    selected_rows = []
    summary_rows = []

    for sektor in sectors:
        pearson_df = pearson_results.get(sektor, pd.DataFrame())
        spearman_df = spearman_results.get(sektor, pd.DataFrame())
        cointegration_df = cointegration_results.get(sektor, pd.DataFrame())

        top_pearson = _top_row(pearson_df, "Correlation")
        top_spearman = _top_row(spearman_df, "Correlation")
        top_cointegration = _top_row(cointegration_df, "P_Value")

        summary_rows.append(
            {
                "Sektor": sektor,
                "Pearson_Pair": (
                    f"{top_pearson['Saham_1']}-{top_pearson['Saham_2']}"
                    if top_pearson
                    else None
                ),
                "Pearson_Correlation": (
                    top_pearson["Correlation"] if top_pearson else None
                ),
                "Spearman_Pair": (
                    f"{top_spearman['Saham_1']}-{top_spearman['Saham_2']}"
                    if top_spearman
                    else None
                ),
                "Spearman_Correlation": (
                    top_spearman["Correlation"] if top_spearman else None
                ),
                "Cointegration_Pair": (
                    f"{top_cointegration['Saham_1']}-{top_cointegration['Saham_2']}"
                    if top_cointegration
                    else None
                ),
                "Cointegration_P_Value": (
                    top_cointegration["P_Value"] if top_cointegration else None
                ),
            }
        )

        if not pearson_df.empty:
            rows = pearson_df.head(top_n).copy()
            rows["Sektor"] = sektor
            rows["Method"] = "Pearson"
            rows = rows.rename(columns={"Correlation": "Score"})
            selected_rows.append(rows[["Sektor", "Method", "Saham_1", "Saham_2", "Score"]])

        if not spearman_df.empty:
            rows = spearman_df.head(top_n).copy()
            rows["Sektor"] = sektor
            rows["Method"] = "Spearman"
            rows = rows.rename(columns={"Correlation": "Score"})
            selected_rows.append(rows[["Sektor", "Method", "Saham_1", "Saham_2", "Score"]])

        if not cointegration_df.empty:
            rows = cointegration_df.head(top_n).copy()
            rows["Sektor"] = sektor
            rows["Method"] = "Cointegration"
            rows = rows.rename(columns={"P_Value": "Score"})
            selected_rows.append(rows[["Sektor", "Method", "Saham_1", "Saham_2", "Score"]])

    if selected_rows:
        selected_pairs_df = pd.concat(selected_rows, ignore_index=True)
    else:
        selected_pairs_df = pd.DataFrame(
            columns=["Sektor", "Method", "Saham_1", "Saham_2", "Score"]
        )

    summary_df = pd.DataFrame(summary_rows)

    return selected_pairs_df, summary_df
