from .get_file import GetFile
from .get_raw import GetRaw
from .download_lmages import DownloadImages
from jmcomic_api.models.core.route import Route
from typing import List

__all__: List[Route] = [GetFile, GetRaw, DownloadImages]
