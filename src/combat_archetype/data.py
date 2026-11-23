"""Data loading for the Pokémon combat archetype analysis."""

from pathlib import Path

from pandas import DataFrame, read_csv

STAT_COLUMNS = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]


def load_pokemon(path: str | Path = "pokemon.csv") -> DataFrame:
    df = read_csv(path)
    missing = [column for column in STAT_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(
            f"{path} is missing required stat columns: {', '.join(missing)}"
        )
    return df
