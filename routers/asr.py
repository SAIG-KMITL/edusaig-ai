from fastapi import APIRouter, HTTPException
from utils.response import success_response_status, error_response_status
from internal.YoutubeDownloader import YoutubeDownloader  
from internal.transcription import transcribe_audio
import traceback

router = APIRouter()

@router.post("/asr")
async def asr_youtube(url: str):
    """
    Endpoint to download audio from YouTube, transcribe it, and return the transcription.
    """
    try:
        # Initialize the senior downloader
        downloader = YoutubeDownloader(output_dir="downloads")
        
        # Download audio as MP3
        result = downloader.download(url, format_type="mp3")
        
        #result = "/Users/mattew/Desktop/saig_work/edusaig-ai/downloads/How_Elon_Musk_Became_Trump's_Super_Fan.mp3"
        
        if result:
            file_path = result
            
            # Call the transcription logic
            transcription = transcribe_audio(file_path)
            
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