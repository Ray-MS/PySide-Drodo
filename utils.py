def get_steam_id(account_id: int) -> str:
    return str(0x110000100000000 + account_id)


def get_account_id(steam_id: str) -> int:
    return int(steam_id) - 0x110000100000000
