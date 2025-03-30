from abc import ABC, abstractmethod
from typing import List


class Route(ABC):
    path: str
    method: List

    @abstractmethod
    async def route_def(self):
        pass
