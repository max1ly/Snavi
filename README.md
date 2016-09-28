This script is written for purpose of taking random screenshots of a video.
It run against a single video as well as for directory and subdirectories(if specified)
recursively for videos to take a screenshot at random second.

###Prerequisites
1. It supports [python3](https://www.python.org)
1. It uses [ffmpeg](https://ffmpeg.org/), so it has to be installed

###Run:
    $ python3 snavi.py -h
       Usage:  snavi.py -f <file>
               snavi.py -i <inputfolder>

       Options:
             -h, --help
                   See help

             -f, --file=<path to file>
                  Path to single video file

             -i, --input=<path to directory>
                  Directory where input videos are stored

             -o, --output=<path to directory>
                  Directory where output pictures will be saved (creates if it doesn't exist)

             -n, --no-overwrite
                  Do not overwrite output pictures

             -r, --recursive
                  Run the script recursively for every video file inside inner directories of given folder


