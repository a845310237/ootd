"""Aliyun OSS service for file uploads."""
import oss2
from typing import Optional, Tuple
from app.core.config import settings
import uuid
from datetime import datetime
import os


class OSSService:
    """Aliyun OSS storage service."""

    def __init__(self):
        """Initialize OSS service with credentials from settings."""
        # Validate OSS configuration
        if not all([settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET, settings.OSS_BUCKET, settings.OSS_REGION]):
            raise ValueError(
                "OSS configuration is incomplete. Please set OSS_ACCESS_KEY_ID, "
                "OSS_ACCESS_KEY_SECRET, OSS_BUCKET, and OSS_REGION in your .env file."
            )

        try:
            self.auth = oss2.Auth(
                settings.OSS_ACCESS_KEY_ID,
                settings.OSS_ACCESS_KEY_SECRET
            )
            self.bucket = oss2.Bucket(
                self.auth,
                f"https://{settings.OSS_REGION}.aliyuncs.com",
                settings.OSS_BUCKET
            )
            self.bucket_name = settings.OSS_BUCKET
            self.region = settings.OSS_REGION

            # Test connection by trying to get bucket info
            try:
                bucket_info = self.bucket.get_bucket_info()
                print(f"OSS service initialized successfully for bucket: {self.bucket_name}")
            except Exception as conn_error:
                print(f"Warning: Could not verify OSS bucket connection: {str(conn_error)}")
                print("OSS service will continue, but uploads may fail if credentials are invalid")

        except Exception as e:
            raise ValueError(f"Failed to initialize OSS service: {str(e)}")

    def generate_object_name(self, filename: str, prefix: str = "uploads") -> str:
        """
        Generate unique object name for OSS.

        Args:
            filename: Original filename
            prefix: Optional prefix for the object path

        Returns:
            Generated object key
        """
        # Extract file extension
        file_ext = os.path.splitext(filename)[1]

        # Generate unique filename with date-based path
        date_str = datetime.now().strftime("%Y/%m")
        unique_name = f"{uuid.uuid4()}{file_ext}"

        # Create full object path
        object_name = f"{prefix}/{date_str}/{unique_name}"
        return object_name

    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        prefix: str = "uploads"
    ) -> Tuple[str, int]:
        """
        Upload file to OSS.

        Args:
            file_content: File content as bytes
            filename: Original filename
            content_type: MIME type of the file
            prefix: Optional prefix for the object path

        Returns:
            Tuple of (object URL, file size)

        Raises:
            Exception: If upload fails
        """
        try:
            # Generate object name
            object_name = self.generate_object_name(filename, prefix)

            # Upload to OSS with proper headers
            result = self.bucket.put_object(
                object_name,
                file_content,
                headers={
                    'Content-Type': content_type,
                    'x-oss-object-acl': 'public-read'  # Make file publicly readable
                }
            )

            if result.status != 200:
                raise Exception(f"OSS upload failed with status {result.status}: {result.headers.get('x-oss-request-id', 'Unknown error')}")

            # Generate public URL
            file_url = f"https://{self.bucket_name}.{self.region}.aliyuncs.com/{object_name}"

            return file_url, len(file_content)

        except oss2.exceptions.OssError as e:
            raise Exception(f"OSS error during upload: {e.status} - {e.message}")
        except Exception as e:
            raise Exception(f"Failed to upload file to OSS: {str(e)}")

    def delete_file(self, object_name: str) -> bool:
        """
        Delete file from OSS.

        Args:
            object_name: Object key to delete

        Returns:
            True if successful
        """
        try:
            self.bucket.delete_object(object_name)
            return True
        except Exception as e:
            print(f"Failed to delete file from OSS: {str(e)}")
            return False

    def file_exists(self, object_name: str) -> bool:
        """
        Check if file exists in OSS.

        Args:
            object_name: Object key to check

        Returns:
            True if file exists
        """
        try:
            return self.bucket.object_exists(object_name)
        except Exception:
            return False


# Create global OSS service instance
try:
    oss_service = OSSService()
except ValueError as e:
    print(f"Warning: OSS service initialization failed: {e}")
    oss_service = None