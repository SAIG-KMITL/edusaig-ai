from fastapi import APIRouter, HTTPException
from utils.response import success_response_status, error_response_status
from internal.YoutubeDownloader import YoutubeDownloader  

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
        
        if result["status"] == "success" and result.get("file_path"):
            file_path = result["file_path"]
            
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
        return error_response_status(500, f"Error: {str(e)}")
