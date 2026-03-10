"""Alibaba Cloud OSS service for image upload."""
import os
import uuid
from typing import Optional, Dict
import oss2


class OSSService:
    """Service for uploading files to Alibaba Cloud OSS."""

    def __init__(self):
        """Initialize OSS service with configuration from environment."""
        self.region = os.getenv('OSS_REGION', '')
        self.access_key_id = os.getenv('OSS_ACCESS_KEY_ID', '')
        self.access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET', '')
        self.bucket_name = os.getenv('OSS_BUCKET', '')

        # Create auth and bucket instances if configured
        self._auth = None
        self._bucket = None

        if self._is_configured():
            self._auth = oss2.Auth(self.access_key_id, self.access_key_secret)
            endpoint = f'https://{self.region}.aliyuncs.com'
            self._bucket = oss2.Bucket(self._auth, endpoint, self.bucket_name)

    def _is_configured(self) -> bool:
        """Check if OSS is properly configured."""
        return bool(self.region and self.access_key_id and self.access_key_secret and self.bucket_name)

    def is_configured(self) -> bool:
        """Public method to check if OSS is properly configured."""
        return self._is_configured()

    def generate_object_key(self, filename: str) -> str:
        """
        Generate object key for OSS upload.

        Args:
            filename: Original filename

        Returns:
            str: Object key in format: uploads/YYYY/MM/uuid-filename
        """
        from datetime import datetime

        now = datetime.now()
        year = now.year
        month = f"{now.month:02d}"
        unique_id = str(uuid.uuid4())

        return f"uploads/{year}/{month}/{unique_id}-{filename}"

    def get_public_url(self, object_key: str) -> str:
        """
        Get public URL for an OSS object.

        Args:
            object_key: OSS object key

        Returns:
            str: Full URL to the object
        """
        if not self._is_configured():
            return ''

        return f'https://{self.bucket_name}.{self.region}.aliyuncs.com/{object_key}'

    def upload_file(
        self,
        file_data: bytes,
        filename: str,
        content_type: str = 'image/jpeg'
    ) -> Dict[str, any]:
        """
        Upload file to OSS.

        Args:
            file_data: File data as bytes
            filename: Original filename
            content_type: Content type of the file

        Returns:
            dict: Upload result with keys:
                - success: bool indicating if upload succeeded
                - url: public URL of the uploaded file
                - error: error message if upload failed
        """
        if not self._is_configured():
            return {
                'success': False,
                'error': 'OSS is not configured'
            }

        try:
            object_key = self.generate_object_key(filename)

            # Upload to OSS
            self._bucket.put_object(
                object_key,
                file_data,
                headers={'Content-Type': content_type}
            )

            # Get public URL
            url = self.get_public_url(object_key)

            return {
                'success': True,
                'url': url,
                'object_key': object_key
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'OSS upload failed: {str(e)}'
            }

    def delete_file(self, object_key: str) -> Dict[str, any]:
        """
        Delete file from OSS.

        Args:
            object_key: OSS object key to delete

        Returns:
            dict: Delete result with keys:
                - success: bool indicating if delete succeeded
                - error: error message if delete failed
        """
        if not self._is_configured():
            return {
                'success': False,
                'error': 'OSS is not configured'
            }

        try:
            self._bucket.delete_object(object_key)
            return {'success': True}
        except Exception as e:
            return {
                'success': False,
                'error': f'OSS delete failed: {str(e)}'
            }


# Global service instance
oss_service = OSSService()
