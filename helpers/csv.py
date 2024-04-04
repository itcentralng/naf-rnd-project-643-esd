import csv
from io import StringIO

def get_vehicles_from_csv(file):
    data = []
    file_contents = file.stream.read().decode("utf-8")
    file.seek(0)  # Reset the file pointer
    csv_reader = csv.reader(StringIO(file_contents), delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        data.append(row)
    return data