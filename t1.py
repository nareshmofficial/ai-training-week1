
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Read CSV file
df = pd.read_csv("emp.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Remove spaces from text values
df["department"] = df["department"].astype(str).str.strip()

# Convert salary into numeric
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")

# Check column names
print("Columns:", df.columns.tolist())

print("\nEmployee Data:")
print(df.head())

# Check required columns
required_columns = ["id", "department", "salary"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

# ==================================
# 1. BAR CHART
# Average Salary per Department
# ==================================

avg_salary = df.groupby("department")["salary"].mean()

plt.figure(figsize=(8, 5))

bars = plt.bar(avg_salary.index, avg_salary.values)

plt.title("Average Salary per Department")
plt.xlabel("Department")
plt.ylabel("Average Salary")

plt.bar_label(bars, fmt="%.0f")

plt.tight_layout()
plt.savefig("charts/bar_chart.png")
plt.close()

# ==================================
# 2. HISTOGRAM
# Salary Distribution
# ==================================

plt.figure(figsize=(8, 5))

plt.hist(df["salary"].dropna(), bins=5, edgecolor="black")

plt.title("Employee Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Number of Employees")

plt.tight_layout()
plt.savefig("charts/histogram.png")
plt.close()

# ==================================
# 3. SCATTER PLOT
# Employee ID vs Salary
# ==================================

plt.figure(figsize=(8, 5))

for department in df["department"].dropna().unique():

    department_data = df[df["department"] == department]

    plt.scatter(
        department_data["id"],
        department_data["salary"],
        label=department
    )

plt.title("Employee ID vs Salary")
plt.xlabel("Employee ID")
plt.ylabel("Salary")

plt.legend(title="Department")

plt.tight_layout()
plt.savefig("charts/scatter_plot.png")
plt.close()

# ==================================
# 4. LINE CHART
# Monthly Sales
# ==================================

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

sales = [12, 15, 14, 18, 22, 25]

plt.figure(figsize=(8, 5))

plt.plot(
    months,
    sales,
    marker="o",
    linestyle="-"
)

plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.grid(True)

plt.tight_layout()
plt.savefig("charts/line_chart.png")
plt.close()

# ==================================
# SUCCESS MESSAGE
# ==================================

print("\nAll 4 charts created successfully!")

print("\nSaved Files:")
print("1. charts/bar_chart.png")
print("2. charts/histogram.png")
print("3. charts/scatter_plot.png")
print("4. charts/line_chart.png")
