import pandas as pd
import numpy as np
import json
import os

# Task 1: Create a DataFrame from a dictionary
data = {
    'Name': ['Alice', 'Bob', 'charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
task1_data_frame = pd.DataFrame(data)

# Add new column
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]

# Modify existing column
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1

# Save to CSV without index
task1_older.to_csv('employees.csv', index=False)

# Task 2: Loading Data
task2_employees = pd.read_csv('employees.csv')

json_data = {
    "Name": ["Eve", "Frank"],
    "Age": [28, 40],
    "City": ["Miami", "Seattle"],
    "Salary": [60000, 95000]
}
with open('additional_employees.json', 'w') as file:
    json.dump(json_data, file)

json_employees = pd.read_json('additional_employees.json')

more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)

# Task 3: DataFrame Operations
first_three = more_employees.head(3)
last_two = more_employees.tail(2)
employee_shape = more_employees.shape

# Task 4: Data Cleaning
dirty_data = pd.read_csv('dirty_data.csv')  
clean_data = dirty_data.copy()

# Remove duplicate rows
clean_data = clean_data.drop_duplicates()

# Convert Age to numeric and handle missing values
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')

# Convert Salary to numeric and replace placeholders with NaN
clean_data['Salary'] = clean_data['Salary'].str.strip()
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'].replace(['unknown', 'n/a'], np.nan))

# Fill missing numeric values
clean_data['Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())

# Convert Hire Date to datetime with mixed format
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], format='mixed', errors='coerce')

# Strip whitespace and convert Name and Department to uppercase
clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()