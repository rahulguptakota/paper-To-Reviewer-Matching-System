files = ["k7","k9"]
# ,"features_k6.txt","features_k7.txt","features_k9.txt","features_k10.txt","features_k12.txt"]

data = {}

fd = open("db/MeaningfulCitationsDataset/ValenzuelaAnnotations.csv",'rb')
t = fd.read()
i=0
for line in t.decode().split("\n"):
    if i != 0:
        line = line.split(",")
        try:
            data[(line[1],line[2])] = {}
            data[(line[1],line[2])]["test"] = line[-1]
            # print(line)
        except:
            pass
    i = i + 1
fd.close()

# print(data)

for f in files:
    fd = open("features_" + f + ".txt",'rb')
    t = fd.read()
    i=0
    for line in t.decode().split("\n"):
        line = line.split(" ")
        data[(line[0],line[1])][f] = line[-1]
        # print(line)
        i = i + 1
    fd.close()
print(data)
