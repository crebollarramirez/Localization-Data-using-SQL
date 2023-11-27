import sqlite3
import matplotlib.pyplot as plt

# Just gets the month from the date
def convertDate(date):
	return int(date.split('-')[1])


# Getting the date from database using SQLite
con = sqlite3.connect("sample.db")
cur = con.cursor()
cur.execute("SELECT * FROM account_date_session")
rows = cur.fetchall()

monthsActive = [0] * 12
for row in rows:
	if(row[3] > 300): # 5 minutes in game considers as active
		monthsActive[convertDate(row[1]) - 1] += row[2]

months = [i for i in range(1,13)]

plt.plot(months, monthsActive)
plt.xlabel("Months")
plt.ylabel("Active people")
plt.title("DAU Overtime")

plt.legend()
plt.show()



print(monthsActive)





