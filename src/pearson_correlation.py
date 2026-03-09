from itertools import combinations

import pandas as pd


def calculate_pearson(cleaned_df):
    """Calculate pairwise Pearson correlations per sector."""
    pearson_results = {}
    top_pearson = {}

    for sektor, df_sektor in cleaned_df.items():
        # Skip sectors with fewer than 2 stocks.
        if df_sektor.empty or df_sektor.shape[1] < 2:
            pearson_results[sektor] = pd.DataFrame(
                columns=["Saham_1", "Saham_2", "Correlation"]
            )
            continue

        corr_matrix = df_sektor.corr(method="pearson")

        pairs = []
        for saham1, saham2 in combinations(corr_matrix.columns, 2):
            corr_value = corr_matrix.loc[saham1, saham2]
            pairs.append((saham1, saham2, corr_value))

        pair_df = pd.DataFrame(pairs, columns=["Saham_1", "Saham_2", "Correlation"])
        pair_df = pair_df.sort_values(by="Correlation", ascending=False).reset_index(
            drop=True
        )

        pearson_results[sektor] = pair_df

        if not pair_df.empty:
            top_pearson[sektor] = pair_df.iloc[0]

    frames = [
        df.assign(Sektor=sektor)
        for sektor, df in pearson_results.items()
        if not df.empty
    ]
    if frames:
        all_pearson_df = pd.concat(frames, ignore_index=True)
    else:
        all_pearson_df = pd.DataFrame(
            columns=["Saham_1", "Saham_2", "Correlation", "Sektor"]
        )

    return pearson_results, top_pearson, all_pearson_df
