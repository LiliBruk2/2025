# count_transactions.py

import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_transactions.py \"filename\"")
        return

    filename = sys.argv[1]
    started = set()
    completed = set()

    try:
        with open(filename, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                line = line.strip()
                if "transaction" in line and "begun" in line:
                    # Extract transaction ID
                    try:
                        tx_id = line.split("transaction ")[1].split(" begun")[0]
                        started.add(tx_id)
                    except IndexError:
                        continue

                elif "transaction done, id=" in line:
                    try:
                        tx_id = line.split("id=")[1].strip()
                        completed.add(tx_id)
                    except IndexError:
                        continue

        # Only count transactions that started and also completed
        full_transactions = started & completed
        print(len(full_transactions))

    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    main()
