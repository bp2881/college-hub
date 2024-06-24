import time
from datetime import datetime
import os

try:
	streak = int(open("streak.txt", "r+").read())
except FileNotFoundError:
	streak = 0

login_date = datetime.now().date()

if os.path.exists("last_date.txt"):
	last_login_date = open("last_date.txt", "r+").read()
else:
	last_login_date = login_date

t = time.time()

try:
	r = float(open("log.txt", "r+").read())
	last_login_time = round(abs(float(t) - r))

	if last_login_time >= 86400:
		streak = 0

	elif "1 day" in str(login_date - last_login_date):
		streak += 1
		open("streak.txt", "w").write(str(streak))
		open("log.txt", "w").write(str(t))
		print("we good")

	elif last_login_date == login_date:
		open("last_date.txt", "w").write(str(login_date))

	print("hello")

except FileNotFoundError:
	open("log.txt", "w").write(str(t))