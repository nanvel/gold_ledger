import datetime
from io import BytesIO

import shortuuid
from PIL import Image as PImage

from app.models import Image


class ImagesService:
    def __init__(self, s3_client, s3_bucket: str, key_prefix: str, thumb_size: int):
        self._s3_client = s3_client
        self._s3_bucket = s3_bucket
        self._key_prefix = key_prefix
        self._thumb_size = thumb_size

    def upload(self, f: BytesIO, file_name: str) -> Image:
        slug = shortuuid.uuid()
        date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        ext = file_name.split(".")[-1]
        base_key = "/".join((self._key_prefix, date_str, slug))
        s3_key = base_key + "." + ext
        thumb_s3_key = base_key + "-t.jpg"

        img = PImage.open(f)
        content_type = f"image/{img.format.lower()}"
        width, height = img.size
        img.thumbnail((self._thumb_size, self._thumb_size))
        thumb = BytesIO()
        img.save(thumb, "JPEG")

        upload_kwargs = {
            "ACL": "public-read",
            "ContentDisposition": "inline",
            "ContentType": content_type,
        }
        self._s3_client.upload_fileobj(
            f,
            self._s3_bucket,
            s3_key,
            ExtraArgs=upload_kwargs,
        )
        upload_kwargs["ContentType"] = "image/jpeg"
        self._s3_client.upload_fileobj(
            thumb,
            self._s3_bucket,
            thumb_s3_key,
            ExtraArgs=upload_kwargs,
        )

        return Image(
            id=0,
            url=f"https://{self._s3_bucket}.s3.amazonaws.com/{s3_key}",
            thumb_url=f"https://{self._s3_bucket}.s3.amazonaws.com/{thumb_s3_key}",
            size=f.getbuffer().nbytes,
            width=width,
            height=height,
        )
