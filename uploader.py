import shutil
import logging
import asyncio
from datetime import datetime, timezone
from pathlib import Path
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from config import (
    LOCAL_DATA_DIR,
    S3_BUCKET_NAME,
    S3_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    S3_PREFIX,
    UPLOAD_DELAY_MINUTES
)

logger = logging.getLogger("MarketDataUploader")

class MarketDataUploader:
    def __init__(self, base_dir: str = LOCAL_DATA_DIR):
        self.base_dir = Path(base_dir)
        self.running = False
        self.task = None

        # Configure global AWS region environment variables so that any internal clients 
        # created by botocore (e.g. for credential refreshing) have a default region.
        import os
        if S3_REGION:
            os.environ.setdefault("AWS_DEFAULT_REGION", S3_REGION)
            os.environ.setdefault("AWS_REGION", S3_REGION)

        # Initialize boto3 Session and S3 client
        # If credentials are not specified, boto3 automatically searches local env variables, 
        # AWS shared credentials file, or IAM instance profile.
        session_kwargs = {}
        if S3_REGION:
            session_kwargs["region_name"] = S3_REGION
            
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
            session_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
            logger.info("Initializing S3 client with configured credentials.")
        else:
            logger.info("Initializing S3 client using IAM Instance Profile or system environment.")
            
        self.session = boto3.Session(**session_kwargs)
        self.s3_client = self.session.client("s3")

    async def start(self):
        """Start the background uploader task."""
        self.running = True
        self.task = asyncio.create_task(self._run_uploader_loop())
        logger.info("Market Data Uploader successfully started.")

    async def stop(self):
        """Stop the background uploader gracefully."""
        self.running = False
        if self.task:
            self.task.cancel()
        logger.info("Market Data Uploader stopped.")

    async def _run_uploader_loop(self):
        """Periodically checks if there is completed day data that needs to be zipped and uploaded."""
        while self.running:
            try:
                # Run the upload check on startup and then every hour
                await self.check_and_upload_completed_days()
            except Exception as e:
                logger.error(f"Error in uploader loop iteration: {e}")
            
            # Sleep for 1 hour before checking again
            await asyncio.sleep(3600)

    async def check_and_upload_completed_days(self):
        """Scan the local cache directory for folders representing past UTC days, zip, and upload them."""
        # Current day in UTC
        today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        
        # Scan local directory
        if not self.base_dir.exists():
            return

        for path in self.base_dir.iterdir():
            if not path.is_dir():
                continue

            dir_name = path.name
            # Check if directory is named YYYYMMDD (length 8 and is numeric)
            if len(dir_name) == 8 and dir_name.isdigit():
                # If directory represents a completed day (older than today)
                if dir_name < today_str:
                    # Double-check: Make sure we are at least UPLOAD_DELAY_MINUTES past midnight UTC
                    # so that all late writers are completely finished and handles are closed.
                    now_utc = datetime.now(timezone.utc)
                    midnight_utc = datetime.combine(now_utc.date(), datetime.min.time(), tzinfo=timezone.utc)
                    minutes_since_midnight = (now_utc - midnight_utc).total_seconds() / 60.0
                    
                    if minutes_since_midnight < UPLOAD_DELAY_MINUTES:
                        logger.info(f"Day {dir_name} is completed, but waiting for {UPLOAD_DELAY_MINUTES} minutes past midnight UTC buffer. (Current minutes: {minutes_since_midnight:.1f})")
                        continue

                    logger.info(f"Found completed day directory ready for S3 upload: {dir_name}")
                    # Run CPU-bound zipping and S3 uploading in executors to prevent blocking event loop
                    await asyncio.to_thread(self._process_day_upload, path)

    def _process_day_upload(self, day_dir: Path):
        """Synchronous CPU/Network-bound routine to zip and upload a completed day."""
        day_str = day_dir.name
        year = day_str[0:4]
        month = day_str[4:6]
        day = day_str[6:8]

        zip_file_path = self.base_dir / f"{day_str}.zip"
        
        try:
            logger.info(f"Compressing {day_dir} into {zip_file_path}...")
            # Create a zip archive containing the day directory as the root (e.g. 20260616/binance/...)
            archive_base = self.base_dir / day_str
            shutil.make_archive(
                str(archive_base),
                "zip",
                root_dir=str(day_dir.parent),
                base_dir=day_str
            )
            
            if not zip_file_path.exists():
                raise FileNotFoundError(f"Failed to create zip file: {zip_file_path}")

            # Calculate S3 target key: e.g. crypto-market-data/2026/06/16/20260616.zip
            s3_key = f"{S3_PREFIX}{year}/{month}/{day}/{day_str}.zip"
            
            logger.info(f"Uploading {zip_file_path} to s3://{S3_BUCKET_NAME}/{s3_key}...")
            
            # Perform S3 upload
            self.s3_client.upload_file(
                Filename=str(zip_file_path),
                Bucket=S3_BUCKET_NAME,
                Key=s3_key
            )
            
            logger.info(f"S3 upload successful for {day_str}!")
            
            # On success, clean up local folders to save space
            logger.info(f"Cleaning up local directories and temp files for {day_str}...")
            shutil.rmtree(day_dir)
            zip_file_path.unlink()
            logger.info(f"Cleanup finished. Day {day_str} successfully archived to S3.")

        except (NoCredentialsError, PartialCredentialsError) as cred_err:
            logger.error(f"S3 Upload failed due to credentials error: {cred_err}. Leaving files local.")
            # Delete the temp zip file so we don't waste disk space, but leave the directory to try again
            if zip_file_path.exists():
                zip_file_path.unlink()
        except Exception as e:
            logger.error(f"Failed to process and upload {day_str}: {e}. Leaving files local.")
            if zip_file_path.exists():
                zip_file_path.unlink()
