import streamlit as st
import pandas as pd
import numpy as np
import random
import streamlit.components.v1 as components
import warnings
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import fastf1
import fastf1.plotting
import seaborn as sns
import os
cache_dir = '/tmp/fastf1_cache'  
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)
import matplotlib.pyplot as plt



#Site formatting
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;  /* white background */
        color: #ffffff;  /* Black text color for contrast */
    }
    .stApp {
        background-color: #ffffff; /* Background for entire app */
    }
    .css-1lcbz5j {
        color: #aa1316;  /* Change the color of streamlit header */
    }
     section[data-testid="stSidebar"] * {
        color: white !important;
    }
    .stButton>button {
        background-color: #ffffff; /* white button */
        color: red;
    }
    .stButton>button:hover {
        background-color: #aa1316;  /* Darker red on hover */
    }
    .stSidebar {
        background-color: #aa1316;  /* Sidebar color */
    }
    .stAppHeader {
        background-color: #aa1316;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def render_leaderboard(df):
    table_html = """
    <style>
        .custom-table {
            border-collapse: collapse;
            width: 100%;
            font-family: monospace;
        }
        .custom-table th, .custom-table td {
            border: 1px solid #444;
            padding: 8px 12px;
            text-align: center;
            color: white;
        }
        .custom-table thead {
            background-color: #111;
        }
        .custom-table tbody tr:nth-child(even) {
            background-color: #222;
        }
        .custom-table tbody tr:nth-child(odd) {
            background-color: #333;
        }
    </style>
    <table class="custom-table">
        <thead>
            <tr>
                <th>Position</th>"""
    
    if "Driver" in df.columns:
        table_html += "<th>Driver</th>"

    if "Points" in df.columns:
        table_html += "<th>Points</th>"

    if "Constructor" in df.columns:
        table_html += "<th>Constructor</th>"

    table_html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        table_html += "<tr>"
        table_html += f"<td>{row['Position']}</td>"
        if "Driver" in df.columns:
            table_html += f"<td>{row['Driver']}</td>"
        if "Constructor" in df.columns:
            table_html += f"<td>{row['Constructor']}</td>"    
        if "Points" in df.columns:
            table_html += f"<td>{row['Points']}</td>"
        table_html += "</tr>"

    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)




option = st.sidebar.radio("Pages",["**Home**", "**Revvy** ***NEW***", "**Grand Prix Positions**", "**Current Leaderboard**", "**Telemetry**", "**Hypothetical Chaos Mode**", "**Driver Information**", "**Construction Information**", "**Track Information**", "**Words of Wisdom**", "**McLaren Loopholes**", "Patch Notes"])

if option == "**Home**":
    st.title("kiley's f1 2025 season track: for the girls by the girls")
    st.image("https://steamuserimages-a.akamaihd.net/ugc/1914618053679846010/5E74EF96A5A44D3DD1266F77DFA85ED77770D675/")
    
##File Uploads
alpine_australia_drivers = ("Pierre Gasly", "Jack Doohan")
alpine_imola_drivers = ("Pierre Gasly", "Franco Colapinto")
alpine1_tracks = ("Australia", "China", "Japan", "Bahrain", "Saudi Arabia", "Miami")
alpine2_tracks = ("Imola", "Monaco")
aston_martin_drivers = ("Fernando Alonso", "Lance Stroll")
ferrari_drivers = ("Charles Leclerc", "Lewis Hamilton")
haas_drivers = ("Esteban Ocon", "Oliver Bearman")
kick_sauber_drivers = ("Nico Hulkenberg", "Gabriel Bortoleto")
mclaren_drivers = ("Lando Norris", "Oscar Piastri")
mercedes_drivers = ("George Russell", "Kimi Antonelli")
red_bull_racing_australia_drivers = ("Max Verstappen", "Liam Lawson")
red_bull_racing_japan_drivers = ("Max Verstappen", "Yuki Tsunoda")
redbull1_tracks = ("Australia", "China")
redbull2_tracks = ("Japan", "Bahrain", "Saudi Arabia", "Miami", "Imola", "Monaco")
racing_bulls_australia_drivers = ("Yuki Tsunoda", "Isack Hadjar")
racing_bulls_japan_drivers = ("Liam Lawson", "Isack Hadjar")
williams_drivers = ("Carlos Sainz", "Alexander Albon")

AA23_valid_names = ("Alex Albon", "Albon", "alex albon", "albon", "23")
AKA12_valid_names = ("Andrea Kimi Antonelli", "Antonelli", "Kimi Antonelli", "andrea kimi antonelli", "antonelli", "kimi antonelli", "12")
CL16_valid_names = ("Charles Leclerc", "Leclerc", "charles leclerc", "leclerc", "16")
CS55_valid_names = ("Carlos Sainz", "carlos sainz", "Sainz", "carlos Sainz", "Sainz", "sainz", "55")
EO31_valid_names = ("Esteban Ocon", "Ocon", "esteban ocon", "ocon", "31")
FA14_valid_names = ("Fernando Alonso", "Alonso", "The Rookie", "Fernando", "fernando alonso", "alonso", "fernando", "the rookie", "14")
FC43_valid_names = ("Franco Colapinto", "Colapinto", "franco colapinto", "colapinto", "43")
GB5_valid_names = ("Gabriel Bortoleto", "Bortoleto", "gabriel bortoleto", "bortoleto")
GR63_valid_names = ("George Russell", "Russell", "George Russel", "Russel", "george russell", "russell", "george russel", "russel", "63")
IH6_valid_names = ("Isack Hadjar", "Hadjar", "isack hadjar", "hadjar", "6")
JD7_valid_names = ("Jack Doohan", "Doohan", "jack doohan", "doohan", "7")
LH44_valid_names = ("Lewis Hamilton", "Hamilton", "lewis hamilton", "hamilton", "44")
LL30_valid_names = ("Liam Lawson", "Lawson", "liam lawson", "lawson", "30")
LN4_valid_names = ("Lando Norris", "Lando", "Norris", "lando norris", "lando", "norris", "4")
LS18_valid_names = ("Lance Stroll", "Stroll", "Daddy's Money", "lance stroll", "stroll", "daddy's money", "18")
MV33_valid_names = ("Max Verstappen", "Verstappen", "max verstappen", "verstappen", "1", "33", "2024 World Champion", "2024 world champion")
NH27_valid_names = ("Nico Hulkenberg", "Hulkenberg", "nico hulkenberg", "hulkenberg", "27")
OB87_valid_names = ("Oliver Bearman", "oliver bearman", "Ollie Bearman", "ollie bearman", "Ollie in the Wallie", "ollie in the wallie", "87")
OP81_valid_names = ("Oscar Piastri", "oscar piastri", "Piastri", "piastri", "Pastry", "pastry", "Great Barrier Chief", "great barrier chief", "Wizard of Aus", "wizard of aus", "oscar", "Oscar", "81")
PG10_valid_names = ("Pierre Gasley", "pierre gasley", "Gasley", "gasley", "10", "Pierre Gasly", "pierre gasly", "gasly")
YT22_valid_names = ("Yuki Tsunoda", "Tsunoda", "yuki tsunoda", "tsunoda", "22")
valid_driver_names = set(AA23_valid_names + AKA12_valid_names + CL16_valid_names + CS55_valid_names + EO31_valid_names + FA14_valid_names + FC43_valid_names + GB5_valid_names + GR63_valid_names + IH6_valid_names + JD7_valid_names + LH44_valid_names + LL30_valid_names + LN4_valid_names + LS18_valid_names + MV33_valid_names + NH27_valid_names + OB87_valid_names + OP81_valid_names + PG10_valid_names + YT22_valid_names)
invalid_driver_names = set()


#driver photos
driver_photos = {
    "Pierre Gasly": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/P/PIEGAS01_Pierre_Gasly/piegas01.png",
    "Jack Doohan": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/J/JACDOO01_Jack_Doohan/jacdoo01.png",
    "Fernando Alonso": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/F/FERALO01_Fernando_Alonso/feralo01.png",
    "Lance Stroll": "https://media.formula1.com/d_default_fallback_image.png/content/dam/fom-website/2018-redesign-assets/drivers/number-logos/LANSTR01.png",
    "Charles Leclerc": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png",
    "Lewis Hamilton": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.png",
    "Oliver Bearman": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/O/OLIBEA01_Oliver_Bearman/olibea01.png",
    "Esteban Ocon": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/E/ESTOCO01_Esteban_Ocon/estoco01.png",
    "Nico Hulkenberg": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/N/NICHUL01_Nico_Hulkenberg/nichul01.png",
    "Gabriel Bortoleto": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/G/GABBOR01_Gabriel_Bortoleto/gabbor01.png",
    "Lando Norris": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png",
    "Oscar Piastri": "https://media.cnn.com/api/v1/images/stellar/prod/gettyimages-2172131554-copy.jpg?c=original",
    "George Russell": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.png",
    "Kimi Antonelli": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/K/ANDANT01_Kimi_Antonelli/andant01.png",
    "Max Verstappen": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png",
    "Yuki Tsunoda": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/Y/YUKTSU01_Yuki_Tsunoda/yuktsu01.png",
    "Isack Hadjar": "https://www.formulaonehistory.com/wp-content/uploads/2024/12/Isack-Hadjar-F1-2024-RB.webp",
    "Liam Lawson": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LIALAW01_Liam_Lawson/lialaw01.png",
    "Alexander Albon": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/A/ALEALB01_Alexander_Albon/alealb01.png",
    "Carlos Sainz": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.png"
}

#Main Race
gp = pd.read_csv('https://raw.githubusercontent.com/Rooniford/formula1forthegirlies/main/2025RaceResults.csv')
sprint = pd.read_csv('https://raw.githubusercontent.com/Rooniford/formula1forthegirlies/main/2025SprintResults.csv')
season = pd.concat([gp, sprint])

##GRAND PRIX POSITIONS
gp_clean = gp.dropna(subset=["Track", "Pos"])
tracks = gp_clean["Track"].unique()

if option == "**Grand Prix Positions**":
    for track in tracks:
        race_data = gp_clean[gp_clean["Track"] == track] 

        st.markdown(f"<h2 style='text-align: center;'>{track}</h2>", unsafe_allow_html=True)

        race_results = []

        for pos in range(1, 21):  
            driver_row = race_data[race_data["Pos"] == str(pos)]
            if not driver_row.empty:
                driver_name = driver_row.iloc[0]["Driver"]
                race_results.append([pos, driver_name])
            else:
                race_results.append([pos, "No data"])

        results_df = pd.DataFrame(race_results, columns = ["Position", "Driver"])

        render_leaderboard(results_df)
        st.divider()
    st.caption("six people did not complete the Australia GP, I have tried so hard to fix the file and havent done it yet so their names aren't listed...soz")

##STANDINGS

elif option == "**Current Leaderboard**":

    #WDC
    st.markdown(f"<h2 style='text-align: center;'>World Drivers Championship</h2>", unsafe_allow_html=True)
    
    gp_points_table = {
        "1": 25,
        "2": 18,
        "3": 15,
        "4": 12,
        "5": 10,
        "6": 8,
        "7": 6,
        "8": 4,
        "9": 2,
        "10": 1
    }

    sprint_points_table = {
        "1": 8,
        "2": 7,
        "3": 6,
        "4": 5,
        "5": 4,
        "6": 3,
        "7": 2,
        "8": 1
    }

    def calculate_gp_points(results):
        results["Clean_Pos"] = results["Pos"].astype(str).str.strip() #cleans up in case of whitespace or DNF
        valid_gp_positions = results[results["Clean_Pos"].isin(gp_points_table.keys())]
        if valid_gp_positions.empty:
            return pd.DataFrame()
        valid_gp_positions["Points"] = valid_gp_positions["Clean_Pos"].map(gp_points_table)
        gp_leaderboard = valid_gp_positions.groupby(["Driver", "Track"])["Points"].sum().reset_index()
        gp_leaderboard = gp_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)                                                                 
        return gp_leaderboard
        

    def calculate_sprint_points(results):
        results["Clean_Pos"] = results["Pos"].astype(str).str.strip()
        valid_sprint_positions = results[results["Clean_Pos"].isin(sprint_points_table.keys())]
        if valid_sprint_positions.empty:
            return pd.DataFrame()

        valid_sprint_positions["Points"] = valid_sprint_positions["Clean_Pos"].map(sprint_points_table)
        sprint_leaderboard = valid_sprint_positions.groupby(["Driver", "Track"])["Points"].sum().reset_index()
        sprint_leaderboard = sprint_leaderboard.sort_values(by="Points", ascending=True).reset_index(drop=True)
        return sprint_leaderboard

    
    gp_leaderboard = calculate_gp_points(gp)
    sprint_leaderboard = calculate_sprint_points(sprint)

    if not gp_leaderboard.empty and not sprint_leaderboard.empty:
        full_leaderboard = pd.concat([gp_leaderboard, sprint_leaderboard])
        full_leaderboard = full_leaderboard.groupby(["Driver", "Track"])["Points"].sum().reset_index()
        full_leaderboard = full_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)

        full_leaderboard["Position"] = full_leaderboard.index + 1
    full_leaderboard["Position"] = full_leaderboard["Position"].apply(
        lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
    )

    full_leaderboard = full_leaderboard[["Position", "Driver", "Points", "Track"]]

    full_leaderboard_copy = full_leaderboard.copy()
    combined = pd.concat([full_leaderboard_copy[["Driver", "Points", "Track"]]])
    full_combined_with_track = combined.copy()
    combined = combined.groupby("Driver", as_index=False)["Points"].sum()
    combined = combined.sort_values(by="Points", ascending=False).reset_index(drop=True)
    combined["Position"] = combined.index + 1
    combined["Position"] = combined["Position"].apply(
        lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
    )

    combined = combined[["Position", "Driver", "Points"]]
    
    render_leaderboard(combined)

    #CC_retry

    alpine_australia_only = full_combined_with_track[
        (full_combined_with_track["Driver"].isin(alpine_australia_drivers)) &
        (full_combined_with_track["Track"].isin(alpine1_tracks))
    ]
    alpine_australia_points = alpine_australia_only["Points"].sum()
    alpine_imola_only = full_combined_with_track[
        (full_combined_with_track["Driver"].isin(alpine_imola_drivers)) &
        (full_combined_with_track["Track"].isin(alpine2_tracks))
    ]
    alpine_imola_points = alpine_imola_only["Points"].sum()
    alpine_points = alpine_australia_points + alpine_imola_points 

    aston_martin_only = combined[combined["Driver"].isin(aston_martin_drivers)]
    aston_martin_points = aston_martin_only["Points"].sum()

    ferrari_only = combined[combined["Driver"].isin(ferrari_drivers)]
    ferrari_points = ferrari_only["Points"].sum()

    haas_only = combined[combined["Driver"].isin(haas_drivers)]
    haas_points = haas_only["Points"].sum()

    kick_sauber_only = combined[combined["Driver"].isin(kick_sauber_drivers)]
    kick_sauber_points = kick_sauber_only["Points"].sum()

    mclaren_only = combined[combined["Driver"].isin(mclaren_drivers)]
    mclaren_points = mclaren_only["Points"].sum()

    mercedes_only = combined[combined["Driver"].isin(mercedes_drivers)]
    mercedes_points = mercedes_only["Points"].sum()

    red_bull_racing_australia_only = full_combined_with_track[
        (full_combined_with_track["Driver"].isin(red_bull_racing_australia_drivers)) &
        (full_combined_with_track["Track"].isin(redbull1_tracks))
    ]
    red_bull_racing_australia_points = red_bull_racing_australia_only["Points"].sum()
    red_bull_racing_japan_only = full_combined_with_track[
        (full_combined_with_track["Driver"].isin(red_bull_racing_japan_drivers)) &
        (~full_combined_with_track["Track"].isin(redbull1_tracks))
    ]
    red_bull_racing_japan_points = red_bull_racing_japan_only["Points"].sum()
    red_bull_racing_points = red_bull_racing_australia_points + red_bull_racing_japan_points

    racing_bulls_australia_only = full_combined_with_track[
        (full_combined_with_track["Driver"].isin(racing_bulls_australia_drivers)) &
        (full_combined_with_track["Track"].isin(redbull1_tracks))
    ]
    racing_bulls_australia_points = racing_bulls_australia_only["Points"].sum()
    racing_bulls_japan_only = full_combined_with_track[
        (full_combined_with_track["Driver"].isin(racing_bulls_japan_drivers)) &
        (~full_combined_with_track["Track"].isin(redbull1_tracks))
    ]
    racing_bulls_japan_points = racing_bulls_japan_only["Points"].sum()
    racing_bulls_points = racing_bulls_australia_points + racing_bulls_japan_points

    williams_only = combined[combined["Driver"].isin(williams_drivers)]
    williams_points = williams_only["Points"].sum()
    
    
    cc_leaderboard = pd.DataFrame([
        {"Constructor": "Alpine", "Points": alpine_points},
        {"Constructor": "Aston Martin", "Points": aston_martin_points},
        {"Constructor": "Ferrari", "Points": ferrari_points},
        {"Constructor": "Haas", "Points": haas_points},
        {"Constructor": "Kick Sauber", "Points": kick_sauber_points},
        {"Constructor": "McLaren", "Points": mclaren_points},
        {"Constructor": "Mercedes", "Points": mercedes_points},
        {"Constructor": "Red Bull Racing", "Points": red_bull_racing_points},
        {"Constructor": "Racing Bulls", "Points": racing_bulls_points},
        {"Constructor": "Williams", "Points": williams_points}
    ])

    cc_leaderboard["Points"] = pd.to_numeric(cc_leaderboard["Points"], errors="coerce").fillna(0)
    cc_leaderboard = cc_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)
    cc_leaderboard["Position"] = cc_leaderboard.index + 1
    cc_leaderboard["Position"] = cc_leaderboard["Position"].apply(
        lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
    )
    
    st.markdown(f"<h2 style='text-align: center;'>Constructors' Championship", unsafe_allow_html=True)
    render_leaderboard(cc_leaderboard)                                                                      

