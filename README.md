# Stock Selection for Pair Trading

## What Is Pair Trading?
Pair trading is a market-neutral strategy that trades two stocks with historically related price movements.
The core idea is:
- Find two stocks that usually move together.
- When their relative spread diverges abnormally, go long on the undervalued stock and short on the overvalued stock.
- Close both positions when the spread reverts to its normal level (mean reversion).

This strategy is less about overall market direction and more about the relative relationship between two assets.

## Why Correlation and Cointegration Matter for Pair Selection
Not every stock pair is suitable for pair trading, so statistical filtering is needed.
This project uses:
- **Pearson Correlation** to measure linear relationship strength.
- **Spearman Correlation** to measure monotonic relationship strength based on rank (more robust to outliers).
- **Cointegration Test** to validate whether two price series have a stable long-run equilibrium relationship.

In practice:
- Correlation helps screen pairs that move similarly.
- Cointegration helps confirm whether that relationship is stable enough for a mean-reversion strategy.

## Project Scope
This project selects stock pairs by sector in the Indonesia Stock Exchange (IDX) using:
- Pearson Correlation
- Spearman Correlation
- Cointegration Test

## Workflow
1. Download historical stock price data by sector from Yahoo Finance.
2. Clean and preprocess the dataset.
3. Compute all stock-pair combinations for:
   - Pearson
   - Spearman
   - Cointegration
4. Select top candidate pairs.
5. Export results to Excel in the `result/` folder.

## Estimated Runtime
- A full run usually takes around **7-10 minutes**.
- Runtime may be longer depending on internet connection and how many tickers return valid data.

## Output
Running `main.py` creates a file like:
- `result/hasil_korelasi_<timestamp>.xlsx`

The Excel workbook contains multiple sheets, for example:
- `pearson_all`
- `spearman_all`
- `cointegration_all`
- `selected_pairs`
- `summary_top`
- `top_pearson`
- `top_spearman`
- `top_cointegration`

Note:
- The output can be **very large** because all pair combinations are calculated per sector.

## How to Read the Results
### 1) Pearson Correlation
- Correlation values are in the range `-1` to `1`.
- For pair trading, you typically inspect pairs with:
  - **highest values** (close to `1`) for strongest positive co-movement.
  - **lowest values** (close to `-1`) for strongest negative relationship.
- If your strategy prefers same-direction movement, prioritize high Pearson values.

### 2) Spearman Correlation
- Also ranges from `-1` to `1`, but rank-based.
- General interpretation:
  - **higher values** indicate stronger monotonic relationship.
  - **lower (negative) values** indicate stronger inverse monotonic relationship.

### 3) Cointegration (P-Value)
- Main metric is `P_Value`.
- **Lower p-value** indicates stronger evidence of cointegration.
- For pair trading, pairs with the smallest p-values are usually stronger candidates.

## Run the Project
```bash
pip install -r requirements.txt
python main.py
```

## Main Dependencies
- pandas
- numpy
- yfinance
- statsmodels
- openpyxl
