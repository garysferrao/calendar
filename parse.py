import datetime
import dateutil.parser as dp
import pandas as pd;

df = pd.read_csv("months.csv", parse_dates=[0])
months = list(list(df.to_dict().values())[0].values())
# sanity check. did i miss any value?
prev_month = dp.parse("1908/11/24 03:22 +05:30")
total_td = datetime.timedelta()
for month in months:
    td = month - prev_month
    total_td += td
    if td.days != 29:
        print(td.days)
    prev_month = month
print(f"average month td =  {total_td/len(months)}")

df = pd.read_csv("years.csv", parse_dates=[0])
years = list(list(df.to_dict().values())[0].values())
# sanity check. did i miss any value?
prev_year = dp.parse("1907/12/23 05:21 +05:30")
total_td = datetime.timedelta()
for year in years:
    td = year - prev_year
    total_td += td
    if td.days != 365:
        print(td.days)
    prev_year = year
print(f"average year  td = {total_td/len(years)}")


# start calculating calendar
class Day:
    greg_date: datetime
    day_of_week: int
    def __init__(self, d : datetime.datetime, w: int):
        self.greg_date = d
        self.day_of_week = w
    def __str__(self) -> str:
        return f"({self.greg_date.strftime('%Y-%m-%d %a')}, w={self.day_of_week})"

class Month:
    days: list[Day]
    def __init__(self):
        self.days = []
    def append(self, d : Day):
        self.days.append(d)
    def __str__(self) -> str:
        s = f"\n\n{self.days[0]}\n"
        s += "Su Mo Tu We Th Fr Sa \n"
        for _ in range(0, self.days[0].day_of_week):
            s += "   "
        for day_index in range(0, len(self.days)):
            if self.days[day_index].day_of_week == 0:
                s += "\n"
            day_str = f"{day_index}"
            s += f"{day_str.rjust(2)} "
        return s
            
    def list_days(self) -> str:
        s = "\t[\n"
        for (i, d) in enumerate(self.days):
            s += f"\t\t{i}:\t{d}\n"
        s += "\t]\n"
        return s

class Year:
    months: list[Month]
    def __init__(self):
        self.months = []
    def append(self, m : Month):
        self.months.append(m)
    def __str__(self) -> str:
        s = "\n\t["
        for m in self.months:
            s += f"{m}"
        s += "\t]\n"
        return s

class Calendar:
    years: list[Year]
    def __init__(self):
        self.years = []
    def append(self, y: Year):
        self.years.append(y)
    def __str__(self) -> str:
        s = "\n{"
        for m in self.months:
            s += f"{m}"
        s += "}\n"
        return s

m = Month()
y = Year()
c = Calendar()

start_day = dp.parse("1908/12/23 00:00 +05:30")
start_day_of_week = 1
month_index = 0
year_index = 0

# print(f"===============YEAR {year_index}============={years[0]}")
for day_index in range(0, 43084):
    day = start_day + datetime.timedelta(days=day_index)
    week_index = (start_day_of_week + day_index) % 7

    end_of_this_month = pd.Timestamp(months[month_index + 1]).ceil("1d").to_pydatetime()
    beg_of_next_month = pd.Timestamp(months[month_index + 1]).floor("1d").to_pydatetime()

    end_of_this_year = pd.Timestamp(years[year_index + 1]).ceil("1d").to_pydatetime()
    beg_of_this_year = pd.Timestamp(years[year_index + 1]).floor("1d").to_pydatetime()

    if day < beg_of_next_month:
        m.append(Day(d=day, w=week_index))
    else:
        if day < end_of_this_month:
            m.append(Day(d=day, w=week_index))
        y.append(m)
        # print(m.list_days())
        # print(months[month_index+1]) # prints day, beginning of next month
        m = Month()
        month_index += 1
        if day >= beg_of_next_month:
            m.append(Day(d=day, w=week_index))
        # this is breaking my head. i will just list the year index for now.
        if day >= end_of_this_year:
            c.append(y)
            y = Year()
            year_index += 1
            # print(f"===============YEAR {year_index}============={years[year_index]}")


idx = 0
for yr in c.years:
    print(f"===============YEAR {idx}============={years[idx]}")
    print(yr)
    idx += 1
    pass
# print(y)
