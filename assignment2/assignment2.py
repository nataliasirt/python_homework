# Assignment 2
import csv
import traceback
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Task 2: Read a CSV File
def read_employees():
    data = {}
    rows = []
    
    try:
        with open('../csv/employees.csv', 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    data['fields'] = row
                else:
                    rows.append(row)
            data['rows'] = rows
    
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = []
        for trace in trace_back:
            stack_trace.append(f'File: {trace[0]}, Line: {trace[1]}, Func.Name: {trace[2]}, Message: {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        return {}
    
    return data

employees = read_employees()
print(employees)

# Task 3: Find the Column Index
def column_index(column_name):
    if column_name in employees["fields"]:
        return employees["fields"].index(column_name)
    else:
        print(f"Column '{column_name}' not found in fields.")
        return None

def employee_id_column():
    index = column_index("employee_id")
    if index is None:
        raise KeyError("The 'employee_id' column was not found in fields.")
    return index

# Task 4: Find the Employee First Name
def first_name(row_number):
    index = column_index("first_name")
    if index is None or row_number not in range(len(employees["rows"])):
        return None
    return employees["rows"][row_number][index]

# Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):
    column = employee_id_column()
    if column is None:
        raise KeyError("Employee ID column not found.")
    def employee_match(row):
        return int(row[employee_id_column()]) == employee_id

    match = list(filter(employee_match, employees["rows"]))
    return match

# Task 6: Find the Employee with a Lambda
def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column()]) == employee_id, employees["rows"]))
    return matches

# Task 7: Sort the Rows by last_name Using a Lambda
def sort_by_last_name():
    last_name_index = column_index("last_name")
    if last_name_index is None:
        raise KeyError("The 'last_name' column was not found in fields.")

    employees["rows"].sort(key=lambda row: row[last_name_index])
    return employees["rows"]

# Task 8: Create a dict for an Employee
def employee_dict(row):
    if "fields" not in employees:
        raise Exception("MissingDataError: 'fields' key is missing in the 'employees' dictionary.")

    employee_data = {}
    for i, field in enumerate(employees["fields"]):
        if field != "employee_id":
            employee_data[field] = row[i]
    return employee_data

# Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    employees_dict = {}
    for row in employees["rows"]:
        employee_id = row[column_index("employee_id")]
        employees_dict[employee_id] = employee_dict(row)
    return employees_dict

# Task 10: Use the os Module

def get_this_value():
    return os.getenv("THISVALUE")

print(get_this_value())

# Task 11: Creating Your Own Module
import custom_module

def set_that_secret(new_secret):
    return custom_module.set_secret(new_secret)

# Task 12: Read minutes1.csv and minutes2.csv
def read_minutes():
    def read_csv_to_dict(file_path):
        try:
            result = {}
            rows_lst = []
            with open(file_path, "r") as file:
                csv_data = csv.reader(file)
                for i, row in enumerate(csv_data):
                    if i == 0:
                        result["fields"] = row
                    else:
                        rows_lst.append(tuple(row))
                result["rows"] = rows_lst
            return result
        except Exception as e:
            print(f"Error reading files: {e}")
            exit(1)

    minutes1 = read_csv_to_dict("../csv/minutes1.csv")
    minutes2 = read_csv_to_dict("../csv/minutes2.csv")
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
print("minutes1", minutes1)
print("minutes2", minutes2)

# Task 13: Create minutes_set
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    set1.update(set2)
    return set1

minutes_set = create_minutes_set()
print("minutes set: ", minutes_set)

# Task 14: Convert to datetime
def create_minutes_list():
    global minutes_list
    minutes_list = list(minutes_set)
    minutes_list = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list))

    return minutes_list

minutes_list = create_minutes_list()
print("minutes_list ", minutes_list)

# Task 15: Write Out Sorted List
def write_sorted_list():
    minutes_list.sort(key=lambda row: row[1])
    sorted_lst = list(map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list))
    try:
        with open("./minutes.csv", "w", newline="") as file:
            output = csv.writer(file)
            output.writerow(minutes1["fields"])
            output.writerows(sorted_lst)
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
    return sorted_lst

write_sorted_list()