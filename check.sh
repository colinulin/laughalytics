# This file checks to see if new files were 
# added to the samples directory then analyzes them.
# 
# Audio files start in /audio/pending, are normalized and analyzed in /audio/normalize, and end in /audio/analyzed
# 
# sudo sh listen.sh

# inotifywait -m audio/pending -e create # for linux
fswatch -Ie '.*\.*$' -i '.*\.wav$' -0 audio/pending | while read -d "" event
	do
		if [ -f $event ]
		then
		    file=$(basename "$event")
		    mv $event $PWD/audio/normalize/$file
		    sox --norm=-1 $PWD/audio/normalize/$file $PWD/audio/normalize/normalized-$file
		    rm $PWD/audio/normalize/$file
		    python analyze.py $PWD/audio/normalize/normalized-$file > /dev/null
		    mv $PWD/audio/normalize/normalized-$file $PWD/audio/analyzed/normalized-$file
	    fi
	done