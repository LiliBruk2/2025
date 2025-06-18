# count_true_errors.py

import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python count_true_errors.py \"filename\"")
        return

    filename = sys.argv[1]
    error_count = 0

    try:
        with open(filename, "r", encoding="utf-8", errors="replace") as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) > 1 and parts[1] == "ERROR":
                    error_count += 1
        print(error_count)
    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    main()
