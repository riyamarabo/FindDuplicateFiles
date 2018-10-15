from Project1 import p1utils
import time
import os


def search(file_list):
    """Looking for duplicate files"""

    listOfLists = []
    while file_list:
        chl=[]
        ch = file_list.pop(0)
        chl.append(ch)
        for i in range(len(file_list)-1, -1, -1):
            if p1utils.compare(ch, file_list[i]):
                chl.append(file_list.pop(i))
        if len(chl) > 1:
            listOfLists.append(chl)
    listOfLists.sort(reverse=True, key=len)
    return listOfLists


def fasterSearch(file_list):
    """Looking for duplicate files"""


def report(file_list):
    """ report search results"""

    print("\nThe file with the most duplicates is: ", file_list[0][0])
    print("\nHere are its " , len(file_list[0]), " copies: ","\n".join(str(x) for x in file_list[0]))

    largestSize = 0
    for i in range(0, len(file_list)):
        currentSize = os.path.getsize(file_list[i][0])
        currentSize*=len(file_list[i])
        if currentSize>largestSize:
            largestSize=currentSize
            index = i

    print("\nThe most disk space " , largestSize , " could be recovered, by deleting copies of this file: \n", "\n".join(str(x) for x in file_list[index]))


# find all files in the provided directory
files = p1utils.allFiles("." + os.sep + "smallset")
print("Number of smallset files found: ", len(files))

# fullsetfiles = p1utils.allFiles("."+os.sep+"fullset")
# print("Number of Fullset files found: ", len(fullsetfiles))

# measure how long the search and reporting takes:
t0 = time.time()
report(search(files))
print("Runtime: %.2f secs" % (time.time() - t0))

# print(" .. and now w/ a faster search implementation:")
# t0 = time.time()
# report(fasterSearch(files))
# print("Runtime: %.2f secs" % (time.time() - t0))
