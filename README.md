# Simple-Youtube-LoFi-radio-streamer-py
🎶 An effortless solution for continuous remote streaming on YouTube. Stream your prepared video files with audio or automatically generate visually captivating videos based on your audio using my additional library, Magic-FFT-audio-visualizer-py!

**Simply watch this YouTube video and judge for yourself (clickable):**

[![Watch the video](https://img.youtube.com/vi/PbPL1uChWfQ/maxresdefault.jpg)](https://youtu.be/PbPL1uChWfQ)

**Usage:**

- Place the audio files you want to include in your radio in the "resource/music_files" folder.
- After video generation, they will be stored in the "resource/ready_videos" folder.

**Running:**

- You can use the "run.sh" script or launch a Docker container. A "Dockerfile" is available in the repository for this purpose.

```bash
docker run -d -v ${PWD}/resource/music_files:/app/Simple-Youtube-LoFi-radio-streamer-py/resource/music_files -v ${PWD}/resource/ready_videos:/app/Simple-Youtube-LoFi-radio-streamer-py/resource/ready_videos -it -e YOUTUBE_STREAM_KEY="your-stream-key" -e VIDEO_GROUPED="5" radio
```

**Environment Variables:**

- YOUTUBE_STREAM_KEY (Your streaming key, obtainable from the YouTube live streaming scheduling page).
- VIDEO_GROUPED (This variable groups multiple videos into one. Recommended values range from 3 to 10 for multiple video files. For a single large video file, set it to 1).
- FFMPEG_THREADS_COUNT (This variable specifies the number of CPU threads for streaming. Recommended to set it to 2).
Additional Information:

Videos are streamed in a random order.
After streaming the last video, the playlist shuffles to set a new random order.

**Note:**

You can choose not to use the video generator "video_master" if you already have your own fullHD MP4 format videos, preferably at 60 fps. 

**Customization:**

The code is relatively straightforward and customizable. You can easily modify aspects like animation speed, FPS, screen dimensions, and more.

Wishing you successful radio streams and many listeners!

**[ACTUAL DEMO](https://www.youtube.com/@ukrainiandoomer/streams)**

**Technologies used include:**
- FFT analyzer for Animation Frames (FFT is used to analyze audio, extracting frequency data to generate synchronized, visually appealing animation frames)
- YouTube Streaming with FFMPEG by RTMP protocol (FFMPEG and the RTMP protocol enable real-time video streaming to YouTube)

About the FFT analyzer used here for generating beautiful video frames, and for further details on its customization and enhancement, please refer to my repository specifically focused on the FFT analyzer: [Magic-FFT-audio-visualizer-py](https://github.com/nordost8/Magic-FFT-audio-visualizer-py).

[![Telegram](https://img.icons8.com/color/48/000000/telegram-app.png)](https://t.me/nordost8)
