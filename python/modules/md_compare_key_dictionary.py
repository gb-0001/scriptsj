#!/usr/bin/python
#GB-0001 github


# compare if the key exists in the dictionary 1=OK 0=NOK
def mdkeyExistsInDictionary(key, dictionary):
        val = 0
        #Compare Key
        if key not in dictionary:
            val = val + 0
        else:
            val = val + 1
        return(val)

#example resultexit=mdkeyExistsInDictionary(key, dictionary)

#compare the key between the dictionaries and returns the list in addition or in deletion
def mdCompareKeyBetweenDictionnaries(dictionary1, dictionary2):
        addList = {}
        delList = {}
        #compares the key of dictionary 1 with the key of dictionary 2 
        for key in dictionary1:
            if key not in dictionary2:
                addList.update({key: ""})
                #print("The key in dictionary 1 does not exist in dictionary 2")
                        
        #compares the key of dictionary 2 with the key of dictionary 1 and addList
        for key in dictionary2:
            if key not in dictionary1:
                delList.update({key: ""})
                #print("The key in dictionary 1 does not exist in dictionary 2")
        return(addList,delList)
#example resultaddList,resultDelList = mdCompareKeyBetweenDictionnaries(dictionary1, dictionary2)





