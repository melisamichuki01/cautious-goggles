from connect import connect_to_mysql, connect_to_postgresql

def reconstruct_students_table():
    """
    Reconstruct the full `Students` table by combining:
    - `students_personal` in MySQL (Site 1)
    - `students_degree` in PostgreSQL (Site 2)
    """
    mysql_conn = connect_to_mysql()
    postgres_conn = connect_to_postgresql()

    if mysql_conn and postgres_conn:
        mysql_cursor = mysql_conn.cursor()
        postgres_cursor = postgres_conn.cursor()

        try:
            # Step 1: Fetch `students_personal` data from MySQL (Site 1)
            mysql_cursor.execute("SELECT Student_ID, Name, Campus, Enrollment_Date FROM students_personal")
            students_personal_data = mysql_cursor.fetchall()

            # Step 2: Fetch `students_degree` data from PostgreSQL (Site 2)
            students_degree_data = {}
            for student in students_personal_data:
                student_id = student[0]
                postgres_cursor.execute("SELECT Degree_ID, Degree_Name FROM students_degree WHERE Student_ID = %s", (student_id,))
                degree_data = postgres_cursor.fetchone()
                if degree_data:
                    students_degree_data[student_id] = degree_data

            # Step 3: Combine the data from both fragments
            reconstructed_students = []
            for student in students_personal_data:
                student_id = student[0]
                name, campus, enrollment_date = student[1], student[2], student[3]
                degree_data = students_degree_data.get(student_id, (None, "Unknown"))
                degree_id, degree_name = degree_data
                reconstructed_students.append((student_id, name, campus, enrollment_date, degree_id, degree_name))

            # Step 4: Output the reconstructed data
            print("Reconstructed Students Data:")
            for student in reconstructed_students:
                print(student)

        except Exception as e:
            print(f"Error during reconstruction: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()
            postgres_cursor.close()
            postgres_conn.close()

if __name__ == "__main__":
    reconstruct_students_table()
