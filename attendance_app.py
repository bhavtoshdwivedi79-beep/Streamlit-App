
import streamlit as st
from attendance_connection import get_connection

st.set_page_config(
    page_title="Student Attendance System",
    page_icon="🎓",
    layout="wide"
)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student" not in st.session_state:
    st.session_state.student = None

if "page" not in st.session_state:
    st.session_state.page = "Login"


# Login function
def login_student(username, password):
    con = get_connection()
    cursor = con.cursor(dictionary=True)

    try:
        query = """
        SELECT student_id, username, full_name, roll_no
        FROM students
        WHERE username = %s AND password = %s
        """
        cursor.execute(query, (username, password))
        return cursor.fetchone()

    finally:
        cursor.close()
        con.close()


# Registration function
def register_student(username, password, full_name, roll_no):
    con = get_connection()
    cursor = con.cursor()

    try:
        query = """
        INSERT INTO students (username, password, full_name, roll_no)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (username, password, full_name, roll_no)
        )
        con.commit()
        return True, "Registration successful! Please login."

    except Exception as e:
        con.rollback()

        if "Duplicate entry" in str(e):
            return False, "Username or Roll Number already exists."

        return False, "Registration failed. Please check your details."

    finally:
        cursor.close()
        con.close()


# Sidebar
st.sidebar.title("🎓 Student Portal")

page = st.sidebar.radio(
    "Navigation",
    ["Login", "Registration", "Dashboard"],
    key="page"
)

st.sidebar.divider()

if st.session_state.logged_in:
    st.sidebar.success("Logged in")
    st.sidebar.write(
        f"Student: {st.session_state.student['full_name']}"
    )

    
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.student = None
        st.rerun()


# Login page
if page == "Login":
    st.title("🔐 Student Login")
    st.write("Login using your registered username and password.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if submitted:
        if not username.strip() or not password:
            st.warning("Please enter username and password.")

        else:
            try:
                student = login_student(username.strip(), password)

                if student:
                    st.session_state.logged_in = True
                    st.session_state.student = student
                    st.session_state.page = "Dashboard"
                    st.rerun()

                else:
                    st.error(
                        "Invalid username or password. "
                        "Please register if you don't have an account."
                    )

            except Exception:
                st.error(
                    "Database connection failed. "
                    "Please check your MySQL settings."
                )


# Registration page
elif page == "Registration":
    st.title("📝 Student Registration")
    st.write("Create your account to access your attendance.")

    with st.form("registration_form"):
        full_name = st.text_input("Full Name")
        roll_no = st.text_input("Roll Number")
        username = st.text_input("Create Username")
        password = st.text_input(
            "Create Password",
            type="password"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Register",
            use_container_width=True
        )

    if submitted:
        if not all([
            full_name.strip(),
            roll_no.strip(),
            username.strip(),
            password,
            confirm_password
        ]):
            st.warning("Please fill in all the fields.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:
            try:
                success, message = register_student(
                    username.strip(),
                    password,
                    full_name.strip(),
                    roll_no.strip()
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)

            except Exception:
                st.error(
                    "Database connection failed. "
                    "Please check your MySQL settings."
                )


# Dashboard page
elif page == "Dashboard":
    if not st.session_state.logged_in:
        st.warning("Please login first to access the dashboard.")

    else:
        student = st.session_state.student

        st.title("📊 Student Dashboard")
        st.subheader(f"Welcome, {student['full_name']}! 👋")

        st.write(f"**Roll Number:** {student['roll_no']}")
        st.write(f"**Username:** {student['username']}")

        try:
            con = get_connection()
            cursor = con.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total_days,
                    SUM(CASE WHEN status = 'Present'
                        THEN 1 ELSE 0 END) AS present_days,
                    SUM(CASE WHEN status = 'Absent'
                        THEN 1 ELSE 0 END) AS absent_days
                FROM attendance
                WHERE student_id = %s
                """,
                (student["student_id"],)
            )

            result = cursor.fetchone()

            total_days = result[0] or 0
            present_days = result[1] or 0
            absent_days = result[2] or 0

            cursor.close()
            con.close()

            percentage = (
                (present_days / total_days) * 100
                if total_days > 0 else 0
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Days", total_days)
            col2.metric("Present Days", present_days)
            col3.metric("Absent Days", absent_days)
            col4.metric("Attendance %", f"{percentage:.1f}%")

            st.divider()

            st.subheader("📅 Attendance Details")

            con = get_connection()
            cursor = con.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT attendance_date, status
                FROM attendance
                WHERE student_id = %s
                ORDER BY attendance_date DESC
                """,
                (student["student_id"],)
            )

            records = cursor.fetchall()

            cursor.close()
            con.close()

            if records:
                st.dataframe(
                    records,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No attendance records found yet.")

        except Exception:
            st.error(
                "Unable to load attendance. "
                "Please check your database connection."
            )
