This script captures random frames from video files as still images.

This is useful when dealing with a large number of unsorted, unknown, or poorly named videos. By quickly browsing through the resulting images, you can identify the contents of the videos without having to watch them individually. This is especially helpful when managing large collections of home videos that have accumulated on your computer and need to be sorted or cleared to free up disk space.

###Install:
1. [python3](https://www.python.org)
2. [ffmpeg](https://ffmpeg.org/)
3. [imagemagick](https://www.imagemagick.org/) (optional) 
4. checkout the repo, or download zip file and unpack it

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
