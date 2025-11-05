from typing import Optional

from pydantic import BaseModel, Field


class GemTDGood(BaseModel):
    id: str
    price: Optional[int] = Field(default=None)
    pic: str
    rarity: str


class GemTDGoodsResponse(BaseModel):
    err: int
    list: dict[str, GemTDGood]
    expire: int
    onsale: str
