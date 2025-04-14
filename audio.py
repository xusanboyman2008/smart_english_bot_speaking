# Install the assemblyai package by executing the command `pip3 install assemblyai` (macOS) or `pip install assemblyai` (Windows).
import os

# Import the AssemblyAI module
import assemblyai as aai

from ai import get_scores


def transcript_audio(file_name):
    # Your API token is already set here
    aai.settings.api_key = "1b4cc8f059484b96951a22d66b563845"

    # Create a transcriber object.
    transcriber = aai.Transcriber()

    # If you have a local audio file, you can transcribe it using the code below.
    # Make sure to replace the filename with the path to your local audio file.
    transcript = transcriber.transcribe(f"{file_name}")

    # Alternatively, if you have a URL to an audio file, you can transcribe it with the following code.
    # Uncomment the line below and replace the URL with the link to your audio file.
    # transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/espn-bears.m4a")

    # After the transcription is complete, the text is printed out to the console.
    print(transcript.text)
    text = get_scores(transcript.text)
    os.remove(file_name)
    return text