import os
from datetime import datetime, timedelta

# File to store the streak data
file = 'streak_data.txt'

def read_streak_data():
    if os.path.exists(file):
        with open(file, 'r') as file:
            last_date_str = file.readline().strip()
            streak_count = int(file.readline().strip())
            last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
            return last_date, streak_count
    else:
        return None, 0

def write_streak_data(last_date, streak_count):
    with open(file, 'w') as file:
        file.write(f"{last_date}\n{streak_count}")

def update_streak():
    last_date, streak_count = read_streak_data()
    today = datetime.now().date()

    if last_date is None or today > last_date:
        if last_date is None or today == last_date + timedelta(days=1):
            streak_count += 1
        else:
            streak_count = 1
        last_date = today
        write_streak_data(last_date, streak_count)

    return streak_count

if __name__ == '__main__':
    streak_count = update_streak()
    print(f"Current streak: {streak_count} days")