#RACE TELEMETRY
elif option == "**Telemetry**":
    driver_name_to_code = {
        **dict.fromkeys(AA23_valid_names, "ALB"),
        **dict.fromkeys(AKA12_valid_names, "ANT"),
        **dict.fromkeys(CL16_valid_names, "LEC"),
        **dict.fromkeys(CS55_valid_names, "SAI"),
        **dict.fromkeys(EO31_valid_names, "OCO"),
        **dict.fromkeys(FA14_valid_names, "ALO"),
        **dict.fromkeys(FC43_valid_names, "COL"),
        **dict.fromkeys(GB5_valid_names, "BOR"),
        **dict.fromkeys(GR63_valid_names, "RUS"),
        **dict.fromkeys(IH6_valid_names, "HAD"),
        **dict.fromkeys(JD7_valid_names, "DOO"),
        **dict.fromkeys(LH44_valid_names, "HAM"),
        **dict.fromkeys(LL30_valid_names, "LAW"),
        **dict.fromkeys(LN4_valid_names, "NOR"),
        **dict.fromkeys(LS18_valid_names, "STR"),
        **dict.fromkeys(MV33_valid_names, "VER"),
        **dict.fromkeys(NH27_valid_names, "HUL"),
        **dict.fromkeys(OB87_valid_names, "BEA"),
        **dict.fromkeys(OP81_valid_names, "PIA"),
        **dict.fromkeys(PG10_valid_names, "GAS"),
        **dict.fromkeys(YT22_valid_names, "TSU")
    }

    from fastf1 import get_session

    telemetry_type = st.selectbox("choose the type of telemetry you want to analyze", 
            ["",
            "qualifying", 
            "lap times", 
            "race pace",]
        )

    if telemetry_type == "choose the type of telemetry you want to analyze":
        st.write("please note that the earliest season is 2018, but only drivers from the 2025 season are currently available.")
    # qualifying 
    elif telemetry_type == "qualifying":
        st.write("")
        season = st.text_input("Season (e.g. 2024):")
        race = st.text_input("Grand Prix name (e.g. Miami):")
        drivers_input = st.text_input("Enter driver names seperated by commas:")

        if st.button("generate graph"):
            if season and race and drivers_input:
                try:
                    with st.spinner('please wait while your graph is loading'):
                        session = get_session(int(season), race, 'Q')
                        session.load()
                    driver_names = [name.strip() for name in drivers_input.split(",")]
                    driver_codes = []
                    for name in driver_names:
                        code = driver_name_to_code.get(name)
                        if code:
                            driver_codes.append(code)
                        else:
                            st.warning(f"Driver not recognized: {name}")
                    if len(driver_codes) < 1:
                        st.warning("no valid drivers found")
                    else:
                        fig, ax = plt.subplots()

                        for code in driver_codes:
                            lap_data = session.laps.pick_driver(code).pick_fastest()
                            tel = lap_data.get_telemetry()
                            ax.plot(tel['Distance'], tel['Speed'], label=code)
                        ax.set_xlabel('Distance [m]')
                        ax.set_ylabel('Speed [km/h]')
                        ax.set_title('Fastest Qualifying Lap Comparison')
                        ax.plot([0, 1], [0, 1])
                        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                        plt.subplots_adjust(right=0.8)
                        
                        st.pyplot(fig)
                except Exception as e:
                    st.write("")

    # fastest lap
    elif telemetry_type == "lap times":
        season = st.text_input("Season (e.g. 2024):")
        race = st.text_input("Grand Prix name (e.g. Bahrain):")
        drivers_input = st.text_input("Enter driver names seperated by commas:")
        lap = st.text_input("Lap (e.g. 32 or Fastest)")

        
        if st.button("generate graph"):
            if season and race and drivers_input and lap == "Fastest":
                try:
                    with st.spinner('please wait while your graph is loading'):
                        session = get_session(int(season), race, 'R')
                        session.load()

                        # Split and clean input
                        driver_names = [name.strip() for name in drivers_input.split(",") if name.strip()]

                        # Get corresponding driver codes
                        driver_codes = []
                        for name in driver_names:
                            code = driver_name_to_code.get(name)
                            if code:
                                driver_codes.append(code)
                            else:
                                st.warning(f"Driver not recognized: {name}")

                        if len(driver_codes) < 1:
                            st.error("No valid drivers found.")
                        else:
                            fig, ax = plt.subplots()

                            for code in driver_codes:
                                lap_data = session.laps.pick_driver(code).pick_fastest()
                                tel = lap_data.get_telemetry()
                                ax.plot(tel['Distance'], tel['Speed'], label=code)

                            ax.set_xlabel('Distance [m]')
                            ax.set_ylabel('Speed [km/h]')
                            ax.set_title('Fastest Lap Speed Comparison')
                            ax.plot([0, 1], [0, 1])
                            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                            plt.subplots_adjust(right=0.8)

                            st.pyplot(fig)

                except Exception as e:
                    st.write("")
            if season and race and drivers_input and lap:
                lap_number = lap
                try:
                    with st.spinner('please wait while your graph is loading'):
                        session = get_session(int(season), race, 'R')
                        session.load()

                        # Split and clean input
                        driver_names = [name.strip() for name in drivers_input.split(",") if name.strip()]

                        # Get corresponding driver codes
                        driver_codes = []
                        for name in driver_names:
                            code = driver_name_to_code.get(name)
                            if code:
                                driver_codes.append(code)
                            else:
                                st.warning(f"Driver not recognized: {name}")

                        if len(driver_codes) < 1:
                            st.error("No valid drivers found.")
                        else:
                            fig, ax = plt.subplots()

                            for code in driver_codes:
                                lap_data = session.laps.pick_driver(code).query(f"LapNumber == {lap_number}")
                                tel = lap_data.get_telemetry()
                                ax.plot(tel['Distance'], tel['Speed'], label=code)

                            ax.set_xlabel('Distance [m]')
                            ax.set_ylabel('Speed [km/h]')
                            ax.set_title('Fastest Lap Speed Comparison')
                            ax.legend()

                            st.pyplot(fig)

                except Exception as e:
                    st.write("")

    # gear shifts

    # race pace
    elif telemetry_type == "race pace":
        season = st.text_input("Season (e.g. 2024):")
        race = st.text_input("Grand Prix (e.g. Miami):")
        
        if st.button("generate graph"):
            if season and race:
                try:
                    with st.spinner("please wait while your graph is loading"):
                        session = fastf1.get_session(int(season), race, 'R')  # Use 'get_session' instead of 'get'
                        session.load()
                        st.write(f"Session for {season} {race} loaded successfully!")

                        point_finishers = session.drivers[:10]
                        driver_laps = session.laps.pick_drivers(point_finishers).pick_quicklaps()
                        driver_laps = driver_laps.reset_index()

                        finishing_order = [session.get_driver(driver_id)["Abbreviation"] for driver_id in point_finishers]

                        fig, ax = plt.subplots(figsize=(10, 5))

                        driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()

                        sns.boxplot(data=driver_laps,
                                    x="Driver",
                                    y="LapTime(s)",
                                    hue="Driver",
                                    order=finishing_order,
                                    legend=False,
                                    )

                        sns.stripplot(data=driver_laps,
                                    x="Driver",
                                    y="LapTime(s)",
                                    order=finishing_order,
                                    hue="Compound",
                                    palette=fastf1.plotting.get_compound_mapping(session=session),  # Use session, not race
                                    hue_order=["SOFT", "MEDIUM", "HARD"],
                                    linewidth=0,
                                    size=4,
                                    )
                        
                        ax.set_xlabel("Driver")
                        ax.set_ylabel("Lap Time (s)")
                        ax.set_facecolor('lightgray')
                        ax.set_title(f"{season} {race} Lap Time Distributions")
                        ax.legend()
                        st.pyplot(fig)

                except Exception as e:
                    st.write("")

##Hypothetical Chaos Mode

elif option == "**Hypothetical Chaos Mode**":
    st.markdown(f"<h2 style='text-align: center;'>Hypothetical Chaos Mode</h2>", unsafe_allow_html=True)
    race_type = st.selectbox("Choose a Race Type",
                 ["","Sprint", "Main Race"
        ])

    name_input = {
        "Pierre Gasly": ["pierre gasley", "gasley", "gasly", "pierre gasly", "Pierre Gasley", "Pedo Pierre", "pedo pierre", "Pierre", "Gasly"],
        "Jack Doohan": ["jack doohan", "jack", "doohan", "Jack", "Doohan", "jack doohan"],
        "Fernando Alonso": ["fernando alonso", "the rookie", "The Rookie", "Alonso", "alonso", "fernando", "Fernando"],
        "Lance Stroll": ["lance stroll", "Lance", "lance", "Stroll", "stroll", "Daddy's Money", "daddy's money"],
        "Charles Leclerc": ["Charles", "charles", "Leclerc", "leclerc", "charles leclerc"],
        "Lewis Hamilton": ["lewis hamilton", "lewis", "Lewis", "Hamilton", "hamilton"],
        "Esteban Ocon": ["Estie Bestie", "estie bestie", "esteban ocon", "Ocon", "ocon", "Esteban", "esteban"],
        "Oliver Bearman": ["oliver bearman", "Ollie Bearman", "ollie bearman", "Ollie", "ollie", "Oliver", "oliver", "Bearman", "bearman", "ollie in the wallie", "Ollie in the Wallie"],
        "Nico Hulkenberg": ["nico hulkenberg", "Hulkenberg", "hulkenberg", "Nico", "nico"],
        "Gabriel Bortoleto": ["gabriel bortoleto", "gabi bortoleto", "Gabi Bortoleto", "Gabriel", "gabriel", "Gabi", "gabi", "Bortoleto", "bortoleto"],
        "Lando Norris": ["lando norris", "Lando", "lando", "Norris", "norris"],
        "Oscar Piastri": ["oscar piastri", "oscar", "piastri", "Oscar", "Piastri", "Great Barrier Chief", "great barrier chief"],
        "George Russell": ["george russell", "George", "george", "Russell", "russell"],
        "Kimi Antonelli": ["Andrea Kimi Antonelli", "andrea kimi antonelli", "Antonelli", "antonelli", "kimi antonelli", "Kimi", "kimi"],
        "Max Verstappen": ["max verstappen", "max", "Max", "Verstappen", "verstappen"],
        "Yuki Tsunoda": ["yuki tsunoda", "Yuki", "yuki", "Tsunoda", "tsunoda"],
        "Isack Hadjar": ["isack hadjar", "Isack", "isack", "Hadjar", "hadjar"],
        "Liam Lawson": ["liam lawson", "liam", "Liam", "Lawson", "lawson"],
        "Carlos Sainz": ["Carlos Sainz", "carlos sainz", "carlos seinz", "Carlos Seinz", "Carlos", "carlos", "Sainz", "sainz", "Seinz", "seinz"],
        "Alexander Albon": ["alexander albon", "Alex Albon", "alex albon", "Alexander", "alexander", "Alex", "alex", "Albon", "albon"]
    }

    name_alias_map = {}
    for official_name, aliases in name_input.items():
        for alias in aliases:
            name_alias_map[alias.strip().lower()] = official_name

    #Leaderboard
    gp_points_table = {
        "1": 25,
        "2": 18,
        "3": 15,
        "4": 12,
        "5": 10,
        "6": 8,
        "7": 6,
        "8": 4,
        "9": 2,
        "10": 1
    }

    sprint_points_table = {
        "1": 8,
        "2": 7,
        "3": 6,
        "4": 5,
        "5": 4,
        "6": 3,
        "7": 2,
        "8": 1
    }

    def calculate_gp_points(results):
        results["Clean_Pos"] = results["Pos"].astype(str).str.strip() #cleans up in case of whitespace or DNF
        valid_gp_positions = results[results["Clean_Pos"].isin(gp_points_table.keys())]
        if valid_gp_positions.empty:
            return pd.DataFrame()
        valid_gp_positions["Points"] = valid_gp_positions["Clean_Pos"].map(gp_points_table)
        gp_leaderboard = valid_gp_positions.groupby(["Driver", "Track"])["Points"].sum().reset_index()
        gp_leaderboard = gp_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)                                                                 
        return gp_leaderboard
        

    def calculate_sprint_points(results):
        results["Clean_Pos"] = results["Pos"].astype(str).str.strip()
        valid_sprint_positions = results[results["Clean_Pos"].isin(sprint_points_table.keys())]
        if valid_sprint_positions.empty:
            return pd.DataFrame()

        valid_sprint_positions["Points"] = valid_sprint_positions["Clean_Pos"].map(sprint_points_table)
        sprint_leaderboard = valid_sprint_positions.groupby(["Driver", "Track"])["Points"].sum().reset_index()
        sprint_leaderboard = sprint_leaderboard.sort_values(by="Points", ascending=True).reset_index(drop=True)
        return sprint_leaderboard

    
    gp_leaderboard = calculate_gp_points(gp)
    sprint_leaderboard = calculate_sprint_points(sprint)

    if not gp_leaderboard.empty and not sprint_leaderboard.empty:
        full_leaderboard = pd.concat([gp_leaderboard, sprint_leaderboard])
        full_leaderboard = full_leaderboard.groupby(["Driver", "Track"])["Points"].sum().reset_index()
        full_leaderboard = full_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)

        full_leaderboard["Position"] = full_leaderboard.index + 1
    full_leaderboard["Position"] = full_leaderboard["Position"].apply(
        lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
    )

    full_leaderboard = full_leaderboard[["Position", "Driver", "Points", "Track"]]
    if race_type == "Sprint":
        st.write("Type the names of 2025 drivers in the position you predict they'll finish in")
        # Create an editable table for 10 positions
        pos_labels = [f"{i+1}{'st' if i+1 == 1 else 'nd' if i+1 == 2 else 'rd' if i+1 == 3 else 'th'}" for i in range(10)]
        hypothetical_input = pd.DataFrame({"Position": pos_labels, "Driver": [""] * 10})
        edited_data = st.data_editor(hypothetical_input, num_rows="fixed", use_container_width=True, hide_index=True)

        #hypothetical entries wdc
        hypothetical_entries = []
        for idx, row in edited_data.iterrows():
            driver_name_input = row["Driver"].strip().lower()
            if driver_name_input:
                normalized_name = name_alias_map.get(driver_name_input, None)
                if normalized_name:
                    position_number = str(idx + 1)
                    if position_number in sprint_points_table:
                        hypothetical_entries.append({
                            "Driver": normalized_name,
                            "Points": sprint_points_table[position_number]
                        })
                else:
                    st.warning(f"Unrecognized driver name: {row['Driver']}")

        if hypothetical_entries:
            hypothetical_df = pd.DataFrame(hypothetical_entries)

            if hypothetical_df["Driver"].duplicated().any():
                st.warning("Each driver should only appear once")
            else:
                full_leaderboard_copy = full_leaderboard.copy()
                combined = pd.concat([full_leaderboard_copy[["Driver", "Points", "Track"]], hypothetical_df])
                full_combined_with_track = combined.copy()
                combined = combined.groupby("Driver", as_index=False)["Points"].sum()
                combined = combined.sort_values(by="Points", ascending=False).reset_index(drop=True)
                combined["Position"] = combined.index + 1
                combined["Position"] = combined["Position"].apply(
                    lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
                )

                combined = combined[["Position", "Driver", "Points"]]
                
                st.markdown(f"<h3 style='text-align: center;'>Projected World Drivers Championship</h3>", unsafe_allow_html=True)
                render_leaderboard(combined)
                
        else:
            st.info("Enter at least one driver to see the leaderboard.")

        

        #hypothetical entries cc

        if hypothetical_entries:
            st.markdown(f"<h3 style='text-align: center;'>Projected Constructors Championship</h3>", unsafe_allow_html=True)
    
            alpine_australia_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(alpine_australia_drivers)) &
                (full_combined_with_track["Track"].isin(alpine1_tracks))
            ]
            alpine_australia_points = alpine_australia_only["Points"].sum()
            alpine_imola_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(alpine_imola_drivers)) &
                (full_combined_with_track["Track"].isin(alpine2_tracks))
            ]
            alpine_imola_points = alpine_imola_only["Points"].sum()
            alpine_points = alpine_australia_points + alpine_imola_points 

            aston_martin_only = combined[combined["Driver"].isin(aston_martin_drivers)]
            aston_martin_points = aston_martin_only["Points"].sum()

            ferrari_only = combined[combined["Driver"].isin(ferrari_drivers)]
            ferrari_points = ferrari_only["Points"].sum()

            haas_only = combined[combined["Driver"].isin(haas_drivers)]
            haas_points = haas_only["Points"].sum()

            kick_sauber_only = combined[combined["Driver"].isin(kick_sauber_drivers)]
            kick_sauber_points = kick_sauber_only["Points"].sum()

            mclaren_only = combined[combined["Driver"].isin(mclaren_drivers)]
            mclaren_points = mclaren_only["Points"].sum()

            mercedes_only = combined[combined["Driver"].isin(mercedes_drivers)]
            mercedes_points = mercedes_only["Points"].sum()

            red_bull_racing_australia_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(red_bull_racing_australia_drivers)) &
                (full_combined_with_track["Track"].isin(redbull1_tracks))
            ]
            red_bull_racing_australia_points = red_bull_racing_australia_only["Points"].sum()
            red_bull_racing_japan_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(red_bull_racing_japan_drivers)) &
                (~full_combined_with_track["Track"].isin(redbull1_tracks))
            ]
            red_bull_racing_japan_points = red_bull_racing_japan_only["Points"].sum()
            red_bull_racing_points = red_bull_racing_australia_points + red_bull_racing_japan_points

            racing_bulls_australia_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(racing_bulls_australia_drivers)) &
                (full_combined_with_track["Track"].isin(redbull1_tracks))
            ]
            racing_bulls_australia_points = racing_bulls_australia_only["Points"].sum()
            racing_bulls_japan_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(racing_bulls_japan_drivers)) &
                (~full_combined_with_track["Track"].isin(redbull1_tracks))
            ]
            racing_bulls_japan_points = racing_bulls_japan_only["Points"].sum()
            racing_bulls_points = racing_bulls_australia_points + racing_bulls_japan_points

            williams_only = combined[combined["Driver"].isin(williams_drivers)]
            williams_points = williams_only["Points"].sum()
            
            cc_leaderboard = pd.DataFrame([
                {"Constructor": "Alpine", "Points": alpine_points},
                {"Constructor": "Aston Martin", "Points": aston_martin_points},
                {"Constructor": "Ferrari", "Points": ferrari_points},
                {"Constructor": "Haas", "Points": haas_points},
                {"Constructor": "Kick Sauber", "Points": kick_sauber_points},
                {"Constructor": "McLaren", "Points": mclaren_points},
                {"Constructor": "Mercedes", "Points": mercedes_points},
                {"Constructor": "Red Bull Racing", "Points": red_bull_racing_points},
                {"Constructor": "Racing Bulls", "Points": racing_bulls_points},
                {"Constructor": "Williams", "Points": williams_points}
            ])

            cc_leaderboard["Points"] = pd.to_numeric(cc_leaderboard["Points"], errors="coerce").fillna(0)
            cc_leaderboard = cc_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)
            cc_leaderboard["Position"] = cc_leaderboard.index + 1
            cc_leaderboard["Position"] = cc_leaderboard["Position"].apply(
                lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
            )

            render_leaderboard(cc_leaderboard)
        else:
            st.write("")

    if race_type == "Main Race":
        st.write("Type the names of 2025 drivers in the position you predict they'll finish in")
        # Create an editable table for 10 positions
        pos_labels = [f"{i+1}{'st' if i+1 == 1 else 'nd' if i+1 == 2 else 'rd' if i+1 == 3 else 'th'}" for i in range(10)]
        hypothetical_input = pd.DataFrame({"Position": pos_labels, "Driver": [""] * 10})
        edited_data = st.data_editor(hypothetical_input, num_rows="fixed", use_container_width=True, hide_index=True)

        #hypothetical entries wdc
        hypothetical_entries = []
        for idx, row in edited_data.iterrows():
            driver_name_input = row["Driver"].strip().lower()
            if driver_name_input:
                normalized_name = name_alias_map.get(driver_name_input, None)
                if normalized_name:
                    position_number = str(idx + 1)
                    if position_number in gp_points_table:
                        hypothetical_entries.append({
                            "Driver": normalized_name,
                            "Points": gp_points_table[position_number]
                        })
                else:
                    st.warning(f"Unrecognized driver name: {row['Driver']}")

        if hypothetical_entries:
            hypothetical_df = pd.DataFrame(hypothetical_entries)

            if hypothetical_df["Driver"].duplicated().any():
                st.warning("Each driver should only appear once")
            else:
                full_leaderboard_copy = full_leaderboard.copy()
                combined = pd.concat([full_leaderboard_copy[["Driver", "Points", "Track"]], hypothetical_df])
                full_combined_with_track = combined.copy()
                combined = combined.groupby("Driver", as_index=False)["Points"].sum()
                combined = combined.sort_values(by="Points", ascending=False).reset_index(drop=True)
                combined["Position"] = combined.index + 1
                combined["Position"] = combined["Position"].apply(
                    lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
                )

                combined = combined[["Position", "Driver", "Points"]]
                
                st.markdown(f"<h3 style='text-align: center;'>Projected World Drivers Championship</h3>", unsafe_allow_html=True)
                render_leaderboard(combined)
                
        else:
            st.info("Enter at least one driver to see the leaderboard.")

        

        #hypothetical entries cc

        if hypothetical_entries:
            st.markdown(f"<h3 style='text-align: center;'>Projected Constructors Championship</h3>", unsafe_allow_html=True)
    
            alpine_australia_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(alpine_australia_drivers)) &
                (full_combined_with_track["Track"].isin(alpine1_tracks))
            ]
            alpine_australia_points = alpine_australia_only["Points"].sum()
            alpine_imola_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(alpine_imola_drivers)) &
                (full_combined_with_track["Track"].isin(alpine2_tracks))
            ]
            alpine_imola_points = alpine_imola_only["Points"].sum()
            alpine_points = alpine_australia_points + alpine_imola_points

            aston_martin_only = combined[combined["Driver"].isin(aston_martin_drivers)]
            aston_martin_points = aston_martin_only["Points"].sum()

            ferrari_only = combined[combined["Driver"].isin(ferrari_drivers)]
            ferrari_points = ferrari_only["Points"].sum()

            haas_only = combined[combined["Driver"].isin(haas_drivers)]
            haas_points = haas_only["Points"].sum()

            kick_sauber_only = combined[combined["Driver"].isin(kick_sauber_drivers)]
            kick_sauber_points = kick_sauber_only["Points"].sum()

            mclaren_only = combined[combined["Driver"].isin(mclaren_drivers)]
            mclaren_points = mclaren_only["Points"].sum()

            mercedes_only = combined[combined["Driver"].isin(mercedes_drivers)]
            mercedes_points = mercedes_only["Points"].sum()

            red_bull_racing_australia_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(red_bull_racing_australia_drivers)) &
                (full_combined_with_track["Track"].isin(redbull1_tracks))
            ]
            red_bull_racing_australia_points = red_bull_racing_australia_only["Points"].sum()
            red_bull_racing_japan_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(red_bull_racing_japan_drivers)) &
                (~full_combined_with_track["Track"].isin(redbull1_tracks))
            ]
            red_bull_racing_japan_points = red_bull_racing_japan_only["Points"].sum()
            red_bull_racing_points = red_bull_racing_australia_points + red_bull_racing_japan_points

            racing_bulls_australia_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(racing_bulls_australia_drivers)) &
                (full_combined_with_track["Track"].isin(redbull1_tracks))
            ]
            racing_bulls_australia_points = racing_bulls_australia_only["Points"].sum()
            racing_bulls_japan_only = full_combined_with_track[
                (full_combined_with_track["Driver"].isin(racing_bulls_japan_drivers)) &
                (~full_combined_with_track["Track"].isin(redbull1_tracks))
            ]
            racing_bulls_japan_points = racing_bulls_japan_only["Points"].sum()
            racing_bulls_points = racing_bulls_australia_points + racing_bulls_japan_points

            williams_only = combined[combined["Driver"].isin(williams_drivers)]
            williams_points = williams_only["Points"].sum()
            
            cc_leaderboard = pd.DataFrame([
                {"Constructor": "Alpine", "Points": alpine_points},
                {"Constructor": "Aston Martin", "Points": aston_martin_points},
                {"Constructor": "Ferrari", "Points": ferrari_points},
                {"Constructor": "Haas", "Points": haas_points},
                {"Constructor": "Kick Sauber", "Points": kick_sauber_points},
                {"Constructor": "McLaren", "Points": mclaren_points},
                {"Constructor": "Mercedes", "Points": mercedes_points},
                {"Constructor": "Red Bull Racing", "Points": red_bull_racing_points},
                {"Constructor": "Racing Bulls", "Points": racing_bulls_points},
                {"Constructor": "Williams", "Points": williams_points}
            ])

            cc_leaderboard["Points"] = pd.to_numeric(cc_leaderboard["Points"], errors="coerce").fillna(0)
            cc_leaderboard = cc_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)
            cc_leaderboard["Position"] = cc_leaderboard.index + 1
            cc_leaderboard["Position"] = cc_leaderboard["Position"].apply(
                lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
            )

            render_leaderboard(cc_leaderboard)
        else:
            st.write("")


