import traceback  # Helps us see where errors happen
#Assignment 2. Task 1
try:
    # Open diary.txt in append mode ('a') using a with statement
    with open('diary.txt', 'a') as file:
        # First prompt
        line = input("What happened today? ")
        file.write(line + '\n')  # Write the line with a newline
        
        # Loop for more entries
        while True:
            line = input("What else? ")
            file.write(line + '\n')  # Write each line with a newline
            if line == "done for now":
                break  # Exit the loop when "done for now" is entered

except Exception as e:
    # If something goes wrong, show the error details
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = []
    for trace in trace_back:
        stack_trace.append(f'File: {trace[0]}, Line: {trace[1]}, Func.Name: {trace[2]}, Message: {trace[3]}')
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")