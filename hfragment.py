from connect import connect_to_mysql

def create_fragmented_students_table():
    """
    Create fragmented tables for students based on campus, dropping existing tables first.
    """
    mysql_conn = connect_to_mysql()
    if mysql_conn:
        mysql_cursor = mysql_conn.cursor()
        try:
            campuses = ["Main Campus", "East Campus", "West Campus"]
            for campus in campuses:
                table_name = campus.replace(" ", "_").lower() + "_students"
                
                # Drop the table if it exists
                drop_table_sql = f"DROP TABLE IF EXISTS {table_name};"
                mysql_cursor.execute(drop_table_sql)

                # Create table for each campus
                create_table_sql = f"""
                CREATE TABLE {table_name} (
                    Student_ID INT PRIMARY KEY,
                    Name VARCHAR(255),
                    Department_ID INT,
                    Enrollment_Date DATE,
                    Campus VARCHAR(50)
                );
                """
                mysql_cursor.execute(create_table_sql)
                mysql_conn.commit()
                print(f"Table {table_name} created successfully.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()

def create_fragmented_enrollments_table():
    """
    Create fragmented tables for enrollments based on campus, dropping existing tables first.
    """
    mysql_conn = connect_to_mysql()
    if mysql_conn:
        mysql_cursor = mysql_conn.cursor()
        try:
            campuses = ["Main Campus", "East Campus", "West Campus"]
            for campus in campuses:
                table_name = campus.replace(" ", "_").lower() + "_enrollments"
                
                # Drop the table if it exists
                drop_table_sql = f"DROP TABLE IF EXISTS {table_name};"
                mysql_cursor.execute(drop_table_sql)

                # Create table for each campus
                create_table_sql = f"""
                CREATE TABLE {table_name} (
                    Enrollment_ID INT PRIMARY KEY,
                    Student_ID INT,
                    Course_ID INT,
                    Enrollment_Date DATE,
                    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
                );
                """
                mysql_cursor.execute(create_table_sql)
                mysql_conn.commit()
                print(f"Table {table_name} created successfully.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()

def insert_data_into_fragmented_students():
    """
    Insert data into fragmented students tables based on campus.
    """
    mysql_conn = connect_to_mysql()
    if mysql_conn:
        mysql_cursor = mysql_conn.cursor()
        try:
            campuses = ["Main Campus", "East Campus", "West Campus"]
            for campus in campuses:
                table_name = campus.replace(" ", "_").lower() + "_students"
                insert_sql = f"""
                INSERT INTO {table_name} (Student_ID, Name, Department_ID, Enrollment_Date, Campus)
                SELECT Student_ID, Name, Department_ID, Enrollment_Date, Campus
                FROM Students
                WHERE Campus = %s;
                """
                mysql_cursor.execute(insert_sql, (campus,))
                mysql_conn.commit()
                print(f"Data inserted into {table_name} successfully.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()

def insert_data_into_fragmented_enrollments():
    """
    Insert data into fragmented enrollments tables based on campus.
    """
    mysql_conn = connect_to_mysql()
    if mysql_conn:
        mysql_cursor = mysql_conn.cursor()
        try:
            campuses = ["Main Campus", "East Campus", "West Campus"]
            for campus in campuses:
                table_name = campus.replace(" ", "_").lower() + "_enrollments"
                insert_sql = f"""
                INSERT INTO {table_name} (Enrollment_ID, Student_ID, Course_ID, Enrollment_Date)
                SELECT Enrollment_ID, Student_ID, Course_ID, Enrollment_Date
                FROM Enrollments
                WHERE Student_ID IN (
                    SELECT Student_ID FROM Students WHERE Campus = %s
                );
                """
                mysql_cursor.execute(insert_sql, (campus,))
                mysql_conn.commit()
                print(f"Data inserted into {table_name} successfully.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()

from connect import connect_to_mysql

def view_hfragmented_data():
    """
    View fragmented data for students or enrollments, based on campus.
    """
    mysql_conn = connect_to_mysql()
    if mysql_conn:
        mysql_cursor = mysql_conn.cursor()

        try:
            campuses = ["Main Campus", "East Campus", "West Campus"]
            while True:
                # Ask the user which campus they want to view
                print("\nWhich campus data do you want to view?")
                print("1. Main Campus")
                print("2. East Campus")
                print("3. West Campus")
                campus_choice = input("Enter your choice (1/2/3): ")

                if campus_choice == "1":
                    campus = "Main Campus"
                elif campus_choice == "2":
                    campus = "East Campus"
                elif campus_choice == "3":
                    campus = "West Campus"
                else:
                    print("Invalid choice. Exiting.")
                    return

                # Ask the user what data they want to view
                print("\nDo you want to view:")
                print("1. Students")
                print("2. Enrollments")
                data_choice = input("Enter your choice (1/2): ")

                if data_choice == "1":
                    # Display student data by campus
                    table_name = campus.replace(" ", "_").lower() + "_students"
                    query = f"SELECT COUNT(*) FROM {table_name}"
                    mysql_cursor.execute(query)
                    count = mysql_cursor.fetchone()[0]
                    print(f"\n{campus} - Students Count: {count}")
                    mysql_cursor.execute(f"SELECT * FROM {table_name}")
                    students = mysql_cursor.fetchall()
                    for student in students:
                        print(student)

                elif data_choice == "2":
                    # Display enrollment data by campus
                    table_name = campus.replace(" ", "_").lower() + "_enrollments"
                    query = f"SELECT COUNT(*) FROM {table_name}"
                    mysql_cursor.execute(query)
                    count = mysql_cursor.fetchone()[0]
                    print(f"\n{campus} - Enrollments Count: {count}")
                    mysql_cursor.execute(f"SELECT * FROM {table_name}")
                    enrollments = mysql_cursor.fetchall()
                    for enrollment in enrollments:
                        print(enrollment)

                else:
                    print("Invalid choice. Please choose 1 or 2.")

                # Ask user if they want to continue or exit
                again = input("\nDo you want to continue? (yes/no): ").strip().lower()
                if again == "no":
                    print("Exiting...")
                    break
                elif again != "yes":
                    print("Invalid input. Exiting.")
                    break

        except Exception as e:
            print(f"Error while viewing data: {e}")
        finally:
            mysql_cursor.close()
            mysql_conn.close()



def campus_data():
    """
    Main function to create fragmented tables, insert data, and allow users to view the data.
    """
    print("Creating fragmented students tables...")
    create_fragmented_students_table()

    print("Creating fragmented enrollments tables...")
    create_fragmented_enrollments_table()

    print("Inserting data into fragmented students tables...")
    insert_data_into_fragmented_students()

    print("Inserting data into fragmented enrollments tables...")
    insert_data_into_fragmented_enrollments()

    # Prompt to view fragmented data
    view_hfragmented_data()


