from abc import ABC, abstractmethod

import aiohttp

from baseten_benchmarks.types import RequestResult


class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self, prompt: str, session: aiohttp.ClientSession
    ) -> RequestResult:
        pass
