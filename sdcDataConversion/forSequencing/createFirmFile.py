import csv

data = open("S&P_500_IT/salesforce.csv")
dataReader = csv.reader(data)

actualData = []
skip=1
for line in dataReader:	
	if skip>=2:
		actualData.append(line)
	skip+=1

cuspIDFirmMap = {}
firmPrimarySicMap = {}
firmAllSicMap = {}
testList = []
for line in actualData:
	firms = line[0].split("\n")
	cuspids = line[1].split("\n")
	primarysics = line[2].split("\n")
	for i in range(0,len(firms)):
		cuspIDFirmMap[cuspids[i]]=firms[i]
		firmPrimarySicMap[firms[i]]=primarysics[i]

for firm in firmPrimarySicMap.keys():
	firmAllSicMap[firm]=[]


for line in actualData:
	firms = line[0].split("\n")
	allsics = line[3].split("\n")
	curIndex = len(allsics)-1
	for firm in reversed(firms):
		while allsics[curIndex]!=firmPrimarySicMap[firm]:
			firmAllSicMap[firm].append(allsics[curIndex])
			curIndex-=1
		firmAllSicMap[firm].append(allsics[curIndex])
		curIndex-=1

for key in firmAllSicMap.keys():
	firmAllSicMap[key]=set(firmAllSicMap[key])
	firmAllSicMap[key]=list(firmAllSicMap[key])

resList = []
for key in cuspIDFirmMap.keys():
	cuspid=key
	firm = cuspIDFirmMap[key]
	firmPrimarySic = firmPrimarySicMap[firm]
	firmAllSics = str(firmAllSicMap[firm])
	firmAllSics = firmAllSics.replace("[","")
	firmAllSics = firmAllSics.replace("]","")
	firmAllSics = firmAllSics.replace("'","")
	firmAllSics = firmAllSics.replace(" ","")
	firmAllSics = firmAllSics.replace(",","|")
	resList.append((key,firm,firmPrimarySic,firmAllSics))
	#print(key,firm,firmPrimarySic,firmAllSics)

#print resList

with open('firmDataFileTemp.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(["cuspid","name","primarySIC","allSIC"])
    writer.writerows(resList)


data = open("firmDataFileTemp.csv")
dataReader = csv.reader(data)

actualData = []
skip=1
for line in dataReader:	
	if skip>=2:
		actualData.append(line)
	skip+=1

coveredCuspIds = []
resList=[]
for line in actualData:
	if line[0]=="cuspid":
		pass
	else:
		if line[0] not in coveredCuspIds:
			coveredCuspIds.append(line[0])
			resList.append((line[0],line[1],line[2],line[3]))

with open('firmDataFile.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["cuspid","name","primarySIC","allSIC"])
    writer.writerows(resList)