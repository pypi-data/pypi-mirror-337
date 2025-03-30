from typing import List

from jmcomic_api.models.core.route import Route

from .download_lmages import DownloadImages
from .get_file import GetFile
from .get_raw import GetRaw
from .get_raw_ranking import GetRawRanking
from .get_raw_search import GetRawSearch

__all__: List[Route] = [GetFile, GetRaw, DownloadImages, GetRawSearch, GetRawRanking]
