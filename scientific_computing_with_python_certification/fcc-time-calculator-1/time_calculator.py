def add_time(start, duration, day=None):
    days_of_the_week = ["Sunday", "Monday", "Tuesday",
            "Wednesday", "Thursday", "Friday", "Saturday"]
    add_hours = 12 if start.endswith('PM') else 0
    h, m = [int(i) for i in start.split(' ')[0].split(':')]
    h2a, m2a = [int(i) for i in duration.split(':')]
    mins = divmod(m+m2a, 60)
    hours = divmod(h+h2a+add_hours+mins[0], 24)
    days = hours[0]
    hours_form = divmod(hours[1], 12)
    ampm = "PM" if hours_form[0] else "AM"
    day_or_days = f" (next day)" if days==1 else f" ({days} days later)"
    day_or_days = day_or_days if days else ''
    if(day):
        the_day=days_of_the_week.index(day.title())
        final_day = days_of_the_week[(the_day+days)%7]
        day = f", {final_day}{day_or_days}"
    else:
        day=day_or_days
    return f"{hours_form[1] if hours_form[1] else 12}:{mins[1]:02} {ampm}{day}"


