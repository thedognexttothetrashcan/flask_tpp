from datetime import datetime, timedelta

CLEAN_TIME = 20


def calc_time(time_data, duration, clean_time=CLEAN_TIME):
    date_time = time_data.split(" ")
    date_start = date_time[0]
    time_start = date_time[1]

    year_month_day = date_start.split("-")
    hour_minute_second = time_start.split(":")

    year = int(year_month_day[0])
    month = int(year_month_day[1])
    day = int(year_month_day[2])

    hour = int(hour_minute_second[0])
    minute = int(hour_minute_second[1])
    second = int(hour_minute_second[2])

    end_time = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second) + timedelta(minutes=duration+clean_time)

    print(end_time)

    print(type(end_time))

    return str(end_time)