import csv

with open('P_NP_Input.csv', mode='w') as csvfile:
    with open('P_NP_Output.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                csvfile.write(','.join(row[1:]))
            else:
                csvfile.write('\n' + ','.join(row[1:]))
            line_count += 1