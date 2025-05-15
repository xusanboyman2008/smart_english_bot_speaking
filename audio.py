import os
import assemblyai as aai
from ai import get_scores

def transcript_audio(file_name):
    aai.settings.api_key = "1b4cc8f059484b96951a22d66b563845"

    config = aai.TranscriptionConfig(
        punctuate=True,
        format_text=True
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_name, config=config)

    # Format transcript with timestamps
    if transcript.utterances:
        segments = []
        for utterance in transcript.utterances:
            start_time = round(utterance.start / 1000)
            minutes = start_time // 60
            seconds = start_time % 60
            timestamp = f"[{minutes:02}:{seconds:02}]"
            segments.append(f"{utterance.text} {timestamp}")
    print(transcript.text)
    scored_text = get_scores(transcript.text)

    os.remove(file_name)

    return scored_text
