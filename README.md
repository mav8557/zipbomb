# zipbomb.py
zipbomb.py is a short program for creating simple zip bombs, described [here](https://en.wikipedia.org/wiki/Zip_bomb). This program creates zip bombs of a specified depth in a set output directory. 

## sizes
Each depth has DEPTH_FILE_NUMBER of zips. To calculate full size when unzipped recursively, do DEPTH_FILE_NUMBER^depths. For the default of **10** and a **3** depth bomb we get 10^3 or **1000 GiB** fully expanded.

## technical details
Standard deflate compression is used, with the zip64 extensions explicitly set to be used. This provides good compression without special steps. Better compression options include bzip2. With bzip2, compression of the initial dummy file goes from 1.0GiB to 785 bytes, a substantial improvement. There are no external dependencies for zipbomb.py. Time can be managed by the time utility on \*NIX systems.

## limitations
All file operations are at some point written to disk and then either removed or used later; there have been no attempts to do these operations in memory. If generating a large amount of data on disk repeatedly that is not necessary to keep, it might be advantageous to do so with a ramdisk, to over time reduce wear and tear on a drive. You can set one up in a terminal: 
```bash
mount -t tmpfs tmpfs /mnt/ramdisk -o size=2048M
```
This will create a tmpfs at /mnt/ramdisk (must exist prior) with a size of 2 GiB.
