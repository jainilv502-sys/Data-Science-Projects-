# ---------------------------------------------------------
# Titanic Dataset - Exploratory Data Analysis (EDA)
# ---------------------------------------------------------

# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set plot style
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# 2. Load Dataset (make sure you use train.csv, not test.csv)
df = pd.read_csv("tested.csv")

print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:\n", df.head())

# 3. Basic Info
print("\n--- Dataset Info ---")
print(df.info())
print("\n--- Summary Stats ---")
print(df.describe(include="all"))

# 4. Missing Values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# Visualize missing data
sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
plt.title("Missing Values Heatmap")
plt.show()

# 5. Univariate Analysis

# Survived distribution
sns.countplot(x="Survived", data=df, palette="Set2")
plt.title("Survival Count")
plt.show()

# Sex distribution
sns.countplot(x="Sex", data=df, hue="Sex", palette="pastel", legend=False)
plt.title("Sex Distribution")
plt.show()

# Passenger class distribution
sns.countplot(x="Pclass", data=df, hue="Pclass", palette="muted", legend=False)
plt.title("Passenger Class Distribution")
plt.show()

# Age distribution
sns.histplot(df['Age'], bins=30, kde=True, color="blue")
plt.title("Age Distribution")
plt.show()

# Fare distribution
sns.boxplot(y=df["Fare"], color="orange")
plt.title("Fare Distribution")
plt.show()

# 6. Bivariate Analysis

# Survival vs Sex
sns.countplot(x="Sex", hue="Survived", data=df, palette="Set1")
plt.title("Survival by Gender")
plt.show()

# Survival vs Pclass
sns.countplot(x="Pclass", hue="Survived", data=df, palette="Set2")
plt.title("Survival by Passenger Class")
plt.show()

# Survival vs Age
sns.histplot(data=df, x="Age", hue="Survived", bins=30, palette="Set1")
plt.title("Survival by Age")
plt.show()

# Survival vs Fare
sns.boxplot(x="Survived", y="Fare", data=df, palette="coolwarm")
plt.title("Fare vs Survival")
plt.show()

# 7. Correlation Heatmap (only numeric columns)
numeric_df = df.select_dtypes(include=[np.number])
plt.figure(figsize=(8, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

# 8. Feature Engineering

# Family Size
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
sns.countplot(x="FamilySize", hue="Survived", data=df, palette="Paired")
plt.title("Survival by Family Size")
plt.show()

# Extract Title from Name
df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
sns.countplot(x="Title", hue="Survived", data=df,
              order=df['Title'].value_counts().index, palette="Set3")
plt.xticks(rotation=45)
plt.title("Survival by Passenger Title")
plt.show()

print("\n--- EDA Completed Successfully ---")
