f = open("data_test.txt",'r', encoding="utf8")
data = f.read().split("\n")
# print(data)
for i in data:
    i = i.replace("?","")
    print("- " + i)