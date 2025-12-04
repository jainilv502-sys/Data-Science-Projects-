# 📊 Expense Analyzer

Analyze your personal spending patterns with ease.  
This project takes a CSV of your expenses, cleans it, summarizes it, and generates insights with charts.

---

## 📂 Project Structure
```
expense-analyzer-project/
│
├── data/
│   └── personal_expenses_sample.csv      # Example dataset
│
├── outputs/                              # Auto-generated reports & charts
│   ├── summary.txt
│   ├── monthly_summary.csv
│   ├── category_summary.csv
│   ├── monthly_vs_budget.csv
│   ├── chart_monthly_trend.png
│   ├── chart_top_categories.png
│   └── chart_category_share.png
│
├── expense_analyzer.py                   # Main script
├── requirements.txt                      # Dependencies
└── README.md                             # This file
```

---

## ⚙️ Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Usage
Run basic analysis:
```bash
python expense_analyzer.py --csv data/personal_expenses_sample.csv --outdir outputs
```

Run with monthly budget:
```bash
python expense_analyzer.py --csv data/personal_expenses_sample.csv --budget 25000 --outdir outputs
```

---
