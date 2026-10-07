import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🎓 Student Performance Analysis Dashboard")

st.write(
    "This dashboard analyzes student marks, attendance, grades, "
    "departments, gender, and age using a dataset of 1000 students."
)

# =========================================================
# LOAD CSV DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("student_marks_1000_records.csv")
    return df


df = load_data()

# =========================================================
# BASIC DATA CLEANING
# =========================================================

# Remove accidental spaces from column names
df.columns = df.columns.str.strip()

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔍 Student Filters")

# Department filter
department_options = ["All"] + sorted(
    df["Department"].dropna().unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Department",
    department_options
)

# Gender filter
gender_options = ["All"] + sorted(
    df["Gender"].dropna().unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)

# Grade filter
grade_options = ["All"] + sorted(
    df["Grade"].dropna().unique().tolist()
)

selected_grade = st.sidebar.selectbox(
    "Grade",
    grade_options
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if selected_department != "All":
    filtered_df = filtered_df[
        filtered_df["Department"] == selected_department
    ]

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]

if selected_grade != "All":
    filtered_df = filtered_df[
        filtered_df["Grade"] == selected_grade
    ]

# =========================================================
# CHECK WHETHER DATA EXISTS
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No students match the selected filters."
    )

    st.stop()

# =========================================================
# 1. LOAD AND INSPECT DATA
# =========================================================

st.header("1️⃣ Load and Inspect the Data")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Students",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Total Columns",
        len(filtered_df.columns)
    )

with col3:
    st.metric(
        "Average Marks",
        f"{filtered_df['Marks'].mean():.2f}"
    )

with col4:
    st.metric(
        "Average Attendance",
        f"{filtered_df['Attendance'].mean():.2f}%"
    )

# ---------------------------------------------------------
# DISPLAY DATASET
# ---------------------------------------------------------

