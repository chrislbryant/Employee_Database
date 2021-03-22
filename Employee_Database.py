from datetime import date
from datetime import datetime
from dateutil import relativedelta
import pickle 
import os.path
from os import path
import pandas as pd
   
class Person:
    """ Blueprint for a Person instance. """

    def __init__(self,name):
        self.name = name     

class Employee(Person):
    """ Blueprint for a Employee instance. """

    def __init__(self, employee_id, name, title, salary, start_date, end_date=None, rating=None, review=None):
        super().__init__(name)
        self.employee_id = employee_id
        self.title       = title
        self.salary      = salary
        self.start_date  = start_date
        self.end_date    = end_date
        self.rating      = rating
        self.review      = review

    def fetch_months_of_service(self):
        now  = datetime.now()
        diff = relativedelta.relativedelta(now, self.start_date)
        diff = diff.years * 12 + diff.months
        return diff

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __str__(self):
        return f""" 
ID: {self.employee_id}
NAME: {self.name} 
TITLE: {self.title}
SALARY: {self.salary}
START DATE: {self.start_date}
END DATE: {self.end_date}
RATING: {self.rating}
REVIEW: {self.review} 
        """

class EmployeeDatabase:
    """ Blueprint for a Database instance. """

    def __init__(self,employees = []):
        if not isinstance(employees, list):
            raise ValueError("Argument Must Be a List")
        if len(employees):
            for employee in employees:
                if not isinstance(employee, Employee):
                    raise TypeError(f"All objects must be employees. {employee} is not an employee.")
                    
        self.employees = employees 

    def __iter__(self):
        self.iter = 0 
        return self.iter

    def __next__(self):
        if self.iter < len(self.employees):
            e = self.employees[self.iter]
            self.iter = self.iter + 1
            return e
        else:
            raise StopIteration("Out of Bounds") 

    def add_employee(self, name, title, salary, start_date):
        employee_id = len(self.employees) + 1
        employee = Employee(employee_id, name, title, salary, start_date)
        self.employees.append(employee)
        return employee

    def update_employee(self, employee_id, params):
        rows_affected = 0
        for employee in self.employees:
            if employee.employee_id == employee_id:
                for param, value in params.items():
                    employee[param] = value
                rows_affected = +1
        return rows_affected    

    def search_employees(self, params):
        emp_list = []
        for employee in self.employees:
            for param, value in params.items():
                if isinstance(employee[param], str) and value.lower() in employee[param].lower() \
                or value == employee[param]:
                    emp_list.append(employee)
        return emp_list 

    def remove_employee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                self.employees.remove(employee)
                return employee
            else:
                return None

    def load_database(self, load_file):
        with open(f"C:/Users/chrisb/Desktop/Chris/Michael_Projects/Michael_Projects/Employee_Database/{load_file}.pickle", "rb") as pickle_file:
            try:
                self.employees = pickle.load(pickle_file)
            except EOFError:
                self.employees = []
        return load_file
    
    def save_database(self, save_file):
        with open(f"C:/Users/chrisb/Desktop/Chris/Michael_Projects/Michael_Projects/Employee_Database/{save_file}.pickle", "wb") as pickle_file:
            pickle.dump(self.employees, pickle_file)  
        return save_file        

    def export_database(self, export_file):
        df = pd.DataFrame([vars(f) for f in self.employees])
        df.to_csv(f"C:/Users/chrisb/Desktop/Chris/Michael_Projects/Michael_Projects/Employee_Database/{export_file}.csv", index=False)
        return export_file

