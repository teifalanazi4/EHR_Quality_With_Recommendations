import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = "data/health_records.csv"
df = pd.read_csv(file_path)

os.makedirs("results", exist_ok=True)

def quality_score_with_recommendation(row):
    score = 100
    recommendations = []

    if "ICD_Code" in row and (pd.isna(row["ICD_Code"]) or row["ICD_Code"] == ""):
        score -= 30
        recommendations.append("أدخل الكود الطبي (ICD)")

    if "Admission_Date" in row and "Discharge_Date" in row:
        if pd.isna(row["Discharge_Date"]) or row["Discharge_Date"] == "":
            score -= 30
            recommendations.append("أدخل تاريخ الخروج")
        elif row["Admission_Date"] > row["Discharge_Date"]:
            score -= 20
            recommendations.append("تأكد أن تاريخ الدخول قبل تاريخ الخروج")

    if "Notes" in row:
        if pd.isna(row["Notes"]) or row["Notes"] == "":
            score -= 20
            recommendations.append("أضف ملاحظات عن حالة المريض")
        elif len(str(row["Notes"]).split()) < 3:
            score -= 10
            recommendations.append("قم بتوسيع الملاحظات لتكون واضحة")

    return pd.Series([score, ", ".join(recommendations)])

df[["Quality_Score", "Recommendations"]] = df.apply(quality_score_with_recommendation, axis=1)
df.to_excel("results/quality_scores_with_recommendations.xlsx", index=False)

plt.hist(df["Quality_Score"], bins=5, edgecolor="black")
plt.title("Distribution of EHR Quality Scores")
plt.xlabel("Quality Score")
plt.ylabel("Number of Patients")
plt.show()
