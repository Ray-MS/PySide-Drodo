from pydantic import BaseModel, Field


class GemTDQuest(BaseModel):
    quest_expire: int
    quest: str
    quest_finish_count: int
    pass_: int = Field(alias='pass')
    season: int


class GemTDHeroesData(BaseModel):
    hero_sea: dict
    quest: GemTDQuest


class GemTDHeroesResponse(BaseModel):
    err: int
    msg: str
    data: dict[str, GemTDHeroesData]
