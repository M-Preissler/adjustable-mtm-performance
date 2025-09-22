"""
Entry point for the Office Assistant prototype.

This script orchestrates the recording of audio and screen, transcribes
the audio, generates a summary of the transcript, and logs window
activity. It saves the raw transcript, the summary, and the window
activity log to disk using a user-provided prefix. Use the --duration
option to control how long the recording and tracking run.
"""

from __future__ import annotations

import argparse
import json
from typing import Tuple

from recorder import record_audio_and_screen
from transcriber import transcribe
from summarizer import summarize_text
from tracker import track_activity



def run_session(duration: int, prefix: str) -> Tuple[str, str, str, str]:
    """
    Run a complete recording/transcription/summarization/tracking session.

    Parameters
    ----------
    duration: int
        Duration in seconds for recording and tracking.
    prefix: str
        Prefix for all output files (audio, video, transcript, summary, activity).

    Returns
    -------
    Tuple[str, str, str, str]
        Paths to the audio file, video file, transcript, and summary files.
    """
    audio_file = f"{prefix}_audio.wav"
    video_file = f"{prefix}_screen.avi"
    transcript_file = f"{prefix}_transcript.txt"
    summary_file = f"{prefix}_summary.txt"
    activity_file = f"{prefix}_activity.json"

    # Record audio and screen concurrently
    record_audio_and_screen(audio_file, video_file, duration)

    # Transcribe the audio
    transcript = transcribe(audio_file)
    with open(transcript_file, "w", encoding="utf-8") as tf:
        tf.write(transcript)

    # Summarize the transcript
    summary = summarize_text(transcript)
    with open(summary_file, "w", encoding="utf-8") as sf:
        sf.write(summary)

    # Track window activity during the recording period
    activity = track_activity(duration)
    with open(activity_file, "w", encoding="utf-8") as af:
        json.dump(activity, af, indent=2)

    print(f"Session complete.\nAudio: {audio_file}\nVideo: {video_file}\nTranscript: {transcript_file}\nSummary: {summary_file}\nActivity log: {activity_file}")
    return audio_file, video_file, transcript_file, summary_file



def main() -> None:
    parser = argparse.ArgumentParser(description="Office Assistant prototype: record, transcribe, summarize, and log activity.")
    parser.add_argument("--duration", type=int, default=60, help="Duration in seconds to record and track.")
    parser.add_argument("--prefix", type=str, default="session", help="Prefix for output files.")
    args = parser.parse_args()
    run_session(args.duration, args.prefix)


if __name__ == "__main__":
    main()
