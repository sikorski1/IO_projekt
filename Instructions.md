# How to install dependencies


## for macos:
`brew install python-tk`

## for windows:


## for linux:


## for everyone: 

`uv pip install -r requirements.txt`

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