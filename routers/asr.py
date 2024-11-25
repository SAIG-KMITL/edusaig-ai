from fastapi import APIRouter, HTTPException
from utils.response import success_response_status, error_response_status
from internal.transcription import transcribe_audio
from models.asr import ASRRequest
from internal.VideoProcessor import VideoProcessor
import os
import tempfile
import traceback

router = APIRouter()

@router.post("/asr")
async def asr(body: ASRRequest):
    try:
        processor = VideoProcessor()

        # Specify the custom temporary directory
        custom_temp_dir = "downloads/"
        os.makedirs(custom_temp_dir, exist_ok=True)

        video_name = "video"  # The base name for the video file (without extension)
        print("Start download and extract ...")

        # Use a temporary file in the custom directory
        with tempfile.NamedTemporaryFile(suffix=".mp4", dir=custom_temp_dir, delete=False) as temp_video_file:
            temp_video_path = temp_video_file.name
            temp_audio_path = temp_video_path.replace('.mp4', '.mp3')

            # Extract the audio and save it to the temporary file
            status, message, audio_file_path = processor.download_and_extract_audio(
                body.url, temp_video_path, temp_audio_path
            )

        print("Result after load and extract:", status, message, temp_audio_path)
        if status and os.path.exists(temp_audio_path):
            try:
                # Call the transcription logic
                transcription = transcribe_audio(temp_audio_path, language=body.language)

                return success_response_status(200, {
                    "transcription": transcription,
                })
            finally:
                # Ensure the temporary file is deleted after processing
                os.remove(temp_video_path)
                os.remove(temp_audio_path)
        else:
            # Handle download errors
            return error_response_status(500, "Unknown error occurred during download.")
    except Exception as e:
        traceback.print_exc()
        return error_response_status(500, f"Error: {str(e)}")
