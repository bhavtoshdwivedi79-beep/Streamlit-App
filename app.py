import streamlit as st

from crud import (
    add_student,
    get_students,
    delete_student,
    update_student,
    save_attendance,
    get_attendance
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)


# =========================
# TITLE
# =========================

st.title("🎓 Student Management System")


# =========================
# SIDEBAR
# =========================

st.sidebar.title("📚 Menu")

option = st.sidebar.radio(
    "Select Option",
    [
        "📝 Student Attendance",
        "📊 Attendance Status",
        "➕ Add New Student",
        "🗑️ Delete Student",
        "✏️ Update Student"
    ]
)


# ==================================================
# 1. STUDENT ATTENDANCE
# ==================================================

if option == "📝 Student Attendance":

    st.header("📝 Student Attendance")

    st.write(
        "Select the checkbox for students who are Present."
    )

    students = get_students()

    if len(students) == 0:

        st.warning(
            "No students found in the database."
        )

    else:

        attendance_data = []

        for student in students:

            roll_no = student[0]
            name = student[1]

            present = st.checkbox(
                f"{roll_no} - {name}",
                key=f"attendance_{roll_no}"
            )

            if present:
                status = "P"
            else:
                status = "A"

            attendance_data.append(
                (
                    roll_no,
                    name,
                    status
                )
            )


        st.divider()


        if st.button(
            "✅ Submit Attendance",
            use_container_width=True
        ):

            save_attendance(
                attendance_data
            )

            st.success(
                "Attendance submitted successfully!"
            )


# ==================================================
# 2. ATTENDANCE STATUS
# ==================================================

elif option == "📊 Attendance Status":

    st.header("📊 Attendance Status")

    attendance = get_attendance()

    if len(attendance) == 0:

        st.info("No attendance records found.")

    else:

        import pandas as pd

        df = pd.DataFrame(
            attendance,
            columns=[
                "Roll No",
                "Name",
                "Status",
                "Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# 3. ADD NEW STUDENT
# ==================================================

elif option == "➕ Add New Student":

    st.header("➕ Add New Student")

    roll_no = st.number_input(
        "Roll No",
        min_value=1,
        step=1
    )

    name = st.text_input(
        "Student Name"
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        step=1
    )

    course = st.text_input(
        "Course"
    )

    marks = st.number_input(
        "Marks",
        min_value=0,
        max_value=100,
        step=1
    )


    if st.button(
        "➕ Add Student",
        use_container_width=True
    ):

        if name.strip() == "":
            
            st.warning(
                "Please enter student name."
            )

        elif course.strip() == "":
            
            st.warning(
                "Please enter course."
            )

        else:

            try:

                add_student(
                    roll_no,
                    name,
                    age,
                    course,
                    marks
                )

                st.success(
                    "Student added successfully!"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )


# ==================================================
# 4. DELETE STUDENT
# ==================================================

elif option == "🗑️ Delete Student":

    st.header("🗑️ Delete Student Record")

    students = get_students()

    if len(students) == 0:

        st.warning(
            "No students found."
        )

    else:

        student_options = {
            f"{student[0]} - {student[1]}": student[0]
            for student in students
        }

        selected_student = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        delete_roll_no = student_options[
            selected_student
        ]


        if st.button(
            "🗑️ Delete Student",
            use_container_width=True
        ):

            delete_student(
                delete_roll_no
            )

            st.success(
                "Student deleted successfully!"
            )

            st.rerun()


# ==================================================
# 5. UPDATE STUDENT
# ==================================================

elif option == "✏️ Update Student":

    st.header("✏️ Update Student")

    students = get_students()

    if len(students) == 0:

        st.warning("No students found in the database.")

    else:

        # Student selection
        student_options = {
            f"{student[0]} - {student[1]}": student
            for student in students
        }

        selected_student = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        student = student_options[selected_student]

        roll_no = student[0]

        # Student details
        name = st.text_input(
            "Student Name",
            value=student[1]
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=student[2]
        )

        course = st.text_input(
            "Course",
            value=student[3]
        )

        marks = st.number_input(
            "Marks",
            min_value=0,
            max_value=100,
            value=student[4]
        )

        # Update button
        if st.button(
            "✏️ Update Student",
            use_container_width=True
        ):

            update_student(
                roll_no,
                name,
                age,
                course,
                marks
            )

            st.success(
                "Student updated successfully!"
            )

            st.rerun()