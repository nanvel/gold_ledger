from io import BytesIO
from unittest.mock import Mock

from app.services.images import ImagesService


def test_image_service(data):
    client = Mock()
    service = ImagesService(
        s3_client=client,
        s3_bucket="bucket",
        key_prefix="prefix",
        thumb_size=320,
    )

    with open(data.rel("example.jpg"), "rb") as f:
        result = service.upload(BytesIO(f.read()), file_name="example.jpg")

    assert result.id == 0
    assert result.url.startswith("https://bucket.s3.amazonaws.com/prefix/")
    assert result.thumb_url.startswith("https://bucket.s3.amazonaws.com/prefix/")
    assert result.size == 179903
    assert result.width == 1920
    assert result.height == 1100

    assert client.upload_fileobj.call_count == 2
