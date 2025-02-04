from dataclasses import dataclass


@dataclass(frozen=True)
class DisplayImage:
    id: int
    url: str
    thumb_url: str
    size: int
    width: int
    height: int
    created_at: int
