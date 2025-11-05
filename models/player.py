from pydantic import BaseModel

from .steam import SteamPlayerSummary


class Player:
    steam: SteamPlayerSummary
