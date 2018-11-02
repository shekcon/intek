# Rsync
### Core project
### Notions: linux filesystem and advanced I/O
## Introduction

This subject is both a system and an algorithm project. 

First, it aims to give you a thorough understanding of the Linux filesystem by manipulating it. Since your Hyperspace you know that files have permissions, times and some other properties as displayed by a ls -l. 

Through this project, you will understand how those file properties can be manipulated from inside a program, as well as learn a few advanced I/O functionalities. It's probably not the most fascinating topic for most of you, but you need a decent understanding of how the system works to program on it!

Secondly, it will initiate you to a particular algorithm problematic: the Longest Common Subsequence problem.

## What is rsync?

rsync is an utility that allows you to copy or update a file in another location - you "synchronise" the file from one location to another. The file at destination is then the exact copy of the source.

Its specificity is that the file is not entirely copied in some cases. Because rsync is can copy files from one computer to another (instead of just locally), it was designed to reduce network usage and to send as little data as possible. Thus, when the two files already share many parts (for example if a line has just been added at the end), only the parts that are different are copied.

To do that, rsync splits both files into chunks and uses an algorithm called the "rolling checksum" algorithm to check which chunks are equal and which are different, before sending only the differences over the network. That practice of sending data as differences ('deltas') rather than complete files is called delta encoding. The particularity of the "rolling checksum" algorithm is that it allows for comparison of two files without needing to access both files at the same time.

It's okay if that doesn't make much sense to you at the first read: you won't have to implement the "rolling checksum" algorithm anyway!

## Your mission

You will implement a simplified variant of rsync. Your program will only work locally, on your computer, and not over the network.

What your program will do, in its core part, is take two files as arguments, check if the destination file is different from the source, in which case it will update only the differences. So if the source and destination file are different only by a few characters, you shouldn't rewrite the destination file entirely when you update it!

There are several aspects to this project: 

- Understanding the rsync utility and what you can do with it 
- Understanding the longest common subsequence problem
- Getting familiar with the Linux filesystem
- Being able to use advanced I/O functions

All those aspects will play a part in the project review.

## Directions

Your program must be called rsync.py and be present at the root of your git repository.

It must respect the following rules:

- It will copy a file from source to destination, both files must be strictly identical
- The destination file will have the same permissions as the source file (equivalent to option -p of rsync, which becomes the default behavior)
- The destination file will have the same access/modification times as the source file (equivalent to option -t of rsync, which becomes the default behavior)
- You will keep symlinks and hardlinks (equivalent to options -l and -H of rsync, which become the default behavior)
- You will only copy the parts that are different between the source file and the destination file (if they are already identical, nothing should be written!)

By default, your program will decide if the destination file needs to be updated by checking the size & modification time (like rsync does).

To be able to change that default behavior, you will implement the following options:

- -u
- -c

Usage of your program: ./rsync.py [OPTIONS] SRC_FILE DESTINATION

DESTINATION can either be a file or an existing directory. You might have to do some checks on the arguments first thing into your program...!

Note: your implementation must behave like rsync does, except for hardlinks. By default rsync doesn't copy a hardlink if both files are not specified as source, but you will copy it anyway.

## Guided examples

Analyze the examples below to understand how the regular rsync works, and how your own version behaves by default.

Of course you shouldn't limit yourself to those tests, do your own to understand how the -u and -c options work, as well as the symlinks and hardlinks!

    $ ls -l
    total 8
    -rwxr-xrwx  1 laurie  wheel  6 Oct 19 17:17 file1

    # let's see how rsync behaves by default
    $ rsync file1 dest_basic
    $ ls -l
    total 16
    -rwxr-xr-x  1 laurie  wheel  6 Oct 19 17:44 dest_basic
    -rwxr-xrwx  1 laurie  wheel  6 Oct 19 17:17 file1

    # let's see option -t
    $ rsync -t file1 dest_with_times
    $ ls -l
    total 24
    -rwxr-xr-x  1 laurie  wheel  6 Oct 19 17:44 dest_basic
    -rwxr-xr-x  1 laurie  wheel  6 Oct 19 17:17 dest_with_times
    -rwxr-xrwx  1 laurie  wheel  6 Oct 19 17:17 file1

    # now let's see option -p
    $ rsync -p file1 dest_with_perms
    $ ls -l
    total 32
    -rwxr-xr-x  1 laurie  wheel  6 Oct 19 17:44 dest_basic
    -rwxr-xrwx  1 laurie  wheel  6 Oct 19 17:45 dest_with_perms
    -rwxr-xr-x  1 laurie  wheel  6 Oct 19 17:17 dest_with_times
    -rwxr-xrwx  1 laurie  wheel  6 Oct 19 17:17 file1

    # now we see the default behavior of your program!
    $ ls -l
    total 88
    -rwxr-xrwx  1 laurie  wheel      6 Oct 19 17:17 file1
    -rwxr-xr-x  1 laurie  wheel  30148 Oct 19 17:55 rsync.py
    $ ./rsync.py file1 dest1
    $ ls -l
    total 96
    -rwxr-xrwx  1 laurie  wheel      6 Oct 19 17:17 dest1
    -rwxr-xrwx  1 laurie  wheel      6 Oct 19 17:17 file1
    -rwxr-xr-x  1 laurie  wheel  30148 Oct 19 17:55 rsync.py

    # What if the destination is an existing directory?
    $ mkdir dir1
    $ ls -l
    total 88
    drwxr-xr-x  2 laurie  wheel     64 Oct 19 17:59 dir1
    -rwxr-xrwx  1 laurie  wheel      6 Oct 19 17:17 file1
    -rwxr-xr-x  1 laurie  wheel  30148 Oct 19 17:55 rsync.py
    $ ./rsync.py file1 dir1
    $ ls -lR
    total 88
    drwxr-xr-x  3 laurie  wheel     96 Oct 19 17:59 dir1
    -rwxr-xrwx  1 laurie  wheel      6 Oct 19 17:17 file1
    -rwxr-xr-x  1 laurie  wheel  30148 Oct 19 17:55 rsync.py

    ./dir1:
    total 8
    -rwxr-xrwx  1 laurie  wheel  6 Oct 19 17:17 file1
    $



