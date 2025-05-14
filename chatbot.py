import streamlit as st
import fastf1
fastf1.Cache.enable_cache('/workspaces/formula1forthegirlies/__pycache__') 

from fastf1 import get_session

# Example: 2024 Bahrain Grand Prix - Race
session = get_session(2024, 'Bahrain', 'R')  # 'FP1', 'Q', 'R', etc.
session.load()

laps = session.laps.pick_driver('VER')  # Pick driver by 3-letter code
print(laps[['LapNumber', 'LapTime', 'Compound', 'TyreLife']])