##Interesting Factoid

driver_info = {
    "Alex Albon": """
        **Current Team**: Williams
        **Previous Teams**: Red Bull Junior Team, Toro Rosso (Racing Bulls), Red Bull
        
        **Hometown**: Westminster, London, England
        
        **Championships Prior to Formula 1**:
        - 2006 Super 1 National Honda Cadet Championship and other kartin championships
    
        **Awards**
        - 2019 Richard Millie Rookie of the Year
        
        **Records**:
        - First Thai driver to achieve a podium in Formula 1
     
        **Fun Facts**:
        People joke that he's just the wife of his pro golfer wife
        Previously was teammates with Charles Leclerc in GP3
        """,
    "Andrea Kimi Antonelli": """
        **Current Team**: Mercedes
        **Previous Teams**: N/A
        
        **Hometown**: Bologna, Emilia-Romagna, Italy
        
        **Championships Prior to Formula 1**:
        - 2022 Italian F4 Championship
        - 2022 ADAC Formula 4
        - 2023 Formula Regional Champion

        **Awards**
        - 2024 Dallara Award for Best Overtaking Maneuver 
    
        
        **Records**:
        - Third youngest driver in formula 1 history (18 years old)
        - Second youngest driver to score points in a formula 1 race
        - Youngest driver to lead an F1 race
        - Youngest driver to score the fastest lap in an F1 race
        - Youngest driver to hold pole position for a formula one race in any format
     
        **Fun Facts**:
        - He chose the number 12 as a nod to his idol, Ayrton Senna
        - He passed his driving test six weeks before his F1 debut

        """,
    "Charles Leclerc": """
        **Current Team**: Ferrari
        **Previous Teams**: 
        
        **Hometown**: Monte Carlo, Monaco
        
        **Championships Prior to Formula 1**:
        - 2016 GP3 Series
        - 2017 FIA Formula 2 Championship

        **Awards**
        - 2019 FIA Pole Position Trophy for most pole position starts
        - Lorenzo Bandini Trophy
        
        **Records**:
        - Fourth driver to win GP2/Formula 2 in their rookie season.
        - Second youngest pole-sitter in Formula 1 history
        - First Monegasque driver to win the Monaco Grand Prix in 93 years
     
        **Fun Facts**:
        - Ended Ferrari's record nine-year no-win drought, earning him the nickname "il Predestinato" (the predestined)
        - In 2017, his Charles Leclerc lost his father and in his final days, he told is father a white lie. That he'd made it to Formula 1; that he'd signed the contract. It wasn't true then, but his driving has made it true now, and look what he's done with the opportunity. The grandstands he saw built as a kid growing up now rise for him and for the first time in 93 years, this fabled race is won by one of their own. Charles Leclerc wins the Monaco grand prix to achieve his dream.
        """,
    "Carlos Sainz": """
        **Current Team**: Williams
        **Previous Teams**: Ferrari, Red Bull Junior Team, Renault, McLaren
        
        **Hometown**: Madrid, Spain
        
        **Championships Prior to Formula 1**:
        - 2011 Formula Renault NEC
        - 2014 Formula Renault 3.5 Series
     
        **Fun Facts**:
        Known for singing "Smooth Operator" after particularly good races

        """,
    "Esteban Ocon": """
        **Current Team**: Haas
        **Previous Teams**: Manor, Racing Point, Mercedes reserve driver, Renault/Alpine
        
        **Hometown**: Evreux, Eure, France
        
        **Championships Prior to Formula 1**:
        - 2014 FIA Formula 3 European Championship
        - 2015 GP3 Series
     
        **Fun Facts**:
        Most known for getting punched by Max Verstappen 

        """,
    "Fernando Alonso": """
        **Current Team**: Aston Martin
        **Previous Teams**: Renault, McLaren
        
        **Hometown**: Oviedo, Asturias, Spain
        
        **Championships**:
        - 2005 World Drivers Champion
        - 2006 World Drivers Champion

        **Championships Prior to Formula 1**:
        - 1999 Euro Open by Nissan

        **Awards**
        - 2003 Autosport Gregor Grant Award
        - 2005 Lorenzo Bandini Trophy
        - FIA Hall of Fame for being a F1 World Champion and FIA World Endurance Champion.
        - 2005 F1 World Drivers' Champion
        - 2006 F1 World Drivers' Champion
        
        **Records**:
        - First driver to be inducted into the FIA Hall of Fame twice
        - Only driver to have won both the Formula One World Drivers' Championship and the World Endurance Drivers' Championship
        - Then-youngest polesitter
        - First World Drivers' Champion from Spain, then-youngest in Formula 1 history (24 years old)
     
        **Fun Facts**:

        """,
    "Gabriel Bortoleto": """
        **Current Team**: Sauber (to be Audi)
        **Previous Teams**: McLaren Driver Development Program
        
        **Hometown**: Sao Paulo, Brazil
        
        **Championships Prior to Formula 1**:
        - 2023 FIA Formula 3 World Champion
        - 2024 FIA Formula 2 Champion
    

        **Awards**
        - 2024 FIA Rookie of the Year
        - 2024 Anthoine Hubert Award
    
        
        **Records**:
        - First driver to win from last in the grid in either Formula 2 or Formula 1
        - Seventh driver in history to win the GP2/Formula 2 title in their rookie season
     
        **Fun Facts**:
        - He's a protoge of current Aston Martin driver Fernando Alonso
        - Elphaba in the 2025 Chinese GP Wicked Poster recreation

        """,
    "George Russell": """
        **Current Team**: Mercedes
        **Previous Teams**: Williams
        
        **Hometown**: King's Lynn, Norfolk, England
        
        **Championships Prior to Formula 1**:
        - 2014 BRDC F4 Championship
        - 2017 GP3 Series
        - 2018 FIA Formula 2 Championship

        **Awards**
        - 2014 Autosport BRDC Award
        - 2022 Hawthorn Memorial Trophy
        - 2024 Lorenzo Bandini Trophy
        
        **Records**:
        - Second driver to win both the GP3 and Formula 2 in their rookie season
        - Fifth driver in history to win GP2/Formula 2 in their rookie season
     
        **Fun Facts**:
        - He's considered an "instinctive" driver, often compared to Lewis Hamilton's driving style. He brakes earlier to carry more speed through the corner. 
        - Apparently really really good at tire management?
        - Once cried happy tears getting p9

        """,
    "Isack Hadjar": """
        **Current Team**: Racing Bulls
        **Previous Teams**: N/A
        
        **Hometown**: Paris, France
        
        **Championships Prior to Formula 1**:
        - 2023 Runner up FIA Formula 2 champion

        **Awards**
        - 2024 Aramco Best Performance for Melbourne
        
        **Records**:
        N/A
     
        **Fun Facts**:
        - He destroyed ze caaaa!
        - Nicknamed "Le Petit Prost" in France
        - His father is a researcher in quantum mechanics and features physics formulas on his racing helmet.

        """, 
    "Jack Doohan": """
        **Current Team**: Alpine
        **Previous Teams**: Red Bull Junior Team
        
        **Hometown**: Gold Coats, Queensland, Australia
        
        **Championships Prior to Formula 1**:
        - 2015 Australian Kart Championship

        **Awards**
        N/A
        
        **Records**:
        - First F2 driver to take pole position, record the fastest lap, lead every lap, and win the race at the 2023 Hungarian GP. 
     
        **Fun Facts**:
        - Galinda in the 2025 Chinese GP Wicked poster recreation
        - Son of motorcycle world champion Mick Doohan
        - His first gokart was gifted to him by Michael Schumacher

        """,
    "Lewis Hamilton": """
        **Current Team**: Ferrari
        **Previous Teams**: Mercedes, McLaren, McLaren-Mercedes Young Driver Programme
        
        **Hometown**: Stevenage, Hertfordshire, England

        **Championships**:
        - 2008 World Drivers Champion
        - 2014 World Drivers Champion
        - 2015 World Drivers Champion
        - 2017 World Drivers Champion
        - 2018 World Drivers Champion
        - 2019 World Drivers Champion
        - 2020 World Drivers Champion
        
        **Championships Prior to Formula 1**:
        - Formula 3 Euro Series Champion
        - GP2 Series Champion

        **Awards**
        - 2007 Pride of Britain Award
        - 2017 FIA Hall of Fame
        - 2018 PETA Person of the Year
        - 2019 Honorary Fellow of the Royal Academy of Engineering
        - 2020 Time's 100 most influential people globally
        - Literally too many to list them all
        
        **Records**:
        - 2008 then-youngest World Drivers Champion.
        - Tied for most world drivers championships (7)
        - All-time Win record (105 GP wins)
        - He is number 1, 2, 4, and 7 for most wins at a grand prix, tied three ways with himself in 7th (most wins at the British, Hungarian, Canadian, US, Chinese, and Spanish GP)
     
        **Fun Facts**:
        - Partial owner of the Denver Broncos 
        - Some people (including other F1 drivers)consider him an eight time world champion rather than seven, citing the controversial 2021 Abu Dhabi Grand Prix which resulted in Max Verstappen's first WDC win.
        - In the 2014-2016 seasons, Hamilton and his driving partner Rosberg won 51 of 59 grand prixs. 
        - His yellow helmet is a nod to late F1 driver Ayrton Senna

        """,
    "Liam Lawson": """
        **Current Team**: Racing Bulls
        **Previous Teams**: Redbull Racing
        
        **Hometown**: Hastings, New Zealand
        
        **Championships Prior to Formula 1**:
        - 2019 Toyota Racing Series
        - 2016-2017 New Zealand FFord

        **Awards**
        N/A
        
        **Records**:
        - Fastest driver replacement in F1 history, competing in only two races. (Previous record when Verstappen replaced Kvyat after four races, also in Redbull)
     
        **Fun Facts**:
        - His number 30 is in honor of his karting mentor
        - Huge Lightning Mcqueen fan

        """,
    "Lando Norris": """
        **Current Team**: McLaren
        **Previous Teams**: N/A
        
        **Hometown**: Glastonbury, England
        
        **Championships Prior to Formula 1**:
        - 2015 MSA Formula Champioship
        - 2016 Toyota Racing Series
        - 2016 Formula Renault Eurocup
        - 2016 Formula Renault NEC
        - 2017 Formula 3 European Championship

        **Awards**
        - 2016 Autosport BRDC
        
        **Records**:
        - Youngest driver to ever set a pole position at a national meeting (7 years old)
        - Youngest karting world championship winner (14 years old)
        - Tied for most podiums before taking a first win
        
        **Fun Facts**:
        - Used to be called Lando "No Wins" Norris
        """,
    "Lance Stroll": """
        **Current Team**: Aston Martin 
        **Previous Teams**: Williams, Ferrari Driver Academy
        
        **Hometown**: Montreal, Quebec, canada
        
        **Championships Prior to Formula 1**:
        - 2014 Italian F4 Championship
        - 2015 Toyota Racing Series
        - 2016 FIA Formula 3 European Championship

        **Awards**
        - Canadian Motorsport Hall of Fame Rising Star Award
        
        **Records**:
        - Then-second youngest driver to score a podium finish (18)
        - Most formula 1 race starts without ever claiming a fastest lap
     
        **Fun Facts**:
        - His daddy owns the company (my father will hear about this!)
        - He speaks five languages and is a whiner in all of them

        """,
    "Max Verstappen": """
        **Current Team**: Redbull
        **Previous Teams**: 
        
        **Hometown**: Hasselt, Flanders, Belgium
        
        **Championships**:
        - 2021 World Drivers Champion
        - 2022 World Drivers Champion
        - 2023 World Drivers Champion
        - 2024 World Drivers Champion

        **Championships Prior to Formula 1**:
        A lot of karting
        - 2014 Zandvoort Masters
    

        **Awards**
        - 2015, 16, 19 FIA Action of the year
        - 2015 FIA Rookie of the Year
        - 2016 Lorenzo Bandini Trophy
        - 2024 Time's 100
    
        
        **Records**:
        - First driver since his father to win two european karting champions in the same season
        - First driver to win two european karting championships in direct-driver and gearbox classes
        - Youngest ever driver to win gearbox World Championship, beating out Charles Leclerc who is just a month younger
        - Longest time leading the F1 Drivers' World Championship (1007 days)
        - First driver to win from 10 different grid positions
        - Youngest driver to take first place in an F1 race weekend (17 and 3 days)
        - Youngest driver to race in F1 (17 and 166 days)
        - Youngest driver to score points in F1 (17 and 180 days)
        - Youngest F1 race winner (18 and 228 days) until 2025
        - Youngest to set a fastest lap (19 and 44 days) until 2025
        - Youngest to score an F1 grand slam (taking pole, fastest lap, victory while leading every lap of the race) (23 and 277 days)
        - Most podoum finishes in an F1 season (20)
        - Most world championship points in a season (549)
        - Most wins in an F1 season (18)
        - Most consecutive race wins (10)
        - Highest percentage of wins in a season (77.27%)
        - Most consecutive points scored in F1 (1055)
        - Most consecutive pole positions (8, tied with Ayrton Senna)
        - First driver to win the championship driving for a third-placed constructor in 41 years
        - (a lot more, this guy is no joke)
     
        **Fun Facts**:
        - Son of former Formula 1 driver Jos Verstappen and Belgian kart racr Sophie Kumpen
        - Very upsetty spaghetti about Liam Lawson being demoted
        - Bonus dad
        - Under the fake name of "Franz Hermann", Max recently tested a ferrari GT3 car, setting the lap record on the track during this session on a full tank of gas
        

        """,
    "Nico Hulkenberg": """
        **Current Team**: Kick Sauber
        **Previous Teams**: Williams, Renault, Aston Martin
        
        **Hometown**:Emmerich am Rhein, North Rhine-Westphalia, West Germany
        
        **Championships Prior to Formula 1**:
        - 2015 24 Hours of Le Mans
        - 2007 Masters of Formula 3
        - 2008 Formula 3 Euro Series
        - 2009 GP2 Series

        **Awards**
        - Gregor Grant Award 
    
        
        **Records**:
        - Most races without a win (229, ongoing)
        - Third driver in history to win GP2/Formula 2 in their rookie season
        - First active F1 driver to win Le Mans in over 2 decades
     
        **Fun Facts**:
        - He's a dad
        - Huuuuuuuuuulkenberg

        """,
    "Oliver Bearman": """
        **Current Team**: Haas
        **Previous Teams**: Ferrari Drier Academy, reserve for Ferrari and Haas in 2024
        
        **Hometown**: Havering, London, England
        
        **Championships Prior to Formula 1**:
        - 2021 Italian F4 Championship
        - 2021 ADAC F4 Championship

        **Awards**
        - 2021 Henry Surtees Award
        - 2023 Pirelli Highlight of the Year Award
        
        **Records**:
        - Youngest driver to compete for Ferrari
        - First driver to debut with Ferrari since 1972
        - Third youngest driver to score points in F1
        - Youngest driver to test in F1
     
        **Fun Facts**:
        - When Carlos Sainz came down with appendicitis, he had to race for Ferrari in 2024 at the Saudi Arabian Grand Prix, known as one of the most difficult and highest speed tracks. He placed p7, ahead of Lewis Hamilton and Lando Norris. 
        - Crashed into the wall twice on his F1 Debut Grand Prix, earning him the rather harsh nickname, "Ollie in the Wallie"
        - Once him and Kimi Antonelli stole his manager's credit card and over the course of two hours ordered MANY many things to be delievered to the managers house
        """,
    "Oscar Piastri": """
        **Current Team**: McLaren
        **Previous Teams**:
        Test driver for Alpine Renault
        
        **Hometown**: Melbourne, Australia
        
        **Championships Prior to Formula 1**: 
        - 2019 Formula Renault Eurocup
        - 2020 FIA Formula 3
        - 2021 FIA Formula 2

        **Awards**
        - FIA Rookie of the Year: 2021, 2023
        - Autosport Awards Rookie of the Year: 2020, 2021, 2023
        - March 2025 Overtake of the Month Award 
        
        **Records**:
        - Only driver in history to win Formula Renault, Formula 3, and Formula 2 championships in consecutive seasons
        - Sixth driver in history to win GP2/Formula 2 title in rookie season. 
        - Second highest points driver in their F1 rookie season (97 points, current record held by Lewis Hamilton at 105)

        **Fun Facts**:
        - Red Bull Racing principal Christian Horner has said he regrets not signing Piastri while he was running in Formula 4
        - McLaren and Alpine went to court fighting over Piastri after he was both a reserve driver for McLaren and a test driver for Alpine in 2022
        """,
    "Pierre Gasly": """
        **Current Team**: Alpine
        **Previous Teams**: Redbull Jr Team, Racing Bulls, Red Bull
        
        **Hometown**: Rouen, Seine-Maritime, France
        
        **Championships Prior to Formula 1**:
        - 2013 Formula Renault Eurocup
        - 2016 GP2 Series

        **Awards**
        N/A
        
        **Records**:
        - Only current F1 driver to have never lost a full season points battle head to head. 
        - 2024 No crash damage
     
        **Fun Facts**:
        - He was close friends with Anthoine Hubert, who passed during an F2 race in 2019 and who Gasly still races for
        - He has achieved 3 of his 5 F1 podiums starting from 10th place or lower

        """,
    "Yuki Tsunoda": """
        **Current Team**: Redbull
        **Previous Teams**: Racing Bulls
        
        **Hometown**: Sagamihara, Kanagawa, Japan
        
        **Championships Prior to Formula 1**:
        - 2016 Super FJ All-Japan Final
        - 2017 JAF Japan F4 East Series
        - 2018 F4 Japanese Championship

        **Awards**
        - 2020 FIA Rookie of the Year
        - 2020 Anthoine Hubert Award
        
        **Records**:
        - Youngest Japanese F1 driver in history
     
        **Fun Facts**:
        - He's just a little guy who swears like a sailor
        - Needs a step stool to get into the car

        """,
}

