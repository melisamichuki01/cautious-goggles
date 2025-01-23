from connect import connect_to_mysql, connect_to_postgresql

def drop_existing_tables():
    """
    Drop existing fragmented tables if they exist.
    """
    mysql_conn = connect_to_mysql()
    postgres_conn = connect_to_postgresql()

    if mysql_conn and postgres_conn:
        mysql_cursor = mysql_conn.cursor()
        postgres_cursor = postgres_conn.cursor()

        try:
            # Drop the fragmented tables if they exist
            mysql_cursor.execute("DROP TABLE IF EXISTS students_personal")
            postgres_cursor.execute("DROP TABLE IF EXISTS students_degree")
            mysql_conn.commit()
            postgres_conn.commit()
            print("Existing fragmented tables dropped successfully.")
        except Exception as e:
            print(f"Error while dropping tables: {e}")
        finally:
            mysql_cursor.close()
            postgres_cursor.close()

def vertical_fragmentation():
    """
    Perform vertical fragmentation:
    - `students_personal` in MySQL (Site 1) with personal details.
    - `students_degree` in PostgreSQL (Site 2) with student-degree mapping.
    """
    mysql_conn = connect_to_mysql()
    postgres_conn = connect_to_postgresql()

    if mysql_conn and postgres_conn:
        mysql_cursor = mysql_conn.cursor()
        postgres_cursor = postgres_conn.cursor()

        try:
            # Step 1: Create `students_personal` fragment in MySQL (Site 1)
            create_personal_fragment = """
            CREATE TABLE IF NOT EXISTS students_personal AS 
            SELECT Student_ID, Name, Campus, Enrollment_Date 
            FROM Students;
            """
            mysql_cursor.execute(create_personal_fragment)

            # Step 2: Create `students_degree` fragment in PostgreSQL (Site 2)
            create_degree_fragment = """
            CREATE TABLE IF NOT EXISTS students_degree (
                Student_ID INT PRIMARY KEY,
                Name VARCHAR(255),
                Degree_ID INT,
                Degree_Name VARCHAR(255),
                FOREIGN KEY (Degree_ID) REFERENCES degree(Degree_ID)
            );
            """
            postgres_cursor.execute(create_degree_fragment)

            # Step 3: Fetch Student_ID, Name, Degree_ID from MySQL (Site 1)
            mysql_cursor.execute("SELECT Student_ID, Name, Degree_ID FROM Students")
            student_data = mysql_cursor.fetchall()

            if student_data:
                # Step 4: Fetch Degree_Name from PostgreSQL (Site 2)
                degree_ids = {row[2] for row in student_data}  # Unique Degree_IDs
                degree_names = {}

                for degree_id in degree_ids:
                    postgres_cursor.execute("SELECT Degree_Name FROM degree WHERE Degree_ID = %s", (degree_id,))
                    degree_name = postgres_cursor.fetchone()
                    if degree_name:
                        degree_names[degree_id] = degree_name[0]

                # Step 5: Insert combined data into students_degree in PostgreSQL
                student_degree_data = [
                    (student_id, name, degree_id, degree_names.get(degree_id, "Unknown"))
                    for student_id, name, degree_id in student_data
                ]

                insert_query = "INSERT INTO students_degree (Student_ID, Name, Degree_ID, Degree_Name) VALUES (%s, %s, %s, %s)"
                postgres_cursor.executemany(insert_query, student_degree_data)
                postgres_conn.commit()
                print("Inserted student degree data into PostgreSQL.")

            print("Vertical fragmentation completed successfully.")

        except Exception as e:
            print(f"Error during vertical fragmentation: {e}")
            mysql_conn.rollback()
            postgres_conn.rollback()
        finally:
            mysql_cursor.close()
            mysql_conn.close()
            postgres_cursor.close()
            postgres_conn.close()

def view_vfragmented_data():
    """
    View fragmented data for students personal details and student-degree mappings.
    """
    mysql_conn = connect_to_mysql()
    postgres_conn = connect_to_postgresql()

    if mysql_conn and postgres_conn:
        mysql_cursor = mysql_conn.cursor()
        postgres_cursor = postgres_conn.cursor()

        try:
            # Ask the user what data they want to view
            print("\nDo you want to view:")
            print("1. Students Personal Details (MySQL - Site 1)")
            print("2. Student Degree Mappings (PostgreSQL - Site 2)")
            choice = input("Enter your choice (1/2): ")

            if choice == "1":
                # Display student personal details from MySQL
                mysql_cursor.execute("SELECT COUNT(*) FROM students_personal")
                count = mysql_cursor.fetchone()[0]
                print(f"\nStudents Personal Details - Count: {count}")
                mysql_cursor.execute("SELECT * FROM students_personal")
                students = mysql_cursor.fetchall()
                for student in students:
                    print(student)

            elif choice == "2":
                # Display student degree mappings from PostgreSQL
                postgres_cursor.execute("SELECT COUNT(*) FROM students_degree")
                count = postgres_cursor.fetchone()[0]
                print(f"\nStudent Degree Mappings - Count: {count}")
                postgres_cursor.execute("SELECT * FROM students_degree")
                student_degrees = postgres_cursor.fetchall()
                for student_degree in student_degrees:
                    print(student_degree)

            else:
                print("Invalid choice. Please choose 1 or 2.")

            # Prompt user for another action
            again = input("\nDo you want to perform another action? (yes/no): ").strip().lower()
            if again == "yes":
                view_vfragmented_data()
            else:
                print("Exiting...")

        except Exception as e:
            print(f"Error while viewing fragmented data: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()
            postgres_cursor.close()
            postgres_conn.close()

def student_details():
    """
    Main function to drop existing tables, perform vertical fragmentation, and allow users to view the data.
    """
    
    drop_existing_tables()

    print("Performing vertical fragmentation...")
    vertical_fragmentation()

    # Prompt to view fragmented data
    view_vfragmented_data()


