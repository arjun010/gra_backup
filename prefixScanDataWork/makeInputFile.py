import csv
import random
import json
import sys
import itertools

firmFile =sys.argv[1]
allianceFile =sys.argv[2]
lst = [1, 2, 3, 4, 5, 6, 7]
allCombinations = []

for i in xrange(1, len(lst)+1):
    els = [list(x) for x in itertools.combinations(lst, i)]
    allCombinations.extend(els)

allCombinations.append([])


def getTypeID(forCombination):
	return allCombinations.index(forCombination)+1

def isCrossSIC(SICList):
	SICcountMap = {}
	for sic in SICList:
		SICcountMap[sic]=0
	for sic in SICList:
		SICcountMap[sic]+=1
	#return SICcountMap
	if(len(SICcountMap)==1):
		return "n"
	elif(SICcountMap.values()[1:] == SICcountMap.values()[:-1]):
		return "y"
	else:
		for count in SICcountMap.values():
			if count>1:
				return "b"

def getPrimarySIC(forID,cuspidSICMap):
	if len(forID)<6:
		for i in range(0,(6-len(forID))):
			forID="0"+forID
	return cuspidSICMap[forID]

def getCrossSICMap(allianceList,cuspidSICMap):
	crossSICMap = {}
	allianceIds = []
	allianceIDSICMap = {}

	for alliance in allianceList:
		allianceIds.append(alliance[0])
	
	allianceIdSet = set(allianceIds)

	for entry in allianceIdSet:
		crossSICMap[entry]=[]		
		allianceIDSICMap[entry]=[]

	for allianceID in crossSICMap.keys():
		tempSICList = []
		for alliance in allianceList:
			if alliance[0]==allianceID:
				allianceIDSICMap[allianceID].append(getPrimarySIC(alliance[1],cuspidSICMap))
				allianceIDSICMap[allianceID].append(getPrimarySIC(alliance[2],cuspidSICMap))
	

	for allianceID in allianceIDSICMap.keys():
		crossSICMap[allianceID]=isCrossSIC(allianceIDSICMap[allianceID])
	
	return crossSICMap


def main():

	firms = open(firmFile)
	firmsReader = csv.reader(firms)

	cuspidFirmMap = {}
	firmSICMap = {}
	cuspidSICMap = {}
	output = {}
	firmCuspidMap = {}

	i=0
	for line in firmsReader:
		if i>0:
			cuspidFirmMap[line[0]]=line[1]
			firmSICMap[line[1]]=line[2]
			cuspidSICMap[line[0]]=line[2]
		i=1


	output=cuspidFirmMap.copy()
	for key in output.keys():
		output[key]=[]

	
	alliances = open(allianceFile)
	alliancesReader = csv.reader(alliances)	
	
	allAlliances = []
	i=0
	for allianceEntry in alliancesReader:
		if i>0:
			allAlliances.append(allianceEntry)
		i=1

	crossSICMap=getCrossSICMap(allAlliances,cuspidSICMap)
	
	for key in output.keys():
		for alliance in allAlliances:
			if alliance[1]==key or alliance[2]==key:
				allianceTypesList = []
				typeID = -1
				if int(alliance[4])==1 or int(alliance[5])==1:
					allianceTypesList.append(1)
				if int(alliance[6])==1 or int(alliance[7])==1:
					allianceTypesList.append(2)
				if int(alliance[8])==1:
					allianceTypesList.append(3)
				if int(alliance[9])==1:
					allianceTypesList.append(4)
				if int(alliance[10])==1:
					allianceTypesList.append(5)
				if int(alliance[11])==1:
					allianceTypesList.append(6)
				if int(alliance[12])==1:
					allianceTypesList.append(7)
				
				typeId = getTypeID(allianceTypesList)				
				output[key].append(typeId)
	
	optFile = open("seqData_try4.txt","w")
	for key in output.keys():
		typeIDList = output[key]
		if len(typeIDList)>0:
			#optFile.write(str(cuspidFirmMap[key])+": ")
			for entry in typeIDList:
				if entry!=128:
					primaryTypeIDS = returnCombination(entry)
					optFile.write(str([x for x in primaryTypeIDS])+" -1 ")
			optFile.write("-2\n")

	optFile.close()


combinationMap = {}
def createCombinationMap():
	
	for i in range(1,129):
		combinationMap[i]=[]

	index = 1
	for combination in allCombinations:
		combinationMap[index]=combination
		index+=1


def returnCombination(forID):
	return combinationMap[forID]

createCombinationMap()
main()