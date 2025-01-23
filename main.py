from hfragment import campus_data
from vfragment import student_details
from reconstruction import reconstruct_students_table



def main():
    """
    Main function to run the application with options for reconstruction and viewing fragmented data.
    """
    while True:
        print("\nWelcome to the Student Management System (SMS) Application!")
        print("Choose an option:")
        print("1. View Student details & Degree Data")
        print("2. View Campus Data")
        print("3. Reconstruct Students Table and View All Students & Degrees")
        print("4. Exit")

        user_choice = input("Enter your choice (1/2/3/4): ").strip()

        if user_choice == "1":
            student_details()
        elif user_choice == "2":
            campus_data()
        elif user_choice == "3":
            reconstruct_students_table()
        elif user_choice == "4":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
