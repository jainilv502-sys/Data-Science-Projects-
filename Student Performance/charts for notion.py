import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve
import joblib

# 1️⃣ Load dataset
df = pd.read_csv("student_performance_dataset.csv")

# Create target column (Pass/Fail)
df["Passed"] = (df["Test_Score"] >= 50).astype(int)

# 2️⃣ Load trained model (you already saved pass_fail_model.pkl)
best_model = joblib.load("pass_fail_model.pkl")

# 3️⃣ Split dataset again (to get X_test, y_test for plots)
from sklearn.model_selection import train_test_split
features = ["Gender", "Age", "Study_Hours", "Attendance",
            "Parental_Education", "Internet_Access", "Extracurricular"]

X = df[features]
y = df["Passed"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ========== 📊 Charts ==========

# 1. Target Distribution
plt.figure(figsize=(5,4))
sns.countplot(x="Passed", data=df, palette="pastel")
plt.title("Target Distribution (0=Fail, 1=Pass)")
plt.savefig("target_distribution.png")
plt.show()

# 2. Confusion Matrix
y_pred = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix - Random Forest")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png")
plt.show()

# 3. ROC Curve
probs = best_model.predict_proba(X_test)[:,1]
fpr, tpr, _ = roc_curve(y_test, probs)
plt.figure(figsize=(5,4))
plt.plot(fpr, tpr, label="ROC Curve")
plt.plot([0,1],[0,1],"--", color="grey")
plt.title("ROC Curve - Random Forest")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.savefig("roc_curve.png")
plt.show()

# 4. Precision-Recall Curve
from sklearn.metrics import precision_recall_curve
precision, recall, _ = precision_recall_curve(y_test, probs)
plt.figure(figsize=(5,4))
plt.plot(recall, precision, label="PR Curve")
plt.title("Precision-Recall Curve - Random Forest")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.savefig("pr_curve.png")
plt.show()
