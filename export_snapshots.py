import os
import subprocess
import sys

DEFAULT_INTERVAL = 1


def main():
    video_path = sys.argv[1]
    output_dir = sys.argv[2]
    interval = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_INTERVAL
    quality_args = ["-q:v", f"{sys.argv[4]}"] if len(sys.argv) > 4 else None

    os.makedirs(output_dir, exist_ok=True)

    params = ["ffmpeg", "-i", video_path, "-vf", f"fps=1/{interval}", os.path.join(output_dir, "%04d.jpg")]
    if quality_args:
        params = params[:3] + quality_args + params[3:]
    print(params)
    subprocess.run(params)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} [video file] [output dir] [(optional) interval] [(optional) quality]\n"
              "       interval = seconds\n"
              "       quality  = 1 - 31, 1 is best")
    else:
        main()
