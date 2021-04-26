from cs50 import SQL

def closest(data, value):

    return data[min(range(len(data)), key = lambda i: abs(data[i]-value))]


db = SQL("sqlite:///info.db")

value = db.execute("SELECT size FROM countries WHERE name = ?", "")
state_sizes = db.execute("SELECT * FROM states")

'''
#value = value[0]["size"]

data = []


for i in state_sizes:
    data.append(i["size"])


result = closest(data, value)

state = db.execute("SELECT name FROM states WHERE size = ?", result)
state = state[0]["name"]
'''

print(state_sizes)