import itertools
import os
import random
import time

from vidgear.gears import WriteGear

from video_master import get_file_paths_and_names, PATH_TO_VIDEOS_FOLDER

YOUTUBE_STREAM_KEY = os.getenv('YOUTUBE_STREAM_KEY', '5pr3-hqe6-baph-6h5b-7xc5')
FFMPEG_THREADS_COUNT = os.getenv('FFMPEG_THREADS_COUNT', 2)
VIDEO_GROUPED_COUNT = int(os.getenv('VIDEO_GROUPED', 5))

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


def get_n_els_from_cycle(cycle_ptr, n):
    while True:
        temp = []
        for _ in range(n):
            temp.append(next(cycle_ptr))
        yield temp


class YoutubeStreamer:
    video_queue = []
    writer = None

    def __init__(self):
        self.video_paths_by_names = None

        while True:
            self.actualize_playlist()
            if not self.video_queue:
                print("Audio clips not found ;(\n Please add minimum 1 video with .mp4 format!")
            else:
                break
            time.sleep(1)

    def start(self):
        video_queue_cycled = ShuffleCycle(self.video_queue)
        for video_names in get_n_els_from_cycle(video_queue_cycled, VIDEO_GROUPED_COUNT):
            self.actualize_playlist()

            video_paths = [self.video_paths_by_names[video_name] for video_name in video_names]
            writer = WriteGear(video_paths[0], logging=True)

            cmd = ['-y']

            dynamic_args = list(itertools.chain.from_iterable(('-re', '-i', path) for path in video_paths))
            cmd += dynamic_args

            filter_complex = ' '.join([f'[{i}:v] [{i}:a]' for i in range(VIDEO_GROUPED_COUNT)])
            concat_filter = f'concat=n={VIDEO_GROUPED_COUNT}:v=1:a=1'

            filter_complex_str = f'{filter_complex} {concat_filter}'

            cmd += [
                '-filter_complex', f'{filter_complex_str} [v] [a]',
                '-map', '[v]',
                '-map', '[a]',
                '-ar', '96000',
                '-vcodec', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-f', 'flv',
                '-preset', 'ultrafast',
                '-r', '60',
                '-g', str(int(60 * 4.5)),
                '-profile:v', 'high',
                '-c:a', 'aac',
                '-ac', '2',
                '-threads', f'{FFMPEG_THREADS_COUNT}',
                f'rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_STREAM_KEY}'
            ]

            writer.execute_ffmpeg_cmd(cmd)
            writer.close()

    def actualize_playlist(self):
        actual_videos = get_file_paths_and_names(PATH_TO_VIDEOS_FOLDER, '.mp4')
        if self.video_queue != list(actual_videos):
            self.video_paths_by_names = actual_videos
            new_videos = [video_name for video_name, video_path in actual_videos.items() if
                          video_name not in self.video_queue]
            self.video_queue += new_videos


if __name__ == '__main__':
    youtube_streamer = YoutubeStreamer()
    youtube_streamer.start()
