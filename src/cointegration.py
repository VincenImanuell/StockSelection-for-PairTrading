from itertools import combinations

import pandas as pd
from statsmodels.tsa.stattools import coint


def calculate_cointegration(cleaned_df):
    """Calculate pairwise cointegration test per sector."""
    cointegration_results = {}
    top_cointegration = {}

    for sektor, df_sektor in cleaned_df.items():
        if df_sektor.empty or df_sektor.shape[1] < 2:
            cointegration_results[sektor] = pd.DataFrame(
                columns=["Saham_1", "Saham_2", "Test_Statistic", "P_Value"]
            )
            continue

        pairs = []
        for saham1, saham2 in combinations(df_sektor.columns, 2):
            series1 = df_sektor[saham1]
            series2 = df_sektor[saham2]
            score, pvalue, _ = coint(series1, series2)
            pairs.append((saham1, saham2, score, pvalue))

        pair_df = pd.DataFrame(
            pairs,
            columns=["Saham_1", "Saham_2", "Test_Statistic", "P_Value"],
        )
        pair_df = pair_df.sort_values(by="P_Value", ascending=True).reset_index(drop=True)

        cointegration_results[sektor] = pair_df

        if not pair_df.empty:
            top_cointegration[sektor] = pair_df.iloc[0]

    frames = [
        df.assign(Sektor=sektor)
        for sektor, df in cointegration_results.items()
        if not df.empty
    ]
    if frames:
        all_cointegration_df = pd.concat(frames, ignore_index=True)
    else:
        all_cointegration_df = pd.DataFrame(
            columns=["Saham_1", "Saham_2", "Test_Statistic", "P_Value", "Sektor"]
        )

    return cointegration_results, top_cointegration, all_cointegration_df
