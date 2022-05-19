from http import HTTPStatus
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.weird_text.decoder import Decoder
from app.weird_text.encoder import Encoder
from app.weird_text.parser import DecodingException

VERSION = "/v1/"


class Payload(BaseModel):
    text: str


app = FastAPI()


@app.get("/")
def read_root():
    return "Welcome to WeirdText Api!"


@app.post(f"{VERSION}encode/", response_model=Payload)
def encode(payload: Payload):
    weird_text = Encoder.encode(payload.text)

    return _payload_from(weird_text)


@app.post(f"{VERSION}decode/", response_model=Payload)
def decode(payload: Payload):
    try:
        decoded_text = Decoder.decode(payload.text)
    except DecodingException as err:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(err))

    return _payload_from(decoded_text)


def _payload_from(text: str) -> dict:
    return {"text": text}
