import pandas as pd
import pathlib as path
# district summary
df_schools = pd.read_csv("PyCitySchools/Resources/schools_complete.csv")
df_students = pd.read_csv("PyCitySchools/Resources/students_complete.csv")
print(df_schools.head())
print(df_students.head())
# number of schools and students using len
number_of_schools = len(df_schools["school_name"])
print(number_of_schools)
number_of_students = len(df_students["student_name"])
print(number_of_students)
# find total budget by using sum()
total_budget = df_schools["budget"].sum()
print(total_budget)
# find average math and reading score by using mean()
ave_math_score = df_students["math_score"].mean()
print(ave_math_score)
ave_read_score = df_students["reading_score"].mean()
print(ave_read_score)
# find number of students and percettage who passed math
pass_math = df_students[(df_students["math_score"] >= 70)].count()["student_name"]
print(pass_math)
perc_pass_math = pass_math * 100 / number_of_students
print(perc_pass_math)
#  find number of students and percettage who passed reading
pass_read = df_students[(df_students["reading_score"] >= 70)].count()["student_name"]
print(pass_read)
perc_pass_read = pass_read * 100 / number_of_students
print(perc_pass_read)
# find find number of students and percettage who passed math and reading
pass_read_math = df_students[(df_students["reading_score"] >= 70) & (df_students["math_score"] >= 70)].count()["student_name"]
print(pass_read_math)
perc_pass_read_math = pass_read_math * 100 / number_of_students
print(perc_pass_read_math)
# do formatting to DataFrame 
result_summary = {"Total schools" : [number_of_schools],
"Total students" : [number_of_students],
"Total budget" : [total_budget],
"Average Math score" : [ave_math_score],
"Average Reading score" : [ave_read_score],
"% Passing math" : [perc_pass_math], 
"% Passing reading" : [perc_pass_read], 
"% Overall passing" : [perc_pass_read_math]

}
# formating integers in columns
district_summary = pd.DataFrame(result_summary)
district_summary["Total students"] = district_summary["Total students"].map("{:,.2f}".format)
district_summary["Total budget"] = district_summary["Total budget"].map("${:,.2f}".format)
district_summary["Average Math score"] = district_summary["Average Math score"].map("{:,.2f}".format)
district_summary["Average Reading score"] = district_summary["Average Reading score"].map("{:,.2f}".format)
district_summary["% Passing math"] = district_summary["% Passing math"].map("{:,.2f}".format)
district_summary["% Passing reading"] = district_summary["% Passing reading"].map("{:,.2f}".format)
district_summary["% Overall passing"] = district_summary["% Overall passing"].map("{:,.2f}".format)

print(district_summary)

### School Summary

# merge two Data Frames 
df_complete = pd.merge(df_schools, df_students, how = "left", on =["school_name", "school_name"])
# print(df_complete.head())
#  print(df_complete.columns)

# use groupby to find number of students, budget per school and average reding, math score per school 
stud_budget_score = df_complete.groupby("school_name")[["size", "budget", "reading_score", "math_score"]].mean()
# find budget per student
stud_budget_score["Per Student Budget"] = stud_budget_score["budget"] / stud_budget_score["size"]
# print(stud_budget_score)

# find percentage of student who passed math and reading
stud_budget_score["Math"] = df_complete[df_complete["math_score"] >= 70].groupby("school_name")["Student ID"].count()
print(stud_budget_score["Math"])
stud_budget_score["Reading"] = df_complete[df_complete["reading_score"] >= 70].groupby("school_name")["Student ID"].count()
# print(stud_budget_score["Reading"])
stud_budget_score["% Passing Math"] = stud_budget_score["Math"] * 100 / stud_budget_score["size"]
stud_budget_score["% Passing Reading"] = stud_budget_score["Reading"] * 100 /stud_budget_score["size"]
# print(stud_budget_score["% Passing Math"])
# print(stud_budget_score["% Passing Reading"])

# find percentage of students who passed math AND reading
stud_budget_score["Math,Read"] = df_complete[(df_complete["math_score"] >= 70) & (df_complete["reading_score"] >= 70)].groupby("school_name")["Student ID"].count()
stud_budget_score["% Overall Passing"] = stud_budget_score["Math,Read"] * 100 / stud_budget_score["size"]
# print(stud_budget_score["% Overall Passing"])
# rename columns in stud_budget_score
stud_budget_score.rename(columns ={"size":"Total Students", "budget":"Budget", "math_score":"Average Math Score", "reading_score":"Average Reading Score"}, inplace=True)
# print(stud_budget_score)
# format stud_budget_score to per_school_summary DataFrame
per_school_summary = pd.DataFrame(stud_budget_score)

# per_school_summary["School Type"] = df_complete["type"]
# print(per_school_summary["School Type"])

# format integers in per_school_summary DataFrame
per_school_summary["Budget"] = per_school_summary["Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"]
# .map("${:,.2f}".format)
per_school_summary["% Passing Math"] = per_school_summary["% Passing Math"]
# .map("{:,.2f}".format)
per_school_summary["% Passing Reading"] = per_school_summary["% Passing Reading"]
# .map("{:,.2f}".format)
per_school_summary["% Overall Passing"] = per_school_summary["% Overall Passing"]
# .map("{:,.2f}".format)
# delete unnesessary columns 
per_school_summary.drop(["Math,Read", "Math", "Reading"], axis=1, inplace=True)

print(per_school_summary)

# find 5 best and 5 lowest results by % Overall Passing
highest = per_school_summary.sort_values(by="% Overall Passing", ascending=False).head(5)
print(highest)
top_schools = pd.DataFrame(highest)
bottom = per_school_summary.sort_values(by="% Overall Passing", ascending=True).head(5)
print(bottom)
bottom_schools = pd.DataFrame(bottom)
# find average math and reading score for each grade in each school groupby and pivot
math_by_grade = df_complete.groupby(["school_name", "grade"])["math_score"].mean().reset_index()
math_by_grade_p = math_by_grade.pivot(index="school_name", columns = "grade", values="math_score")
# print(math_by_grade_p)
# reading
read_by_grade = df_complete.groupby(["school_name", "grade"])["reading_score"].mean().reset_index()
read_by_grade_p = read_by_grade.pivot(index="school_name", columns = "grade", values="reading_score")
# print(read_by_grade_p)

# Scores by school spending
per_school_summary["School name"] = per_school_summary.index
spend = per_school_summary[["School name", "Per Student Budget", "Average Math Score", "Average Reading Score", "% Passing Math", "% Passing Reading", "% Overall Passing"]]

df = pd.DataFrame(spend)

spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]
# labels = [585, 585-630, 630-645, 645-680]
df["Spending ranges"] = pd.cut(df["Per Student Budget"], bins=spending_bins, labels = labels)

spending_summary = df.groupby(["Spending ranges"]).agg({
    "Average Math Score": 'mean',
    "Average Reading Score": 'mean',
    "% Passing Math": 'mean',
    "% Passing Reading": 'mean',
    "% Overall Passing": 'mean'
})

# spending_summary.to_csv('spending_summary.csv')
# print(spending_summary)

size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

size = pd.cut(per_school_summary["Total Students"], bins=size_bins, labels = labels)
# print(size)


