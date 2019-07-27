#!/usr/bin/env python
'''
	Author			: Chaitanya Kumar Guduru
	Organization	: Teradata
	Tool			: Version Check Tool
	Module_Name		: Result Generator
'''

def generator(dict1, dict2, hash1, hash2, emptyFiles, log):

	global listSetA, listSetB, sizeSetA, sizeSetB, hashSetA, hashSetB
	listSetA = []
	listSetB = []
	sizeSetA = {}
	sizeSetB = {}
        hashSetA = {}
        hashSetB = {}
        flag_A   = 0
        flag_B   = 0
        hashFlag_A = 0
        hashFlag_B = 0
	
	log('\nCreating DataStructure for '+dict1.keys()[0]+':\n', 2)
	fileDictA = dict1.values()
        hashDictA = hash1.values()
	listDictA = fileDictA[0].items()
        md5DictA  = hashDictA[0].items()
	for SetA in listDictA:
		if isinstance(SetA[1], unicode):
			log('\t-Processing: '+SetA[1]+'...\n', 3)
			listSetA.append(SetA[0])
		else:
			for itr in SetA[1].keys():
				log('\t-Processing: '+itr+'...\n', 3)
				listSetA.append(SetA[0]+','+itr)
				if type(SetA[1]) is dict:
					flag_A += 1
					sizeSetA.update({SetA[0]+','+itr:SetA[1][itr]})
        for hSetA in md5DictA:
                if isinstance(hSetA[1], unicode):
                        log('.', 3)
                else:
                        for itr in hSetA[1].keys():
                                if type(hSetA[1]) is dict:
                                        hashFlag_A += 1
                                        hashSetA.update({hSetA[0]+','+itr:hSetA[1][itr]})

	log(dict1.keys()[0]+' file\'s  data structure is formed.\n', 3)

	log('\nCreating DataStructure for: '+dict2.keys()[0]+':\n', 2)
	fileDictB = dict2.values()
        hashDictB = hash2.values()
	listDictB = fileDictB[0].items()
        md5DictB  = hashDictB[0].items()
	for SetB in listDictB:
		if isinstance(SetB[1], unicode):
			log('\t-Processing: '+SetB[1]+'...\n', 3)
			listSetB.append(SetB[0])
		else:
			for itr in SetB[1]:
				log('\t-Processing: '+itr+'...\n', 3)
				listSetB.append(SetB[0]+','+itr)
				if type(SetB[1]) is dict:
					flag_B += 1
					sizeSetB.update({SetB[0]+','+itr:SetB[1][itr]})
        for hSetB in md5DictB:
                if isinstance(hSetB[1], unicode):
                        log('.', 3)
                else:
                        for itr in hSetB[1].keys():
                                if type(hSetB[1]) is dict:
                                        hashFlag_B += 1
                                        hashSetB.update({hSetB[0]+','+itr:hSetB[1][itr]})

	log(dict2.keys()[0]+' file\'s  data structure is formed.\n', 3)

	file = 'Comparison of '+dict1.keys()[0]+' & '+dict2.keys()[0]+'\n'
	file += '\nCommon files:\n'
	inter = [val for val in listSetA if val in listSetB]
	file += 'Serial no., Platform, File Name\n'
	log('\nProcessing intersection of '+dict1.keys()[0]+' & '+dict2.keys()[0], 3)
        totalCommonFiles = 0
	for val in inter:
                totalCommonFiles = totalCommonFiles+1
		file += str(totalCommonFiles)+','+val+'\n'
		log('\n\t-'+val, 3)
        file += ',Total Common files:,'+str(totalCommonFiles)+'\n'
        log('Total Common files:\t'+str(totalCommonFiles)+'\n', 3)
	
	file +=  '\nFiles only in: '+dict1.keys()[0]+'\n'
	OnlyA = [val for val in listSetA if val not in listSetB]	
	file += 'Serial no., Platform, File Name\n'
	log('\n\nProcessing Unique files of '+dict1.keys()[0], 3)
        slno1 = 0
	for val in OnlyA:
                slno1+=1
		file += str(slno1)+','+val+'\n'
		log('\n\t-'+val, 3)
        file += ',Total no of Unique files:,'+str(slno1)+'\n'
        log('Total no of Unique files:\t'+str(slno1)+'\n', 3)

	file +=  '\nFiles only in: '+dict2.keys()[0]+'\n'
	OnlyB = [val for val in listSetB if val not in listSetA]
	file += 'Serial no., Platform, File Name\n'
	log('\n\nProcessing Unique files of '+dict2.keys()[0], 3)
        slno2 = 0
	for val in OnlyB:
                slno2+=1
		file += str(slno2)+','+val+'\n'
		log('\n\t-'+val, 3)
        file += ',Total no of Unique files:,'+str(slno2)+'\n'
        log('Total no of Unique files:\t'+str(slno2)+'\n', 3)
		
	if (flag_A != 0 and flag_B != 0):
		log('\n\nProcessing common files with different file sizes of '+dict1.keys()[0]+' & '+dict2.keys()[0]+'\n', 3)
		file +=  '\nSize Diff in Common files:\n'
		file += 'Serial no., Platform, File name, Size in '+dict1.keys()[0]+', Size in '+dict2.keys()[0]+', Difference of size (Bytes)\n'
		log('Sl no.  Platform\t\tFile name:\t\t\t\tSize in '+dict1.keys()[0]+'\t Size in '+dict2.keys()[0]+'\t Difference of size (Bytes)', 3)
                totalSizeDiffFiles = 0
		for val in inter:
			if sizeSetA[val] != sizeSetB[val]:
                                totalSizeDiffFiles = totalSizeDiffFiles+1
				file +=  str(totalSizeDiffFiles)+','+val+','+str(sizeSetA[val])+','+str(sizeSetB[val])+','+str(sizeSetA[val]-sizeSetB[val])+'\n'
				log('\n\t-'+val+':\t\t\t--\t'+str(sizeSetA[val])+'\t|\t'+str(sizeSetB[val])+'\t|\t'+str(sizeSetA[val]-sizeSetB[val])+'|', 3)
                file += ',Count of \"Same name files\" with different sizes:,'+str(totalSizeDiffFiles)+'\n'
                log('\nCount of \"Same name files\" with different sizes:\t'+str(totalSizeDiffFiles), 3)

        if (hashFlag_A != 0 and hashFlag_B != 0):
                log('\n\nProcessing common files with different file md5-check-sum of '+dict1.keys()[0]+' & '+dict2.keys()[0]+'\n', 3)
                file +=  '\nDiff MD5 in Common files:\n'
                file += 'Serial no., Platform, File name, MD5 in '+dict1.keys()[0]+', MD5 in '+dict2.keys()[0]+'\n'
                log('Sl no.  Platform\t\tFile name:\t\t\t\tSize in '+dict1.keys()[0]+'\t Size in '+dict2.keys()[0], 3)
                totalDiffMD5Files = 0
                for val in inter:
                        if hashSetA[val] != hashSetB[val]:
                                totalDiffMD5Files = totalDiffMD5Files+1
                                file +=  str(totalDiffMD5Files)+','+val+','+str(hashSetA[val])+','+str(hashSetB[val])+'\n'
                                log('\n\t-'+val+':\t\t\t--\t'+str(hashSetA[val])+'\t|\t'+str(hashSetB[val])+'\t|', 3)
                file += ',Count of \"Same name files\" with different MD5 checkSum:,'+str(totalDiffMD5Files)+'\n'
                log('\nCount of \"Same name files\" with different MD5 checkSum:\t'+str(totalDiffMD5Files), 3)
                file += '\n,Count of files that are unchanged:,'+str(totalCommonFiles-totalDiffMD5Files)
                log('\nCount of files that are unchanged:\t'+str(totalCommonFiles-totalDiffMD5Files), 3)

	log('\n\nEmpty File:', 3) 
	file += '\nEmpty files:\n'
	for val in emptyFiles:
		file += val+'\n'
		log('\n\t-'+val, 3)
	file += '\n'+'-*-*-*,'*2+' Completed '+',*-*-*-'*2+'\n'
	log('\n\nComparision process completed for '+dict1.keys()[0]+' & '+dict2.keys()[0]+'\n', 2)
	return file
