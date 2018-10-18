"""
Program: Running a search on a directory of files to find duplicates using two types of search algorithms
Author: Riyam Arabo
Last Modified: 10/17/2018

Purpose: Finding duplicate files, measuring the disk space they're wasting, and potentially deleting them depending on the user's preferences.
"""
from Project1 import p1utils
import time
import os


def search(file_list):
    """Looking for duplicate files"""

    localList = list(file_list)
    listOfLists = []

    # remove an element, and loop through the rest of the list to find duplicates
    while localList:
        chl=[localList.pop(0)]
        for i in range(len(localList)-1, -1, -1):

            # if duplicates are found, append them in the same list
            if p1utils.compare(chl[0], localList[i]):
                chl.append(localList.pop(i))

        # then append them to a list of lists
        if len(chl) > 1: listOfLists.append(chl)
    return listOfLists


def fasterSearch(file_list):
    """Looking for duplicate files"""

    localList = list(file_list)
    hashedDict={}
    listOfLists=[]

    # Create hashes of files and store them in a dictionary as keys, list of filenames as values
    for element in localList:
        hashedDict[p1utils.hash_file(element)] = [element]

    # Create hashes again and loop through the dicitonary to check if they repeat
    for element in localList:
        if p1utils.hash_file(element) in hashedDict:

            # Element is appended to filenames list if hash is found and the element is not in the list
            if element not in hashedDict[p1utils.hash_file(element)]:
                hashedDict[p1utils.hash_file(element)].append(element)

    #  Create list of each dictionary value list
    for key in hashedDict:
        keysList = list(hashedDict[key])

        # Run file comparison on items in the same list to check if they're the same
        while keysList:
            chl = [keysList.pop(0)]
            for i in range(len(keysList)-1, -1, -1):
                if p1utils.compare(chl[0], keysList[i]): chl.append(keysList.pop(i))
            if len(chl) > 1: listOfLists.append(chl)

    return listOfLists


def report(file_list):
    """ report search results"""

    if file_list:
        print("\nThe file with the most duplicates is: \n", max(file_list, key=len)[0])
        print("\nHere are its " , len(max(file_list, key=len))-1, " copies: \n","\n".join(str(x) for x in max(file_list, key=len)[1:len(file_list)+1]))

        # Calculate sizes of files and store largest wasted disk space value
        largestSize = 0
        for i in range(0, len(file_list)):
            currentSize = os.path.getsize(file_list[i][0]) * (len(file_list[i])-1)
            if currentSize > largestSize:
                largestSize = currentSize
                index = i

        print("\nThe most disk space " , largestSize , " could be recovered, by deleting copies of this file: \n", file_list[index][0], "\nhere are its ",len(file_list[index])-1 ," copies: \n","\n".join(str(x) for x in file_list[index][1:len(file_list[index])]))
    else: print("Sorry, no duplicate files found")


# find all files in the provided directory
files = p1utils.allFiles("." + os.sep + "smallset")
print("Number of smallset files found: ", len(files))

# fullsetfiles = p1utils.allFiles("."+os.sep+"fullset")
# print("Number of Fullset files found: ", len(fullsetfiles))

# measure how long the search and reporting takes:
t0 = time.time()
report(search(files))
print("Runtime: %.2f secs" % (time.time() - t0))

print(" .. and now w/ a faster search implementation:")
t0 = time.time()
report(fasterSearch(files))
print("Runtime: %.2f secs" % (time.time() - t0))
