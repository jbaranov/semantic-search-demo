from tempfile import NamedTemporaryFile
from typing import List
import httpx

from pydantic import BaseModel
from fastapi import UploadFile


class DocumentProxy:

    @staticmethod
    def from_file(file: UploadFile):
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.file.read())
            return temp_file

    @staticmethod
    def from_url(url: str):
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(httpx.get(url).content)
            return temp_file


class DocumentRequest(BaseModel):
    url: str


class DocumentResponse(BaseModel):
    task_id: str
    status: str


class SearchRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    score: float
    payload: dict


class SearchResponse(BaseModel):
    results: List[SearchResult]
