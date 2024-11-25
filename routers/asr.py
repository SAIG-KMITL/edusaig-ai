from fastapi import APIRouter, HTTPException
from utils.response import success_response_status, error_response_status
from internal.transcription import transcribe_audio
from models.asr import ASRRequest
from internal.VideoProcessor import VideoProcessor
import traceback

router = APIRouter()

@router.post("/asr")
async def asr(body: ASRRequest):
    try:
        processor = VideoProcessor()

        video_name = "video"  # The base name for the video file (without extension)
        print("Start download and extract ...")
        status, message, audio_file_path = processor.download_and_extract_audio(body.url, video_name)

        print("Result after load and extract:", status, message, audio_file_path)
        if audio_file_path:
            file_path = audio_file_path
            
            # Call the transcription logic
            transcription = transcribe_audio(file_path, language=body.language)
            
            return success_response_status(200, {
                "file_path": file_path,
                "transcription": transcription,
            })
        else:
            # Handle download errors
            
            return error_response_status(500, "Unknown error occurred during download.")
    except Exception as e:
        traceback.print_exc()
        return error_response_status(500, f"Error: {str(e)}")