if option == "**Driver Information**":
    text_input = st.text_input("enter a driver")
    driverstats = None

    if text_input is None:
        st.write("")
    if text_input in AA23_valid_names:
        driverstats = "Alex Albon"
        driver_name = "Alexander Albon"
        st.image(driver_photos[driver_name], width=200)
    elif text_input in AKA12_valid_names:
        driverstats = "Andrea Kimi Antonelli"
        driver_name = "Kimi Antonelli"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in CL16_valid_names:
        driverstats = "Charles Leclerc"
        driver_name = "Charles Leclerc"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in CS55_valid_names:
        driverstats = "Carlos Sainz"
        driver_name = "Carlos Sainz"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in EO31_valid_names:
        driverstats = "Esteban Ocon"
        driver_name = "Esteban Ocon"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in FA14_valid_names:
        driverstats = "Fernando Alonso"
        driver_name = "Fernando Alonso"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in GB5_valid_names:
        driverstats = "Gabriel Bortoleto"
        driver_name = "Gabriel Bortoleto"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in GR63_valid_names:
        driverstats = "George Russell"
        driver_name = "George Russell"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in IH6_valid_names:
        driverstats = "Isack Hadjar"
        driver_name = "Isack Hadjar"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in JD7_valid_names:
        driverstats = "Jack Doohan"
        driver_name = "Jack Doohan"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in LH44_valid_names:
        driverstats = "Lewis Hamilton"
        driver_name = "Lewis Hamilton"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in LL30_valid_names:
        driverstats = "Liam Lawson"
        driver_name = "Liam Lawson"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in LN4_valid_names:
        driverstats = "Lando Norris" 
        driver_name = "Lando Norris"
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in LS18_valid_names:
        driverstats = "Lance Stroll"
        driver_name = driverstats
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in MV33_valid_names:
        driverstats = "Max Verstappen"
        driver_name = driverstats
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in NH27_valid_names:
        driverstats = "Nico Hulkenberg"
        driver_name = driverstats
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in OB87_valid_names:
        driverstats = "Oliver Bearman"
        driver_name = driverstats
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in OP81_valid_names:
        driverstats = "Oscar Piastri"
        driver_name = driverstats
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in PG10_valid_names:
        driverstats = "Pierre Gasly"
        driver_name = driverstats
        st.image(driver_photos[driver_name], width= 200)
    elif text_input in YT22_valid_names:
        driverstats = "Yuki Tsunoda"
        driver_name = driverstats
        st.image(driver_photos[driver_name], width= 200)

        
    if driverstats in driver_info:
        st.markdown(driver_info[driverstats], unsafe_allow_html=True)
    else:
        st.write("")

        
##TRACK INFORMATION

if option == "**Track Information**":

    track = st.selectbox("Choose a Circuit",
                 ["Australia",
                  "China",
                  "Japan",
                  "Bahrain",
                  "Saudi Arabia",
                  "Miami",
                  "Imola",
                  "Monaco",
                  "Spain",
                  "Canada",
                  "Austria",
                  "Great Britain",
                  "Belgium",
                  "Hungary",
                  "Netherlands",
                  "Italy",
                  "Azerbaijan",
                  "Singapore",
                  "United States",
                  "Mexico",
                  "Brazil",
                  "Las Vegas",
                  "Qatar",
                  "Abu Dhabi"
        ])

    if track in ["Australia", "China", "Japan", "Bahrain"]:
        st.write("we already passed this before i made it so i snooze you lose")
    elif track == "Saudi Arabia":
        st.image("https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Saudi_Arabia_Circuit")
        st.subheader("**Lap Record:** 1:30.734")
        st.subheader(f"**2024 Winner:** Max Verstappen")
        st.write("**Important Notes:**")
        st.write("Safety car occurance: 100%")
        st.write("Many corners are quite difficult because they're highspeed and blind, with legends like Schumacher even crashing")
        st.write("With three DRS zones and many high speed corners, there are many overtaking opportunities.")
        st.write("**Fun Moments:**")
        st.write("Ollie Bearman's 2024 F1 Debut: Ollie filled in for Carlos Sainz on Ferrari and placed p7 ahead of Lando Norris and Lewis Hamilton")
    elif track == "Miami":
        st.image("https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit")
        st.subheader("**Lap Record: 1:29.708**")
        st.text("Max Verstappen, 2023")
        st.subheader("**2024 Main Race Winner:** Lando Norris")
        st.subheader("**2024 Sprint Race Winner:** Max Verstappen")
        st.write("**Important Notes**")
        st.write("The track is considered a street circuit. So far in the 2025 season, Red bull has had advantages on street circuts")
        st.markdown('''
                The track features many high speed turns, but also includes an extremely low speed corner section, where cars remain in low gears throughout turns 11-16.  
                High speed corners will favor drivers such as Oscar Piastri and Lando Norris due to driving style and the style of the MCL39. The low speed corners will allow drivers with more downforce-heavy cars or with a different driving style to catch up, such as Max Verstappen and Charles Leclerc or the Williams drivers.
            ''')
        st.write("It's often compared to the Melbourne circuit because of their similarities, which Lando Norris won in 2025. Oscar Piastri exhibited great pace but a rain storm took him out of the running, and Max Verstappen put up a valiant effort for first place")
        st.write("Miami 2024 marks Lando Norris' first F1 race win, ending his streak as Lando 'No Wins' Norris")
    elif track == "Imola":
        st.image("https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Emilia_Romagna_Circuit")
        st.markdown('''
                :red-background[**2024 Winner:**] Max Verstappen
                
                :red-background[**Lap Record:**] 1:15.484 by Lewis Hamilton in a Mercedes
                
                **Important Information**
                - Historically 100% rate of a safety car occurance
                - As it's one of the two races in Italy, Ferrari will be looking to win this one for their home race!
                - Despite being narrow, it's still an exciting race and many drivers are in love with the track
                - Ayrton Senna still holds the record of most consecutive pole positions in Imola, which he scored before his tragic accident in Imola in 1994 alongside fellow driver Roland Ratzenberger
            ''')
    else:
        st.write("be patient")

##CONSTRUCTION INFORMATION

alpine_valid_names = ("Alpine", "alpine", "renault", "A525")
aston_martin_valid_names = ("Aston Martin", "aston martin", "Aston", "aston", "Aston martin")
ferrari_valid_names = ("Ferrari", "ferrari", "Scuderia Ferrari", "scuderia ferrari", "SF25")
kick_sauber_valid_names = ("Kick Sauber" "Kick sauber", "kick sauber", "Kick", "kick")
haas_valid_names = ("Haas", "haas")
mclaren_valid_names = ("McLaren", "mclaren", "Mclaren", "McLaren Mercedes", "mclaren mercedes", "MCL39", "MCL38")
mercedes_valid_names = ("Mercedes", "mercedes", "Merc", "merc", "F1 W16", "W16")
redbull_valid_names = ("Red Bull", "Redbull", "redbull", "Red bull", "red bull", "RB21")
racing_bulls_valid_names = ("Racing Bulls", "Racing bulls", "racing bulls", "VCARB", "vcarb")
williams_valid_names = ("Williams", "williams")


