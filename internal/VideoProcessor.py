import requests
# from moviepy.editor import VideoFileClip
from internal.FFmpegSetup import FFmpegSetup
from pathlib import Path
import os

class VideoProcessor:
    """
    A class for downloading MP4 videos and extracting audio as MP3 files.
    """
    def __init__(self, output_dir="downloads"):
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
        
        script_dir = Path(__file__).parent # edusaig-ai\internal
        ffmpeg_setup = FFmpegSetup()
        setup_location = ffmpeg_setup.setup_ffmpeg(script_dir) 
        self.ffmpeg_location = os.path.join(setup_location, r'bin/ffmpeg.exe')
        self.ffprobe_location = os.path.join(setup_location, r'bin/ffprobe.exe')

    def get_mp4_save_path(self, video_name):
        """
        Generate the full path to save the MP4 file.
        
        Args:
            video_name (str): The name of the video file.

        Returns:
            Path: Full path where the MP4 file will be saved.
        """
        return self.output_dir + f"/{video_name}.mp4"
    
    def get_mp3_save_path(self, video_name):
        """
        Generate the full path to save the MP3 file.
        
        Args:
            video_name (str): The name of the video file.

        Returns:
            Path: Full path where the MP3 file will be saved.
        """
        return self.output_dir + f"/{video_name}.mp3"

    def download_mp4(self, url, video_name):
        """
        Downloads an MP4 file from a URL and saves it locally in the output directory.

        Args:
            url (str): The URL of the .mp4 file.
            video_name (str): The name of the video (used for the filename).

        Returns:
            tuple: (status, message, file_path)
                status (bool): True if successful, False otherwise.
                message (str): Description of the result.
                file_path (Path): The path where the file was saved.
        """
        mp4_path = self.get_mp4_save_path(video_name)  # Get the save path
        
        try:
            # Send a GET request to the URL
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Check for HTTP errors
            
            # Save the content to the specified path
            with open(mp4_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                    file.write(chunk)
            
            return True, f"MP4 file successfully downloaded to {mp4_path}.", mp4_path
        except requests.exceptions.RequestException as e:
            return False, f"Failed to download the MP4 file: {e}", None

    def extract_mp3_from_mp4(self, mp4_path, video_name):
        """
        Extracts audio from an MP4 video file and saves it as an MP3 file.

        Args:
            mp4_path (str): Path to the input MP4 video file.
            video_name (str): The name of the video (used for the MP3 filename).

        Returns:
            tuple: (status, message, audio_file_path)
                status (bool): True if successful, False otherwise.
                message (str): Description of the result.
                audio_file_path (Path): The path where the audio file was saved.
        """
        mp3_path = self.get_mp3_save_path(video_name)  # Get the save path for MP3
        
        try:
            # # Load the video file
            # video = VideoFileClip(mp4_path)
            
            # # Extract the audio and save it as an MP3
            # video.audio.write_audiofile(mp3_path)

            import subprocess

            # Full path to ffmpeg executable
            # ffmpeg_path = r'C:\path\to\ffmpeg\bin\ffmpeg.exe'  # Change this to the correct path

            # Run ffmpeg command using subprocess
            subprocess.call([self.ffmpeg_location, '-i', mp4_path, '-vn', mp3_path])
            return True, f"Audio successfully extracted to {mp3_path}.", mp3_path
        except Exception as e:
            return False, f"Failed to extract MP3: {e}", None

    def download_and_extract_audio(self, url, video_name):
        """
        Downloads an MP4 file and extracts the audio as MP3 in one step.

        Args:
            url (str): The URL of the MP4 file.
            video_name (str): The name of the video (used for the filename).

        Returns:
            tuple: (status, message, audio_file_path)
                status (bool): True if successful, False otherwise.
                message (str): Description of the result.
                audio_file_path (Path): The path where the audio file was saved.
        """
        # Download the MP4 file
        status, message, mp4_path = self.download_mp4(url, video_name)
        if not status:
            return status, message, None  # Return if download fails
        
        # Extract the audio to MP3
        return self.extract_mp3_from_mp4(mp4_path, video_name)

"""
def main():
    processor = VideoProcessor()

    url = "http://example.com/video.mp4" 
    video_name = "video"  # The base name for the video file (without extension)
    
    # Download MP4 and extract audio as MP3
    status, message, audio_file_path = processor.download_and_extract_audio(url, video_name)
    print(message)
    if status:
        print(f"Audio file saved at: {audio_file_path}")
        
if __name__ == "__main__":
    main()
"""