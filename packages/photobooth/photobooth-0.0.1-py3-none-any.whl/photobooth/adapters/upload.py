import io
import typing
from PyQt5 import QtCore


class UploadWorker(QtCore.QThread):
    def __init__(
        self,
        domain: str,
        resolution: typing.Tuple[int, int],
        auth: typing.Optional[typing.Tuple[str, str]],
        config: typing.Dict[str, typing.Any],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        import httpx

        if auth is not None:
            username, password = auth
            auth_ = httpx.BasicAuth(username=username, password=password)
        else:
            auth_ = None

        self._client = httpx.Client(auth=auth_, **config)
        self._url = domain
        self._resolution = resolution

    def upload(self, image_data: bytes, filename: str):
        try:
            from PIL import Image

            image = Image.open(io.BytesIO(image_data))
            image.thumbnail(self._resolution)
            buffer = io.BytesIO()
            image.save(buffer, 'JPEG', exif=image.getexif())
            buffer.seek(0)

            self._client.put(
                self._url,
                files={'file': (filename, buffer.getvalue(), 'image/jpeg')},
            )
        except Exception:
            pass
