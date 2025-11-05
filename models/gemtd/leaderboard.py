from typing import Dict, List

from pydantic import BaseModel


class GemTDCoop(BaseModel):
    kill: int
    player_ids: str
    towers: str


class GemTDRace(BaseModel):
    player_id: str
    race_level: int


class GemTDLeaderboardData(BaseModel):
    p1: List[GemTDCoop]
    p2: List[GemTDCoop]
    p3: List[GemTDCoop]
    p4: List[GemTDCoop]
    race: List[GemTDRace]


class GemTDLeaderboardResponse(BaseModel):
    err: int
    msg: str
    data: GemTDLeaderboardData
