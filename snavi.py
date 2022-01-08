#!/usr/bin/env python3
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


input_path = ""
output_path = ""
recursive = False
overwrite = True
run_in_folder = False
video_file = ""
colors = Colors()


def print_no_newline(*strs):
    for str in strs:
        sys.stdout.write(str)
    sys.stdout.flush()


def read_arguments():
    """
    Reads and parses cli arguments
    """
    try:
        # TODO - silent output mode
        opts, args = getopt.getopt(sys.argv[1:], 'hnrf:i:o:',
                                   ['help', 'file=', 'no-overwrite', 'recursive', 'input=', 'output='])
        if not opts:
            usage()
    except getopt.GetoptError:
        usage()

    global input_path
    global overwrite
    global recursive
    global run_in_folder
    global video_file
    global imagemagick_installed

    print()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()

        if not run_in_folder and opt in ('-f', '--file'):
            video_file = arg
            print('Input file   :', video_file)

        if opt in ('-n', '--no-overwrite'):
            overwrite = False

        if opt in ('-r', '--recursive'):
            recursive = True

        if opt in ("-i", "--input"):
            run_in_folder = True
            input_path = arg
            print('Input folder :', input_path)

        if opt in ("-o", "--output"):
            out = arg
            set_output_path(out)

    if not output_path:
        set_output_path()

    print()


def set_output_path(*out):
    global output_path
    if len(out) > 0:
        output_path = out[0]
    elif not run_in_folder and not output_path:
        output_path = os.path.join(os.path.dirname(video_file), "pics")
    create_output_dir_if_not_exists(output_path)
    print('Output folder:', output_path)


def create_output_dir_if_not_exists(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


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
          colors.BOLD, "       -h, --help", colors.ENDC, "\n",
          "              See the help\n\n",
          colors.BOLD, "       -f, --file=<path to file>", colors.ENDC, "\n"
          "              Path to single video file\n\n",
          colors.BOLD, "       -i, --input=<path to directory>", colors.ENDC, "\n"
          "              Directory where input videos are stored\n\n",
          colors.BOLD, "       -o, --output=<path to directory>", colors.ENDC, "\n"
          "              Directory where output pictures will be saved (creates if it doesn't exist)\n\n",
          colors.BOLD, "       -n, --no-overwrite", colors.ENDC, "\n"
          "              Do not overwrite output pictures\n\n",
          colors.BOLD, "       -r, --recursive", colors.ENDC, "\n"
          "              Run the script recursively for every video file inside inner directories of given folder\n\n")
    sys.exit(2)


def get_duration_and_random_second(file):
    """
    Calculates duration of a video file and takes a random second of the duration
    :param file: file location
    :return: full video duration and a random second as a tuple
    """
    print("Calculating duration of ", file)
    duration_command = "ffprobe -i \"" + file + "\" -show_entries format=duration -v quiet -of csv=\"p=0\""
    process = subprocess.Popen(duration_command,
                               shell=True,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print(err.decode())

    if out is None:
        return -1

    duration = float(out)
    duration_range = int(duration)
    if duration_range == 0:
        return duration, 0
    else:
        return duration, random.randint(0, duration_range)


def format_time(random_second):
    """Format random number of seconds to string hh:mm:ss
    :param random_second: time in seconds
    """

    date = datetime.timedelta(seconds=random_second)
    time_string = date.__str__()

    return time_string


def take_screenshot(file_path, random_time):
    """
    Takes a picture of a given video file at given time
    :param file_path: video file location
    :param random_time: time, format: hh:mm:ss
    :return: True if picture was taken, False if not
    """
    """get file name without extension"""
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(output_path, file_name + ".png")
    screenshot_command = "ffmpeg -i \"" + file_path + "\" -ss " + random_time + \
                         " -vframes 1 \"" + output_file + "\""
    screenshot_command = screenshot_command + " -y" if overwrite else screenshot_command + " -n"
    process = subprocess.Popen(screenshot_command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print(colors.FAIL, "[ FAIL ] return code:", return_code, "\n")
        print("[ ERROR ]", err.decode(), colors.ENDC, "\n")
        return False, ""
    else:
        print(colors.OKGREEN, "[ OK ]", colors.ENDC, "\n")
        return True, output_file


def is_correct_video_file(file_path):
    """
    This verifies if the given file in video file
    :param file_path: file location
    :return: true if it's video format, false if there are any errors
    """
    print(colors.BOLD, file_path, "-->", colors.ENDC)
    mime_type = None
    mime = mimetypes.guess_type(file_path, False)[0]
    if mime is not None:
        mime_type = mime.split("/", 1)[0]
    if mime_type != "video":
        print(colors.WARNING, "[ WARN ] Not a video file", colors.ENDC, "\n")
        return False

    check_file_command = "ffprobe -v error \"" + file_path + "\""
    status = subprocess.Popen(check_file_command,
                              shell=True,
                              stdin=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              stdout=subprocess.PIPE).communicate()[0]
    if status != b'':
        print(colors.FAIL, status.decode(), colors.ENDC)
        return False
    return True


def run_for_videos_in(input_dir):
    """
    Loop goes through all files in specified directory and takes screenshots
    of video files presented in folder and subdirectories.

    It does one ffmpeg thread at a time on Linux, not sure how it runs on others OSes
    :return: status; 0 - success
    """
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        isdir = os.path.isdir(file_path)
        if recursive and isdir:
            run_for_videos_in(file_path)
        if not isdir and is_correct_video_file(file_path):
            take_screenshot_for_file(file_path)
        continue
    return 0


def take_screenshot_for_file(file_path):
    duration, random_second = get_duration_and_random_second(file_path)
    timestamp = format_time(random_second)
    duration_formatted = format_time(duration)
    print("    Full duration       ", duration_formatted)
    print_no_newline("    Taking screenshot at " + timestamp),
    taken, picture_file = take_screenshot(file_path, timestamp)
    if imagemagick_installed and taken:
        add_timestamp(picture_file, duration_formatted, timestamp)


def add_timestamp(picture_file, duration_formatted, timestamp):
    """
    add text to the picture
    """
    text = "Duration: " + duration_formatted + ", taken at: " + timestamp
    text_command = "convert " + picture_file + \
                   " -gravity SouthEast -pointsize 22" + \
                   " -fill \"#FF0000\"" + \
                   " -draw \"text 5,5 '" + text + "'\" " + \
                   picture_file
    process = subprocess.Popen(text_command,
                               shell=True,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print(colors.FAIL, "[ FAIL ] adding text to picture. Return code:", return_code, "\n")
        print("[ ERROR ]", err.decode(), colors.ENDC, "\n")


def check_imagemagick_installed():
    """
    Checks if ImageMagick is installed
    :return: True if installed, False if not
    """
    process = subprocess.Popen("which convert",
                               shell=True,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        return False
    else:
        return True


if __name__ == "__main__":
    try:
        imagemagick_installed = check_imagemagick_installed()
        read_arguments()
        if run_in_folder:
            run_for_videos_in(input_path)
        else:
            take_screenshot_for_file(video_file)
    except (KeyboardInterrupt, SystemExit):
        print("\n\n" + Colors.FAIL + "Execution was interrupted. Exiting..." + Colors.ENDC)
        sys.exit(2)
