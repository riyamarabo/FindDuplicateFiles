"""Utilities for CSIS 250 Project 1.

Functions:
    hash_file(filename) -> str
    compare(f1,f2) -> bool
    allFiles(directory) -> []
    getCompareCounter() -> int
    getFileCounter() ->int
"""
import os
import filecmp
import hashlib

__all__ = ['hash_file', 'compare', 'allFiles', 'getCompareCounter', 'getFileCounter']


def hash_file(filename):
    """"This function returns the SHA-1 hash of the file passed into it"""
    h = hashlib.sha1()
    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    # return the hex representation of digest
    return h.hexdigest()


def compare(f1, f2):
    """Utilities for comparing file content
    Compare the files named f1 and f2, returning True if the contents of the files is the same."""
    global compareCounter
    compareCounter += 1
    return filecmp.cmp(f1, f2, False)


def allFiles(directory):
    """ returns a list, containing ALL files, found in the given directory structure."""
    global fileCounter
    files = []
    dirs = [directory]
    while 0 < len(dirs):
        try:
            f = dirs.pop(0)
            # add all visible directories to the dirs list
            dirs.extend([f + os.sep + item for item in os.listdir(f) if
                         not item.startswith('.') and os.path.isdir(f + os.sep + item)])
            # add all visible files to the files list
            files.extend([f + os.sep + item for item in os.listdir(f) if
                          not item.startswith('.') and os.path.isfile(f + os.sep + item)])
        except:
            pass
    fileCounter = len(files)
    return files


def getCompareCounter():
    """Number of times the file compare function was used"""
    return compareCounter


def getFileCounter():
    """Number of files that were discovered in the dir structure"""
    return fileCounter

def test():
    # quick test
    dir_name = "tmp123"
    content = "The quick brown fox jumps over the lazy dog"
    os.mkdir(dir_name)
    f = open(dir_name + os.sep + "f1", "w")
    f.write(content)
    f.close()
    f = open(dir_name + os.sep + "f2", "w")
    f.write(content)
    f.close()
    f = open(dir_name + os.sep + "f3", "w")
    f.write(content * 2)
    f.close()
    assert 3 == len(allFiles(dir_name)) == getFileCounter()
    assert hash_file(dir_name + os.sep + "f1") == hash_file(dir_name + os.sep + "f2")
    assert hash_file(dir_name + os.sep + "f1") != hash_file(dir_name + os.sep + "f3")
    assert compare(dir_name + os.sep + "f1", dir_name + os.sep + "f2")
    assert not compare(dir_name + os.sep + "f1", dir_name + os.sep + "f3")
    assert 2 == getCompareCounter()
    os.remove(dir_name + os.sep + "f1")
    os.remove(dir_name + os.sep + "f2")
    os.remove(dir_name + os.sep + "f3")
    os.rmdir(dir_name)


compareCounter = 0
fileCounter = 0


if __name__ == '__main__':
    test()


