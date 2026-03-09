from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.cointegration import calculate_cointegration
from src.fetch_data import preproccess, sektor
from src.pearson_correlation import calculate_pearson
from src.select_pairs import select_top_pairs
from src.spearman_correlation import calculate_spearman


def _resolve_excel_engine():
    try:
        import openpyxl  # noqa: F401

        return "openpyxl"
    except ModuleNotFoundError:
        try:
            import xlsxwriter  # noqa: F401

            return "xlsxwriter"
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Tidak ada engine Excel terpasang. Install `openpyxl` atau `xlsxwriter`."
            ) from exc


def download_sector_prices(
    sector_map,
    start_date="2016-01-01",
    end_date="2019-12-31",
    min_rows=200,
):
    """Download close price data for each sector."""
    all_df = {}

    for sector_name, tickers in sector_map.items():
        print(f"Download sektor: {sector_name}")
        prices = pd.DataFrame()

        for ticker in tickers:
            try:
                data = yf.download(
                    ticker + ".JK",
                    start=start_date,
                    end=end_date,
                    multi_level_index=False,
                    progress=False,
                    auto_adjust=False,
                )
                if data.empty or "Close" not in data.columns:
                    continue
                close_series = data["Close"]
                if close_series.isna().all() or len(close_series) < min_rows:
                    continue
                prices[ticker] = close_series
            except Exception as exc:
                print(f"  Gagal {ticker}: {exc}")

        all_df[sector_name] = prices
        print(f"  Shape: {prices.shape}")

    return all_df


def run_pipeline(top_n=5):
    all_df = download_sector_prices(sektor)
    cleaned_df = preproccess(all_df)

    pearson_results, top_pearson, all_pearson_df = calculate_pearson(cleaned_df)
    spearman_results, top_spearman, all_spearman_df = calculate_spearman(cleaned_df)
    cointegration_results, top_cointegration, all_cointegration_df = calculate_cointegration(
        cleaned_df
    )

    selected_pairs_df, summary_df = select_top_pairs(
        pearson_results,
        spearman_results,
        cointegration_results,
        top_n=top_n,
    )

    result_dir = Path("result")
    result_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = result_dir / f"hasil_korelasi_{timestamp}.xlsx"

    excel_engine = _resolve_excel_engine()
    with pd.ExcelWriter(output_path, engine=excel_engine) as writer:
        all_pearson_df.to_excel(writer, sheet_name="pearson_all", index=False)
        all_spearman_df.to_excel(writer, sheet_name="spearman_all", index=False)
        all_cointegration_df.to_excel(writer, sheet_name="cointegration_all", index=False)
        selected_pairs_df.to_excel(writer, sheet_name="selected_pairs", index=False)
        summary_df.to_excel(writer, sheet_name="summary_top", index=False)

        pd.DataFrame(top_pearson).T.reset_index(drop=True).to_excel(
            writer, sheet_name="top_pearson", index=False
        )
        pd.DataFrame(top_spearman).T.reset_index(drop=True).to_excel(
            writer, sheet_name="top_spearman", index=False
        )
        pd.DataFrame(top_cointegration).T.reset_index(drop=True).to_excel(
            writer, sheet_name="top_cointegration", index=False
        )

    print(f"\nFile hasil berhasil dibuat: {output_path}")
    return output_path


if __name__ == "__main__":
    run_pipeline(top_n=5)
