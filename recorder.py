"""
Recorder module for the Office Assistant prototype.

This module provides functions to record the user's screen and microphone
simultaneously. The recordings are saved to disk as separate audio and
video files. Screen capture is performed via PyAutoGUI and OpenCV,
while audio capture relies on the sounddevice library. Recording
functions can be composed using threads to run concurrently.

The functions exposed here are simple wrappers with reasonable
defaults. They can be imported and called from a larger application
without modification.
"""

from __future__ import annotations

import cv2
import numpy as np
import pyautogui
import sounddevice as sd
import wave
import threading
from typing import Tuple


def record_audio(filename: str, duration: int, fs: int = 44100, channels: int = 2) -> None:
    """
    Record audio from the default microphone and write it to a WAV file.

    Parameters
    ----------
    filename: str
        Output WAV file path.
    duration: int
        Duration to record in seconds.
    fs: int, optional
        Sampling frequency in Hz. Defaults to 44.1 kHz which is
        a typical CD-quality sample rate.
    channels: int, optional
        Number of audio channels. Defaults to 2 for stereo recording.
    """
    print(f"Recording audio to {filename} for {duration} seconds ...")
    # Record audio using sounddevice; returns a NumPy array
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='int16')
    sd.wait()
    # Write the recording to a WAV file using the wave module
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio uses 2 bytes per sample
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    print(f"Audio saved: {filename}")


def record_screen(filename: str, duration: int, fps: int = 20) -> None:
    """
    Record a video of the entire screen and save to an AVI file.

    Parameters
    ----------
    filename: str
        Output AVI file path.
    duration: int
        Duration to record in seconds.
    fps: int, optional
        Frames per second for the capture. Defaults to 20.
    """
    screen_size = pyautogui.size()
    # Define the codec and create the VideoWriter object. XVID is widely supported.
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, fps, screen_size)
    print(f"Recording screen to {filename} for {duration} seconds ...")
    for _ in range(int(duration * fps)):
        # Take a screenshot and convert the PIL image to a NumPy array
        img = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        out.write(frame)
    out.release()
    print(f"Screen recording saved: {filename}")


def record_audio_and_screen(audio_file: str, video_file: str, duration: int) -> Tuple[str, str]:
    """
    Record both audio and screen concurrently.

    Parameters
    ----------
    audio_file: str
        Filename for the audio recording (WAV).
    video_file: str
        Filename for the screen recording (AVI).
    duration: int
        Duration to record in seconds.

    Returns
    -------
    Tuple[str, str]
        A tuple of the audio and video file names once recording completes.
    """
    audio_thread = threading.Thread(target=record_audio, args=(audio_file, duration))
    video_thread = threading.Thread(target=record_screen, args=(video_file, duration))
    audio_thread.start()
    video_thread.start()
    audio_thread.join()
    video_thread.join()
    return audio_file, video_file