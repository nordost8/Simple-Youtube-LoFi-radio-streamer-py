import os
import random
import time

from vidgear.gears import CamGear
from vidgear.gears import WriteGear

from video_master import get_file_paths_and_names, PATH_TO_VIDEOS_FOLDER

YOUTUBE_STREAM_KEY = 'eesv-9bje-4bfb-au40-7w7h' # or change to string, example: "5s63-hte6-baph-6h5b-7777"


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
            first_path = self.video_paths_by_names[self.video_queue[0]] if hasattr(self, 'video_paths_by_names') else None
            if first_path is None:
                print("Audio clips not found ;(\n Please add minimum 1 video with .mp4 format!")
            else:
                break
            time.sleep(1)


        self.writer = self.get_yt_writer(first_path)
        # Odd code due to asynchrony:
        # We write frames as stated in the documentation (this is mandatory)
        # When the stream breaks - ValueError - we close the writer and continue the work of the farmer, who also sees
        # that the writer died, and activates a new writer and starts passing the path of the next song to it
        for frame, video_path in self.framer():
            try:
                self.writer.write(frame)
            except ValueError:
                self.writer.close()
                self.writer = None

    def actualize_playlist(self):
        actual_videos = get_file_paths_and_names(PATH_TO_VIDEOS_FOLDER, '.mp4')
        if self.video_queue != list(actual_videos):
            self.video_paths_by_names = actual_videos
            new_videos = [video_name for video_name, video_path in actual_videos.items() if
                          video_name not in self.video_queue]
            if not self.video_queue:
                # if first:
                random.shuffle(new_videos)
            self.video_queue += new_videos

    def framer(self):
        video_queue_cycled = ShuffleCycle(self.video_queue)
        for video_name in video_queue_cycled:
            self.actualize_playlist()
            video_path = self.video_paths_by_names[video_name]
            stream = CamGear(source=video_path).start()
            while True:
                fframe = stream.read()
                print('frame:', str(fframe)[:10])
                if not self.writer or fframe is None:
                    stream.stop()
                    break
                yield fframe, video_path

    def get_yt_writer(self, video_path):
        self.output_params['-i'] = video_path
        return WriteGear(
            output="rtmp://a.rtmp.youtube.com/live2/{}".format(YOUTUBE_STREAM_KEY),
            logging=True,
            **self.output_params
        )


YoutubeStreamer()
