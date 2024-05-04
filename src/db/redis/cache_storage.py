from abc import ABC, abstractmethod


class BaseCacheStorage(ABC):
    @abstractmethod
    async def put_to_cache(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_from_cache(self, *args, **kwargs):
        raise NotImplementedError
