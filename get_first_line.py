# get_first_line.py

import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python get_first_line.py \"filename\"")
        return

    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8", errors="replace") as f:
            first_line = f.readline().rstrip("\n")
            print(first_line)
    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    main()