class DatabaseInterface:
    """ Blueprint for a Database Interface instance. """

    def __init__(self, employees):
        self.database = EmployeeDatabase(employees)
    
    def add_employee(self):
        name = f"Enter Employee's Name: "
        title = f"Enter Employee's Title: "
        salary = f"Enter Employee's Salary (No Comma's): "
        start_date = f"Enter Employee's Start Date (Month/Day/Year): "

        employee_name = input(name)
        employee_title = input(title)
        employee_salary = input(salary)
        employee_start_date = input(start_date)

        employee = self.database.add_employee(
            employee_name, 
            employee_title, 
            employee_salary, 
            employee_start_date
        )
        print(employee)

    def update_employee(self):
        keys = ("name", "title", "salary", "rating", "review")
        id_selection = f"Enter Employee Id: "
        employee_id_error = f"""Please enter a number."""
        selection_error = f"""Selection must be 1-5."""
        menu = f"""
1. Name
2. Title
3. Salary
4. Rating
5. Review

Select a menu option: """


        value = lambda x: f"Enter Value for Employee's {x}: "
        try:
            employee_id = int(input(id_selection))
        except ValueError:
            print(employee_id_error)
        try:
            selection = int(input(menu))
        except ValueError:
            print(selection_error)
        value = input(value(keys[selection - 1]))
        params = {keys[selection - 1]: value}

        employee = self.database.update_employee(employee_id, params)
        print(employee)

    def search_employees(self):
        keys = ("name", "title", "salary", "rating", "review")
        menu = f"""
1. Name
2. Title
3. Salary
4. Rating
5. Review

Select a menu option: """

        value = lambda x: f"Enter Value for Employee's {x}: "

        selection = int(input(menu))
        value = input(value(keys[selection - 1]))
        params = {keys[selection - 1]: value}

        employees = self.database.search_employees(params)
        for employee in employees:
            print(employee)

    def remove_employee(self):
        id_selection = f"Enter Employee Id to Remove Employee: "

        employee_id = int(input(id_selection))

        employee = self.database.remove_employee(employee_id)
        print(employee)

    def print_employees(self):
        print("Current Employees")
        employees = self.database.employees
        if not len(employees):
            print("Database has no entries.")
        else:
            for employee in employees:
                print(employee)

    def should_be_reviewed(self, employee, end=datetime.now()):
        start = datetime.strptime(employee.start_date, "%m/%d/%Y")
        dif   = relativedelta.relativedelta(end, start)
        dif   = dif.years * 12 + dif.months
        if dif %6 == 0:
            return True
        return False

    def employees_for_review(self, date):
        print("Employees that need a review")
        employees = self.database.employees
        for employee in employees:
            if self.should_be_reviewed(employee):
                print(employee.name)
            else:
                print("All Employees have been reviewed")

    def load_file(self):
        name = f"Enter File Name: "

        file_name = input(name)

        load_file = self.database.load_database(file_name)
        print(f"Loading {load_file}.")

    def save_file(self):
        name = f"Enter File Name: "

        file_name = input(name)
        while path.exists(f"C:/Users/chrisb/Desktop/Chris/Michael_Projects/Michael_Projects/Employee_Database/{file_name}.pickle"):
            file_name = input(name)

        save_file = self.database.save_database(file_name)
        print(f"Saving {save_file}.")

    def export_file(self):
        name = f"Enter File Name: "

        file_name = input(name)
        while path.exists(f"C:/Users/chrisb/Desktop/Chris/Michael_Projects/Michael_Projects/Employee_Database/{file_name}.csv"):
            file_name = input(name)

        save_file = self.database.export_database(file_name)
        print(f"{save_file} Exported.")

    def menu(self):
        menu = f"""
1. Add Employee
2. Update Employee
3. Search Employee
4. Remove Employee
5. Print Employee
6. Employee's That Need a Review
7. Load File
8. Save File
9. Export File
10. Exit
    
Select a menu option: """
        selection_error = f"""Selection must be 1-10."""

        selection = None

        while selection != 10:
            try:
                selection = int(input(menu))
            except ValueError:
                print(selection_error)
            if selection == 1:
                self.add_employee()
            elif selection == 2:
                self.update_employee()
            elif selection == 3:
                self.search_employees()
            elif selection == 4:
                self.remove_employee()
            elif selection == 5:
                self.print_employees()
            elif selection == 6:
                self.employees_for_review(date)
            elif selection == 7:
                self.load_file() 
            elif selection == 8:
                self.save_file()      
            elif selection == 9:
                self.export_file()      

    def run(self):
        self.menu()

def main():
    employees = []
    dbi = DatabaseInterface(employees)
    dbi.run()

if __name__ == "__main__":
    main()
   