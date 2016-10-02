This script is for taking random screenshot of a video.

For instance, if you've got bunch of videos unsorted, unknown and poorly named -
you can screenshot all of them and then go through pictures to see what are they about.

The common use case, I guess, is heaps of home shots stored on computer,
say you need some disk space to free and there is no time to watch all of them...

###Install:
1. [python3](https://www.python.org)
1. [ffmpeg](https://ffmpeg.org/)
1. checkout the repo, or download zip file and unpack it

###To run:
    $ python3 snavi.py -h
       Usage:  snavi.py -f <file>
               snavi.py -i <inputfolder>

       Options:
             -h, --help
                   See the help

             -f, --file=<path to file>
                  Path to single video file

             -i, --input=<path to directory>
                  Directory where input videos are stored

             -o, --output=<path to directory>
                  Directory where output pictures will be saved (creates if it doesn't exist)

             -n, --no-overwrite
                  Do not overwrite output pictures

             -r, --recursive
                  Run the script recursively for every video file inside subdirectories
                  of given folder. Doesn't work with option '-f'

It can run for directory and subdirectories recursively (if specified) of videos.
It simply takes a screenshot at random second:

    $ python3 snavi.py -i ~/Videos -o ~/Videos/pics -r
