"""
Summarizer module for the Office Assistant prototype.

This module wraps the OpenAI ChatCompletion API to provide a simple
summarization function. Given a block of text, it produces a short
summary describing the key points. To use this module, an
OpenAI API key must be available via the OPENAI_API_KEY environment
variable. See https://beta.openai.com/ for more information and to
generate API keys.
"""

from __future__ import annotations

import os
from typing import Optional
import openai


def summarize_text(text: str, max_tokens: int = 150, model: str = "gpt-3.5-turbo") -> str:
    """
    Summarize the given text using OpenAI's chat completion API.

    Parameters
    ----------
    text: str
        The input text to summarize.
    max_tokens: int, optional
        Maximum number of tokens to include in the summary output. Defaults to 150.
    model: str, optional
        The chat model to use. Defaults to "gpt-3.5-turbo".

    Returns
    -------
    str
        The summary text.

    Raises
    ------
    RuntimeError
        If the OPENAI_API_KEY environment variable is not set.
    """
    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set. Please set it to your OpenAI API key.")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": text},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    # Extract the content of the assistant's reply
    return response["choices"][0]["message"]["content"].strip()