import csv

w1, w2, w3, w4 = 0.5, 0.2, 0.2, 0.1

head_string = ['Date', 'Profit', 'TempAvgF', 'HumidityAvgPercent', 'VisibilityAvgMiles', 'WindAvgMPH', 'Events']


class Day:
    def __init__(self, row):
        self.daily_inc = 0
        self.is_w_event = False

        row = self.parse_row(row)

        self.date = row[0]
        self.avg_temp = float(row[1])
        self.avg_hum = float(row[2])
        self.avg_vis = float(row[3])
        self.avg_wind = float(row[4])

    def parse_row(self, row):
        for i in range(len(row)):
            if row[i] == '-':
                row[i] = 0

        if len(row[20]) > 1:
            self.is_w_event = True
        return row[0], row[2], row[8], row[14], row[17]

    def daily_income(self):
        return round(w1 * self.avg_temp + w2 * self.avg_hum + w3 * self.avg_vis + w4 * self.avg_wind, 2)

    def array_data(self):
        return [self.date, self.daily_inc, self.avg_temp, self.avg_hum, self.avg_vis, self.avg_wind, self.is_w_event]


def input_data():
    days = []
    with open('austin_weather.csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_line = True
        for row in csv_reader:
            if not first_line:
                days.append(Day(row))
            else:
                first_line = False
    return days


def output_data(rows):
    with open('daily_income.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(head_string)
        for row in rows:
            writer.writerow(row)


def main():
    days = input_data()
    output_rows = []

    w_event_day_profit = 0

    print('Days with a profit of less than $30 per day:')
    for day in days:
        day.daily_inc = day.daily_income()

        if day.daily_inc < 30:
            print({day.date: day.daily_inc})

        if day.is_w_event:
            w_event_day_profit += day.daily_inc

        output_rows.append(day.array_data())

    print(f'Total profit on days when there were weather events: {round(w_event_day_profit, 2)}')

    output_data(output_rows)


if __name__ == '__main__':
    main()
