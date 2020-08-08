def add_time(start, duration, day=None):
    # List of days of the week to be passed
    days_of_the_week = ["Sunday", "Monday", "Tuesday",
            "Wednesday", "Thursday", "Friday", "Saturday"]
    # Adding PM/AM vairable to match military time
    add_hours = 12 if start.endswith('PM') else 0
    # Parsing hours and minutes from given start time as int
    h, m = [int(i) for i in start.split(' ')[0].split(':')]
    # Parsing hours and minutes to add as int
    h2a, m2a = [int(i) for i in duration.split(':')]
    # Parsing minutes sum in 60 base
    mins = divmod(m+m2a, 60)
    # Parsing hours sum as 24 base
    hours = divmod(h+h2a+add_hours+mins[0], 24)
    # Additional days
    days = hours[0]
    # Hours form in AM/PM format
    hours_form = divmod(hours[1], 12)
    # Defining AM/PM tag
    ampm = "PM" if hours_form[0] else "AM"
    # Defining addition based on the amount of days
    day_or_days = f" (next day)" if days==1 else f" ({days} days later)"
    # Filtering out the possiblity of days being 0
    day_or_days = day_or_days if days else ''
    # Formatting addition if day is provided in the function
    if(day):
        # initial day
        the_day=days_of_the_week.index(day.title())
        # day of the week that will be
        final_day = days_of_the_week[(the_day+days)%7]
        # formatted string
        day = f", {final_day}{day_or_days}"
    else:
        day=day_or_days
    # Final output
    return f"{hours_form[1] if hours_form[1] else 12}:{mins[1]:02} {ampm}{day}"


