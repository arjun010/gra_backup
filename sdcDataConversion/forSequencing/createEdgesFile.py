import csv
import itertools

def getCombinations(cuspids):
	combinationObjects = itertools.combinations(cuspids,2)
	allCombinations = []
	for comboObject in combinationObjects:
		allCombinations.append(comboObject)
	return allCombinations

def getTypeFlags(line):
	if(line[22].lower()=="n" or line[22].lower()=="no"):
		isJointVenture=0
	else:
		isJointVenture=1
	if(line[15].lower()=="n" or line[15].lower()=="no"):
		isTechtrans=0
	else:
		isTechtrans=1
	if(line[21].lower()=="n" or line[21].lower()=="no"):
		isMarketing=0
	else:
		isMarketing=1
	if(line[12].lower()=="n" or line[12].lower()=="no"):
		isLicensing=0
	else:
		isLicensing=1
	if(line[20].lower()=="n" or line[20].lower()=="no"):
		isRnd=0
	else:
		isRnd=1
	if(line[13].lower()=="n" or line[13].lower()=="no"):
		isExLicensing=0
	else:
		isExLicensing=1
	if(line[14].lower()=="n" or line[14].lower()=="no"):
		isManufacturing=0
	else:
		isManufacturing=1
	if(line[23].lower()=="n" or line[23].lower()=="no"):
		isOem=0
	else:
		isOem=1
	if(line[19].lower()=="n" or line[19].lower()=="no"):
		isSupply=0
	else:
		isSupply=1
	if(line[24].lower()=="n" or line[24].lower()=="no"):
		isCbAlliance=0
	else:
		isCbAlliance=1
	if(line[18].lower()=="n" or line[18].lower()=="no"):
		isStrategic=0
	else:
		isStrategic=1

	return isLicensing,isExLicensing,isManufacturing,isOem,isMarketing,isRnd,isStrategic,isSupply,isTechtrans,isCbAlliance,isJointVenture

data = open("S&P_500_IT/salesforce.csv")
dataReader = csv.reader(data)

actualData = []
skip=1
for line in dataReader:	
	if skip>=2:
		actualData.append(line)
	skip+=1

cuspIDFirmMap = {}
for line in actualData:
	firms = line[0].split("\n")
	cuspids = line[1].split("\n")
	primarysics = line[2].split("\n")
	for i in range(0,len(firms)):
		cuspIDFirmMap[cuspids[i]]=firms[i]

#allianceid,cusip1,cusip2,effective,licensing,exlicensing,manufacturing,oem,marketing,rnd,strategic,supply,techtrans,cballiance,jv

resList = []

lastAllianceId = open("lastAllianceId.txt","r")
allianceid = int(lastAllianceId.readline())

for line in actualData:
	cuspids = line[1].split("\n")
	allCombinations = getCombinations(cuspids)
	dateEffective = line[5]
	isLicensing = -1
	isExLicensing = -1
	isManufacturing = -1
	isOem = -1
	isMarketing = -1
	isRnd = -1
	isSupply = -1
	isTechtrans = -1
	isCbAlliance = -1
	isJointVenture = -1
	isStrategic = -1
	isLicensing,isExLicensing,isManufacturing,isOem,isMarketing,isRnd,isStrategic,isSupply,isTechtrans,isCbAlliance,isJointVenture = getTypeFlags(line)
	for combination in allCombinations:		
		resTuple = (allianceid,combination[0],combination[1],dateEffective,isLicensing,isExLicensing,isManufacturing,isOem,isMarketing,isRnd,isStrategic,isSupply,isTechtrans,isCbAlliance,isJointVenture)
		resList.append(resTuple)
	allianceid+=1

with open('edgesFileTemp.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(["allianceid","cusip1","cusip2","effective","licensing","exlicensing","manufacturing","oem","marketing","rnd","strategic","supply","techtrans","cballiance","jv"])
    writer.writerows(resList)

newAllianceId = open("lastAllianceId.txt","w")
newAllianceId.write(str(allianceid))
newAllianceId.close()

data = open("edgesFileTemp.csv")
dataReader = csv.reader(data)

actualData = []
skip=1
for line in dataReader:	
	if skip>=2:
		actualData.append(line)
	skip+=1

resList=[]
for line in actualData:
	if line[0]=="allianceid":
		pass
	elif line[3]=="":
		pass
	else:
		resList.append(line)

with open('edgesFile.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["allianceid","cusip1","cusip2","effective","licensing","exlicensing","manufacturing","oem","marketing","rnd","strategic","supply","techtrans","cballiance","jv"])
    writer.writerows(resList)