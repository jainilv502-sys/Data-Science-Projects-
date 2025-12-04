# ----------------------------
# Create subfolders
# ----------------------------
New-Item -Path "data" -ItemType Directory -Force | Out-Null
New-Item -Path "outputs" -ItemType Directory -Force | Out-Null

# ----------------------------
# Create expense-analyzer.py
# ----------------------------
@"
import pandas as pd
import matplotlib.pyplot as plt
import os

# Default paths
CSV_FILE = "data/myExpenses1.csv"
OUTPUT_DIR = "outputs"

def load_data(csv_file):
    return pd.read_csv(csv_file)

def analyze_expenses(df):
    summary = {}
    summary['total_expense'] = df['Amount'].sum()
    summary['by_category'] = df.groupby('Category')['Amount'].sum().to_dict()
    summary['by_day'] = df.groupby('day')['Amount'].sum().to_dict()
    summary['by_item'] = df.groupby('Item')['Amount'].sum().sort_values(ascending=False).to_dict()
    return summary

def save_plots(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(6, 4))
    df.groupby("Category")["Amount"].sum().plot(kind="bar")
    plt.title("Expenses by Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "expenses_by_category.png"))
    plt.close()

    plt.figure(figsize=(6, 4))
    df.groupby("day")["Amount"].sum().plot(kind="bar")
    plt.title("Expenses by Day")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "expenses_by_day.png"))
    plt.close()

    plt.figure(figsize=(6, 4))
    df.groupby("Item")["Amount"].sum().nlargest(10).plot(kind="bar")
    plt.title("Top 10 Expense Items")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "top10_items.png"))
    plt.close()

def save_summary(summary, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "summary.txt"), "w") as f:
        f.write("Expense Summary\n")
        f.write("====================\n")
        f.write(f"Total Expense: {summary['total_expense']}\n\n")
        f.write("Expenses by Category:\n")
        for k, v in summary['by_category'].items():
            f.write(f"  {k}: {v}\n")
        f.write("\nExpenses by Day:\n")
        for k, v in summary['by_day'].items():
            f.write(f"  {k}: {v}\n")
        f.write("\nTop Items:\n")
        for k, v in list(summary['by_item'].items())[:10]:
            f.write(f"  {k}: {v}\n")

def main():
    print("📂 Loading data...")
    df = load_data(CSV_FILE)

    print("📊 Analyzing...")
    summary = analyze_expenses(df)

    print("💾 Saving plots and summary...")
    save_plots(df, OUTPUT_DIR)
    save_summary(summary, OUTPUT_DIR)

    print(f"✅ Done! Reports saved in '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    main()
"@ | Set-Content -Path "expense-analyzer.py"

# ----------------------------
# Create requirements.txt
# ----------------------------
@"
pandas
matplotlib
"@ | Set-Content -Path "requirements.txt"

# ----------------------------
# Create README.md
# ----------------------------
@"
# Expense Analyzer Project

This project analyzes personal expenses from a CSV file (`data/myExpenses1.csv`) and generates:
- Summary report (text)
- Visualizations (bar charts)

## How to run
```bash
python expense-analyzer.py


```bash 
python expense-analyzer.py


