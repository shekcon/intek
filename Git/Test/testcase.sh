#!/bin/bash
echo "-----------------INIT----------------"
./git_bonus.py init
echo "Welcome to Intek" > file1
echo "Welcome to Intek" > file2
echo "Welcome to Intek" > file3
echo "------------------ADD------------------"
./git_bonus.py add file1 file2 file3
echo "-----------------STATUS----------------"
./git_bonous.py status
echo "-----------------COMMIT----------------"
./git_bonus.py commit -m "1st commit master"
echo "-----------------BRANCH----------------"
./git_bonus.py branch Intek
./git_bonus.py branch
echo "-----------------MODIFIED--------------"
echo "Shekcon is my nickname" > file1 
echo "Welcome to Hyperspace" > hyper
echo "-----------------ADD-------------------"
./git_bonus.py add file1 hyper
echo "-----------------COMMIT----------------"
./git_bonus.py commit -m "2st commit master"
echo "-----------------CHECKOUT--------------"
./git_bonus.py checkout Intek
./git_bonus.py branch
echo "------------------LOG----------------"
./git_bonus.py log
echo "------------------ADD----------------"
echo "Best environment of IT" > file5
echo "INTEK applied institude" > file6
./git_bonus.py add file5 file6
echo "------------------LOG----------------"
./git_bonus.py log
echo "------------------LOG----------------"
./git_bonus.py log

