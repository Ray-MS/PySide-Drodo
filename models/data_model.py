from datetime import datetime
from typing import Dict, Optional, Union

from pydantic import BaseModel, Field


class GemTDQuest(BaseModel):
    quest_expire: int
    quest: str
    quest_finish_count: int
    pass_: int = Field(alias='pass')
    season: int


class BestKills(BaseModel):
    p1: int
    p2: int
    p3: int
    p4: int


class GemTDRankInfo(BaseModel):
    rankall: Union[int, str]
    rankcoop: Union[int, str]
    rankrace: str
    score: int
    best_kills: BestKills


class GemTDHero(BaseModel):
    ability: Dict[str, int]
    effect: str
    extend: Optional[int] = Field(default=None)


class GemTDOndutyHero(GemTDHero):
    hero_id: str


class GemTDHeroesData(BaseModel):
    time: str = Field(default_factory=lambda: datetime.now().isoformat())
    hero_sea: Dict[str, GemTDHero]
    onduty_hero: GemTDOndutyHero
    shell: int
    ice: int
    candy: int
    quest: GemTDQuest
    rank_info: GemTDRankInfo


class GemTDHeroesResponse(BaseModel):
    err: int
    msg: str
    data: Dict[str, GemTDHeroesData]
