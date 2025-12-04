#!/usr/bin/env python3
"""
Expense Analyzer
- Load a personal expenses CSV
- Clean & enrich
- Summaries + simple charts (Matplotlib only)
Usage:
  python expense_analyzer.py --csv personal_expenses_sample.csv --budget 25000 --outdir outputs
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_and_clean(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Basic cleaning
    if "Date" not in df.columns or "Amount" not in df.columns:
        raise ValueError("CSV must include at least 'Date' and 'Amount' columns.")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date", "Amount"])
    # Enforce numeric amount
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])
    df["Amount"] = df["Amount"].abs()  # ensure positive spends
    # Standardize text columns if present
    if "Category" in df.columns:
        df["Category"] = df["Category"].astype(str).str.strip().str.title()
    if "Payment Method" in df.columns:
        df["Payment Method"] = df["Payment Method"].astype(str).str.strip().str.title()
    # Enrich
    df["Month"] = df["Date"].values.astype("datetime64[M]")
    df["Week"] = df["Date"] - pd.to_timedelta(df["Date"].dt.weekday, unit="D")
    df["Week"] = df["Week"].values.astype("datetime64[D]")
    df["Weekday"] = df["Date"].dt.day_name()
    return df.sort_values("Date").reset_index(drop=True)

def summarize(df: pd.DataFrame, monthly_budget: float | None = None) -> dict:
    daily_totals = df.groupby(df["Date"].dt.date)["Amount"].sum()
    monthly_totals = df.groupby("Month")["Amount"].sum().sort_index()
    category_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False) if "Category" in df.columns else None

    summary = {
        "total_spend": float(df["Amount"].sum()),
        "avg_daily_spend": float(daily_totals.mean()),
        "num_days": int(daily_totals.shape[0]),
        "top_categories": category_totals.head(5).to_dict() if category_totals is not None else {},
    }

    if monthly_budget is not None:
        budget_df = pd.DataFrame({"Spend": monthly_totals})
        budget_df["Budget"] = monthly_budget
        budget_df["Over/Under"] = budget_df["Spend"] - budget_df["Budget"]
    else:
        budget_df = pd.DataFrame({"Spend": monthly_totals})

    return summary, monthly_totals, category_totals, budget_df

def save_tables(outdir: Path, monthly_totals: pd.Series, category_totals: pd.Series | None, budget_df: pd.DataFrame):
    outdir.mkdir(parents=True, exist_ok=True)
    monthly_totals.to_csv(outdir / "monthly_summary.csv", header=["Amount"])
    budget_df.to_csv(outdir / "monthly_vs_budget.csv")
    if category_totals is not None:
        category_totals.to_csv(outdir / "category_summary.csv", header=["Amount"])

def _pie_aggregate(series: pd.Series, top_n: int = 7) -> pd.Series:
    if series.shape[0] <= top_n:
        return series
    head = series.head(top_n)
    other = pd.Series({"Other": series.iloc[top_n:].sum()})
    return pd.concat([head, other])

def make_charts(outdir: Path, monthly_totals: pd.Series, category_totals: pd.Series | None):
    outdir.mkdir(parents=True, exist_ok=True)

    # Monthly trend (line)
    plt.figure()
    monthly_totals.index = pd.to_datetime(monthly_totals.index)
    monthly_totals.sort_index().plot(kind="line", marker="o")
    plt.title("Monthly Spend Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(outdir / "chart_monthly_trend.png", dpi=150)
    plt.close()

    if category_totals is not None:
        # Top categories (bar)
        plt.figure()
        category_totals.head(10).sort_values(ascending=True).plot(kind="barh")
        plt.title("Top Categories by Spend")
        plt.xlabel("Amount")
        plt.ylabel("Category")
        plt.tight_layout()
        plt.savefig(outdir / "chart_top_categories.png", dpi=150)
        plt.close()

        # Category share (pie)
        plt.figure()
        _pie_aggregate(category_totals, top_n=7).plot(kind="pie", autopct="%1.1f%%", ylabel="")
        plt.title("Category Share of Spend")
        plt.tight_layout()
        plt.savefig(outdir / "chart_category_share.png", dpi=150)
        plt.close()

def save_summary_text(outdir: Path, summary: dict):
    outdir.mkdir(parents=True, exist_ok=True)
    lines = [
        f"Total spend: {summary['total_spend']:.2f}",
        f"Average daily spend: {summary['avg_daily_spend']:.2f}",
        f"Days with spending: {summary['num_days']}",
        "Top categories:"
    ]
    for k, v in summary.get("top_categories", {}).items():
        lines.append(f"  - {k}: {v:.2f}")
    (outdir / "summary.txt").write_text("\n".join(lines), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Expense Analyzer")
    parser.add_argument("--csv", required=True, help="Path to expenses CSV")
    parser.add_argument("--budget", type=float, default=None, help="Monthly budget (optional)")
    parser.add_argument("--outdir", default="outputs", help="Directory to save results")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    outdir = Path(args.outdir)
    df = load_and_clean(csv_path)
    summary, monthly_totals, category_totals, budget_df = summarize(df, monthly_budget=args.budget)

    save_tables(outdir, monthly_totals, category_totals, budget_df)
    make_charts(outdir, monthly_totals, category_totals)
    save_summary_text(outdir, summary)

    print("Analysis complete.")
    print(f"Results saved to: {outdir.resolve()}")

if __name__ == "__main__":
    main()
