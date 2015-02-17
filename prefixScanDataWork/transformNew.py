"""
Input: Firm file and edge list 
Output: Each firm and its chronological alliances with details
"""
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
	"""
	if len(SICList)==len(set(SICList)):
		return 2
	for i in range(0,len(SICList)-1):
		for j in range(i+1,len(SICList)):
			if SICList[i]!=SICList[j]:
				return 1
				break
	return 0
	"""

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
	
	#print set(allianceIDSICMap['12576'])
	#sys.exit()

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


	#for cuspid in cuspidFirmMap.keys():
	#	if(cuspidFirmMap[cuspid]==""):
	#		print cuspidFirmMap[cuspid]
	#	output[cuspidFirmMap[cuspid]]=[]
	#	i+=1
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
	#count = 0 
	for key in output.keys():
		for alliance in allAlliances:
			"""
			key1=alliance[1]
			for i in range(0,(6-len(key1))):
				key1="0"+key1
			key2=alliance[2]
			for i in range(0,(6-len(key2))):
				key2="0"+key2
			"""
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
				#if int(alliance[4])==int(alliance[5])==int(alliance[6])==int(alliance[7])==int(alliance[8])==int(alliance[9])==int(alliance[10])==int(alliance[11])==int(alliance[12])==0:
				#	count+=1

				typeId = getTypeID(allianceTypesList)
				allianceDate = alliance[3]
				effectiveDate = allianceDate[5:7]+allianceDate[8:10]+allianceDate[:4]
				crossBorder = ""
				jointVenture = ""
				if int(alliance[13])==1:
					crossBorder="y"
				else:
					crossBorder="n"
				if int(alliance[14])==1:
					jointVenture="y"
				else:
					jointVenture="n"
				crossPrimarySIC = crossSICMap[alliance[0]]

				if alliance[1]==key:
					partnerCuspid = alliance[2]
				elif alliance[2]==key:
					partnerCuspid = alliance[1]

				if partnerCuspid in cuspidFirmMap.keys():
					resTuple = (cuspidFirmMap[partnerCuspid],typeId,effectiveDate,crossBorder,crossPrimarySIC,jointVenture)
					output[key].append(resTuple)
				else:
					pass
				
	
	optFile = open("generatedFiles/finalData_today.txt","w")
	for key in output.keys():
		optFile.write(str(cuspidFirmMap[key])+" | "+str(output[key])+"\n")
	optFile.close()

	optFile = open("generatedFiles/allianceSeqData_today.tsv","w")
	optFile.write("company\ttypeid\teffective_date\tcross_border\tcross_primary_sic\tjoint_venture"+"\n")
	optFile2 = open("generatedFiles/allianceCounts.tsv","w")
	optFile2.write("company\talliancecount"+"\n")
	for key in output.keys():
		optFile2.write(str(cuspidFirmMap[key])+"\t"+str(len(output[key]))+"\n")
		for i in range(0,len(output[key])):
			optFile.write(str(cuspidFirmMap[key])+"\t"+str(output[key][i][0])+"\t"+str(output[key][i][1])+"\t"+str(output[key][i][2])+"\t"+str(output[key][i][3])+"\t"+str(output[key][i][4])+"\n")
	optFile.close()
	optFile2.close()

def createTypeIdMappingFile():
	combinationMap = {}
	for i in range(1,129):
		combinationMap[i]=[]

	index = 1
	for combination in allCombinations:
		combinationMap[index]=combination
		index+=1
	
	optFile = open("generatedFiles/combinationMap.txt","w")
	for key in combinationMap.keys():
		optFile.write(str(key)+" | "+str(combinationMap[key])+"\n")
	optFile.close()


main()
createTypeIdMappingFile()
#checking crossSICMap:
#print (isCrossSIC(['4899', '4899']))
#print (isCrossSIC(['4899', '4892', '4891','4899']))
#print (isCrossSIC(['4899', '4899', '4812', '4899', '4812', '4899']))
#print isCrossSIC(['3577', '3861', '7373', '3861', '7373', '3577', '7372', '3861', '7372', '3577', '7372', '7373', '3651', '3861', '3651', '3577', '3651', '7373', '3651', '7372', '3651', '3861', '3651', '3577', '3651', '7373', '3651', '7372', '3651', '3651', '4899', '3861', '4899', '3577', '4899', '7373', '4899', '7372', '4899', '3651', '4899', '3651']);
#print (isCrossSIC(['4899', '4899','4899', '4899','4899', '4899','4899', '4899','9898','4899']))
#print (isCrossSIC(['4899', '4812', '4813', '4898']))
#print (isCrossSIC(['7372', '3663', '7372']))
#print isCrossSIC(['7373', '7379', '3577', '7379', '3577', '7373', '7372', '7379', '7372', '7373', '7372', '3577'])
"""
for temp in crossSICMap.keys():
		if crossSICMap[temp]=="y":
			print temp,crossSICMap[temp]

	for temp in crossSICMap.keys():
		if temp=="206" or temp=="209":
			print temp,crossSICMap[temp]

	ycount=0
	ncount=0
	print "cross SIC allianceIDS"
	for temp in crossSICMap.keys():
		if crossSICMap[temp]=="y":
			if ycount<3:
				print temp,crossSICMap[temp]
			ycount+=1
	print "non-cross SIC allianceIDS"
	for temp in crossSICMap.keys():
		if crossSICMap[temp]=="n":
			if ncount<3:
				print temp,crossSICMap[temp]
			ncount+=1
"""