import sqlite3
import matplotlib.pyplot as plt
import numpy as np

class Account():
    def __init__(self, country):
        self.country = country
        self.totalPurchased = 0
    
    def addPurchase(self, num):
        self.totalPurchased += num

revenuePerCountry = {}

# Getting data from database using SQLite
con = sqlite3.connect("sample.db")
cur = con.cursor()
cur.execute("SELECT * FROM account")
rows = cur.fetchall()

accounts = {}
for row in rows:
    accounts[row[0]] = Account(row[4])

cur.execute("SELECT * FROM iap_purchase")
rows = cur.fetchall()

revenuePerCountry = {}
for row in rows:
    if accounts[row[0]].country in revenuePerCountry:
        revenuePerCountry[accounts[row[0]].country] += row[3]
    else:
        revenuePerCountry[accounts[row[0]].country] = row[3]

    accounts[row[0]].addPurchase(row[3])


data = np.array(list(revenuePerCountry.values()))
labels = list(revenuePerCountry.keys())
labels.remove(None)
print(labels)
plt.title("Geographic split of the revenue")
plt.pie(data,labels)
plt.show()



    



    


