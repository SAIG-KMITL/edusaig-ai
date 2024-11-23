import os
import sys
import requests
import zipfile
from pathlib import Path
import shutil

class FFmpegSetup:
    def __init__(self):
        self.ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        self.chunk_size = 8192

    def download_ffmpeg(self, download_path):
        """Download FFmpeg archive."""
        try:
            print("Downloading FFmpeg...")
            response = requests.get(self.ffmpeg_url, stream=True)
            response.raise_for_status()
            
            with open(download_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        file.write(chunk)
            print("Download completed.")
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False

    def extract_ffmpeg(self, zip_path, extract_to):
        """Extract FFmpeg zip archive to a static directory name."""
        try:
            print("Extracting FFmpeg...")
            temp_extract_dir = os.path.join(os.path.dirname(extract_to), "temp-ffmpeg-extract")
            
            # Ensure the temporary extraction directory is clean
            if os.path.exists(temp_extract_dir):
                shutil.rmtree(temp_extract_dir)
            
            # Extract the archive to the temporary directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_dir)
            
            # Find the extracted FFmpeg folder
            extracted_dirs = [d for d in os.listdir(temp_extract_dir) if os.path.isdir(os.path.join(temp_extract_dir, d))]
            if not extracted_dirs:
                raise Exception("FFmpeg directory not found after extraction.")
            
            # Rename and move to the target directory
            extracted_ffmpeg_dir = os.path.join(temp_extract_dir, extracted_dirs[0])
            if os.path.exists(extract_to):
                shutil.rmtree(extract_to)
            shutil.move(extracted_ffmpeg_dir, extract_to)
            
            # Clean up temporary extraction directory
            shutil.rmtree(temp_extract_dir)
            print("Extraction completed.")
            return True
        except Exception as e:
            print(f"Extraction failed: {e}")
            return False

    def setup_ffmpeg(self, base_dir):
        """Setup FFmpeg by downloading and extracting."""
        ffmpeg_dir = os.path.join(base_dir, "ffmpeg-static")
        
        # Check if FFmpeg is already set up
        if os.path.exists(ffmpeg_dir):
            print(f"FFmpeg is already set up at: {ffmpeg_dir}")
            return ffmpeg_dir
        
        os.makedirs(base_dir, exist_ok=True)
        
        zip_path = os.path.join(base_dir, "ffmpeg.zip")
        
        # Download FFmpeg if not already downloaded
        if not os.path.exists(zip_path):
            if not self.download_ffmpeg(zip_path):
                print("Failed to download FFmpeg.")
                sys.exit(1)
        
        # Extract FFmpeg
        if not self.extract_ffmpeg(zip_path, ffmpeg_dir):
            print("Failed to extract FFmpeg.")
            sys.exit(1)
        
        # Optionally remove the zip file after extraction
        os.remove(zip_path)
        print(f"FFmpeg setup completed in: {ffmpeg_dir}")
        
        return ffmpeg_dir