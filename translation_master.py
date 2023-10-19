import os
import random
import subprocess as sp
import time

from vidgear.gears import CamGear
from vidgear.gears import WriteGear

from video_master import get_file_paths_and_names, PATH_TO_VIDEOS_FOLDER

YOUTUBE_STREAM_KEY = os.getenv('YOUTUBE_STREAM_KEY') or 'eesv-9bje-4bfb-au40-7w7h' # Youtube stream key example


class ShuffleCycle:
    """
    Implements cyclic shuffling of a given iterable sequence.
    Retrieves elements in a random order upon each cycle.

    Parameters:
    - `iterable` (iterable object): Initial sequence to be shuffled and cyclically utilized.
    """

    def __init__(self, iterable):
        random.shuffle(iterable)
        self.shuffled_iterable = iterable
        self.index = 0
        self.max_index = len(self.shuffled_iterable) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index > self.max_index:
            self.index = 0
            random.shuffle(self.shuffled_iterable)

        value = self.shuffled_iterable[self.index]
        self.index += 1
        return value


class YoutubeStreamer:
    video_queue = []
    writer = None

    def __init__(self):
        self.video_paths_by_names = None
        self.output_params = {
            "-re": True,
            "-i": None,
            "-ar": 96000,
            "-vcodec": "libx264",
            "-pix_fmt": "yuv420p",
            "-f": "flv",
            "-preset": "slow",
            "-r": 60,
            "-g": int(60 * 2),
            "-crf": 18,
            "-c:a": "aac",
            "-ac": 2,
            "-b:a": "320k",
            "-profile:v": "high",
            "-level": "4.0",
            "-bf": 2,
            "-coder": 1,
            "-threads": 6,
        }

        while True:
            self.actualize_playlist()
            if not self.video_queue:
                print("Audio clips not found ;(\n Please add minimum 1 video with .mp4 format!")
            else:
                break
            time.sleep(1)

        video_queue_cycled = ShuffleCycle(self.video_queue)
        for video_name in video_queue_cycled:
            video_path = self.video_paths_by_names[video_name]
            writer = self.get_yt_writer(video_path)

            cmd = ['-y', '-f', 'rawvideo',
             '-vcodec', 'rawvideo', '-s', '1920x1080', '-pix_fmt', 'bgr24', '-i', '-', '-re', '-i',
             video_path,
             '-ar', '96000', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-f', 'flv', '-preset', 'slow', '-r', '60',
             '-g', '120', '-crf', '18', '-c:a', 'aac', '-ac', '2', '-b:a', '320k', '-profile:v', 'high', '-level',
             '4.0', '-bf', '2', '-coder', '1', '-threads', '6', f'rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}']

            writer.execute_ffmpeg_cmd(cmd)
            writer.close()

    def actualize_playlist(self):
        actual_videos = get_file_paths_and_names(PATH_TO_VIDEOS_FOLDER, '.mp4')
        if self.video_queue != list(actual_videos):
            self.video_paths_by_names = actual_videos
            new_videos = [video_name for video_name, video_path in actual_videos.items() if
                          video_name not in self.video_queue]
            self.video_queue += new_videos

    def get_yt_writer(self, video_path):
        self.output_params['-i'] = video_path
        return WriteGear(
            output="rtmp://a.rtmp.youtube.com/live2/{}".format(YOUTUBE_STREAM_KEY),
            logging=True,
            **self.output_params
        )


YoutubeStreamer()
