from itertools import combinations

import pandas as pd


def calculate_spearman(cleaned_df):
    """Calculate pairwise Spearman correlations per sector."""
    spearman_results = {}
    top_spearman = {}

    for sektor, df_sektor in cleaned_df.items():
        if df_sektor.empty or df_sektor.shape[1] < 2:
            spearman_results[sektor] = pd.DataFrame(
                columns=["Saham_1", "Saham_2", "Correlation"]
            )
            continue

        corr_matrix = df_sektor.corr(method="spearman")

        pairs = []
        for saham1, saham2 in combinations(corr_matrix.columns, 2):
            corr_value = corr_matrix.loc[saham1, saham2]
            pairs.append((saham1, saham2, corr_value))

        pair_df = pd.DataFrame(pairs, columns=["Saham_1", "Saham_2", "Correlation"])
        pair_df = pair_df.sort_values(by="Correlation", ascending=False).reset_index(
            drop=True
        )

        spearman_results[sektor] = pair_df

        if not pair_df.empty:
            top_spearman[sektor] = pair_df.iloc[0]

    frames = [
        df.assign(Sektor=sektor)
        for sektor, df in spearman_results.items()
        if not df.empty
    ]
    if frames:
        all_spearman_df = pd.concat(frames, ignore_index=True)
    else:
        all_spearman_df = pd.DataFrame(
            columns=["Saham_1", "Saham_2", "Correlation", "Sektor"]
        )

    return spearman_results, top_spearman, all_spearman_df
