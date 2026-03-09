import pandas as pd
from itertools import combinations

spearman_results = {}

for sektor, df_sektor in cleaned_df.items():

    # hitung matriks korelasi spearman
    corr_matrix = df_sektor.corr(method="spearman")

    pairs = []

    for saham1, saham2 in combinations(corr_matrix.columns, 2):
        corr_value = corr_matrix.loc[saham1, saham2]
        pairs.append((saham1, saham2, corr_value))

    pair_df = pd.DataFrame(pairs, columns=["Saham_1", "Saham_2", "Correlation"])
    pair_df = pair_df.sort_values(by="Correlation", ascending=False)

    spearman_results[sektor] = pair_df

    print(sektor, "→ total pair:", len(pair_df))
    
top_spearman = {}

for sektor, df_pair in spearman_results.items():
    top_spearman[sektor] = df_pair.iloc[0]
    
all_spearman_df = pd.concat(
    [
        df.assign(Sektor=sektor)
        for sektor, df in spearman_results.items()
    ],
    ignore_index=True
)

all_spearman_df

