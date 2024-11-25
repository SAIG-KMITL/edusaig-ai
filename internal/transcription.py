import requests
import librosa
import numpy as np
import os
import soundfile as sf
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()
# Hugging Face API details
API_URL = os.getenv("HUGGING_FACE_ASR_MODEL") # "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
API_KEY = os.getenv("HUGGING_FACE_API_KEY")  # Replace with your actual API key

headers = {"Authorization": f"Bearer {API_KEY}"}

def preprocess_audio(audio_path):
    """
    Load and preprocess the audio file using Librosa.
    """
    # Load audio with librosa
    waveform, sample_rate = librosa.load(audio_path, sr=None)

    # Resample if needed
    if sample_rate != 16000:
        waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=16000)
    # Convert to mono if stereo
    if waveform.ndim == 2:  # Stereo audio
        waveform = np.mean(waveform, axis=0)

    return waveform  # Ensure this is a 1D NumPy array

def split_audio(waveform, chunk_length_seconds=20, overlap_seconds=1):
    """
    Split audio into overlapping chunks.
    """
    # Convert chunk sizes to samples
    chunk_length_samples = chunk_length_seconds * 16000
    overlap_samples = overlap_seconds * 16000

    # Ensure waveform is a NumPy array
    if isinstance(waveform, np.ndarray):
        waveform = waveform  # Already a NumPy array
    else:
        raise ValueError("Waveform must be a NumPy array.")

    # Split the waveform into overlapping chunks
    chunks = []
    for start_sample in range(0, len(waveform), chunk_length_samples - overlap_samples):
        end_sample = min(start_sample + chunk_length_samples, len(waveform))
        chunks.append(waveform[start_sample:end_sample])

    return chunks


def transcribe_chunk(chunk, language='en', filename="downloads/temp_chunk.mp3"):
    """
    Transcribe a single audio chunk by saving it to a file and sending it to the Hugging Face API.
    
    Args:
        chunk: Audio chunk (numpy array or tensor)
        filename: Path to save temporary MP3 file
        
    Returns:
        str: Transcribed text from the audio chunk
    """
    

    if not isinstance(chunk, np.ndarray):
        chunk_np = chunk.squeeze().numpy()
    else:
        chunk_np = chunk

    # Save the chunk as a temporary WAV file first
    temp_wav = filename.replace('.mp3', '.wav')
    sf.write(temp_wav, chunk_np, samplerate=16000)

    with open(temp_wav, "rb") as f:
        data = f.read()
    
    params = {"language": language} #en or th
    response = requests.post(API_URL, headers=headers, data=data, params=params)
    response.raise_for_status()
    result = response.json()
      
    return result.get("text", "")

def transcribe_audio(audio_path, language='en'):
    """
    Transcribe an audio file using Hugging Face Whisper API.
    """
    # Preprocess the audio
    print("Start preprocess_audio")
    waveform = preprocess_audio(audio_path)
    print("Finish preprocess_audio")

    # Split audio into chunks
    print("start split_audio")
    audio_chunks = split_audio(waveform)
    print("Finish split_audio")

    # Transcribe each chunk and combine results
    transcriptions = []
    for i, chunk in enumerate(audio_chunks):
        print(f"Processing chunk {i + 1}/{len(audio_chunks)}...")
        transcription = transcribe_chunk(chunk, language=language)
        print("Result: ", transcription)
        transcriptions.append(transcription)

    # Combine all transcriptions into one
    return " ".join(transcriptions)
