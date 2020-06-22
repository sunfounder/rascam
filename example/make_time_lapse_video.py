from rascam.utils import run_command

run_command("ffmpeg -r 25 -i image_%8d.jpg -vcodec libx264 "`date "+%Y-%m-%d_%H%M%S"`.mp4"")