import yt_dlp
import os
from pathlib import Path
import re
from internal.FFmpegSetup import FFmpegSetup


class YoutubeDownloader:
    def __init__(self, output_dir="downloads"):
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
        
        script_dir = Path(__file__).parent # edusaig-ai\internal
        ffmpeg_setup = FFmpegSetup()
        setup_location = ffmpeg_setup.setup_ffmpeg(script_dir) 
        self.ffmpeg_location = os.path.join(setup_location, r'bin\ffmpeg.exe')
        self.ffprobe_location = os.path.join(setup_location, r'bin\ffprobe.exe')

        self.default_options = {
            'verbose': True,
            'ignoreerrors': True,
            'no_warnings': False,
            'quiet': False,
            'progress_hooks': [self._progress_hook],
            'ffmpeg_location': self.ffmpeg_location if hasattr(self, 'ffmpeg_location') else None,
            'ffprobe_location': self.ffprobe_location if hasattr(self, 'ffprobe_location') else None
        }
        
        # Format-specific options
        self.format_options = {
            'mp3': {
                'format': 'bestaudio/best',
                'extract_audio': True,
                'audio_format': 'mp3',
                'audio_quality': '192K',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'keepvideo': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            },
            'mp4': {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }
        }

    def _sanitize_filename(self, filename):
        """
        Sanitize filename by removing/replacing invalid characters
        """
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        # Remove any other invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        return filename

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percentage = d.get('_percent_str', '?.?%')
                speed = d.get('_speed_str', '?.? KiB/s')
                print(f"\rDownloading: {percentage} at {speed}", end='')
            except Exception:
                print(f"\rDownloading...", end='') 
        elif d['status'] == 'finished':
            print(f"\nDownload completed: {d['filename']}")
            print("Converting...")

    def _find_downloaded_file(self, base_path, format_type):
        """
        Find the downloaded file in the output directory
        """
        directory = os.path.dirname(base_path)
        filename = os.path.basename(base_path)
        
        # List all files in the directory
        if os.path.exists(directory):
            files = os.listdir(directory)
            # Try to find the exact file
            if filename in files:
                return os.path.join(directory, filename)
                
            # Try to find a file with the same name but different extension
            base_name = os.path.splitext(filename)[0]
            for file in files:
                if file.startswith(base_name) and file.lower().endswith(f".{format_type}"):
                    return os.path.join(directory, file)
        
        return None

    def download(self, url, format_type='mp3', quality='best'):
        """
        Download media with specified format (mp3 or mp4)
        
        Args:
            url (str): URL of the video to download
            format_type (str): 'mp3' or 'mp4'
            quality (str): 'best', 'medium', or 'worst' for video quality
        """
        if format_type not in ['mp3', 'mp4']:
            raise ValueError("Format must be either 'mp3' or 'mp4'")

        # Get base options for the specified format
        ydl_opts = self.default_options.copy()
        ydl_opts.update(self.format_options[format_type])

        # Adjust video quality if mp4 is selected
        if format_type == 'mp4':
            if quality == 'worst':
                ydl_opts['format'] = 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]/worst'
            elif quality == 'medium':
                ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                print("Fetching video information...")
                info = ydl.extract_info(url, download=False)
                
                if info:
                    # Sanitize the title
                    sanitized_title = self._sanitize_filename(info.get('title', 'download'))
                    print(f"Title: {info.get('title')}")
                    print(f"Sanitized title: {sanitized_title}")
                    print(f"Duration: {info.get('duration')} seconds")
                    
                    # Update output template with sanitized title
                    ydl_opts['outtmpl'] = os.path.join(self.output_dir, f"{sanitized_title}.%(ext)s")
                    
                    # Proceed with download
                    print("Starting download...")
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
                        result = ydl_download.download([url])
                    
                    # Try to find the downloaded file
                    expected_path = os.path.join(self.output_dir, f"{sanitized_title}.{format_type}")
                    downloaded_file = self._find_downloaded_file(expected_path, format_type)
                    
                    if downloaded_file and os.path.exists(downloaded_file):
                        file_size = os.path.getsize(downloaded_file) / (1024 * 1024)  # Convert to MB
                        print(f"\nSuccessfully saved as: {downloaded_file}")
                        print(f"File size: {file_size:.2f} MB")
                        print(f"Full path: {os.path.abspath(downloaded_file)}")
                        
                        return downloaded_file  # Return the file path of the saved .mp3 or .mp4
                    else:
                        print(f"\nWarning: Could not locate the downloaded file!")
                        print(f"Expected path: {expected_path}")
                    
                    return None
                    
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
            return None

"""
def main():
    downloader = YoutubeDownloader(output_dir="downloads")
    url = "https://www.youtube.com/watch?v=pTB0EiLXUC8"
    saved_file_path = downloader.download(url, format_type="mp3", quality="best")
    
    if saved_file_path:
        print(f"Downloaded and saved file at: {saved_file_path}")
    else:
        print("Download failed.")

if __name__ == "__main__":
    main()
"""