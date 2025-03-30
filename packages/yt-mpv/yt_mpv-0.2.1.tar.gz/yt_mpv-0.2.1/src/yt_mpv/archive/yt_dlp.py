"""
Video downloading functionality using yt-dlp
"""

import logging
import subprocess
from pathlib import Path

from yt_mpv.archive.archive_org import is_archived, upload
from yt_mpv.utils.cache import remove
from yt_mpv.utils.notify import notify

# Configure logging
logger = logging.getLogger("yt-mpv")


def get_filenames(url: str, dl_dir: Path, venv_bin: Path) -> tuple[Path, Path]:
    """Get filenames yt-dlp would use for a URL."""
    dl_dir.mkdir(parents=True, exist_ok=True)
    output_pattern = f"{dl_dir}/yt-mpv-%(id)s.%(ext)s"

    result = subprocess.run(
        [
            str(venv_bin / "yt-dlp"),
            "--print",
            "filename",
            "-o",
            output_pattern,
            "--skip-download",
            url,
        ],
        text=True,
        capture_output=True,
        check=True,
    )

    video_file = Path(result.stdout.strip())
    info_file = video_file.with_suffix(".info.json")

    return video_file, info_file


def download(url: str, dl_dir: Path, venv_bin: Path) -> tuple[Path, Path] | None:
    """Download video using yt-dlp and return paths to video and info files."""
    dl_dir.mkdir(parents=True, exist_ok=True)

    # Simple output pattern based on video ID
    output_pattern = f"{dl_dir}/yt-mpv-%(id)s.%(ext)s"

    # Basic yt-dlp command with minimal arguments
    cmd = [
        str(venv_bin / "yt-dlp"),
        "--write-info-json",
        "-o",
        output_pattern,
        url,
    ]

    try:
        # Run yt-dlp
        logger.info(f"Downloading video: {url}")
        subprocess.run(cmd, check=True)

        # Find the downloaded files
        for video_file in dl_dir.glob("yt-mpv-*"):
            if not video_file.name.endswith(".info.json"):
                info_file = video_file.with_suffix(".info.json")
                if info_file.exists():
                    logger.info(f"Downloaded successfully: {video_file.name}")
                    return video_file, info_file

        # If we got here, no valid files were found
        logger.error("Download completed but files not found")
        notify("Download failed - files not found")
        return None

    except subprocess.CalledProcessError as e:
        logger.error(f"Download failed: {e}")
        notify("Download failed")
        return None


def update(venv_dir: Path, venv_bin: Path) -> bool:
    """Update yt-dlp."""
    try:
        logger.info("Updating yt-dlp")
        subprocess.run(
            [str(venv_bin / "pip"), "install", "--upgrade", "yt-dlp"], check=True
        )
        return True
    except subprocess.CalledProcessError:
        logger.warning("Failed to update yt-dlp")
        return False


def archive_url(url: str, dl_dir: Path, venv_bin: Path) -> bool:
    """Archive a URL to archive.org."""
    # First check if already archived
    archive_url_path = is_archived(url)
    if archive_url_path:
        logger.info(f"URL already archived: {archive_url_path}")
        notify(f"Already archived: {archive_url_path}")
        return True

    try:
        # Download the video
        logger.info("Downloading video for archiving")
        result = download(url, dl_dir, venv_bin)
        if not result:
            return False

        video_file, info_file = result

        # Upload to Archive.org
        success = upload(video_file, info_file, url)

        # Clean up files if upload was successful
        if success:
            if remove(video_file, info_file):
                logger.info("Cache files cleaned up successfully")
            else:
                logger.warning("Failed to clean up some cache files")

        return success

    except Exception as e:
        logger.error(f"Error archiving URL: {e}")
        notify(f"Archive failed: {str(e)}")
        return False
