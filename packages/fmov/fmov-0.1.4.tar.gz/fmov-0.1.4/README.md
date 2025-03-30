# fmov

![fmov logo](https://github.com/dylandibeneditto/fmov/blob/main/logo.png)

A performant way to create rendered video with Python by leveraging `ffmpeg` and `PIL`.

# Rough Benchmarks

time efficiency = video time / render time
| FPS | Resolution | Video Time | Render Time | Video Time / Render Time |
| --- | ---------- | ---------- | ----------- | --------------- |
| 1 | 1920x1080 | 30s | 0.381s | 78.74x |
| 12 | 1920x1080 | 30s | 1.995s | 15.00x |
| 24 | 1920x1080 | 30s | 3.751s | 8.00x |
| 30 | 1920x1080 | 30s | 4.541s | 6.60x |
| 60 | 1920x1080 | 30s | 8.990s | 3.34x |
| 100 | 1920x1080 | 30s | 14.492s | 2.07x |
| 120 | 1920x1080 | 30s | 17.960s | 1.67x |

---

Rendered on a M3 MacBook Air using the [Hello World]() example

# Installing

Install fmov via pip:

```
pip install fmov
```

## Dependencies

Make sure to have ffmpeg installed on your system and executable from the terminal

```
sudo apt install ffmpeg     # Linux
brew install ffmpeg         # MacOS
choco install ffmpeg        # Windows
```

[Downloading FFmpeg](https://ffmpeg.org/download.html)

Install PIL, as that is what you will need to pass frames to fmov

```
pip install pillow
```

# Tutorial

Creating the `Video` object:

```python
from fmov import Video

video = Video(
    dimensions=(1920,1080),
    framerate=30,
    path="./video.mp4"
)

```

Creating frames:

```python
# some code to make a 30 second video displaying the index of each frame

for i in range(video.seconds_to_frame(30)):
    img = Image.new("RGB", (video.width, video.height), "#000000")
    draw = ImageDraw.Draw(img)

    #          x    y                 content of the text                     color
    draw.text((100, video.height//2), f"Hello world! This is frame {str(i)}", fill="#ffffff")

    video.pipe(img)
```

Adding SFX:

```python
video.sound_at_frame(frame=10, path="./audio.mp3", volume=0.5)

video.sound_at_millisecond(time=4000, path="./audio.wav", volume=1.0)

video.sound_at_second(time=25, path="./audio.m4a")
```

Rendering Video:

```python
# will output in the specified path
# all relative paths will start from where you run the code
video.render()
```

> [!NOTE]
> Anytime the program has to delete the temporary file, fmov will prompt the user unless `prompt_deletion` is disabled as an argument in the `video.render` method.
