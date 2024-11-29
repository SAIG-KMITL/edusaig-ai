import requests
import librosa
import numpy as np
import os
import soundfile as sf
from pathlib import Path
import tempfile
from dotenv import load_dotenv
import multiprocessing
from functools import partial

load_dotenv()
# Hugging Face API details
API_URL = os.getenv("HUGGING_FACE_ASR_MODEL")
API_KEY = os.getenv("HUGGING_FACE_API_KEY")

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

    return waveform

def split_audio(waveform, chunk_length_seconds=25, overlap_seconds=1):
    """
    Split audio into overlapping chunks.
    """
    # Convert chunk sizes to samples
    chunk_length_samples = chunk_length_seconds * 16000
    overlap_samples = overlap_seconds * 16000

    # Ensure waveform is a NumPy array
    if not isinstance(waveform, np.ndarray):
        raise ValueError("Waveform must be a NumPy array.")

    # Split the waveform into overlapping chunks
    chunks = []
    for start_sample in range(0, len(waveform), chunk_length_samples - overlap_samples):
        end_sample = min(start_sample + chunk_length_samples, len(waveform))
        chunks.append(waveform[start_sample:end_sample])

    return chunks

def transcribe_chunk(chunk, language='en'):
    """
    Transcribe a single audio chunk by saving it to a temporary file and sending it to the Hugging Face API.
    """
    # Ensure chunk is a numpy array
    if not isinstance(chunk, np.ndarray):
        chunk_np = chunk.squeeze().numpy()
    else:
        chunk_np = chunk

    # Specify the custom temporary directory
    custom_temp_dir = "downloads/"
    os.makedirs(custom_temp_dir, exist_ok=True)

    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", dir=custom_temp_dir, delete=False) as temp_wav:
        temp_wav_name = temp_wav.name
        sf.write(temp_wav_name, chunk_np, samplerate=16000)

    try:
        # Read the temporary file and send to API
        with open(temp_wav_name, "rb") as f:
            data = f.read()

        params = {"language": language} # 'en' or 'th'
        response = requests.post(API_URL, headers=headers, data=data, params=params)
        response.raise_for_status()
        result = response.json()

        return result.get("text", "")
    finally:
        # Clean up the temporary file
        os.remove(temp_wav_name)

def transcribe_audio_multiprocess(audio_path, language='en', max_workers=4):
    """
    Transcribe an audio file using Hugging Face Whisper API with multiprocessing.
    
    Args:
        audio_path (str): Path to the audio file
        language (str, optional): Language of the audio. Defaults to 'en'.
        max_workers (int, optional): Maximum number of worker processes. 
                                     Defaults to None (uses number of CPU cores).
    
    Returns:
        str: Full transcription of the audio
    """
    # Preprocess the audio
    print("Start preprocess_audio")
    waveform = preprocess_audio(audio_path)
    print("Finish preprocess_audio")

    # Split audio into chunks
    print("Start split_audio")
    audio_chunks = split_audio(waveform)
    print("Finish split_audio")

    # If max_workers not specified, use number of CPU cores
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()

    # Create a partial function with fixed language
    transcribe_chunk_partial = partial(transcribe_chunk, language=language)

    # Use multiprocessing to transcribe chunks
    print(f"Transcribing with {max_workers} workers...")
    with multiprocessing.Pool(processes=max_workers) as pool:
        # Map the transcription function to all chunks
        transcriptions = pool.map(transcribe_chunk_partial, audio_chunks)

    # Combine all transcriptions
    full_transcription = " ".join(filter(bool, transcriptions))
    return full_transcription

def transcribe_audio(audio_path, language='en'):
    """
    Transcribe an audio file using Hugging Face Whisper API.
    """
    # Preprocess the audio
    print("Start preprocess_audio")
    waveform = preprocess_audio(audio_path)
    print("Finish preprocess_audio")

    # Split audio into chunks
    print("Start split_audio")
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
