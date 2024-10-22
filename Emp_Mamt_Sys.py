import mysql.connector
from prettytable import PrettyTable #output table format
host = input("Enter database host : ")
user = input("Enter database user :")
password = input("Enter database password: ")
database = input("Enter database name: ")

con=mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
)
def check_employee(emp_id):     
        check=con.cursor() 
        sql="SELECT * FROM Emp_Mang_System WHERE emp_id = %s"
        check.execute(sql,(emp_id,))
        check_ok=check.fetchone() 
        check.close()
        return check_ok
def reassign_ids():
        reasign=con.cursor()
        sql = """
                UPDATE Emp_Mang_System 
                SET emp_id = (
                        SELECT new_id
                        FROM (
                        SELECT emp_id, ROW_NUMBER() OVER (ORDER BY emp_id) AS new_id
                        FROM Emp_Mang_System
                        ) AS ranked_employees
                        WHERE ranked_employees.emp_id = Emp_Mang_System.emp_id);"""
        reasign.execute(sql)
        reasign.execute("DROP TEMPORARY TABLE IF EXISTS temp_ids")
        con.commit()
def table_pretty(data):
        table = PrettyTable()
        table.field_names = ["Employee ID", "Name", "Position", "Salary"]
        for record in data:
                table.add_row(record)
        return table
def add_employee():
        emp_id=input("Enter The Employee Id :")
        add_check=check_employee(emp_id)
        if add_check:
                print(table_pretty([add_check]))
                print("Empolyee Already exist. Enter The New id")
                return
        else:
                print("Enter New Employee Details:")
                emp_name=input("Enter The Name : ")
                emp_post=input("Enter The Post : ")
                emp_salary=float(input("Enter The Salary : "))
        sql="INSERT INTO Emp_Mang_System(emp_id,emp_name, emp_post,emp_salary) VALUES(%s,%s, %s, %s)"
        data=(emp_id,emp_name,emp_post,emp_salary)
        added=con.cursor()
        added.execute(sql, data)
        con.commit()
        reassign_ids()  
        print(table_pretty([data]))
        print("New Employee added successfully.")
        added.close()       
def remove_employee():
        emp_id=input("Enter The Employee Id:")
        remove_check=check_employee(emp_id)
        if not remove_check:
                print("Employee not Found..Enter The Correct Id...")
                return
        else:
                sql="DELETE FROM Emp_Mang_System WHERE emp_id=%s"
        data=(emp_id,)
        remove=con.cursor()
        remove.execute(sql,data)
        con.commit()
        reassign_ids()     
        print(table_pretty([remove_check]))
        print("Employee Removed Successfully...")
        remove.close()
def update_employee():
        emp_id = input("Enter The Employee Id:")
        update_check=check_employee(emp_id)
        if not update_check:
                print("Employee Not Found...Enter Correct Id...")
                return
        print(f"Current details:\n{table_pretty([update_check])}")  
        confirm_post = input("Do you want to update the Post? (yes/no): ").strip().lower()
        if confirm_post == "yes":
                emp_post = input("Enter New Post : ")
        else:
                emp_post = None  
        confirm_salary = input("Do you want to update the Salary? (yes/no): ").strip().lower()
        if confirm_salary == "yes":
                emp_salary = float(input("Enter New Salary : "))
        else:
                emp_salary = None      
        sql = "UPDATE Emp_Mang_System SET emp_post = coalesce(%s,emp_post), emp_salary = coalesce(%s,emp_salary) WHERE emp_id = %s"
        data=(emp_post,emp_salary,emp_id)
        update=con.cursor()
        update.execute(sql, data)
        con.commit()
        display_data = (emp_id, update_check[1], emp_post, emp_salary)
        print(table_pretty([display_data]))
        print("Employee Details Updated sucessfully...")
        update.close()
def display_employee():
        sql="select * from Emp_Mang_System ORDER BY emp_id"
        display=con.cursor()
        display.execute(sql)
        display_all=display.fetchall()
        print("Dislpay  All Employee Details....")
        if display_all:
                print(table_pretty(display_all))
        reassign_ids()       
        display.close()
def select_employee(emp_id):
        select=con.cursor()
        sql="select * from Emp_Mang_System WHERE emp_id=%s"
        select.execute(sql,(emp_id,))
        select_ok=select.fetchone()
        if select_ok:
                print(table_pretty([select_ok]))
        else:
                print("Employee Not found...Enter The Correct Employee Id...")
while True:
        print("\nWelcome to Employee Management Record")
        print("Press:")
        print("1 to Add Employee")
        print("2 to remove Employee")
        print("3 to update Employee")
        print("4 to display Employee")
        print("5 to select employee")
        print("6 to Exit")

        choice=input("entet your choice:")
        if choice == "1":
                        add_employee()
        elif choice == "2":
                        remove_employee()
        elif choice == "3":
                        update_employee()
        elif choice == "4":
                        display_employee()
        elif choice == "5":
                        emp_id=int(input("enter the id : "))
                        select_employee(emp_id)
        elif choice == "6":
                        print("Existing the program.")
                        con.close()
                        break
        else:
                        print("invalid chioce : ")
