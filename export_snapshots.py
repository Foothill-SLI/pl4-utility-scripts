import os
import subprocess
import sys

DEFAULT_INTERVAL = 1


def main():
    video_path = sys.argv[1]
    output_dir = sys.argv[2]
    if len(sys.argv) > 3:
        interval = sys.argv[3]
    else:
        interval = DEFAULT_INTERVAL

    os.makedirs(output_dir, exist_ok=True)

    subprocess.run(["ffmpeg", "-i", video_path, "-vf", f"fps=1/{interval}", os.path.join(output_dir, "%04d.jpg")])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} [video file] [output dir] [(optional) snapshot interval (seconds)]")
    else:
        main()
