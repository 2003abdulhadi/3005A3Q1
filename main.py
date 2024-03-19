from db.db import *

conn = getDBConnection(USER_PARAMS)


def getAllStudents():
    """retrieves and returns all students from db"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM students;")
    students = cur.fetchall()
    cur.close()
    return students


def addStudent(firstName, lastName, email, enrollmentDate):
    """inserts student as
    student{
        first_name=firstName,
        last_name=lastName,
        email=email,
        enrollment_date=enrollmentDate
    }
    returns newly inserted student
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s) RETURNING *",
        (firstName, lastName, email, enrollmentDate),
    )
    conn.commit()
    newStudent = cur.fetchone()
    cur.close()
    return newStudent


def updateStudentEmail(studentID, newEmail):
    """updates student with student_id==studentID with a new email=newEmail.
    returns updated student"""
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET email = %s WHERE student_id = %s RETURNING *",
        (newEmail, studentID),
    )
    conn.commit()
    updatedStudent = cur.fetchone()
    cur.close()
    return updatedStudent


def deleteStudent(studentID):
    """deletes student with student_id=studentID. returns deleted student"""
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id = %s RETURNING *", (studentID,))
    conn.commit()
    deletedStudent = cur.fetchone()
    cur.close()
    return deletedStudent


def main():
    print("getAllStudents()")
    for student in getAllStudents():
        print(student)
    print()

    print('addStudent("Abdul", "Hadi", "abdulhadi@cmail.carleton.ca", "2021-09-05")')
    newStudent = addStudent(
        "Abdul", "Hadi", "abdulhadi@cmail.carleton.ca", "2021-09-05"
    )
    print(f"{newStudent=}")
    for student in getAllStudents():
        print(student)
    print()

    print(f'updateStudentEmail({newStudent[0]=}, "2003abdulhadi@gmail.com")')
    updatedStudent = updateStudentEmail(newStudent[0], "2003abdulhadi@gmail.com")
    print(f"{updatedStudent=}")
    for student in getAllStudents():
        print(student)
    print()

    print(f"deletedStudent({newStudent[0]=})")
    deletedStudent = deleteStudent(newStudent[0])
    print(f"{deletedStudent=}")
    for student in getAllStudents():
        print(student)
    print()

    conn.close()


if __name__ == "__main__":
    main()
