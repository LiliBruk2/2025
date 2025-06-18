with open("exam.log", "r") as file:
    first_line = file.readline()
    print(first_line)

error_count = 0
with open("exam.log", "r") as file:
    for line in file:
        if "ERROR" in line:
            error_count += 1
print("Number of ERROR lines:", error_count)


transaction_count = 0
with open("exam.log", "r") as file:
    for line in file:
        if "transaction" in line and "begun" in line:
            transaction_count += 1

print("Number of transactions:", transaction_count)

from datetime import datetime

def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M:%S.%f")

file_path = "exam.log"  # Update if needed

transaction_times = {}
start_times = {}

with open(file_path, "r") as file:
    for line in file:
        parts = line.split("\t")  # Tab-separated log format
        timestamp = parts[0].split()[-1]  # Extract time part from date-time field

        if "transaction" in line and "begun" in line:
            transaction_id = line.split("transaction ")[-1].split(" begun")[0]
            start_times[transaction_id] = parse_time(timestamp)
        
        elif "transaction done, id=" in line:
            transaction_id = line.split("id=")[-1].strip()
            if transaction_id in start_times:
                duration = (parse_time(timestamp) - start_times.pop(transaction_id)).total_seconds() * 1000
                transaction_times[transaction_id] = duration

if transaction_times:
    fastest_transaction = min(transaction_times, key=transaction_times.get)
    print(f"Fastest Transaction ID: {fastest_transaction}")
else:
    print("No completed transactions found.")


from datetime import datetime

def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M:%S.%f")

file_path = "exam.log"  # Update if needed

transaction_times = {}
start_times = {}

with open(file_path, "r") as file:
    for line in file:
        parts = line.split("\t")  # Tab-separated log format
        timestamp = parts[0].split()[-1]  # Extract time part from date-time field

        if "transaction" in line and "begun" in line:
            transaction_id = line.split("transaction ")[-1].split(" begun")[0]
            start_times[transaction_id] = parse_time(timestamp)
        
        elif "transaction done, id=" in line:
            transaction_id = line.split("id=")[-1].strip()
            if transaction_id in start_times:
                duration = (parse_time(timestamp) - start_times.pop(transaction_id)).total_seconds() * 1000
                transaction_times[transaction_id] = duration

if transaction_times:
    average_transaction_time = sum(transaction_times.values()) / len(transaction_times)
    print(f"Average Transaction Time in ms: {average_transaction_time:.2f}")
else:
    print("No valid transactions found to compute average time.")