if option == "**Construction Information**":
    #specific team information cont. 
    text_input = st.text_input("enter a constructor")
    if text_input in alpine_valid_names:
        st.markdown("**BWT Alpine**")
        st.markdown('''
                    Constructor: Alpine  
                    Engine: Renault  
                    2025 Car Name: A525
            ''')
        st.markdown('''
                    :gray[Suspension Configuration: Pushrod-pushrod]  
                    :gray[Sidepod Configuration: Underbite]  
                    :gray[Sidepod Inlet: N/A]  
                    :gray[Nose Configuration: Second-element]
            ''')
        st.image("https://cdn-8.motorsport.com/images/amp/0qXxlBy6/s6/alpine-a524.jpg")
        st.caption("The A525 with its unconventional underbite sidepod design")
    elif text_input in aston_martin_valid_names:
        st.markdown("**Aston Martin Aramco**")
        st.markdown('''
                    Constructor: Aston Martin  
                    Engine: Mercedes-AMG  
                    2025 Car Name: AMR25
            ''')
        st.markdown('''
                    :gray[Suspension Configuration: Pushrod-pushrod]  
                    :gray[Sidepod Configuration: Overbite]  
                    :gray[Sidepod Inlet: High rectangular]  
                    :gray[Nose Configuration: Second-element]
            ''')
        st.image("https://www.racefans.net/wp-content/uploads/2025/02/racefansdotnet-24-02-23-17-29-33-3-racefansdotnet_aston_martin_amr25_34.jpg")
        st.markdown('''
                :red-background[2026]
                In 2026, the Aston Martin team will take over the Honda engine manufactorer, which is currently working with the Red bull teams. 
            ''')
    elif text_input in ferrari_valid_names:
        st.markdown("**Scuderia Ferrari HP**")
        st.markdown('''
                    Constructor: Ferrari  
                    Engine: Ferrari  
                    2025 Car Name: SF25
            ''')
        st.markdown('''
                    :gray[Suspension Configuration: Pullrod-pullrod]  
                    :gray[Sidepod Configuration: Overbite]  
                    :gray[Sidepod Inlet: P shape]  
                    :gray[Nose Configuration: Second-element]
            ''')
        st.image("https://cdn.ferrari.com/cms/network/media/img/resize/67c83837d12cab001f5ef82d-ferrari-sf-25-social-card-esp?width=1080")
        st.markdown('''
                    :red-background[Significant Changes to the 2025 Car:]  
                    :gray[Changed from a pushrod-pullrod to a dual pullrod suspension]  
                    :gray[Altered the floor and venturi-channel design]
            ''')
        st.divider()
        st.markdown('''
                :red-background[2025 Car]  
                The SF25 chassis includes the same overbite side pod design used in the second half of 2024 and used by most constructors in 2025.
                Their overbite has a sharp, p-shaped inlet for more a more aggressive undercut. It directs the air quickly onto the floor of the car to increase downforce. This is only also seen on the Ferrari car for the 2025 season.  
                  
                Both cars have pushed the inlet right inside the overbite, which allows for a midwing that is more available for utilization. However, these changes make the ride-height of the car incredibly important, meaning any excessive damage to the skid block of the car could greatly affect the side-pod aerodynamics.
                The SF25 is less sensitive than the MCL39, because their inlet is less aggressive, allowing for a more dynamic car. It's also less of a committment, and much more easily adaptable throughout the season.
            ''')
        st.image("https://cdn-3.motorsport.com/images/amp/0RrXg7V0/s6/ferrari-sf-25-technical-detail.jpg")
        st.divider()
        st.markdown('''
                One of the biggest shifts from the SF24 is a change from a pushrod to a pullrod configuration in the front suspension, maintaining the pullrod configuration in the rear.
                Ferrari also uses a pullrod in their rear suspension, and is one of only three constructors to do so. Ferrari is the only constructor currently using a pullrod-pullrod front-rear suspension configuration, with more teams using a pullrod-pushrod or pushrod-pushrod configuration.
            ''')
        st.image("https://www.raceteq.com/-/jssmedia/raceteq/articles/2025/03/2025-preseason-tech/2025-ferrari-suspension-f1.jpg?cx=0.5&cy=0.5&cw=1440&ch=670")
        st.markdown('''  
                A pullrod suspension will pull the suspension backwards when the car goes over a kerb or bump. This will generate more downforce when the car is met with resistance.
                Pullrods also face the rear of the car, meaning they will help with aerodynamics and pushing the airflow as it comes through the front wing.  
                However, while it physically and aerodynamically produces downforce, the pullrod can make mechanical downforce incredibly sensitive, and going over kerbs can be detrimental (as seen at the Saudi GP with Lando Norris' pullrod MCL39). Having a pullrod-pullrod configuration will only make this effect more dramatic.
            ''')
        st.image("https://www.raceteq.com/-/jssmedia/raceteq/articles/2025/03/pullrod-pushrod-2025/tr-comparison-pullrod-pushrod--1-1-1.jpg?cx=0.5&cy=0.5&cw=1440&ch=670")
        st.caption("pullrod vs pushrod configurations in formula 1 car front suspension. the pullrod front suspension configuration is currently being run by ferrari, mclaren, redbull, racing bulls, and kick sauber")
        st.divider()
        st.markdown('''
                The team has also altered their floor and venturi-channel design to generate greater downforce. The Venturi channel is an aerodynamically-generated low pressure zone which pulls the car closer to the ground, creating the bobbing up and down visual and also allowing the cars to drive on the ceiling at top speeds. This will improve the cars grip in all circuits, but the improved venturi channels will give the car an advantage in banked corners.
                However, a car that relies too much on the venturi effect will struggle in the dirty air of a car it's trailing.  
            ''')
        st.image("https://www.raceteq.com/-/jssmedia/raceteq/articles/2025/03/2025-preseason-tech/side-view-f1-ferrari-2025.jpg?cx=0.5&cy=0.5&cw=1440&ch=670")
        st.divider()
        st.markdown('''
                Overall, it appears the SF25 will show some dominance in clean air, as seen by Lewis Hamilton's sprint win in China. In China it was also exhibited just how much of the downforce is dependent on this reaction, as Charles Leclerc was able to drive a functional and still advantageous car with a broken front wing.
            ''')
    elif text_input in haas_valid_names:
        st.markdown("**Moneygram Haas F1 Team**")
        st.markdown('''
                    Constructor: Haas 
                    Engine: Mercedes-AMG  
                    2025 Car Name: VF25
            ''')
        st.markdown('''
                    :gray[Suspension Configuration: Pushrod-pullrod]  
                    :gray[Sidepod Configuration: Overbite]  
                    :gray[Sidepod Inlet: Hooped]  
                    :gray[Nose Configuration: Main-plane]
            ''')
    elif text_input in kick_sauber_valid_names:
        st.write("coming soon")
    elif text_input in mclaren_valid_names:
        st.markdown("**McLaren Mercedes**")
        st.markdown('''
                    Constructor: Mclaren  
                    Engine: Mercedes  
                    2025 Car Name: MCL39
            ''')
        st.markdown('''
            :gray[Suspension Configuration: Pullrod-pushrod]  
            :gray[Sidepod Configuration: Overbite]  
            :gray[Sidepod Inlet: P shape]  
            :gray[Nose Configuration: Second-element]
            ''')
        st.image("https://mclaren.bloomreach.io/cdn-cgi/image/format=webp,quality=80/delivery/resources/content/gallery/mclaren-racing/formula-1/2025/nsr/f1-75-live-m/web/mcl39-papaya-pr-inline-7.jpg")
        st.caption("MCL39 livery as presented by McLaren")
        st.markdown('''
            :red-background[Significant Changes to the 2025 Car:]  
            :gray[Changed the traditional overbite inlet to a P shaped inlet and raised the overbite]
            :gray[Loss of the flexi-wing mini-DRS system]
            :gray[Minor changes in vaning to conduct low pressure zones]
            :gray[Changes to brake cooling]
            ''')
        st.divider()
        st.markdown('''
                    :red-background[2024 Car]  
                    The McLaren car sported what was called "mini DRS", a flexible rear wing that allowed the car to gain an aerodynamic advantage in non-DRS zones such as high speed corners or short straightaways. 
                    This allowed them to easily gain an advantage against other cars.
                    While legal in 2024, it was eventually banned due to safety concerns, with strict restrictions on the flexibility of the rear wing being in place for 2025 and onward.  
                    The system worked by making an extremely flexible rear wing, which flexed downwards in top speeds, opening small spaces between the wing and the edge to allow more air flow beneath the wing, reducing drag and giving the car a few mph advantage.
            ''')
        st.image("https://autoracer.it/wp-content/uploads/2024/12/McLaren-mini-DRS-1024x705.webp")
        st.caption("image render of the mini DRS system used by McLaren in 2024")
        st.divider()
        st.markdown("In 2024, the McLaren also famously sported a spike on the front wing, which was meant to discourage close quarter battles with passing cars as it threatened easy tire punctures." \
        "This was seen as too aggressive and heavier regulations were put in place by the FIA to prevent these spikes.")
        with st.container():
            st.markdown("""
                <div style="display: flex; justify-content: center; gap: 20px;">
                    <div style="flex: 1; text-align: center;">
                        <img src="https://cdn-5.motorsport.com/images/amp/Y99DgD8Y/s6/mclaren-mcl38-front-wing-endpl.jpg" width="100%">
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmUWcPxLvZgie5rKpi_kmmmZycfHXjXDoYIA&s" width="37.5%">
                    </div>
                </div>
            """, unsafe_allow_html=True) 
        st.write("")
        st.divider()
        st.markdown('''
                :red-background[2025 Car]  
                Overall the car is optimized for aerodynamic efficency, giving them an advantage in circuits with many high speed corners but leaving them vulnerable in low-speed high-downforce corners.    
                      
                The MCL39 chassis includes the same overbite side pod design used in the MCL38 and used by most constructors in 2025.
                Their overbite has a sharp, p-shaped inlet for more a more aggressive undercut. It directs the air quickly onto the floor of the car to increase downforce. This is only also seen on the Ferrari car for the 2025 season.  
                Both cars have pushed the inlet right inside the overbite, which allows for a midwing that is more available for utilization. However, these changes make the ride-height of the car incredibly important, meaning any excessive damage to the skid block of the car could greatly affect the side-pod aerodynamics.
            ''')
        st.image("https://preview.redd.it/mcl38-vs-mcl39-sidepods-comparison-v0-8k7nppezxwie1.jpeg?auto=webp&s=4cbcbc03d9f4cdf84d03022eac69e3cfe8a8e7ae")
        st.caption("The inlet is highlighted in green. This is the 'stealth livery' used in Bahrain testing for the 2025 McLaren, which is why it's difficult to see")
        st.divider()
        st.markdown('''
                    Despite the loss of mini DRS, the McLaren car has started the season with a clear advantage over other cars.  
                      
                    While the regulations around rear wing flexing were tightened during the 2025 season, teams were allowed rear wing flexing up to 2mm until the Suzuka grand prix, where it was limited to 0.5mm due to exploiting by teams. McLaren claims to have not needed to change their rear wing due to this regulation change.
                    However, the flow vis demonstrated during testing appeared to show altered aerodynamics around the rear wing, which appear similar to that seen with a flexi-wing system.
            ''')
        st.image("https://d3cm515ijfiu6w.cloudfront.net/wp-content/uploads/2025/02/26140009/McLaren-MCL39-flo-viz-rear-end.jpg")
        st.caption("Green flow vis paint patterns on the McLaren car in Bahrain preseason testing, used to visualize aerodynamics")
        st.markdown('''
                    However, this could also be explained by the slightly raised main-plane trailing edge, which would not be flexible but still exhibit similar effects as mini-DRS. It is not the same part of the car that would flex in a traditional mini-DRS system, and is technically legal for the 2025 season.
            ''')
        with st.container():
            st.markdown("""
                <div style="display: flex; justify-content: center; gap: 20px;">
                    <div style="flex: 1; text-align: center;">
                        <img src="https://d3cm515ijfiu6w.cloudfront.net/wp-content/uploads/2025/03/11142959/McLaren-MCL39-rear-wing-tip.jpg" width="100%">
                        <p style="font-size: 0.9em;">MCL39 Rear Wing System</p>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <img src="https://d3cm515ijfiu6w.cloudfront.net/wp-content/uploads/2025/03/14092909/RED-BULL-RB21-REAR-WING-COMPARISON.jpg" width="100%">
                        <p style="font-size: 0.9em;">RB21 Rear Wing System</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.divider()
        st.markdown('''
                    Other improvements higlighted in the image below include:  
                    Anti-diving front wing suspension to prevent the car diving forward under braking (blue).  
                    A changed vane on the sidepod of the car, meant to change how the aerodynamics work surrounding the cockpit. Oftentimes these will help create low pressure zones close to the car (purple).  
                    Changes to the sidepod inlet, brake ducts, and airbox (yellow)
            ''')
        st.image("https://www.raceteq.com/-/jssmedia/raceteq/articles/2025/03/2025-preseason-tech/2024-mclaren-vs-2025-mclaren-f1-car.jpg?cx=0.5&cy=0.5&cw=1440&ch=670")
        st.caption("Differences between MCL38 (2024) and MCL39")
        st.markdown('''      
                    Due to some problems with the water system (Piastri in Bahrain), there is speculation that McLaren has moved their drink system to sit in front of the driver in the nose of the car rather than behind, a move they would have copied from Redbull.
                    The advantage to this is that throughout the race, the weight of the drink will move back out of the nose further into the rear of the car, allowing for real time weight adjustment throughout the race, which typically is not allowed due to Park Ferme rules. 
                    At the beginning of the race, the drink is in the front of the car, pushing the front nose and wing downwards to improve downforce early on. Later, as the drink is used and the weight is shifted to the back of the car, it can add downforce to the rear, improving rear tyre grip. It also brings the weight away from the front tyres, which will deteriorate quicker with added weight.
                    It also just keeps their drink colder since it is further away from the engine, as the cockpit of the car can get as high as 140oF
            ''')
        st.markdown('''
                    :red-background[The Mclaren Mystery]  
                    In the 2025 season, McLaren seems to have a heavy advantage over it's competitors in regards to it's rear tyre temperature management.
                    This has led to accusations of using water in the tyres to keep them cool, but after an FIA investigation it has been revealed that the cars are up to regulation. However, it's still a mystery what exactly the MCL39 is doing to optimize tyre management.
            ''')
    elif text_input in mercedes_valid_names:
        st.markdown("**Mercedes-AMG Petronas F1 Team**")
        st.markdown('''
                    Constructor: Mercedes  
                    Engine: Mercedes  
                    2025 Car Name: F1 W16
            ''')
        st.markdown('''
            :gray[Suspension Configuration: Pushrod-pushrod]  
            :gray[Sidepod Configuration: Overbite]  
            :gray[Sidepod Inlet: Shark]  
            :gray[Nose Configuration: Mainplane and second element front noses available. Using second-element nose]
            ''')
        st.image("https://cdn-3.motorsport.com/images/amp/Yv8yOnj0/s6/mercedes-f1-w16-technical-deta.jpg")
        st.markdown('''
            Mercedes seems to have taken heavy inspiration from the RB20 sidepod design, which Redbull appeared to have success with. Splitting the overbite's inlet into a horizontal and vertical inlet (nicknamed the shark inlet) allows the car to have a much larger undercut.  
                      
            The shark inlet itself has high aerodynamic capabilities, but is less effective in hotter races as it limits space for cooling. This could be why the W16 struggled more than we typically see in Jeddah, with the first non-podium finish for the primary driver, George Russell.
            ''')
        st.markdown("""
                <div style="display: flex; justify-content: center; gap: 20px;">
                    <div style="flex: 1; text-align: center;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYDsiu7z70eRmbn2rHgHKqLvXxDhqSlWaLNQ&s" width="100%">
                        <p style="font-size: 0.9em;">2025 Mercedes Shark Inlet compared to 2024 Red Bull</p>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRHxF8wKhz2FrubqTOg17uEHXdmRm8PnMYHg&s" width="100%">
                        <p style="font-size: 0.9em;">W15 and W16 inlet design, from vertical to shark</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('''
            An aggressive undercut allows the car to have enhanced rearwing downforce and grip. It also cleanly and quickly directs a lot of air at once into the venturi channels. However, deep undercuts take away a lot of space for cooling systems. In addition, it can make the car incredibly sensitive to ride height. 
            ''')
        st.divider()
        st.markdown('''
            The dual push-rod configuration is currently being used by Mercedes, Aston Martin, Alpine, and Williams. It's the second-most popular configuration, behind the pullrod-pushrod configuration used by five teams.   
            It's possible this is another inspiration from Red bull, who used a pushrod-pushrod configuration in the championship winning RB19 and the RB20. However, for the 2025 season, most top contenders sport a pullrod front suspension, which makes the W16 unique.  
            The front suspension pushrod allows greater flexibility in adjusting the frontwing throughout the season. The configuration will push the suspension towards the tires when the car is met with resistance such as a kerb or bump. The rod configuration will allow the car to be more durable to changes in the airflow, but can harm aerodynamics if they push the air towards the center of the car, in theory.            
            ''')
        st.image("https://www.raceteq.com/-/jssmedia/raceteq/articles/2025/03/pullrod-pushrod-2025/tr-comparison-pullrod-pushrod--1-1-1.jpg?cx=0.5&cy=0.5&cw=1440&ch=670")
        st.caption("pull rod vs push rod design in the front suspension")
        
        st.markdown('''
            If engineered correctly, it's possible that the placement of the pushrods would push some air towards the front nose of the car, which on the surface would seem aerodynamically disadventageous. However, they could contribute more airflow into the Y250 vortices, generating an even stronger venturi effect than can be achieved with the front wing alone.
            ''')
    elif text_input in redbull_valid_names:
        st.markdown("**Oracle Red Bull Racing**")
        st.markdown('''
                    Constructor: Redbull  
                    Engine: Honda  
                    2025 Car Name: RB21. 
            ''')
        st.markdown('''
            :gray[Suspension Configuration: Pullrod-pushrod]  
            :gray[Sidepod Configuration: Overbite]  
            :gray[Sidepod Inlet: Vertical]   
            :gray[Nose Configuration: Both main-plane and second-element available]
            ''')  
        st.markdown('''
            :red-background[2025 Car]
            ''')
        st.markdown('''
            With the RB21 aerodynamically struggling in the beginning of 2025, speculation has arisen that there have been troubles with Redbull's wind tunnel, which may have given faulty data during the construction process.
            ''')
        st.markdown('''
            Redbull confirmed 12 changes to the car for the 2025 season, including a front wing, nose, front suspension, floor body, floor fences, floor edge, engine cover, cooling louvres, rear suspension, beam wing, rear wing, and rear-wing endplate.
            Since starting the season, they've used mulitple front noses and multiple rear wings.
            The cooling changes in particular have been changed from the novel design in the 2024 design to a more traditional cooling system. The novel approach had too much aerodynamic withdraws, it's unclear how the traditional cooling system has been behaving.
            ''')
        st.divider()
        st.markdown('''
            Redbull kept the overbite side-pod concept that they adopted in 2024 for the RB20, after winning three world championships with an underbit car.
            ''')
        st.image("https://pbs.twimg.com/media/GG25QHEWgAA9ggc.jpg:large")
        st.caption("(top) an underbit side-pod concept on the RB19. (bottom) an overbit side-pod concept on the RB20")
        st.markdown('''
            Flow vis patterns at the Bahrain testing suggested some early difficulties with the overbite pattern, with some flow vis spalshing up above the sidepod. However with the less aggressive inlet style, it's possible this was expected by the redbull team, and may not be related to their aerodynamic instability in early races.
            However, this flow pattern coupled with the second-element nose indicates the second-element code isn't directing all the air into the ground-effect capabilities.
            ''')
        st.image("https://d3cm515ijfiu6w.cloudfront.net/wp-content/uploads/2025/02/26113013/RED-BULL-RB21-flo-viz-on-floor.jpg")
        st.divider()
        st.markdown('''
            The RB21 actually features multiple different front nose designs, with different drivers running different designs depending on the race or desired driving style.  
            One front wing has a wider nose attaching to the second element of the wing, with the main plane protruding underneath and forward. Here this will be called the second-element nose. This design is new to the RB21.  
            The older front wing, recognized as extremely similar to the RB20, has a narrow nose extending all the way to the main plane of the car. This will be called a main-plane nose.  
            ''')
        st.image("https://d3cm515ijfiu6w.cloudfront.net/wp-content/uploads/2025/04/01113933/Red-Bull-RB21-front-wing-comparison.jpg")
        st.caption("(top) second-element nose configuration. (bottom) main-plane nose configuration")
        st.image("https://www.raceteq.com/-/jssmedia/raceteq/articles/2025/03/2025-preseason-tech/rbr-front-wings-2025-f1.jpg?cx=0.5&cy=0.5&cw=1440&ch=670")
        st.caption("(top) main-plane nose configuration. (bottom) second-element nose configuration")
        st.markdown('''
            A second-element nose design allows more air to hit the main-plane of the front wing, better directing the aerodynamics around the car, especially into the venturi channels which are important for downforce of the car. In 2025 where ground effect is largely important, it seems the adventageous design.
            The venturi-effect largely comes from the contribution of Y250 vortices from a complex-wing shape. These vortices are not preset on main-plane front wings. 
            The formation also can make the front-tire wake more adventageous because of the way the air flow is directed around the main plane. However, it's much more structurally complex than a main-plane nose. 
            ''')
        st.image("https://ichef.bbci.co.uk/ace/standard/624/cpsprodpb/15318/production/_113180868_f1car'sfrontnoseshowingthey250vortexairflowoverthefrontwing.jpg")
        st.caption("Y250 vortices incorportated in non-mainplane front wing designs, contributing greatly to venturi effect")
        st.markdown('''                 
            The main-plane nose design's largest advantage is its structural integrety, allowing the driver more errors without greatly compromising the front wing aerodynamics. The structural integrity also allows for greater stability in turbulent conditions, making it less sensitive to dirty air or wind changes. However, it does not push as much air into the venturi channels and plays the dual role of aerodynamics and structural stability, leading it to be subpar in both areas. 
            This nose design is also not very adaptable, as none of the front wing can be adjusted without adjusting the entire nose structure.
            ''')
    elif text_input in racing_bulls_valid_names:
        st.write("coming soon")
    elif text_input in williams_valid_names:
        st.write("coming soon")
    
    #all car information
    st.write("")
    st.subheader("**General Formula One Car Construction**")
    st.markdown("""
        :red-background[**Front and Rear Wing Aerodynamics**]
        """)
    st.markdown("""
        The first front wings were introduced to Formula 1 in the 1968 season on the Lotus-Ford 49. These wings resembled airplane wings and were incredibly fragile. Because of the amount of aerodynamic reliance on these early front wings, any sort of damage to them was catastrophic to the cars, leading to high speed straight on crashes. In some cases, such as the Ford 49B in 1969, the cars would catch air from the wing design.
        """)
    st.image("https://www.formulaonehistory.com/wp-content/uploads/2024/01/Lotus-49-Front-Wing.webp")
    st.caption("Lotus-Ford 49, the first F1 car to feature a front wing in 1969")
    st.markdown("""
        With the turn of the century and with front wings getting more and more complex and fragile, tighter regulations were put on the front wings such as crash tests.  
        
        """)
    st.image("https://www.formulaonehistory.com/wp-content/uploads/2024/01/Mercedes-F1-W10-Front-Wing.webp")
    st.caption("The 2019 front wing design of the Mercedes car, which won the Constructor's Championship and the WDC with Lewis Hamilton.")
    st.markdown("""
        **Drag Reduction System (DRS)**  
            DRS was introduced in 2011 and is continuing until it's replaced by MOM in 2026.  
            When the car is on a safe straightaway, the driver can open the rear wing, greatly decreasing the amount of drag they experience and giving their cars and extra 3-4 kph.
            The DRS was introduced to encourage overtaking and can be used within one second of the car in front of them.  
        """)
    st.image("https://d3cm515ijfiu6w.cloudfront.net/wp-content/uploads/2022/07/13143940/ferrari-carlos-sainz-drs-open-closed-spanish-grand-prix-planet-f11-1024x577.jpg")
    st.caption("DRS being deployed on the SF22")
    st.markdown("""
        DRS failures can cause severe crashes very quickly. This is because the car is travelling at top speed and the aerodynamic effeciency of the open rear wing makes the car incredibly difficult to steer.
        This combination means that if a car fails to disable DRS before turning into a corner, they can very easily continue straight into the wall at high speeds.  
        A typical DRS can close in one of three ways; the driver putting pressure on the brakes, the driver lifting off the accelerator, or the driver pressing a manual close button. 
        """)
    st.image("https://ichef.bbci.co.uk/ace/standard/1024/cpsprodpb/29a7/live/3db79830-1130-11f0-ac9f-c37d6fd89579.jpg")
    st.caption("Jack Doohan's crash at the 2025 Japanese grand prix after the DRS was open into a highspeed corner. It's unclear whether this was a DRS failure or Doohan intentionally left the DRS open, but the open rear-wing was what led to him losing control and resulted in a high-speed crash into the wall. Doohan suffered only minor injuries.")
    st.markdown("""
        **Active Low-Drag Reduction and High-Drag Reduction**  
         Starting in 2026, drivers will be able to adjust the elements of both the front and rear wing throughout the race into low-drag reduction modes and high-drag reduction modes. It's assumed that these will correlate to the current DRS activation zones.  
        "Z-mode" will adjust the wings to be more beneficial for cornering, increasing the amount of downforce generated by the front and rear wings.  
        "X-mode" will adjust the wings to be more beneficial for straightaways, increasing the aerodynamic efficiency of the front and rear wing.
        """)
    st.markdown("""
        :red-background[**Engines**]
        """)
    st.markdown("""
        **Manual Override Mode**  
        With DRS being unavailable in 2026 due to the dynamic wing configurations, it will be replaced by MOM to encourage overtaking in straightaways.   
        In close battles when two cars are within 1 second of each other, the trailing car will be allowed to use additional electrical energy on straights to aid in overtaking.  
        The car in front will use the typical electrical power, which will accelerate to 290 kph and then begin to fall. The trailing car can use MOM, drawing maximum electrical power of 350 kw up to 337 kph before dropping. A car using MOM can also recuperate 0.5MJ more energy per lap to use in ERS, which will further aide in overtaking.  
        Essentially, MOM should mimic the effect of DRS while being a bit more safe, and allowing the front and rear wing to participate in the dynamic system.
        """)
    st.image("https://media.formula1.com/image/upload/f_auto,c_limit,w_960,q_auto/t_16by9Centre/f_auto/q_auto/fom-website/2024/2026%20regulations/2")
    st.caption("An example of the 2026 F1 car as presented by the FIA")
    st.markdown("""
        **1947 - 1953: 4.5 Litre Atmospheric or 1.5 Litre Supercharged Engine**
        Teams could choose between a 4.5 litre atmospheric engine or a 1.5 litre supercharged engine.   
                  
        *Atmospheric engines are naturally aspirated. They use atmospheric pressure to draw air into the cylinders for combustion and don't rely on any sort of force-induction system.*  
          
        *Super-charged engines force more air into the engine, which increases the power output.*  
        
        The dominant car in this era was the Alfa-Romeo, which took advantage of the 1.5 litre supercharged four-cylinder inline engine.
        """)
    st.markdown("""
        **1954 - 1966: 2.5 Litre Atmospheric or 0.75 Litre Supercharged Engine**  
        This was the era Ferrari started to take dominance, with their 2.5 litre V12. The engine, nicknamed the "Lampredi" after the designer Aurelio Lampredi, delivered over 250 horsepower.
        A V12 engine has 12 cylinders arranged in a V shape, with 60 degrees between the vectors.
        """)
    st.video("https://youtu.be/cHSmJDF3Chs?si=ghm0FeKBp2s1ks94")
    st.caption("The Lampredi V12 Supercharged Engine")
    st.markdown("""
        **1967 - 1985: 3 Litre Atmospheric Engines**
        This era saw the ban of supercharged engines entirely, nullifying the dominant Lampredi V12.  
        The Cosworth Double Four Valve 3-litre V8 saw dominance with it's debut in 1967, winning the first ever race it was featured in. The engine won 155 races and 12 championships in it's 16 years.  
        Almost every team utilized a Cosworth DFV, except Ferrari who redesigned their V12 engine from previous regulations.
        """)
    st.video("https://youtu.be/gdM9V2LGPLg?si=dqBdjltbD10IxywR")
    st.caption("Cosworth DFV V8 Engine")
    st.markdown("""
        **1977 - 1988: 1.5-Litre V6 Turbo Engine**
        While not required, turbocharging was allowed in F1 cars. The first team to utilize this was Renault in 1977 in their "Yellow Teapot" engine. It had a tendency to overheat and spew smoke, giving it the unfortunate nickname. 
        After this failed, laggy design, Renault perfected their turboengine in 1983 with their driver Alain Prost and many other constructors followed suit. The engine could produce over 1000 hp in qualifying and 800 hp in a race setting.  
        However, these turbocharged engines were extremely dangerous, with sudden bursts of torque that could set drivers off course. This caused the FIA to impose regulations on the fuel limit of turbocharged engines, reducing the power input to 600-700 hp. In 1988, turbocharged engines wer banned alltogether.
        """)
    st.video("https://youtu.be/0oUjvjq3TSE?si=ExXwowroy3z1iiSl")
    st.caption("Renault RS10 Twin Turbo V6 Engine, 1979")
    st.markdown(""" 
        **1989 - 2005: 3.5 Litre Atmospheric Engines**  
        Constructors could choose between different cylinder numbers; the V8, V10, or V12. Most teams opted for the V10, which saw 600-900 hp between 1989 and 2005. Nicknamed the "screaming" engines, the V10s had a distinct sound.
        The Honda V10 RA109E powered McLaren to both championship titles in 1989 with Alain Prost and successed by the RA100E which won both titles in 1990 and 1991 with Ayrton Senna.  
        The Renault RS01 V10 debuted in 1992 and won the next six constructors championships in a row with the Williams and Benneton cars. 
        """)
    st.video("https://youtu.be/O0WTlEmWwng?si=aYKYSn5E4sHRLIPS")
    st.caption("The Honda V10 RA100E driven by Ayrton Senna at the 1991 Australian Grand Prix")
    st.markdown("""
        **2006 - 2013: 2.4 Litre V8 Mandate**  
        The cars were mandated to use a V8 engine configuration, with a slight power-output decrease to 750 hp.  
        The most famous engines of this era were the Mercedes FO108Z V8, Renault RS27 V8, and Ferrari 056 V8 engines. 
        """)
    st.video("https://youtu.be/5jTTMxtv2PY?si=KPm71m6pYFrgQdsr")
    st.caption("2008 F1 car engines under the FIA V8 mandate")
    st.markdown("""
        The V8 era also saw a brief engine modication known as the blown diffuser, used by the Renault R31 in 2011.
        This modification caused exhaust gasses to be blown over the diffuser when the drivers lifted off the throttle, resulting in a huge gain of downforce while cornering and creating a characteristic machine-gun sound.
        Most teams used some sort of blown diffuser before it was banned in 2012. 
        """)
    st.video("https://youtu.be/Kn8JgOPR9WE?si=z0JgvGe-I4-FBSDW")
    st.caption("The Renault R31 2011 blown diffuser")
    st.markdown("""
        **2014 - Current: V6 Turbo-hybrid**  
        In 2025, the power in the unit is 560 kw with the battery element at 120 kw. In the 2026 season, the power unit will use 400 kw and the battery element increasing to 350 kw.   
        One of the most famous engines under this mandate is the Honda RA621H Hybrid, which won the 2021 world championship with Redbull. Honda seems to dominate the V6 turboengines, as they also had the dominant V6 in the 80s with McLaren. They won 15 of 16 races in 1988 and 21 of 22 races with Redbull in 2023.
        """) 
    st.video("https://youtu.be/tqVoLCm9W_c?si=_6260_ch7NsUxUeK") 
    st.caption("The Honda V6 engine in 2023")

    st.markdown("""
        :red-background[**Front Wing Elements**]
        """)
    st.markdown(""" 
        Prior to recent years, the popular front-wing nose connection style was a main-plane nose, with the nose of the chassis extending to the main plane of the front wing.  
        """)
    st.image("https://www.formulaonehistory.com/wp-content/uploads/2024/01/Ferrari-F1-Front-Wing.webp")
    st.caption("Main-plane front wing on the F1-75 from the 2022 season")
    st.markdown("""
        This was a simpler style that allowed the car's suspension to be altered easier throughout the season, however it lessens the amount of air that moves through the planes of the front wing to add to the venturi channels of the car.  
        Most 2025 teams are running a second-element connection design, but a few teams have brought an additional main-plane front wing. Notably this was used by Liam Lawson in the opening Australian grand prix. 
        """)
    st.markdown("""
        In 2003, the second-element front wing was added with the McLaren MP4-18.
        """)
    st.image("https://i.ytimg.com/vi/obvT9Nt1-84/maxresdefault.jpg")
    st.caption("The McLaren MP4-18, notably the first car to feature a second-element front nose design.")
    st.markdown("""
        The second-element front nose configuration at the time reduced the amount of air hitting the front nose, maximizing the redirection of the airflow around the side-cars to contribute to downforce.  
        Since the original design on the MP4-18, the front wing has further been re-engineered to include Y250 vortices to contribute to the venturi-channels below the car's floor. This would further contribute to downforce and improve the grip of the car. 
        """)
    st.image("https://media.formula1.com/image/upload/f_auto,c_limit,w_1440,q_auto/f_auto/q_auto/fom-website/2023/Miscellaneous/ferrari-sf-24-7")
    st.caption("Current typical design of a second-element front nose. Image is of the SF24")
    st.markdown("""
        :red-background[Suspension Configuration]  
        The suspension of an F1 car is very important, as it must deal with the weight of the car and driver as well as the enormous amounts of downforce in the car. At maximum speed, the suspension can experience about four times the car's weight.  
          
        **Inboard Elements**  
        The inboard elements of the suspension are hidden under the bodywork of the car and include the springs, dampers, rockers, and anti-roll bars. Cars can use physical or gas springs. 
          
        **Airflow Elements**  
        The airflow elements are what experience the most airflow and need to be accounted for in the aerodynamic design of the car. They include wishbones, push or pullrods, and track rods.  
          
        Pushrod Suspension:
        A pushrod can be on either the front or rear suspension. It's a more common and simpler design for the airflow elements. The push rod will transfer force from the lower wheel diagonally to a high-point on the chassis.
        When experiencing resistence, the wheel will push against the airflow elements, offering stability in certain scenarios. It's also simpler and allows the engineers greater access to make adjustments throughout the season.
                    
        Pullrod Suspension:
        A pullrod can also be on either the front or rear suspension. 
        **Outboard Elements*  
        The outboard elements of the suspension are connected to the inboard elements via the airflow elements and include the uprights, axels, and bearings.  
        """)
    st.image("https://images.ctfassets.net/1fvlg6xqnm65/6D1WeClRc8256mPhCsPDH/98196333fea0df75a3c6acf3635bbdfe/MQ7-0-image-20191104195321-2_4252.jpg?w=3840&q=75&fm=webp")
    st.caption("Mercedes F1 car's rear suspension, featuring a pull-rod. For the 2025 season, Mercedes uses a push-rod for both their front and rear-suspension.")
    st.markdown("""
        :red-background[Side-pod Configuration]
        """)
    st.markdown("""
        There are two main configurations of the side pod in play in 2025, with several subsets of side-pod inlet designs for each type.
        The more popular overbite design can have a P-shaped, hooped, shark, or rectangular shaped inlet. The only car sporting an underbite has a shallow inlet.
        """)
    st.markdown("""
        :red-background[**Venturi Channels**]
        """)
    st.markdown("""
        coming soon
        """)
 

##WORDS OF WISDOM
if option == "**Words of Wisdom**":
    st.write("wouldnt this look nicer centered? im not that smart, but just pretend it is")

    quotes = [
        "I have a seat, fULL of water. like- full of water",
        "Must be the water",
        "LANDO WE CAN BE WORLD CHAMPION I SAID",
        "Oh my god... I have never looked so good...",
        "noo NOOOOOO.... i destroyed ze CAAA NOOO",
        "its friday then.... saturday sunday what? iTS FRIDAY THEEENN-",
        "Slippery in the wet",
        "I wasn't even trying to race max, I was just trying to cut the grass. I didn't even know he was there honestly",
        "'Honestly, you guys make absolutely no sense' 'OK'",
        "So I unlocked a new problem",
        "If you want to drive the car give it a go - I think you're going to poop your pants",
        "THANK YOU BRYAN",
        "I value my life and my limbs...he says as hes a formula one driver",
        "Oh no.. I've caused a scene",
        "'How do you manage to stay calm when max is right behind you?'   'I dont know, i dont'",
        "ok mate, we got a few hard ons today. we got kyvat and the two willies have gone hard. everybody else with a free choice is medium apart from giovinazzi, whos gone soft",
        "like a winner",
        "'he's been told to give back the position' 'maybe try in spanish'",
        "There's something loose between my legs. Apart from the obvious. Something is flying around my feet. I'd be proud if it was what you think it is, but it's not",
        "smooth operaatoooorrrrrrr",
        "the mistake was running the zero pod concept",
        "wait a minute- are we both cheating?",
        "It’s more like a hobby for me. So obviously I don’t need to do it if I don’t want to",
        "k1 available",
        "im a high performance athelete, athletes sweat. sweat baby, sweat sweat kiki ru ru",
        "'i cheated a little bit' 'oh you jumped the start?' 'no i pushed the other guy into a bush'",
        "my dad did that once to a mechanic with a fork",
        "nothing just an inchident on the race",
        "BRAAAAAKE",
        "Yabba dabba doo!",
        "ive just had a little scream in my helmet. well done",
        "'No Charles, we are not interested, we know.'   'That's rude'",
        "Break everything. This is an opportunity you'll never have again. Break. Everything.",
        "should i let him pass as well?"
    ]

    words_of_wisdom = st.button("click for some words of wisdom")
    if words_of_wisdom:
        random_quote = random.choice(quotes)
        if random_quote.startswith("http"):
            video_url = random_quote
            st.video(video_url)
        else:
            st.markdown(
                f"<h2 style='text-align: center;'>{random_quote}</h2>",
                unsafe_allow_html=True
        )
##CHATBOT
if option == "**Revvy** ***NEW***":

    greeting_data = [
        ("hello", "hiiii what can i do ya for"),
        ("hey", "hi!"),
        ("what's up", "hello! do you like the cars? the cars that go vroom?"),
        ("howdy", "howdy partner!"),
        ("good morning", "hidy ho!"),
        ("goodbye", "later skater!"),
        ("bye", "bye bye! have a good day"),
        ("bye", "bye, thanks for chatting with me!"),
        ("sorry", "no worries, pal"),
        ("what", "sorry, i dont understand. can you rephrase that?"),
        ("i asked about something else", "sorry, i mustve gotten things mixed up. can you ask again?"),
        ("not what i meant", "im sorry, i'm doing my best but some things i just have trouble understanding. if you try rephrasing maybe that will help me"),
        ("do you like", "i like all the cars and teams and drivers... heh..."),
        ("test testing", "i work!"),

        #grand prix results
        ("track", "i know about the winners on each track so far this year, but kiley hasn't taught me about the track qualities yet. you can look on track information though!"),
        ("australia grand prix", "lando norris won the australian grand prix this year after leading from pole position. he fought briefly with oscar piastri before he fell to the back of the pack due to a heavy rain patch. in the end, max verstappen took second and george russell took third"),
        ("china chinese shanghai grand prix gp", "oscar piastri won the chinese grand prix, marking his first pole position and his first win from pole position in a main race. with a brake failure in the last stint of the race, it was impressive to see lando norris finish second, but he wasn't satisfied and tried to fight oscar to the end. george russell did nothing and somehow ended up third"),
        ("sprint china chinese shanghai", "lewis hamilton took a hard fought sprint victory in the less adventagious ferrari car, giving a masterclass in how to race the shanghai circuit"),
        ("japan suzuka grand prix", "max verstappen took his first win of the season in japan, and boy was he excited. his reaction at the end was enough to convince everyone how hard he's had to work to find pace in the redbull car. lando norris and oscar piastri fought with their engineers about papaya rules before finally finishing second and third respectively."),
        ("bahrain grand prix", "oscar piastri took his second win of the season in bahrain after once again taking pole position, keeping his 100% pole conversion rate alive. george russell toook second place, with lando norris in third place. this was the best race for ferrari so far, with them finishing 4th and 5th."),
        ("saudi arabia arabian jeddah grand prix", "oscar piastri won for the third time this year in jeddah after a controversial turn 1 incident with max verstappen, who ultimately suffered a five second penalty and finished second. charles leclerc fought hard and ended up third place, for the first ferrari podium this seaosn."),
        ("sprint miami", "rookie kimi antonelli took pole position in the miami sprint, but lack of experience and an iffy strategy saw him falling to the midfield. the race was ultimately won by lando norris in his disco ball helmet, with his teammate oscar piastri finishing right behind"),
        ("miami grand prix gp", "oscar piastri continued into a three-win streak for his fourth win of the season in miami. his teammate lando norris finished second after struggling to pass an angry max verstappen, who ultimately was passed by george russell as well and finished in fourth. the diamond of the race was certainly one alex albon, who shot up to fifth place in his williams"),
        ("grand prix", "i know a few grand prix results! which one do you want to know about?"),

        # Car-related questions
        ("whats cool?", "the aerodynamics of a formula one car are so efficient, that at top speeds the car could drive on the ceiling without falling off!"),
        ("how does the car drive on the ceiling?", "this is possible mostly because of the venturi channels, the low pressure zones between the car and the floor (or this case, the sky). it sucks the car down (or up) into the surface it's driving on, making it possible for f1 cars to join elphaba in defying gravity"),
        ("front wing", "there's a lot of cool features on the front wing. which one do you want to know about?"),
        ("front wing features", "the features on the front wing that i can tell you about are the wing elements, the front nose configuration, and the contribution to the venturi channels. I could also tell you the history. which one do you want to know more about?"),
        ("wing elements", "a lot of different f1 cars have a different amount of wing elements. currently, the rules is they can't have more than four. this is mostly because if there were more elements, the car would go faster, but it would also be harder to control. in 2026, only two elements will be allowed"),
        ("hard to control", "a few things can make the car difficult to control. if the front wing is too complicated, the aerodynamics might be so efficent that it's hard to break the car out of the air it's passing through. the same goes for if DRS was open all the time."),
        ("history", "im sorry, my memory isn't so great. what do you want to know the history about?"),
        ("history front wing", "the first front wing was added to the Lotus-Ford 49 in 1969 and it looked like doo doo. but hey, it worked, so more and more people started copying it. they realized if they added more elements then the front wing would be even more effective, with the maximum being five, but tighter regulations are making that number less and less."),
        ("rear wing", "if you want to know about rear wing aerodynamics, i'm sure you want to talk about the DRS, am i right?"),
        ("mini DRS mini-drs flexi-wing", "mini-DRS was something that some teams used in 2024, most famously the mclaren team. this system is actually known as a flexi-wing. at high speeds, the rear wing element would flex. that gave the cars effects similar to the actual DRS but made them difficult to control. for safety reasons, these are no longer allowed in the 2025 season. the rear wing cannot flex open more than 0.5mm."),
        ("DRS", "the DRS, or drag reduction system, is one of the coolest things in f1. it's such a shame it's being taken out of the sport in 2026, but it will live on through us!"),
        ("why DRS removed", "DRS is being removed from F1 after the 2025 season because the front and rear wings will be used in active aerodynamic systems. it's also speculated that they're changing this due to the cars being so incredibly difficult to control with DRS open and because of DRS exploits found in 2024"),
        ("DRS exploit", "the most famous DRS exploit is the mini-DRS system"),
        ("what is DRS", "the drag reduction system is a system in which the driver can open up the rear wing element, allowing crazy amounts of air that was once being restricted flow right through. this makes the aerodynamics incredibly efficient, speeding the car up around 10-12 kph and giving the drivers an extra couple of seconds. this system is incredibly strict though, and can only be used in certain situations"),
        ("when DRS used", "DRS can be used during a race if a car is within one second of the car in front of them and in an active DRS zone. these zones are usually straightaways or incredibly high speed-low angle turns, as it's near impossible to make a turn with DRS open due to the aerodynamic efficencly. it can also be used in active DRS zones during free practices and qualifying at any time."),
        ("why within one second", "this is because DRS was initially added to make overtaking easier. when a car is within one second of the car in front, the leading car cannot use DRS, but the trailing car can. this gives the trailing car the speed advantage, making overtaking a little less impossible. but the car in front can still defend by moving slightly or braking late at the end of the DRS zone"),
        ("DRS crash", "DRS failures or mistakes can easily cause crashes. most recently, Jack Doohan didnt close his DRS at the Japanese grand prix, causing him to lick it and send it straight into the wall, completely destroying his car."),
        ("why didnt jack doohan close his drs", "it's controversial, we don't actually know the real reason. some people say the DRS closure system failed, and others say he deliberitely left it open as he had made the turn with DRS open in the simulation"),
        ("what are venturi channels?", "venturi channels are vital in increasing the downforce of an f1 car, and are what sucks the car into the ground so it can even drive upside down! if you want more information, visit 'construction information'"),
        ("second element front nose", "a second element front nose will push more air underneath the car to add to the ground effect, increasing the downforce of the cars"),
        ("mainplane main plane front nose", "a mainplane front wing integrated nose has the nose of the car extend all the way to the bottom plane of the front wing. it's a more simplistic design but tried and true!"),
        ("front nose configuration", "front noses in f1 cars right now are either main-plane integrated or second element integrated"),
        ("car downforce best", "'best' is relative.. the car that seems to be utilizing downforce the best is mercedes. the car that has the MOST downforce is ferrari, who have so much downforce that they've seen their car go faster if they remove some of that downforce"),
        ("who drivers", "what teams drivers do you want to know about?"),
        ("sidepod inlet p-shape shark high rectangle", "if you want more information on a specific shape of inlet you can go to 'construction information' and search what team uses it! do you want to know what inlet a specific team uses?"),
        ("y250", "the y250 vortices are air currents that come off the nose of a car with a second element front wing connection. these air currents typically travel to the underside of the car and contribute to low pressure zones, enhancing the car's downforce and grip"),
        ("engine engines", "in 2025, all cars use a V6 turbo-hybrid engine. would you like to know more about a specific team's engine?"),

        #alpine related questions
        ("alpine drivers", "the current alpine drivers are former redbull driver pierre gasly and former williams driver franco colapinto, with rookie jack doohan racing the first six races and remaining in the reserve driver position"),
        ("who is pierre gasly", "the frenchman fell victim to the redbull second seat curse before finding himself passed around low-tier teams on the f1 grid, but he holds the impressive record of not costing the team a single cent of repairs in his perfect 2024 season."),
        ("who is franco colapinto", "i dont know who this man is, he could be walking down the street...i wouldn't know a thing"),
        ("alpine coach team principal flavio braitore", "current acting-team principal for alpine, flavio briatore, was previously banned from f1 associated events for race fixing. after overturning this rule and turning it to he just couldnt lead a team, he rejoined his old team alpine (then renault) as an executive. after a surprise resignation of alpine team principal oliver oakes following suspected embezzlement charges, flavio took back over the team"),
        ("alpine engine", "alpine utilizes a renault engine, but in 2026 they will switch to the mercedes engine along with several top teams on the grid"),
        ("alpine suspension push pull rod", "alpine uses a dual pushrod suspension configuration"),
        ("alpine overbite underbite sidepod side pod", "alpine is the only team on the 2025 grid utilizing an underbite sidepod"),
        ("alpine nose", "the alpine front nose is using the popular second element design for the 2025 season"),
        ("alpine downforce", "the alpine downforce could struggle if the little bit of air coming off the pushrods disrupt the y250 forces generated by the second element front nose"),

        #aston martin questions
        ("aston martin drivers", "this year the aston martin drivers are 2-time world champion fernando alonso and nepo-baby lance stroll"),
        ("who is lance stroll", "despite being called a nepo baby because his dad owns the aston martin team, lance once held the record for the youngest driver to score a podium finish, with his fellow podium finishers not even sure if he could legally drink the champagne. since then, however, lance is known for his many ridiculous race-exits including rear-ending a driver during a safety car and beaching himself in gravel during the formation lap"),
        ("who is fernando alonso", "the 2-time world champion found his titles with the renault team before and during their cheating scandals, with crashgate helping lead to one of those titles. despite this, the spaniard is the only driver to be inducted into the FIA hall of fame twice"),
        ("aston martin engine", "the aston martin team is using a mercedes-amg engine in 2025. in 2026 they will take over redbull's agreement with honda and use honda engines"),
        ("aston martin suspension push pull rod", "the aston martin team uses a dual push rod suspension configuration"),
        ("aston martin overbite underbite sidepod", "aston martin uses an overbite side pod with a high rectangular sidepod inlet"),
        ("aston martin nose", "aston uses a second element front wing nose connection"),

        #ferrari related questions
        ("ferrari downforce", "it seems ferrari's car this year has the most downforce. but that might not be a good thing. downforce makes cars faster in corners, but slows them down in straightaways. they paid the price of this in the chinese grand prix where charles leclerc was moving faster with a broken front wing that caused him to lose downforce"),
        ("ferrari engine", "ferrari manufactures their own engine! a few other teams also use this ferrari engine"),
        ("ferrari car name", "in 2025 the ferrari's name is SF25"),
        ("ferrari sf25 suspension", "this year the ferrari is using a dual pullrod suspension configuration. more information about that unique setup is in constructor information! search 'ferrari'"),
        ("ferrari overbite underbite sidepod", "the sf25 is using an overbite design like every other team except for alpine"),
        ("ferrari inlet sidepod", "the ferrari is using the same sidepod design as mclaren with an aggressive p-shaped inlet that can be described as high risk and high reward!"),
        ("ferrari nose", "ferrari is following the popular second element nose wing integration design this year"),
        ("ferrari drivers", "this year the ferrari drivers are il predestino charles leclerc and 7-time world champion with mercedes lewis hamilton"),
        ("ferrari china grand prix disqualified", "both ferrari drivers were disqualified from the chinese grand prix after they suffered a collision with each other early into the race. however, the collision had nothing to do with the disqualifications. charles leclercs car was found to be under the minimum weight limit and lewis hamiltons car was found to have excessive wear indicating it was driving too close to the ground. both of these are likely due to the one-stop strategy the team used"),
        ("ferrari drivers", "the current ferrari drivers are former merc driver and 7 time world champion lewis hamilton and loyal ferrari driver charles leclerc"),
        ("who is charles leclerc", "charles leclerc, nicknamed il predestino by the italians for ending the ferrari's nine-year no-win drought, has been driving for ferrari since his third year in f1. hailing from monaco, he's the second youngest pole-sitter in f1 history and the first monegasque to win the monaco grand prix in almost 100 years. despite holding no drivers championships, he's been 4-time world champion max verstappen's rival since they were kids, terrorizing him and pushing him off the track and into puddles in their go kart days"),
        ("who is lewis hamilton", "lewis hamilton won 7 world drivers championship titles before he was finally being dethroned by max verstappen. he tied the record for most championship wins and is in the hunt for his eighth with new team ferrari, after winning the previous seven with mercedes. he has also won the most grand prixs of any driver, with him and his then-teammate nico rosberg winning 51 out of 59 races over the course of three years."),

        #haas related questions
        ("haas engine", "the haas team uses the mercedes-amg team's engine"),
        ("haas car name", "in 2025 the haas car is the VF25"),
        ("haas suspension push pull rod", "the haas team uses a pushrod front suspension and a pullrod rear suspension"),
        ("haas overbite underbite sidepod", "the haas team uses an overbite side pod design with hooped inlets"),
        ("haas nose", "the haas team is one of the only teams on the grid to be using a main-plane integrated front nose of their car"),
        ("haas drivers", "this year's haas drivers are veteran frenchman esteban ocon and rookie ollie bearman"),
        ("who is ollie oliver bearman", "ollie bearman debuted with ferrari when carlos sainz required emergency surgery in 2024, scoring 7th place in his first ever race. since his amazing debut, he found himself on the haas team in a lackluster car, but still is exhibiting impressive overtakes and pace, moving from last place into the points twice already this season."),
        ("who is esteban ocon", "perhaps most known for being punched by max verstappen, estie bestie has hopped around several teams and fallen to the back of the grid, but has been exhibiting some pace this year"),

        #kick sauber related questions
        ("kick sauber drivers", "currently the kick sauber drivers are veteran nico hulkenberg and reigning f2 champion gabriel bortoleto"),
        ("who is gabriel gabi bortoleto", "after winning f2 in 2024, gabi moved to the kick sauber f1 team which will be taken over by audi in 2025. he won the 2024 rookie of the year and is known as the first driver ever to win a race from last in the grid in either f2 or f1, winning that race in f2."),
        ("who is nico hulkenberg", "the german has been racing in formula 1 since 2010 and known as one of the few drivers to ever win f2 in their rookie season"),

        #mclaren related questions
        ("what's cool about the mclaren MCL39?", "i LOVE the mclaren car. i think the coolest feature was actually on their car from 2024, the MCL38. that car had a spike on the front wing to gently discourage people from bumping them"),
        ("describe the mclaren car", "it's really designed for aerodynamics, with arguably one of the best rear wings in the game. the mclaren car is so good this year, that red-bull team principal has already accused them of cheating, twice!"),
        ("what makes the mclaren car so good?", "part of the reason the mclaren car is performing so well is because of their rear tyre managment. no one quite knows how (yet), but their rear tyres just dont overheat as fast as everyone elses"),
        ("mclaren car legal", "while redbull has accused mclaren of cheating several times already in 2025, the mclaren car is currently up to code!"),
        ("why was mclaren accused of cheating?", "redbull thought that mclaren was possibly still using mini-DRS in the 2025 season, which would be against FIA regulations"),
        ("is a car spike legal?", "not anymore. however, in 2024, when mclaren implimented it for the first time, it was within regulations"),
        ("mclaren MCL39 suspension", "mclaren uses a pull-rod front suspension and a push-rod rear suspension"),
        ("whats the mclaren car?", "in 2025, the mclaren team is using the MCL39"),
        ("mclaren overbite underbite sidepod", "the mclaren is using an overbite sidepod design this year, along with the rest of the grid except for alpine, who has stuck with the underbite design"),
        ("mclaren inlet sidepod", "the mclaren is using an aggressive p shaped inlet in 2025. it's especially adventageous in cooling and airflow but also carries a risk of increasing drag if not executed perfectly"),
        ("mclaren car name", "this year osc and lando are driving the mcl39!"),
        ("mclaren engine", "mclaren are continuing their partnership with mercedes and using the mercedes-AMG engine in 2025"),
        ("mclaren nose", "mclaren, along with most teams, is utilizing a second-element front nose"),
        ("mclaren good fast bad advantages disadvantages downsides", "this year the mclaren car has a heavy advantage in high speed corners and in rear-tyre cooling. they may be slightly vulnerable in low speed corners, as the team focused on the car's aerodynamics more than mechanical downforce generation"),
        ("mclaren tyre water tire water", "redbull accused the mclaren team of using water in their rear tyres to help with temperature management, an illegal tactic that redbull themselves have used in the past"),
        ("mclaren drivers", "this year the mclaren drivers are lando norris, who entered as the favorite for the world drivers championship, and underdog up-and-coming youngster oscar piastri"),
        ("who is lando norris", "previously called lando 'no wins' for taking a record-breaking long time to score his first grand prix win, lando norris has shot up the rankings and is in contention for winning the world drivers championship in 2025. his impressive karting carreer named him as the youngest driver to set pole position at the national level and the youngest world champion ever. within formula 1, he's tied for the most podium finishes before taking home the biggest trophy"),
        ("who is oscar piastri", "after two teams going to court over who got to take oscar in his debut f1 season, the ice man started driving at mclaren and in just a few short years has proven himself as a world champ contendor, surprising everyone who thought it was his teammates year to lose. but considering his record as the only driver to ever win formula renault, f3, and f2 consecutively in their rookie season, it's not surprising."),

        #mercedes related questions
        ("mercedes engine", "the mercedes team manufactures their own mercedes engine for their f1 team"),
        ("what's cool about the mercedes W16?", "The coolest thing about the Mercedes F1 W16 is that it uses a dual-push rod suspension configuration as well as a second-element front nose. their extreme amounts of downforce despite the pushrod suspension suggests that they're using the pushrods to direct air into the venturi channels"),
        ("mercedes W16 suspension", "in 2025 the mercedes is using a dual pushrod suspension configuration"),
        ("mercedes overbite underbite sidepod", "the mercedes car is using an overbite sidepod design along with the rest of the grid this year except for alpine, who has stuck with the underbite design"),
        ("mercedes inlet", "mercedes uses the unique shark sidepod inlet that redbull found success with in previous years"),
        ("mercedes nose", "the mercedes car has multiple front wings available, one with a mainplane nose integration and one with a second element nose integration. so far, it seems they're using the second-element front wing more"),
        ("mercedes", "the mercedes car in 2025 has really focused on increasing their downforces, giving the car so much grip that other drivers are commenting on it during races"),
        ("mercedes drivers", "the mercedes drivers are former-second seater george russell and star rookie kimi antonelli"),
        ("who is george russell", "as only the second driver to win gp3 and f2 in his rookie season, george russell sat in the second seat of mercedes for years until he was finally promoted this year to first driver following hamilton's departure. as an instictive driver, his consistency gives him success as he wins the tortise and the hare race into the podium very often"),
        ("who is andrea kimi antonelli", "the high schooler from italy is the youngest driver on the grid this year, and the youngest driver to achieve pole position in any format. taking lewis hamiltons seat, his very experienced engineer, bono, has helped guide him to find incredible pace, achieving fourth place in just his first grand prix race ever, in the RAIN"),

        #redbull related questions
        ("redbull engine", "the redbull teams manufacture their own engines with honda. in 2026, they will continue to make their own engines but without the help of honda"),
        ("redbull car name", "in 2025 the oracle redbull team is driving the RB21"),
        ("redbull suspension push pull rod", "the redbull team is using a pullrod front suspension and a pushrod rear suspension"),
        ("redbull overbite underbite sidepod", "the redbull team uses an overbite sidepod design with a conventional vertical inlet, a stark comparison to previous years where they found success with their novel shark inlet design"),
        ("redbull nose", "the redbull team has both mainplane and second element integrated front wings and seem to use both depending on the track and driver, sometimes with drivers even running different front wing setups"),
        ("redbull red bull drivers", "following an early swap the redbull drivers are 4-time world champion max verstappen and former sister-team driver yuki tsunoda"),
        ("who is max verstappen", "the protegy from belgium had the longest-held lead in the drivers world championship, keeping ahead for over 1000 days. his records list goes on and on with the highest win percentage in a season (77.3%), the youngest f1 race winner, and the youngest driver to acheive a grand slam. no one can deny max's natural driving talent, as he even set a lap record in a gt3 car this season in testing."),
        ("who is yuki tsunoda", "promoted at his home race in japan this year, many believe yuki is just the driver to break the red bull second seat curse. as the youngest japanese driver in f1 history, he raced on red bull's sister team for years and found incredible pace in a second-string car."),
        ("second seat curse", "after the redbull car has been increasingly engineered in favor of driver protegy max verstappen, who has an incredibly unique driving style, the second driver of redbull famously does really really well until they sit in a redbull, where they struggle to even recieve a single point. victims of this curse are daniel ricciardo, alex albon, pierre gasly, liam lawson, yuki tsunoda, and sergio perez, who did the best out of all of them"),

        #vcarb related questions
        ("vcarb racing bulls drivers", "after a swap in the third race of the season, the current vcarb drivers are rookie isack hadjar and rookie-former redbull second seater liam lawson"),
        ("who is liam lawson", "the cars enthusiast credits lighning macqueen as his motivation to racing. after being demoted from the redbull team after just two races, the driver found himself on the redbull sister team in what is known as the fastest driver replacement in f1 history."),
        ("who is isack hadjar", "known for his incredibly french radio outbursts, the parisian is called le petit prost after the multi-world champion alain prost. his helmet features several mathematical equations as a nod to his father who works in quantum mechanics. this season, he's most known for his kardashian lip-syncing videos he forces his teammates into participating in"),

        #williams related questions
        ("what's cool about williams", "the williams team has chosen to focus on the 2026 season. as their team principal has said, 'this is an opportunity we'll never have again, break everything'. with nowhere to go but up, they started the car from scratch and are starting to show some pace ahead of their target season."),
        ("who is alex alexander albon", "the red-bull second seat curse victim has found himself leading williams out of a no-win drought, storming up to fifth place in the mid-to-low-tier car. known more famously for his WAG lily muni, he's the first thai driver to achieve a podium finish in f1 history."),
        ("williams drivers", "the williams drivers this season are former redbull driver alex albon and former ferrari driver carlos sainz"),
        ("who is carlos sainz seinz", "the smooth operator spent time on both mclaren and ferrari, most recently being let go from ferrari in favor of 7-time world champion merc driver lewis hamilton. the spaniard has moved to williams to play the long game, working alongside alex albon to help the team improve the car in hopes of being a top team in the new regulation 2026 season."),

        #other driver related questions
        ("who is sergio perez checo?", "the driver who raced alongside max verstappen for years and fought the hardest against the redbull second seat curse, sergio 'checo' perez is expected to make a comeback in 2026 with rumors circulating about a possible contract with debut team cadillac"),
        ("who is daniel ricciardo?", "quite possibly the most loved driver in f1, daniel ricciardo is enjoying retirement after clinging onto spots all over the grid and struggling to produce results. he's still dearly beloved by all the fans and drivers"),
        ("who is ayrton senna?", "an advocate for f1 safety in his lifetime, ayrton senna is a beloved world champion who raced primarily in the 90s. one of the greatest of all time, he still holds the record for most wins in monaco, the hardest f1 track. due to an unfortunate accident, he passed away in a crash in 1994 at the imola grand prix. his long-standing rival, alain prost, carried his legacy on in improving the safety for the drivers, and only one driver has passed racing since. his legacy still lives on in the drivers, with rookie kimi antonelli using senna's old number 12 and lewis hamilton modeling his helmet after senna's iconic bright yellow one in rememberance"),
   
        #basic
        ("im new to f1", "welcome to f1! the top tier teams this year are mclaren, mercedes, redbull, and ferrari. but it's a close season, and teams williams, haas, racing bulls, kick sauber, aston martin, and alpine can't be counted out! next year an eleventh team will be added, cadillac"),
        ("who is the best driver", "well that depends who youd ask... most people will answer max verstappen, lewis hamilton, or the late ayrton senna")
    ]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_view" not in st.session_state:
        st.session_state.current_view = "chat"

    def switch_to_report():
         st.session_state.current_view = "report"

    def switch_to_chat():
         st.session_state.current_view = "chat"

    # --- Chat View ---
    if st.session_state.current_view == "chat":
            X = [item[0] for item in greeting_data]  # input phrases
            y = [item[1] for item in greeting_data]  # appropriate responses

            vectorizer = TfidfVectorizer()
            X_vec = vectorizer.fit_transform(X)

            def get_best_response(user_input):
                user_vec = vectorizer.transform([user_input])
                similarities = cosine_similarity(user_vec, X_vec)
                best_match_index = similarities.argmax()
                return y[best_match_index]

            st.markdown(f"<h2 style='text-align: center;'>Revvy</h2>", unsafe_allow_html=True)
            st.markdown(f"<h6 style='text-align: center;'>hi! im revvy, i love the f1 stuffs and im here fOR the girls. think of me as kiley's right hand man. please let me know if you want to talk about this stuff!</h6>", unsafe_allow_html=True)
            st.markdown(f"<h6 style ='text-align: center;'>if you have any problems with me, please send a report. kiley would love some help in teaching me! you know how kids can be</h2>", unsafe_allow_html=True)

            user_input = st.chat_input("i love talking about f1!")
        
            if st.button("report a problem with revvy"):
                 switch_to_report()

    # --- Report View ---
    elif st.session_state.current_view == "report":
        user_input = ()
        st.title("Report an Issue with Revvy")

        report_text = st.text_area("Describe the issue you're having with Revvy:")

        if st.button("Submit Report"):
            if report_text.strip():
                with open("bot_reports.txt", "a") as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"{timestamp} - Reported issue: {report_text.strip()}\n")
                st.success("Your issue has been reported. Thank you! I'll try to teach Revvy a little more about this.")
            else:
                st.warning("Please describe the issue before submitting.")

        if st.button("Back to Chat"):
            switch_to_chat()

    if user_input:
        lowered = user_input.lower()
        original_user_input = user_input

        # --- Context Tracking ---
        if "context_topic" not in st.session_state:
                st.session_state.context_topic = None
        elif "alpine" in lowered:
            st.session_state.context_topic = "alpine"
        elif "aston martin" in lowered:
            st.session_state.context_topic = "aston martin"
        elif "ferrari" in lowered or "sf25" in lowered:
            st.session_state.context_topic = "ferrari"
        elif "haas" in lowered:
            st.session_state.context_topic = "haas"
        elif "kick sauber" in lowered or "sauber" in lowered:
            st.session_state.context_topic = "kick sauber"
        elif "mclaren" in lowered or "mcl39" in lowered:
            st.session_state.context_topic = "mclaren"
        elif "mercedes" in lowered:
            st.session_state.context_topic = "mercedes"
        elif "redbull" in lowered or "red bull" in lowered:
            st.session_state.context_topic = "redbull"
        elif "vcarb" in lowered or "racing bulls" in lowered:
            st.session_state.context_topic = "vcarb"
        elif "williams" in lowered:
            st.session_state.context_topic = "williams"


        if st.session_state.context_topic:
            user_input = (
                user_input.replace("it", st.session_state.context_topic)
                        .replace("this car", st.session_state.context_topic)
                        .replace("that car", st.session_state.context_topic)
                        .replace("the car", st.session_state.context_topic)
                        .replace("they", st.session_state.context_topic)
                        .replace("their", st.session_state.context_topic)
                        .replace("them", st.session_state.context_topic)
            )

        st.session_state.messages.append({"role": "user", "content": original_user_input})
        response = get_best_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})

    #chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

