# Script for analyzing folders or files
# 
# sudo sh folder OR sudo sh file.wav

if [ -d $1 ]
then # If passed directory
	for audio in $1/*.wav
	do
		python analyze.py $audio > /dev/null
	done
else # If passed file
	python analyze.py $1 > /dev/null
fi