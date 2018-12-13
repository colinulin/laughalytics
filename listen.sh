# This file records 5 second audio clips into /audio/pending, then moves it to /audio/recording
# 
# sudo sh listen.sh

COUNTER=0
while [  $COUNTER -lt 1 ]; do
	NOW=$(date +"%s")
    # arecord -D hw:CARD=GoMic,DEV=0 -c 2 -f s16_LE -d 2 audio/pending/sample-{$(date +"%s")}.wav # Using ALSA on Raspberry Pi
    sox -b 32 -e unsigned-integer -r 96k -c 2 -d --clobber --buffer $((96000*2*10)) audio/recording/sample-{$NOW}.wav trim 0 5 # Using sox on Mac
    mv audio/recording/sample-$NOW.wav audio/pending/sample-$NOW.wav
    let COUNTER=COUNTER+1
done