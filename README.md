# **Distributed Heterogeneous Database Management System (DDBMS) Report**

## **1. Introduction**
This report details the implementation of a **Distributed Heterogeneous Database Management System (DDBMS)**. The system is designed to handle fragmentation, allocation, and reconstruction of data across multiple sites, each running different database management systems and operating systems.

## **2. System Architecture**
The distributed database environment comprises three different sites with distinct database platforms:

| **Site**  | **Database Platform** | **Operating System**  | **Stored Data** |
|-----------|----------------------|----------------------|----------------|
| **Site 1** | MySQL                 | Ubuntu               | Students (Personal Details) and Enrollments |
| **Site 2** | PostgreSQL            | Ubuntu               | Courses, Degrees, and Departments |
| **Site 3** | MariaDB               | Windows              | Payments |

This heterogeneous setup ensures **data distribution across multiple platforms** while enabling efficient data retrieval and updates.

---
## **3. Fragmentation Implementation**
Fragmentation was implemented in two forms: **horizontal fragmentation** and **vertical fragmentation**.

### **3.1 Horizontal Fragmentation**
- The **Students** and **Enrollments** tables were horizontally fragmented based on the **campus** location.
- Each site stores students and enrollments specific to that campus.

#### **SQL Example for Horizontal Fragmentation:**
```sql
CREATE TABLE students_campus1 AS
SELECT * FROM Students WHERE Campus = 'North Campus';

CREATE TABLE students_campus2 AS
SELECT * FROM Students WHERE Campus = 'South Campus';
```

### **3.2 Vertical Fragmentation**
- The **Students** table was vertically fragmented into two parts:
  - **`students_personal`** in MySQL (Site 1) → Stores Student_ID, Name, Campus, and Enrollment_Date.
  - **`students_degree`** in PostgreSQL (Site 2) → Stores Student_ID, Name, Degree_ID, and Degree_Name.

#### **SQL Example for Vertical Fragmentation:**
```sql
-- Site 1 (MySQL)
CREATE TABLE students_personal AS
SELECT Student_ID, Name, Campus, Enrollment_Date FROM Students;

-- Site 2 (PostgreSQL)
CREATE TABLE students_degree (
    Student_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Degree_ID INT,
    Degree_Name VARCHAR(255),
    FOREIGN KEY (Degree_ID) REFERENCES degree(Degree_ID)
);
```

---
## **4. Query Access Frequencies**
To optimize data distribution, the following query access frequencies were considered:

| **Query** | **Frequency** | **Primary Database** |
|-----------|-------------|------------------|
| Retrieve Student Personal Details | High | MySQL (Site 1) |
| Retrieve Degree Information | Medium | PostgreSQL (Site 2) |
| Retrieve Course & Department Details | Medium | PostgreSQL (Site 2) |
| Retrieve Student Payment Details | Low | MariaDB (Site 3) |

This approach ensures that frequently accessed data remains **localized to a specific database**, minimizing the need for excessive cross-site queries.

---
## **5. Physical Fragment Allocation**
The fragments were allocated as follows:

- **Site 1 (MySQL)** → `students_personal`, `enrollments`
- **Site 2 (PostgreSQL)** → `students_degree`, `courses`, `departments`
- **Site 3 (MariaDB)** → `payments`

Each site handles queries related to its allocated fragments to ensure efficient data access and retrieval.

---
## **6. Decision Site & Reconstruction**
The **decision site** is **Site 1 (MySQL)**, responsible for overseeing the **reconstruction of fragmented data**. Reconstruction was implemented using Python scripts to merge `students_personal` and `students_degree`.

#### **Python Code for Reconstruction:**
```python
from connect import connect_to_mysql, connect_to_postgresql

def reconstruct_students_table():
    mysql_conn = connect_to_mysql()
    postgres_conn = connect_to_postgresql()
    
    if mysql_conn and postgres_conn:
        mysql_cursor = mysql_conn.cursor()
        postgres_cursor = postgres_conn.cursor()
        
        mysql_cursor.execute("SELECT Student_ID, Name, Campus, Enrollment_Date FROM students_personal")
        students_personal_data = mysql_cursor.fetchall()
        
        students_degree_data = {}
        for student in students_personal_data:
            student_id = student[0]
            postgres_cursor.execute("SELECT Degree_ID, Degree_Name FROM students_degree WHERE Student_ID = %s", (student_id,))
            degree_data = postgres_cursor.fetchone()
            if degree_data:
                students_degree_data[student_id] = degree_data

        reconstructed_students = []
        for student in students_personal_data:
            student_id = student[0]
            name, campus, enrollment_date = student[1], student[2], student[3]
            degree_data = students_degree_data.get(student_id, (None, "Unknown"))
            degree_id, degree_name = degree_data
            reconstructed_students.append((student_id, name, campus, enrollment_date, degree_id, degree_name))

        print("Reconstructed Students Data:")
        for student in reconstructed_students:
            print(student)
```
This process allows for a **complete view of student data** by merging **personal and academic information**.

---
## **7. Applications & Calculus Queries**
To verify data integrity and support analytical queries, we used **relational calculus queries**.

### **Tuple Relational Calculus (TRC) Queries:**
- **Retrieve students from North Campus:**
  ```
  { S | S ∈ Students ∧ S.Campus = 'North Campus' }
  ```
- **Retrieve students enrolled in Computer Science:**
  ```
  { S | S ∈ Students ∧ ∃ D (D ∈ Degrees ∧ S.Degree_ID = D.Degree_ID ∧ D.Degree_Name = 'Computer Science') }
  ```

These queries validate the correctness of the fragmented data and ensure logical consistency across the distributed environment.

---
## **8. Conclusion**
This implementation successfully demonstrates:
✅ **Distributed heterogeneous database design** with MySQL, PostgreSQL, and MariaDB.  
✅ **Fragmentation (horizontal and vertical) to optimize query access patterns.**  
✅ **Physical allocation of data to different sites.**  
✅ **Reconstruction using Python scripts to restore full student records.**  
✅ **Query formulation using relational calculus.**  


