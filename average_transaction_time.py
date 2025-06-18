# average_transaction_time.py

import sys
from datetime import datetime

def parse_timestamp(line):
    try:
        timestamp_str = line.split('\t')[0]
        return datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S.%f")
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python average_transaction_time.py \"filename\"")
        return

    filename = sys.argv[1]
    start_times = {}
    durations = []

    try:
        with open(filename, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                line = line.strip()
                ts = parse_timestamp(line)
                if ts is None:
                    continue

                if "transaction" in line and "begun" in line:
                    try:
                        tx_id = line.split("transaction ")[1].split(" begun")[0]
                        start_times[tx_id] = ts
                    except IndexError:
                        continue

                elif "transaction done, id=" in line:
                    try:
                        tx_id = line.split("id=")[1].strip()
                        if tx_id in start_times:
                            duration_ms = (ts - start_times[tx_id]).total_seconds() * 1000
                            durations.append(duration_ms)
                    except IndexError:
                        continue

        if durations:
            average = sum(durations) / len(durations)
            print("{:.2f}".format(average))
        else:
            print("0.00")

    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    main()
