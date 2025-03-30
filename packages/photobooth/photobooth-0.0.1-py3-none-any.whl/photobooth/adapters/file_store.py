from datetime import datetime
import io
from pathlib import Path
import typing
from PyQt5 import QtCore


class FileStoreWorker(QtCore.QThread):
    def __init__(
        self,
        path: str,
        resolution: typing.Tuple[int, int],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._resolution = resolution

        self._path = Path(path).joinpath(datetime.now().strftime('%Y%m%d_%H%M%S'))
        self._path.mkdir(exist_ok=True, parents=True)
        print(f'Filestore: {self._path}')
        self._log_path = self._path.joinpath('images.log')

        with self._log_path.open(mode='w') as file:
            file.write('Images\n')

    def save(self, image_data: bytes, filename: str):
        try:
            from PIL import Image

            image = Image.open(io.BytesIO(image_data))
            image.thumbnail(self._resolution)
            image.save(self._path.joinpath(filename), 'JPEG', exif=image.getexif())

            with self._log_path.open(mode='a') as file:
                file.write(f'{filename}\n')
        except Exception:
            pass
