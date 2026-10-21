import streamlit as st
import pandas as pd
import plotly.express as px

from connect_mysql import get_connection


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Student Analytics Dashboard",
    layout="wide"
)

st.title("Student Analytics Dashboard")
st.write("Student performance and attendance analysis")


# ==========================================
# FETCH STUDENT DATA FROM MYSQL
# ==========================================

def get_student_data():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
        RollNo,
        Name,
        Age,
        Course,
        Branch,
        Gender,
        Attendance,
        English,
        Science,
        Maths
    FROM student
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


students = get_student_data()


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    students,
    columns=[
        "RollNo",
        "Name",
        "Age",
        "Course",
        "Branch",
        "Gender",
        "Attendance",
        "English",
        "Science",
        "Maths"
    ]
)

df["Average Marks"] = (
    df["English"] +
    df["Science"] +
    df["Maths"]
) / 3


# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Filters")


# Branch Filter

branch_options = ["All"] + sorted(
    df["Branch"].dropna().unique().tolist()
)

selected_branch = st.sidebar.selectbox(
    "Select Branch",
    branch_options
)


# Gender Filter

gender_options = ["All"] + sorted(
    df["Gender"].dropna().unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    " Select Gender",
    gender_options
)


# Attendance Filter

attendance_options = [
    "All",
    "Attendance >= 75%",
    "Attendance < 75%"
]

selected_attendance = st.sidebar.selectbox(
    " Attendance",
    attendance_options
)


# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df.copy()


if selected_branch != "All":

    filtered_df = filtered_df[
        filtered_df["Branch"] == selected_branch
    ]


if selected_gender != "All":

    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]


if selected_attendance == "Attendance >= 75%":

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= 75
    ]


elif selected_attendance == "Attendance < 75%":

    filtered_df = filtered_df[
        filtered_df["Attendance"] < 75
    ]


# ==========================================
# DISPLAY STUDENT DATA
# ==========================================

st.header(" Student Data")

st.dataframe(
    filtered_df[
        [
            "RollNo",
            "Name",
            "Branch",
            "Gender",
            "English",
            "Science",
            "Maths",
            "Average Marks",
            "Attendance"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# ==========================================
# METRICS
# ==========================================

st.header(" Student Metrics")


total_students = len(filtered_df)

if total_students > 0:

    average_attendance = filtered_df["Attendance"].mean()

    average_marks = filtered_df["Average Marks"].mean()

else:

    average_attendance = 0
    average_marks = 0


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        " Total Students",
        total_students
    )


with col2:

    st.metric(
        " Average Attendance",
        f"{average_attendance:.2f}%"
    )


with col3:

    st.metric(
        " Average Marks",
        f"{average_marks:.2f}"
    )


# ==========================================
# SQL QUERY 1
# BRANCH-WISE AVERAGE MARKS
# ==========================================

st.header(" Branch-wise Average Marks")


branch_marks = filtered_df.groupby(
    "Branch",
    as_index=False
)["Average Marks"].mean()

branch_marks.columns = [
    "Branch",
    "Average Marks"
]


fig1 = px.bar(
    branch_marks,
    x="Branch",
    y="Average Marks",
    title="Branch-wise Average Marks",
    text_auto=".2f"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ==========================================
# SQL QUERY 2
# BRANCH-WISE AVERAGE ATTENDANCE
# ==========================================

st.header(" Branch-wise Average Attendance")


branch_attendance = filtered_df.groupby(
    "Branch",
    as_index=False
)["Attendance"].mean()

branch_attendance.columns = [
    "Branch",
    "Average Attendance"
]


fig2 = px.bar(
    branch_attendance,
    x="Branch",
    y="Average Attendance",
    title="Branch-wise Average Attendance",
    text_auto=".2f"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ==========================================
# SQL QUERY 3
# TOP 5 STUDENTS
# ==========================================

st.header(" Top 5 Students")


top_students = filtered_df.sort_values(
    by="Average Marks",
    ascending=False
).head(5)


st.dataframe(
    top_students[
        [
            "RollNo",
            "Name",
            "Branch",
            "English",
            "Science",
            "Maths",
            "Average Marks",
            "Attendance"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

fig3 = px.bar(
    top_students,
    x="Name",
    y="Average Marks",
    title="Top 5 Students by Average Marks",
    text="Average Marks"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# SQL QUERY 4
# GENDER-WISE STUDENT COUNT
# ==========================================

st.header(" Gender-wise Student Count")


gender_count = filtered_df.groupby(
    "Gender",
    as_index=False
).size()

gender_count.columns = [
    "Gender",
    "Student Count"
]


fig4 = px.pie(
    gender_count,
    names="Gender",
    values="Student Count",
    title="Gender-wise Student Count"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)