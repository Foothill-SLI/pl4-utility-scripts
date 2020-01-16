import os
import subprocess
import sys

TEMP_CONCAT_SCRIPT_FILE_NAME = "temp-file_list"


def main():
    in_dir = sys.argv[1]
    output_path = sys.argv[2]
    output_dir = os.path.dirname(output_path)

    # concatenation demuxer needs a script file as input
    concat_script_path = os.path.join(output_dir, TEMP_CONCAT_SCRIPT_FILE_NAME)
    with open(concat_script_path, 'w') as concat_script_file:
        for path in sorted([os.path.join(in_dir, path) for path in os.listdir(in_dir)]):
            concat_script_file.write(f"file {path}\n")

    # run command
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_script_path, "-c", "copy", output_path])

    # clean up
    os.remove(concat_script_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [video dir] [output file]")
    else:
        main()
