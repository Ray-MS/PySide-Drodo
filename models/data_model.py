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


class RankInfo(BaseModel):
    rankall: str | int
    rankcoop: str
    rankrace: str
    score: int
    best_kills: BestKills


class GemTDHeroesData(BaseModel):
    hero_sea: dict
    quest: GemTDQuest
    rank_info: RankInfo


class GemTDHeroesResponse(BaseModel):
    err: int
    msg: str
    data: dict[str, GemTDHeroesData]
