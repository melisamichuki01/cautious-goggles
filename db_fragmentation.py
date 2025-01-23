from connect import connect_to_mysql, connect_to_postgresql

def get_students_by_campus(campus):
    """
    Fetch students based on the selected campus.
    """
    mysql_conn = connect_to_mysql()
    if mysql_conn:
        mysql_cursor = mysql_conn.cursor()
        try:
            sql = "SELECT Student_ID, Name, Department_ID, Enrollment_Date FROM Students WHERE Campus = %s"
            mysql_cursor.execute(sql, (campus,))
            students = mysql_cursor.fetchall()
            
            if students:
                print(f"\nStudents in {campus}:")
                for student in students:
                    print(f"ID: {student[0]}, Name: {student[1]}, Department: {student[2]}, Enrollment Date: {student[3]}")
            else:
                print(f"No students found in {campus}.")

        except Exception as e:
            print(f"MySQL error: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()


def get_students_by_course(campus):
    """
    Fetch students and their enrolled courses for the selected campus.
    """
    mysql_conn = connect_to_mysql()
    postgres_conn = connect_to_postgresql()

    if mysql_conn and postgres_conn:
        mysql_cursor = mysql_conn.cursor()
        postgres_cursor = postgres_conn.cursor()
        try:
            # Fetch students from the selected campus (from MySQL - Site 1)
            sql_students = "SELECT Student_ID, Name FROM Students WHERE Campus = %s"
            mysql_cursor.execute(sql_students, (campus,))
            students = mysql_cursor.fetchall()

            if students:
                print(f"\nCourses taken by students in {campus}:")
                for student in students:
                    student_id, student_name = student

                    # Fetch the courses the student is enrolled in (from MySQL - Site 1)
                    sql_enrollments = "SELECT Course_ID FROM Enrollments WHERE Student_ID = %s"
                    mysql_cursor.execute(sql_enrollments, (student_id,))
                    enrolled_courses = mysql_cursor.fetchall()

                    if enrolled_courses:
                        print(f"\n{student_name} (Student ID: {student_id}) is enrolled in:")
                        for course in enrolled_courses:
                            course_id = course[0]

                            # Fetch course details from PostgreSQL (Site 2)
                            sql_course_details = "SELECT Course_Name, Department_ID FROM Courses WHERE Course_ID = %s"
                            postgres_cursor.execute(sql_course_details, (course_id,))
                            course_details = postgres_cursor.fetchone()

                            if course_details:
                                course_name, department_id = course_details
                                print(f"  - {course_name} (Course ID: {course_id}, Department: {department_id})")
                            else:
                                print(f"  - Course ID {course_id} (Details not found in PostgreSQL)")

                    else:
                        print(f"{student_name} is not enrolled in any courses.")

            else:
                print(f"No students found in {campus}.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            mysql_cursor.close()
            postgres_cursor.close()
            mysql_conn.close()
            postgres_conn.close()


def main():
    """
    Main function to allow user to select a campus and view either students or courses.
    """
    campuses = ["Main Campus", "East Campus", "West Campus"]

    print("Select a campus:")
    for i, campus in enumerate(campuses, start=1):
        print(f"{i}. {campus}")

    choice = input("Enter the number of the campus: ")
    if choice in ["1", "2", "3"]:
        selected_campus = campuses[int(choice) - 1]

        print(f"\nFetching data for {selected_campus}...\n")

        # Ask user what they want to see
        print("What would you like to see?")
        print("1. List of students in the campus")
        print("2. Courses students in the campus are enrolled in")

        data_choice = input("Enter 1 or 2: ")

        if data_choice == "1":
            get_students_by_campus(selected_campus)
        elif data_choice == "2":
            get_students_by_course(selected_campus)
        else:
            print("Invalid choice. Please enter 1 or 2.")

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
