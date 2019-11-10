# CLARK

OS: UBUNTU

Note: Make sure you are sudo to root on terminal

1) Extract the zip folder in /home/ directory
unzip CLARK.zip

2) Go to folder CLARK by running below command
cd /home/CLARK

3) run script.sh file which install all dependencies as well as start the driver program
sh script.sh

4) Wait for script.sh script to finish, it will take some time. Once you saw below message, press enter
"nohup: appending output to 'nohup.out'"

5) All is done. Go to browser and open http://127.0.0.1:8050/

6) The page shows empty charts since we haven't feed SOURCE_FILES folder with events file

7) I have already created multiple events file. copy each event file into SOURCE_FILES folder using below command.
cp events1.json ./SOURCE_FILES/
cp events2.json ./SOURCE_FILES/
cp events3.json ./SOURCE_FILES/
cp events4.json ./SOURCE_FILES/

8) Charts on browser will get update on real time as soon as files has been starting placed in SOURCE_FILES

9) Program wait for events file in SOURCE_FILES to get processed.
