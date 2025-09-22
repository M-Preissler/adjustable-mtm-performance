"""
Transcriber module for the Office Assistant prototype.

This module wraps OpenAI's Whisper model to provide a simple
function that accepts an audio file and returns a transcript.
The default model size is "base" which is suitable for short
recordings and testing. Larger models (e.g. small, medium) can
be selected by passing a different model_name when calling
`transcribe`. The whisper package must be installed, and
FFmpeg must be available on the system for audio decoding.
"""

from __future__ import annotations

import whisper

def transcribe(audio_path: str, model_name: str = "base") -> str:
    """
    Transcribe an audio file using OpenAI's Whisper model.

    Parameters
    ----------
    audio_path: str
        Path to the audio file (WAV, MP3, etc.)
    model_name: str, optional
        Name of the Whisper model to load. Defaults to "base".

    Returns
    -------
    str
        The transcribed text from the audio.
    """
    # Load the model. Larger models yield higher accuracy at the cost of more CPU/GPU usage.
    model = whisper.load_model(model_name)
    # transcribe returns a dict with various fields including 'text'
    result = model.transcribe(audio_path)
    return result.get("text", "")