import csv
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv"


def main():
    total = 0
    anomalies = 0
    normal = 0

    with open(DATA_FILE, newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            value = float(row[0])
            total += 1

            if value > 80:
                anomalies += 1
            else:
                normal += 1

    print(f"Total measurements: {total}")
    print(f"Anomalies (> 80): {anomalies}")
    print(f"Normal measurements (<= 80): {normal}")


if __name__ == "__main__":
    main()