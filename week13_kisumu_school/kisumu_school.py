import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. ATTENDANCE FILE - as the officer gave it
attendance_data = [
    {"school_name": "Kisumu Primary School", "average_attendance_pct": 88, "county": "Kisumu"},
    {"school_name": "Maseno Primary", "average_attendance_pct": 92, "county": "Kisumu"},
    {"school_name": "St. Mary's Primary", "average_attendance_pct": 85, "county": "Kisumu"},
    {"school_name": "Kondele Primary School", "average_attendance_pct": 78, "county": "Kisumu"},
    {"school_name": "Milimani Primary", "average_attendance_pct": 95, "county": "Kisumu"},
    {"school_name": "Nyalenda Primary", "average_attendance_pct": 74, "county": "Kisumu"},
    {"school_name": "Manyatta Primary", "average_attendance_pct": 81, "county": "Kisumu"},
    {"school_name": "Dunga Primary", "average_attendance_pct": 89, "county": "Kisumu"},
    {"school_name": "Kibos Primary", "average_attendance_pct": None, "county": "Kisumu"}, # missing value
    {"school_name": "Ahero Primary", "average_attendance_pct": 83, "county": "Kisumu"},
]

# 2. INFRASTRUCTURE FILE - slightly different names
infra_data = [
    {"school_name": "kisumu primary school ", "num_classrooms": 12, "water_access": "Yes"},
    {"school_name": "Maseno Primary", "num_classrooms": 15, "water_access": "Yes"},
    {"school_name": "St Marys Primary", "num_classrooms": 10, "water_access": "No"}, # inconsistency 1: St. Mary's vs St Marys
    {"school_name": "Kondele Primary School", "num_classrooms": 8, "water_access": "Yes"},
    {"school_name": "Milimani Primary", "num_classrooms": 18, "water_access": "Yes"},
    {"school_name": "Nyalenda Primary", "num_classrooms": 6, "water_access": "No"},
    {"school_name": "Manyatta Primary", "num_classrooms": 9, "water_access": "Yes"},
    {"school_name": "Dunga Primary", "num_classrooms": 11, "water_access": "Yes"},
    {"school_name": "Kibos Primary", "num_classrooms": None, "water_access": "Yes"}, # missing value
    {"school_name": "Ahero Primary", "num_classrooms": 10, "water_access": None}, # missing value
    {"school_name": "Ahero Primary", "num_classrooms": 10, "water_access": None}, # DUPLICATE ROW
]

attendance = pd.DataFrame(attendance_data)
infra = pd.DataFrame(infra_data)

print("Before cleaning:")
print(f"Attendance rows: {len(attendance)}, Infra rows: {len(infra)}")
print(f"Infra duplicates: {infra.duplicated().sum()}")

# 3. CLEAN - same trick as Mukasa: lowercase + strip + fix names
def clean_name(name):
    name = str(name).lower().strip()
    name = name.replace(".", "").replace(" ", " ")
    # Fix the 2 naming inconsistencies
    name = name.replace("st marys primary", "st marys primary")
    name = name.replace("kisumu primary school", "kisumu primary")
    name = name.replace("kondele primary school", "kondele primary")
    name = name.replace(" primary school", " primary")
    return name

attendance["school_name_clean"] = attendance["school_name"].apply(clean_name)
infra["school_name_clean"] = infra["school_name"].apply(clean_name)

# Drop duplicate + drop rows with missing values for the analysis
infra = infra.drop_duplicates()
merged = pd.merge(attendance, infra, on="school_name_clean", suffixes=("_att", "_infra"))
merged = merged.dropna(subset=["average_attendance_pct", "num_classrooms"])

print("\nAfter cleaning + merge:")
print(merged[["school_name_att", "average_attendance_pct", "num_classrooms", "water_access"]])
print(f"Merged rows: {len(merged)}")

# 4. ANSWER THE QUESTION: attendance vs classrooms
corr = merged["average_attendance_pct"].corr(merged["num_classrooms"])
print(f"\nCorrelation (attendance vs classrooms): {corr:.2f}")

# 5. SCATTER PLOT
plt.figure(figsize=(8, 5))
plt.scatter(merged["num_classrooms"], merged["average_attendance_pct"], s=100)
for _, row in merged.iterrows():
    plt.text(row["num_classrooms"] + 0.2, row["average_attendance_pct"], row["school_name_att"], fontsize=8)
plt.xlabel("Number of Classrooms")
plt.ylabel("Average Attendance (%)")
plt.title(f"Kisumu: More Classrooms = Higher Attendance? (r = {corr:.2f})")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("kisumu_attendance_vs_classrooms.png")
plt.show()

merged.to_csv("kisumu_merged_clean.csv", index=False)
print("Saved: kisumu_merged_clean.csv + kisumu_attendance_vs_classrooms.png")
