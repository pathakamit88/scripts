"""
Script to download all the liked youtube videos. 
This script works in combination with IFTTT applet 
'if-new-liked-video-then-append-to-a-text-file-in-dropbox'
"""
import os
import subprocess


def main():
  filepath = os.path.expanduser('~/Dropbox/IFTTT/YouTube/youtubelikes.txt')

  output_path = os.path.expanduser('~/Downloads/YouTube/')
  try:
    os.makedirs(output_path)
  except OSError:
    pass

  for line in open(filepath, 'rb'):
    line = line.strip()

    cmd = 'cd %s && youtube-dl -f 22 --no-playlist %s' % (output_path, line)
    mp3cmd = 'cd %s && youtube-dl --extract-audio --audio-format mp3 %s' % (
        output_path, line)

    subprocess.Popen(mp3cmd, shell=True)
    p = subprocess.Popen(cmd, shell=True)
    p.communicate()

  os.remove(filepath)


if __name__ == '__main__':
  main()