## Allowed functions

- argparse module
- os.path module
- os.difflib module
- os.open, os.read, os.write, os.sendfile, os.lseek
- os.mkdir
- os.stat module
- os.symlink, os.link, os.readlink
- os.scandir
- os.unlink
- os.utime, os.chmod

Any function or module that is not explicitly allowed is forbidden for the core part. If you think another module or function is absolutely necessary, ask the mentors.

## How to go about it?

### Step by step!

1. You should start by playing around with rsync to analyse its behavior. Don't know how one option works exactly and what is its output? Just test it! And don't forget to test the error cases as well. (What happens when a file doesn't exist? When you don't have certain rights? Etc.)

2. Once you have a good idea of the edge cases and what is expected of you, you should look up the documentation for the above functions. This will give you an idea of which functions can help you do which job. Code very simple test cases to manipulate them if necessary.

3. Then, code the program and its options (including a proper error handling), but with a naive algorithm that copies over the complete file every time.

4. Once that's stable, you are free to work on the copy algorithm: identify which parts are different from one file to the other, and write on the destination file as little characters as possible.


# BONUS: recursive

### Notions: linux filesystem and advanced I/O

## Multiple files

For this bonus, you need to handle multiple files on the command line as well as recursive copy of folders. Recursive copy will be possible with an -r option.

### Look at the example below and test it yourself!

    $ ls -l
    total 24
    drwxr-xr-x  2 laurie  wheel  64 Oct 21 18:02 dir1
    -rwxr-xrwx  1 laurie  wheel   6 Oct 19 17:17 file1
    -rw-r--r--  1 laurie  wheel   9 Oct 21 18:01 file2
    -rw-r--r--  1 laurie  wheel  13 Oct 21 18:01 file3

    # multiple files on the command line with a directory as destination
    $ rsync file1 file2 file3 dir1
    $ ls -Rl
    total 24
    drwxr-xr-x  5 laurie  wheel  160 Oct 21 18:02 dir1
    -rwxr-xrwx  1 laurie  wheel    6 Oct 19 17:17 file1
    -rw-r--r--  1 laurie  wheel    9 Oct 21 18:01 file2
    -rw-r--r--  1 laurie  wheel   13 Oct 21 18:01 file3

    ./dir1:
    total 24
    -rwxr-xr-x  1 laurie  wheel   6 Oct 21 18:02 file1
    -rw-r--r--  1 laurie  wheel   9 Oct 21 18:02 file2
    -rw-r--r--  1 laurie  wheel  13 Oct 21 18:02 file3
    $ mkdir dir2
    $ ls -R
    dir1	dir2	file1	file2	file3

    ./dir1:
    file1	file2	file3

    ./dir2:
        
    # recursive copy of a directory
    $ rsync -r dir1 dir2
    $ ls -R
    dir1	dir2	file1	file2	file3

    ./dir1:
    file1	file2	file3

    ./dir2:
    dir1

    ./dir2/dir1:
    file1	file2	file3

    # your own version  will do the same
    $ ls -R
    dir1	file1	file2	file3    rsync.py

    ./dir1:
    file1	file2	file3
    $ ./rsync.py -r dir1 dir2
    $ ls -R
    dir1		dir2		file1		file2		file3		rsync.py

    ./dir1:
    file1	file2	file3

    ./dir2:
    dir1

    ./dir2/dir1:
    file1	file2	file3

