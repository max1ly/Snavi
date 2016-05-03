#!/usr/bin/env python
import datetime
import getopt
import mimetypes
import os
import random
import subprocess
import sys


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


inputpath = ""
outputpath = ""
recursive = False
overwrite = True
run_in_folder = False
videofile = ""
colors = Colors()


def print_no_newline(string):
    sys.stdout.write(string)
    sys.stdout.flush()


def read_arguments():
    """
    Reads and parses cli arguments
    """
    try:
        #TODO - silent output mode
        opts, args = getopt.getopt(sys.argv[1:], 'hnrf:i:o:', ['help', 'file=', 'no-overwrite', 'recursive', 'input=', 'output='])
        if not opts:
            usage()
    except getopt.GetoptError:
        usage()

    global inputpath
    global outputpath
    global overwrite
    global recursive
    global run_in_folder
    global videofile

    for opt, arg in opts:
        if not run_in_folder and opt in ('-f', '--file'):
            videofile = arg
        elif not run_in_folder and opt in ('-h', '--help'):
            usage()

        else:
            if opt in ('-n', '--no-overwrite'):
                overwrite = False

            if opt in ('-r', '--recursive'):
                recursive = True

            if opt in ("-i", "--input"):
                run_in_folder = True
                inputpath = arg
                if not os.path.exists(inputpath):
                    usage(inputpath + " - the directory does not exist.")
                outputpath = os.path.join(inputpath, "pics")

            if opt in ("-o", "--output"):
                outputpath = arg

            if not os.path.exists(outputpath):
                os.makedirs(outputpath)

    print('Input folder :', inputpath)
    print('Output folder:', outputpath, "\n")


def usage(*message):
    """
    Prints out the usage info
    :param message: is optional, passed when error text has to be displayed
    """
    if message:
        print(message)
    print(colors.BOLD, "  Usage:", colors.ENDC, "snavi.py -f <file>\n"
          "           snavi.py -i <inputfolder>\n\n",
          "  Options:\n",
          colors.BOLD, "       -h, --help", colors.ENDC, "\n\n",
          "              See help\n",
          colors.BOLD, "       -f, --file=FILE", colors.ENDC, "\n"
          "              Path to single video file\n\n",
          colors.BOLD, "       -i, --input=PATH", colors.ENDC, "\n"
          "              Directory where input videos are stored\n\n",
          colors.BOLD, "       -o, --output=PATH", colors.ENDC, "\n"
          "              Directory where output pictures will be saved (creates if it doesn't exist)\n\n",
          colors.BOLD, "       -n, --no-overwrite", colors.ENDC, "\n"
          "              Do not overwrite output pictures\n\n",
          colors.BOLD, "       -r, --recursive", colors.ENDC, "\n"
          "              Run the script recursively for every video file inside inner directories of given folder\n\n")
    sys.exit(2)


def get_random_time(file):
    """
    Calculates duration of a video file and takes a random second of the duration
    :param file: file location
    :return: a random duration of a given video file
    """
    duration_command = "ffprobe -i " + os.path.join(inputpath, file) + \
                       " -show_entries format=duration -v quiet -of csv=\"p=0\""
    process = subprocess.Popen(duration_command,
                               shell=True,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print(err.decode())

    duration = out
    if duration is None:
        return -1

    duration = float(duration)
    print("    Full duration                 :", format_time(duration))

    return random.randrange(1, int(round(duration)))


def format_time(random_second):
    """Format random number of seconds to string hh:mm:ss
    :param random_second: time in seconds
    """

    date = datetime.timedelta(seconds=random_second)
    time_string = date.__str__()

    return time_string


def take_snapshot(file, random_time):
    """
    Takes a picture of a given video file at given time
    :param file: video file location
    :param random_time: time, format: hh:mm:ss
    """
    snapshot_command = "ffmpeg -i " + os.path.join(inputpath, file) + " -ss " + random_time + \
                       " -vframes 1 " + os.path.join(outputpath, file) + ".png"
    snapshot_command = snapshot_command + " -y" if overwrite else snapshot_command + " -n"
    process = subprocess.Popen(snapshot_command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print(colors.FAIL, "[ FAIL ] return code:", return_code, "\n")
        print("[ ERROR ]", err.decode(), colors.ENDC, "\n")
    else:
        print(colors.OKGREEN, "[ OK ]", colors.ENDC, "\n")


def is_correct_video_file(file):
    """
    This verifies if the given file in video file
    :param file: file location
    :return: true if it's video format, false if there are any errors
    """
    mime_type = mimetypes.guess_type(file, False)[0].split("/", 1)[0]
    if mime_type != "video":
        print(colors.WARNING, "[ WARN ] Not video mime type.", colors.ENDC, "\n")
        return False

    check_file_command = "ffprobe -v error " + os.path.join(inputpath, file)
    status = subprocess.Popen(check_file_command,
                              shell=True,
                              stdin=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              stdout=subprocess.PIPE).communicate()[0]
    if status != b'':
        print(colors.FAIL, status.decode(), colors.ENDC)
        return False
    return True


def run_for_videos_in_folder():
    """
    Loop goes through all files in specified directory and takes snapshots
    of video files presented in folder and subdirectories.

    It does one ffmpeg thread at a time on Linux, not sure how it runs on others OSes
    :return: status; 0 - success
    """
    for file in os.listdir(inputpath):
        if os.path.isdir(os.path.join(inputpath, file)):
            # TODO - go recursively inside the folder
            continue
        take_snapshot_for_file(file)
    return 0


def take_snapshot_for_file(file):
    print(colors.BOLD, file, "-->", colors.ENDC)
    if not is_correct_video_file(file):
        return
    random_time = format_time(get_random_time(file))
    print_no_newline("    Taking snapshot at random time: " + random_time),
    take_snapshot(file, random_time)


if __name__ == "__main__":
    read_arguments()
    if run_in_folder:
        run_for_videos_in_folder()
    else:
        take_snapshot_for_file(videofile)
