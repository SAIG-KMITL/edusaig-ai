from fastapi import APIRouter, HTTPException
from utils.response import success_response_status, error_response_status
from internal.YoutubeDownloader import YoutubeDownloader  
from internal.transcription import transcribe_audio
from models.asr import ASRRequest
from internal.VideoProcessor import VideoProcessor
import traceback

router = APIRouter()

@router.post("/asr")
async def asr_youtube(body: ASRRequest):
    """
    Endpoint to download audio from YouTube, transcribe it, and return the transcription.
    """
    try:
        # Initialize the senior downloader
        downloader = YoutubeDownloader(output_dir="downloads")
        
        # Download audio as MP3
        result = downloader.download(body.url, format_type="mp3")
        
        #result = "/Users/mattew/Desktop/saig_work/edusaig-ai/downloads/How_Elon_Musk_Became_Trump's_Super_Fan.mp3"
        
        if result:
            file_path = result
            
            # Call the transcription logic
            transcription = transcribe_audio(file_path, language=body.language)
            
            return success_response_status(200, {
                "file_path": file_path,
                "transcription": transcription,
            })
        else:
            # Handle download errors
            
            return error_response_status(500, result.get("message", "Unknown error occurred during download."))
    except Exception as e:
        traceback.print_exc()
        return error_response_status(500, f"Error: {str(e)}")
    

@router.post("/asr-public")
async def asr_public(body: ASRRequest):
    """
    Endpoint to download audio from YouTube, transcribe it, and return the transcription.
    """
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