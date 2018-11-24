#!/bin/bash
echo "-----------------INIT----------------"
./git_bonous.py init
echo "Welcome to Intek" > file1
echo "Welcome to Intek" > file2
echo "Welcome to Intek" > file3
echo "------------------ADD------------------"
./git_bonous.py add file1 file2 file3
echo "-----------------STATUS----------------"
./git_bonous.py status
echo "-----------------COMMIT----------------"
./git_bonous.py commit -m "1st commit master"
echo "-----------------BRANCH----------------"
./git_bonous.py branch Intek
./git_bonous.py branch
echo "-----------------MODIFIED--------------"
echo "Shekcon is my nickname" > file1 
echo "Welcome to Hyperspace" > hyper
echo "-----------------ADD-------------------"
./git_bonous.py add file1 hyper
echo "-----------------COMMIT----------------"
./git_bonous.py commit -m "2st commit master"
echo "-----------------CHECKOUT--------------"
./git_bonous.py checkout Intek
./git_bonous.py branch
echo "------------------LOG----------------"
./git_bonous.py log
echo "------------------ADD----------------"
echo "Best environment of IT" > file5
echo "INTEK applied institude" > file6
./git_bonous.py add file5 file6
echo "------------------LOG----------------"
./git_bonous.py log
echo "------------------LOG----------------"
./git_bonous.py log

