from os import stat
import xml.etree.ElementTree as ET
from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import RedirectResponse, JSONResponse
import requests
from loguru import logger
from typing import Dict, cast


app = FastAPI()


class ErrorResponse(BaseModel):
    description: str


class ReelResponse(BaseModel):
    content_url: str
    content_type: str
    user: str
    description: str
    source_url: str


def format_error(code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=code, content=ErrorResponse(description=message).model_dump()
    )


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get(
    "/insta/reel/{reel_id}",
    response_model=ReelResponse,
    responses={
        404: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def reel(reel_id: str) -> ReelResponse | JSONResponse:
    url = f"https://ddinstagram.com/reel/{reel_id}"
    dd_response = requests.get(url, allow_redirects=False)
    if dd_response.status_code == 302:
        logger.info("HTTP 302 response from {url}", url=url)
        return format_error(
            code=status.HTTP_404_NOT_FOUND,
            message="Requested resource most likely does not exist",
        )
    if dd_response.status_code != 200:
        logger.info("Non 200 response from url {url}", url=url)
        return format_error(
            code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=f"Upstream service respnded with HTTP {dd_response.status_code}.",
        )

    html = dd_response.text
    root = ET.fromstring(html)

    head_element = root.find("head")
    if head_element is None:
        logger.info("No head tag in response from {url}", url=url)
        return format_error(
            code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message="Upstream responded with invalid HTML",
        )

    params = {}

    for meta in head_element.findall("meta"):
        prop = meta.get("property")
        if prop == "og:url":
            params["source_url"] = meta.get("content")
        if prop == "og:title":
            params["user"] = meta.get("content")
        if prop == "og:description":
            params["description"] = meta.get("content")
        if prop == "og:video:type":
            params["content_type"] = meta.get("content")
        if prop == "og:video":
            try:
                video_url = meta.get("content")
                if video_url is None:
                    raise ValueError("No video url")
                video_response = requests.get(video_url, allow_redirects=False)
                params["content_url"] = video_response.headers["Location"]
            except Exception:
                logger.exception("could not get content_url for {url}", url=url)
                return format_error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Could not get video url")

                

    if len(list(params.keys())) != 5:
        return format_error(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Could not construct a response. Most likely upstream has changed",
        )

    for key, value in params.items():
        if value is None:
            logger.warning("Could not parse {key} from {url}", key=key, url=url)
            return format_error(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Could not construct a response. Most likely upstream has changed",
            )

    resp = ReelResponse(**cast(Dict[str, str], params))
    return JSONResponse(status_code=200, content=resp.model_dump())
