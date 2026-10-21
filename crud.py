from connect_mysql import get_connection
from datetime import date


# =========================
# ADD STUDENT
# =========================

def add_student(roll_no, name, age, course, marks):

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    INSERT INTO student
    (RollNo, Name, Age, Course, Marks)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        roll_no,
        name,
        age,
        course,
        marks
    )

    cursor.execute(sql, values)

    connection.commit()

    cursor.close()
    connection.close()


# =========================
# GET STUDENTS
# =========================

def get_students():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM student")

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return students


# =========================
# DELETE STUDENT
# =========================

def delete_student(roll_no):

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    DELETE FROM student
    WHERE RollNo = %s
    """

    cursor.execute(sql, (roll_no,))

    connection.commit()

    cursor.close()
    connection.close()


# =========================
# UPDATE STUDENT
# =========================

def update_student(
    roll_no,
    name,
    age,
    course,
    marks
):

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    UPDATE student
    SET Name = %s,
        Age = %s,
        Course = %s,
        Marks = %s
    WHERE RollNo = %s
    """

    values = (
        name,
        age,
        course,
        marks,
        roll_no
    )

    cursor.execute(sql, values)

    connection.commit()

    cursor.close()
    connection.close()


# =========================
# SAVE ATTENDANCE
# =========================

def save_attendance(attendance_data):

    connection = get_connection()
    cursor = connection.cursor()

    today = date.today()

    # Remove today's old attendance
    # so that submitting again
    # doesn't create duplicate records.

    delete_sql = """
    DELETE FROM attendance
    WHERE AttendanceDate = %s
    """

    cursor.execute(delete_sql, (today,))


    # Insert today's attendance

    insert_sql = """
    INSERT INTO attendance
    (RollNo, Name, Attendance, AttendanceDate)
    VALUES (%s, %s, %s, %s)
    """

    for roll_no, name, status in attendance_data:

        values = (
            roll_no,
            name,
            status,
            today
        )

        cursor.execute(
            insert_sql,
            values
        )


    connection.commit()

    cursor.close()
    connection.close()


# =========================
# GET ATTENDANCE
# =========================

def get_attendance():

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    SELECT
        RollNo,
        Name,
        Attendance,
        AttendanceDate
    FROM attendance
    ORDER BY AttendanceDate DESC, RollNo
    """

    cursor.execute(sql)

    attendance = cursor.fetchall()

    cursor.close()
    connection.close()

    return attendance