##MCLAREN LOOPHOLES
if option == "**McLaren Loopholes**":
    st.markdown(f"<h5 style='text-align: center;'>McLaren has a habit of....pushing the boundaries. Here's some iconic tricks they've added to their cars that have since been banned</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align:center;'>2025</h5>", unsafe_allow_html=True)
    st.markdown(f"<h6 style='text-align:center;'>since the season is ongoing, none of these are confirmed by mclaren or other teams, but they have prompted fia investigations</h6>", unsafe_allow_html=True)
    st.markdown('''
        :red-background[**Phase Changing Tyre Cooling System**]   
                  
        Redbull has been the main accuser of McLaren using illegal tactics to cool their rear tyres, with Christian Horner even submitting thermal camera footage of the tires in use to the FIA and prompting an investigation.   
        One of such accusations was that McLaren was using water in their tyres, something explicitly against the rules after Redbull themselves tried the practice.   
        Several FIA investigations, including one after the dominant performance in the extremely hot Miami grand prix, where the McLarens finishes over 30 seconds ahead of any other car, the FIA has been clear that as of right now the car is within regulations.  
          
        One theory of what the McLarens are using is phase changing materials. These would be materials within the brakes that use the heat-generated energy to change phase (gas, solid, liquid) at a certain temperature. This converts the energy entirely to the phase change, stopping the material from using any remaining energy in the form of heat. 
        Essentially, this caps the brakes at a certain temperature.   
        If this is the case, the FIA has decided that this does not count as liquid cooling, which is explicitly banned, but maybe we will see a rule change in the future to cover this loophole.
        ''')
    st.caption("the thermal images taken by redbulla are not yet publically available.")
    st.markdown('''
        :red-background[**Flexi Wing miniDRS pt2**]  
                  
        After the miniDRS recieved scrutiny in 2024, the FIA tightened regulations to only a maximum of 13mm gap in the rear wing.
        Quick into the 2025 season, it appeared this was not nearly enough and stricter regulations were put in place, allowing only a maximum of 0.5mm flex.
        Several teams had to change their rear wings. McLaren allegedly had to change this, due to flow vis patterns observed in Bahrain testing, but denied having to change their rear wing to fit the new regulations.   
        Coincidentally, the first race after regulation changes was the first McLaren loss of the year.
        ''')
    st.image("https://media.discordapp.net/attachments/1364657259849711637/1369149985073004666/IMG_5150.png?ex=68240a4a&is=6822b8ca&hm=cec8debcf81aa57d95afb9b012145fad73ab9896e80f773054664d6f55d85245&=&format=webp&quality=lossless&width=1342&height=1338")
    st.caption("flow vis patterns on the MCL39 at the beginning of the 2025 season in testing vs after the stricter regulations were put in place during the chinese GP.")
    st.markdown(f"<h5 style='text-align:center;'>2024</h5>", unsafe_allow_html=True)
    st.markdown('''
        :red-background[**The Front Wing Wake Control Spike**]  
                  
        The spike added on the rear of the front wing on the MCL38 was added for two reasons. One was obvious, which was discouraging cars from driving too close to the McLaren for fear of tire punctures or scraping on the body.   
        The second was wake control. This spike disrupted the smooth airflow coming off the car and hitting the car behind them, making dirty air dirtier and disrupting the slipstream. In a sense, it weaponized the dirty air.   
        At the time, this was fully within regulations. Immediately after the completion of the season, the FIA placed stricter rules around wake control.
        ''')
    st.image("https://img-s-msn-com.akamaized.net/tenant/amp/entityid/BB1p3Dh7.img?w=768&h=512&m=4&q=84")
    st.markdown('''
        :red-background[**Flexi Wing miniDRS**]  
                  
        During the 2024 season, McLaren unveiled what was later coined the miniDRS. The mechanism consisted of an abnormally flexible rear wing flap, that bent excessively under force. 
        This caused the DRS flap to open slightly at high speeds, giving drivers DRS advantages in zones where DRS would otherwise be illegal. This system did not violate any rules or regulations.
        ''')
    st.image("https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AA1w24cI.img?w=768&h=432&m=6")
    st.caption("data of the mclaren using miniDRS (pia) showing consistent pace and then a clear advantage in a straightaway with no DRS active. this is Oscar Piastri (McLaren, second season) against Charles Leclerc (Ferrari, sixth season)")
    st.markdown('''
        Tighter regulations were placed upon the rear wing flexibility immediately after the 2024 season.
        ''')
    st.markdown(f"<h5 style='text-align:center;'>2011</h5>", unsafe_allow_html=True)
    st.markdown('''
        :red-background[**Extreme Blown Diffuser**]
        ''')
    st.markdown(f"<h5 style='text-align:center;'>2010</h5>", unsafe_allow_html=True)
    st.markdown('''
        :red-background[**F-duct**]
        ''')
    st.markdown(f"<h5 style='text-align:center;'>1998</h5>", unsafe_allow_html=True)
    st.markdown('''
        :red-background[**Brake Steering**]
        ''')

##PATCH NOTES
if option == "Patch Notes":
    st.subheader("1.5.5")
    st.markdown("""
        added monaco race results.  
        fixed error on hypothetical chaos mode that was causing alpine to not be unable to be calculated.  
        """)