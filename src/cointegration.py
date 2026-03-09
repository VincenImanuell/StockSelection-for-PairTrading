from statsmodels.tsa.stattools import coint
from itertools import combinations

cointegration_results = {}

for sektor, df_sektor in cleaned_df.items():

    print(f"\n=== Sektor: {sektor} ===")

    pairs = []
    total_pairs = len(list(combinations(df_sektor.columns, 2)))
    counter = 0

    for saham1, saham2 in combinations(df_sektor.columns, 2):
        counter += 1

        series1 = df_sektor[saham1]
        series2 = df_sektor[saham2]

        score, pvalue, _ = coint(series1, series2)

        print(f"[{counter}/{total_pairs}] {saham1}-{saham2} | p-value: {pvalue:.12e}")

        pairs.append((saham1, saham2, score, pvalue))

    pair_df = pd.DataFrame(
        pairs,
        columns=["Saham_1", "Saham_2", "Test_Statistic", "P_Value"]
    )

    pair_df = pair_df.sort_values(by="P_Value")
    cointegration_results[sektor] = pair_df
    
top_cointegration = {}

for sektor, df_pair in cointegration_results.items():
    top_cointegration[sektor] = df_pair.iloc[0]

for sektor, row in top_cointegration.items():
    print(f"{sektor}: {row['Saham_1']} - {row['Saham_2']} | p-value: {row['P_Value']:.12e}")