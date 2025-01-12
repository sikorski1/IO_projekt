# How to install dependencies


## for macos:
`brew install python-tk`

## for windows:

download from this site 7zip https://www.gyan.dev/ffmpeg/builds/
`git-full`

and move ffmpeg.exe into .venv/Scripts/

 0 Microsoft Sound Mapper - Input, MME (2 in, 0 out) -> we should use 2 in input for mme

## for linux:

sudo apt install ffmpeg
sudo apt install gnome-screenshot

## for everyone: 

`uv pip install -r requirements.txt`

`install ffmpeg as a binary to use from terminal`

# Get input devices

``

what input device should i set there:

`with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback, device=4):` in order to get system audio?



# How to setup loopbacks in order to get audio

## Macos

In order to get a system volume from macos we need to install blackhole https://github.com/ExistentialAudio/BlackHole

Audio midi devices -> choose blackhole 2ch -> use this for sound output

`brew install blackhole-2ch`

https://github.com/ExistentialAudio/BlackHole/wiki/Multi-Output-Device
## Linux

todo

## Windows

Todo



# In order to setup correct video recorder go with `ffmpeg`