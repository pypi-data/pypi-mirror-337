import base64
import json
import struct

import msgpack
import requests
from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt
from nacl.utils import random as nacl_random
from pydantic import BaseModel

from django.utils.timezone import now

from incursions import app_settings


class SSEClient:
    def __init__(self, url: str, secret: str) -> None:
        self.url = url
        self.key = bytes.fromhex(secret) if isinstance(secret, str) else secret
        self.VERSION_BYTE = b'\xBA'

    def branca_encode(self, payload: bytes, timestamp: int | None = None) -> str:
        if len(app_settings.SSE_SECRET) != 32:
            raise ValueError("Branca key must be exactly 32 bytes")

        nonce = nacl_random(24)
        ts_bytes = struct.pack(">I", int(timestamp or now().timestamp()))
        header = self.VERSION_BYTE + ts_bytes + nonce
        key = app_settings.SSE_SECRET.encode()

        ciphertext = crypto_aead_xchacha20poly1305_ietf_encrypt(payload, header, nonce, key)
        token = header + ciphertext
        return base64.urlsafe_b64encode(token).rstrip(b"=").decode()

    def events_url(self, topics: list[str]) -> str:
        request_payload = {"topics": topics}
        payload: bytes = msgpack.packb(request_payload, use_bin_type=True)
        token = self.branca_encode(payload, self.key)
        return f"{self.url}/events?token={token}"

    def submit(self, events: list["SSEEvent"]) -> requests.Response:
        submission = {"events": [event.to_dict() for event in events]}
        payload: bytes = msgpack.packb(submission, use_bin_type=True)
        encoded = self.branca_encode(payload)
        response = requests.post(f"{self.url}/submit", data=encoded)
        return response


class SSEEvent:
    def __init__(self, topic: str, event: str, data: str) -> None:
        self.topic = topic
        self.event = event
        self.data = data

    @classmethod
    def new(cls, topic: str, event: str, data: str) -> "SSEEvent":
        return cls(topic, event, data)

    @classmethod
    def new_json(cls, topic: str, event: str, data: BaseModel | dict) -> "SSEEvent":
        encoded = json.dumps(data)
        return cls(topic, event, encoded)

    def to_dict(self) -> dict:
        return {"topic": self.topic, "event": self.event, "data": self.data}