st.subheader("📋 Student Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

# ---------------------------------------------------------
# DATASET INFORMATION
# ---------------------------------------------------------

with st.expander("📌 View Dataset Information"):

    st.write("### Dataset Shape")

    st.write(
        f"Rows: {filtered_df.shape[0]}"
    )

    st.write(
        f"Columns: {filtered_df.shape[1]}"
    )

    st.write("### Column Names")

    st.write(
        filtered_df.columns.tolist()
    )

    st.write("### Data Types")

    datatype_df = pd.DataFrame(
        filtered_df.dtypes,
        columns=["Data Type"]
    )

    st.dataframe(
        datatype_df,
        use_container_width=True
    )

# =========================================================
# 2. CHECK MISSING VALUES
# =========================================================

st.header("2️⃣ Check for Missing Values")

missing_values = filtered_df.isnull().sum()

missing_table = pd.DataFrame({
    "Column": missing_values.index,
    "Missing Values": missing_values.values
})

missing_table["Missing Percentage"] = (
    missing_table["Missing Values"]
    / len(filtered_df)
    * 100
)

st.dataframe(
    missing_table,
    use_container_width=True
)

total_missing = filtered_df.isnull().sum().sum()

if total_missing == 0:

    st.success(
        "✅ No missing values found in the dataset."
    )

else:

    st.warning(
        f"⚠️ Total missing values: {total_missing}"
    )

# =========================================================
# 3. KEY STATISTICS
# =========================================================

st.header("3️⃣ Calculate Key Statistics")

# ---------------------------------------------------------
# MARKS STATISTICS
# ---------------------------------------------------------

st.subheader("📊 Marks Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Marks",
        f"{filtered_df['Marks'].mean():.2f}"
    )

with col2:
    st.metric(
        "Highest Marks",
        filtered_df["Marks"].max()
    )

with col3:
    st.metric(
        "Lowest Marks",
        filtered_df["Marks"].min()
    )

with col4:
    st.metric(
        "Median Marks",
        filtered_df["Marks"].median()
    )

# ---------------------------------------------------------
# AGE AND ATTENDANCE STATISTICS
# ---------------------------------------------------------

st.subheader("📈 Age and Attendance Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average Age",
        f"{filtered_df['Age'].mean():.2f}"
    )

with col2:
    st.metric(
        "Average Attendance",
        f"{filtered_df['Attendance'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Highest Attendance",
        f"{filtered_df['Attendance'].max()}%"
    )

with col4:
    st.metric(
        "Lowest Attendance",
        f"{filtered_df['Attendance'].min()}%"
    )

# ---------------------------------------------------------
# DESCRIPTIVE STATISTICS
# ---------------------------------------------------------

st.subheader("📋 Statistical Summary")

statistics = filtered_df[
    ["Marks", "Age", "Attendance"]
].describe()

st.dataframe(
    statistics,
    use_container_width=True
)

# =========================================================
# 4. DEPARTMENT-WISE ANALYSIS
# =========================================================

st.header("4️⃣ Department-wise Analysis")

department_stats = (
    filtered_df
    .groupby("Department")["Marks"]
    .agg(
        Students="count",
        Average_Marks="mean",
        Highest_Marks="max",
        Lowest_Marks="min"
    )
    .round(2)
    .sort_values(
        "Average_Marks",
        ascending=False
    )
)

st.dataframe(
    department_stats,
    use_container_width=True
)

# =========================================================
# 5. TOP PERFORMING STUDENTS
# =========================================================

st.header("5️⃣ Top Performing Students")

top_students = (
    filtered_df
    .sort_values(
        "Marks",
        ascending=False
    )
    .head(10)
)

st.subheader("🏆 Top 10 Students")

st.dataframe(
    top_students[
        [
            "Roll Number",
            "Name",
            "Gender",
            "Age",
            "Department",
            "Marks",
            "Grade",
            "Attendance"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------------------------
# HIGHEST SCORING STUDENT
# ---------------------------------------------------------

highest_student = filtered_df.loc[
    filtered_df["Marks"].idxmax()
]

st.subheader("🥇 Highest Scoring Student")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Name",
        highest_student["Name"]
    )

with col2:
    st.metric(
        "Marks",
        highest_student["Marks"]
    )

with col3:
    st.metric(
        "Grade",
        highest_student["Grade"]
    )

with col4:
    st.metric(
        "Attendance",
        f"{highest_student['Attendance']}%"
    )

# =========================================================
# 6. GRADE ANALYSIS
# =========================================================

st.header("6️⃣ Grade Analysis")

grade_counts = (
    filtered_df["Grade"]
    .value_counts()
)

st.dataframe(
    grade_counts.rename("Number of Students"),
    use_container_width=True
)

# =========================================================
# 7. DATA VISUALIZATIONS
# =========================================================

st.header("7️⃣ Data Visualizations")

# ---------------------------------------------------------
# CHART 1 - MARKS DISTRIBUTION
# ---------------------------------------------------------

st.subheader("📊 Distribution of Student Marks")

fig1, ax1 = plt.subplots(
    figsize=(10, 5)
)

ax1.hist(
    filtered_df["Marks"],
    bins=10
)

ax1.set_title(
    "Distribution of Student Marks"
)

ax1.set_xlabel(
    "Marks"
)

ax1.set_ylabel(
    "Number of Students"
)

st.pyplot(fig1)

plt.close(fig1)

# ---------------------------------------------------------
# CHART 2 - AVERAGE MARKS BY DEPARTMENT
# ---------------------------------------------------------

st.subheader("🏫 Average Marks by Department")

department_average = (
    filtered_df
    .groupby("Department")["Marks"]
    .mean()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots(
    figsize=(10, 5)
)

department_average.plot(
    kind="bar",
    ax=ax2
)

ax2.set_title(
    "Average Marks by Department"
)

ax2.set_xlabel(
    "Department"
)

ax2.set_ylabel(
    "Average Marks"
)

plt.xticks(rotation=45)

st.pyplot(fig2)

plt.close(fig2)

# ---------------------------------------------------------
# CHART 3 - MARKS VS ATTENDANCE
# ---------------------------------------------------------

st.subheader("📈 Marks vs Attendance")

fig3, ax3 = plt.subplots(
    figsize=(10, 5)
)

ax3.scatter(
    filtered_df["Attendance"],
    filtered_df["Marks"]
)

ax3.set_title(
    "Marks vs Attendance"
)

ax3.set_xlabel(
    "Attendance (%)"
)

ax3.set_ylabel(
    "Marks"
)

st.pyplot(fig3)

plt.close(fig3)

# ---------------------------------------------------------
# CHART 4 - GRADE DISTRIBUTION
# ---------------------------------------------------------

st.subheader("🎯 Grade Distribution")

fig4, ax4 = plt.subplots(
    figsize=(10, 5)
)

grade_counts.plot(
    kind="bar",
    ax=ax4
)

ax4.set_title(
    "Number of Students by Grade"
)

ax4.set_xlabel(
    "Grade"
)

ax4.set_ylabel(
    "Number of Students"
)

st.pyplot(fig4)

plt.close(fig4)

# ---------------------------------------------------------
# CHART 5 - TOP 10 STUDENTS
# ---------------------------------------------------------

st.subheader("🏆 Top 10 Performing Students")

top10_chart = (
    filtered_df
    .nlargest(
        10,
        "Marks"
    )
    .sort_values(
        "Marks"
    )
)

fig5, ax5 = plt.subplots(
    figsize=(10, 6)
)

ax5.barh(
    top10_chart["Name"],
    top10_chart["Marks"]
)

ax5.set_title(
    "Top 10 Performing Students"
)

ax5.set_xlabel(
    "Marks"
)

ax5.set_ylabel(
    "Student"
)

st.pyplot(fig5)

plt.close(fig5)

# ---------------------------------------------------------
# CHART 6 - ATTENDANCE DISTRIBUTION
# ---------------------------------------------------------

st.subheader("📅 Attendance Distribution")

fig6, ax6 = plt.subplots(
    figsize=(10, 5)
)

ax6.hist(
    filtered_df["Attendance"],
    bins=10
)

ax6.set_title(
    "Distribution of Student Attendance"
)

ax6.set_xlabel(
    "Attendance (%)"
)

ax6.set_ylabel(
    "Number of Students"
)

st.pyplot(fig6)

plt.close(fig6)

# =========================================================
# 8. GENDER ANALYSIS
# =========================================================

st.header("8️⃣ Gender Analysis")

gender_counts = (
    filtered_df["Gender"]
    .value_counts()
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Gender-wise Student Count")

    st.dataframe(
        gender_counts.rename(
            "Number of Students"
        ),
        use_container_width=True
    )

with col2:

    st.subheader("Gender-wise Average Marks")

    gender_average = (
        filtered_df
        .groupby("Gender")["Marks"]
        .mean()
        .round(2)
    )

    st.dataframe(
        gender_average.rename(
            "Average Marks"
        ),
        use_container_width=True
    )

# =========================================================
# 9. SUMMARY OF FINDINGS
# =========================================================

st.header("9️⃣ Summary of Findings")

average_marks = (
    filtered_df["Marks"].mean()
)

highest_marks = (
    filtered_df["Marks"].max()
)

lowest_marks = (
    filtered_df["Marks"].min()
)

average_attendance = (
    filtered_df["Attendance"].mean()
)

best_student = filtered_df.loc[
    filtered_df["Marks"].idxmax()
]

department_average_summary = (
    filtered_df
    .groupby("Department")["Marks"]
    .mean()
)

best_department = (
    department_average_summary
    .idxmax()
)

best_department_average = (
    department_average_summary
    .max()
)

st.info(
    f"""
📌 **Student Performance Summary**

👨‍🎓 Total students analyzed: **{len(filtered_df)}**

📊 Average marks: **{average_marks:.2f}**

🏆 Highest marks: **{highest_marks}**

📉 Lowest marks: **{lowest_marks}**

📅 Average attendance: **{average_attendance:.2f}%**

🥇 Top-performing student: **{best_student['Name']}**

⭐ Top student's marks: **{best_student['Marks']}**

🎯 Top student's grade: **{best_student['Grade']}**

🏫 Best-performing department: **{best_department}**

📈 Department average marks: **{best_department_average:.2f}**
"""
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Student Performance Analysis Dashboard | "
    "Python + Pandas + Matplotlib + Streamlit"
)