import requests
import torchaudio
import torch

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
API_KEY = "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"  # Replace with your actual API key

headers = {"Authorization": f"Bearer {API_KEY}"}

def preprocess_audio(audio_path):
    """
    Load and preprocess the audio file.
    """
    waveform, sample_rate = torchaudio.load(audio_path)

    # Resample to 16000 Hz if necessary
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)

    # Mix down to mono if stereo
    if waveform.shape[0] == 2:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    return waveform

def split_audio(waveform, chunk_length_seconds=30, overlap_seconds=1):
    """
    Split audio into overlapping chunks.
    """
    chunk_length_samples = chunk_length_seconds * 16000
    overlap_samples = overlap_seconds * 16000
    chunks = []

    for start_sample in range(0, waveform.size(1), chunk_length_samples - overlap_samples):
        end_sample = min(start_sample + chunk_length_samples, waveform.size(1))
        chunks.append(waveform[:, start_sample:end_sample])

    return chunks

def transcribe_chunk(chunk):
    """
    Transcribe a single audio chunk using the Hugging Face API.
    """
    chunk_np = chunk.squeeze().numpy()
    payload = {
        "inputs": chunk_np.tolist(),
        "parameters": {"sampling_rate": 16000}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return result.get("text", "")

def transcribe_audio(audio_path):
    """
    Transcribe an audio file using Hugging Face Whisper API.
    """
    # Preprocess the audio
    waveform = preprocess_audio(audio_path)

    # Split audio into chunks
    audio_chunks = split_audio(waveform)

    # Transcribe each chunk and combine results
    transcriptions = []
    for i, chunk in enumerate(audio_chunks):
        print(f"Processing chunk {i + 1}/{len(audio_chunks)}...")
        transcription = transcribe_chunk(chunk)
        transcriptions.append(transcription)

    # Combine all transcriptions into one
    return " ".join(transcriptions)
