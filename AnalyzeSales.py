import sqlite3

class Account():
    def __init__(self, country):
        self.country = country
        self.totalPurchased = 0
    
    def addPurchase(self, num):
        self.totalPurchased += num

revenuePerCountry = {}
revenuePerMarket = {}
accounts = {}

# Getting data from database using SQLite
con = sqlite3.connect("sample.db")
cur = con.cursor()
cur.execute("SELECT * FROM account")
rows = cur.fetchall()


for row in rows:
    accounts[row[0]] = Account(row[4])

cur.execute("SELECT * FROM iap_purchase")
rows = cur.fetchall()

for row in rows:
    # this is to exclude country that is "None" from dict
    if accounts[row[0]].country is None:
        continue

# we will add market to revenuePerMarket Dict. If the user's account already exists, we do not need to increment number of users because then we will have a 
# duplicate count
    if str(row[2]) in revenuePerMarket and str(row[0]) in accounts:
        revenuePerMarket[str(row[2])] = (revenuePerMarket[str(row[2])][0] + row[3], 1)

    elif str(row[2]) not in revenuePerMarket:
        revenuePerMarket[str(row[2])] = (row[3], 1)

    else:
        revenuePerMarket[str(row[2])] = (revenuePerMarket[str(row[2])][0] + row[3], revenuePerMarket[str(row[2])][0][1])

# This adds user to the accounts dict
    if accounts[row[0]].country in revenuePerCountry:
        revenuePerCountry[str(accounts[row[0]].country)] += row[3]
    else:
        revenuePerCountry[str(accounts[row[0]].country)] = row[3]

    accounts[row[0]].addPurchase(row[3])

f = open("outputRevenueInfo.txt", "w")
total = 0
for revenue in revenuePerCountry.values():
    total += revenue

f.write("Geographic Split of the Revenue and the Users\n---------------------------------------------\n")
for info in revenuePerCountry.items():
    f.write(str(info[0]) + " " + str(round(info[1]/total * 100, 3)) + "%\n")

f.close()

f = open("outputRevPerUserPerMar.txt", "w")
f.write("Average Revenue per User per Market\n-----------------------------------\n")
i = 1
for key in revenuePerMarket.keys():
    f.write(str(i) + " $" + str(revenuePerMarket[key][0]/revenuePerMarket[key][1]) + "\n")
    i += 1

f.close()




    



    


