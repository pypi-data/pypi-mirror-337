---
hide:
  - toc
---
# Acoustic Signal Measurement Utilities

The **asmu** Python package enables multichannel real-time audio playback, processing and recording. It is implemented in pure Python with a few additional packages:

- [numpy](https://pypi.org/project/numpy/) - Is the fundamental package for scientific computing, array manipulation and signal processing.
- [sounddevice](https://pypi.org/project/sounddevice/) - Is a Python wrapper for the [PortAudio](https://www.portaudio.com/) functions. It is used for the communication with the soundcard or audio interface.
- [soundfile](https://pypi.org/project/soundfile/) - Is an audio library to read and write sound files through [libsndfile](http://www.mega-nerd.com/libsndfile/).

!!! warning
    This software is still under development. This means:

    - No input checking, which can cause exceptions that are complicated to debug
    - The structure of the package can change drastically
    - No entitlement to backwards compatibility
    - The documentation is still in development and not complete

The main focus of **asmu** is modularity and easy expandability. It provides a few base classes, to implement nearly every "audio processor". Additionally, **asmu** offer some pre implemented audio processors, that can be used right away.
