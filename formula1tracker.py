import streamlit as st
import pandas as pd
import numpy as np


#Site formatting
st.markdown(
    """
    <style>
    body {
        background-color: #ffd5e3;  /* Light pink background */
        color: #000000;  /* Black text color for contrast */
    }
    .stApp {
        background-color: #ffd5e3; /* Background for entire app */
    }
    .css-1lcbz5j {
        color: #ff7da7;  /* Change the color of streamlit header */
    }
    .stButton>button {
        background-color: #ffd5e3; /* Pink button */
        color: white;
    }
    .stButton>button:hover {
        background-color: #ff7da7;  /* Darker pink on hover */
    }
    .stSidebar {
        background-color: #ff7da7;  /* Sidebar color */
    }
    .stAppHeader {
        background-color: #ff7da7;
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




option = st.sidebar.radio("Pages",["Home", "Grand Prix Positions", "Current Leaderboard", "Hypothetical Chaos Mode", "Interesting Factoid", "Construction Information", "Track Information"])

if option == "Home":
    st.title("kiley's f1 2025 season track: for the girls by the girls")


##HOME
if option == "Home":
    st.write("Homepage")

##File Uploads


#Main Race
gp = pd.read_csv('/workspaces/formula1forthegirlies/2025RaceResults.csv')
sprint = pd.read_csv('/workspaces/formula1forthegirlies/2025SprintResults.csv')
season = pd.concat([gp, sprint])

##GRAND PRIX POSITIONS
gp_clean = gp.dropna(subset=["Track", "Pos"])
tracks = gp_clean["Track"].unique()

if option == "Grand Prix Positions":
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

##STANDINGS

elif option == "Current Leaderboard":

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
        gp_leaderboard = valid_gp_positions.groupby("Driver")["Points"].sum().reset_index()
        gp_leaderboard = gp_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)                                                                 


        return gp_leaderboard

    def calculate_sprint_points(results):
        results["Clean_Pos"] = results["Pos"].astype(str).str.strip()
        valid_sprint_positions = results[results["Clean_Pos"].isin(sprint_points_table.keys())]
        if valid_sprint_positions.empty:
            return pd.DataFrame()

        valid_sprint_positions["Points"] = valid_sprint_positions["Clean_Pos"].map(sprint_points_table)
        sprint_leaderboard = valid_sprint_positions.groupby("Driver")["Points"].sum().reset_index()
        sprint_leaderboard = sprint_leaderboard.sort_values(by="Points", ascending=True).reset_index(drop=True)

        return sprint_leaderboard

    
    gp_leaderboard = calculate_gp_points(gp)
    sprint_leaderboard = calculate_sprint_points(sprint)

    if not gp_leaderboard.empty and not sprint_leaderboard.empty:
        full_leaderboard = pd.concat([gp_leaderboard, sprint_leaderboard])
        full_leaderboard = full_leaderboard.groupby("Driver")["Points"].sum().reset_index()
        full_leaderboard = full_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)

        full_leaderboard["Position"] = full_leaderboard.index + 1
        full_leaderboard["Position"] = full_leaderboard["Position"].apply(
        lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
    )

    full_leaderboard = full_leaderboard[["Position", "Driver", "Points"]]

    render_leaderboard(full_leaderboard)

    #CC
    st.markdown(f"<h2 style='text-align: center;'>Constructors' Championship", unsafe_allow_html=True)

    combined_results = pd.concat([gp, sprint])
    combined_results = combined_results[combined_results["Points"].notnull()]

    constructors_leaderboard = combined_results.groupby("Constructor", as_index=False)["Points"].sum()
    constructors_leaderboard = constructors_leaderboard.sort_values(by="Points", ascending=False).reset_index(drop=True)
    constructors_leaderboard["Position"] = constructors_leaderboard.index + 1
    constructors_leaderboard["Position"] = constructors_leaderboard["Position"].apply(
        lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd' if x == 3 else 'th'}"
    )

    constructors_leaderboard = constructors_leaderboard[["Position", "Constructor", "Points"]]
    render_leaderboard(constructors_leaderboard)

        

##Hypothetical Chaos Mode

elif option == "Hypothetical Chaos Mode":
    st.markdown(f"<h2 style='text-align: center;'>Hypothetical Chaos Mode</h2>", unsafe_allow_html=True)


    st.write("Type the name of drivers in the Grand Prix positions as they appear in the Leaderboard")
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

    # Create an editable table for 10 positions
    pos_labels = [f"{i+1}{'st' if i+1 == 1 else 'nd' if i+1 == 2 else 'rd' if i+1 == 3 else 'th'}" for i in range(10)]
    hypothetical_input = pd.DataFrame({"Position": pos_labels, "Driver": [""] * 10})
    edited_data = st.data_editor(hypothetical_input, num_rows="fixed", use_container_width=True, hide_index=True)

    #hypothetical entries wdc
    hypothetical_entries = []
    for idx, row in edited_data.iterrows():
        driver_name = row["Driver"].strip()
        if driver_name:
            position_number = str(idx + 1) #positions are 1-indexed
            if position_number in gp_points_table:
                hypothetical_entries.append({
                    "Driver": driver_name,
                    "Points": gp_points_table[position_number]
                })
                
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
    alpine_drivers = ("Pierre Gasley", "Jack Doohan")
    aston_martin_drivers = ("Fernando Alonso", "Lance Stroll")
    ferrari_drivers = ("Charles Leclerc", "Lewis Hamilton")
    haas_drivers = ("Esteban Ocon", "Oliver Bearman")
    kick_sauber_drivers = ("Nico Hulkenberg", "Gabriel Bortoleto")
    mclaren_drivers = ("Lando Norris", "Oscar Piastri")
    mercedes_drivers = ("George Russell", "Kimi Antonelli")
    red_bull_racing_australia_drivers = ("Max Verstappen", "Liam Lawson")
    red_bull_racing_japan_drivers = ("Max Verstappen", "Yuki Tsunoda")
    redbull1_tracks = ("Australia", "China")
    redbull2_tracks = ("Japan", "Bahrain", "Saudi Arabia")
    racing_bulls_australia_drivers = ("Yuki Tsunoda", "Isack Hadjar")
    racing_bulls_japan_drivers = ("Liam Lawson", "Isack Hadjar")
    williams_drivers = ("Carlos Sainz", "Alexander Albon")

    if hypothetical_entries:
        st.markdown(f"<h3 style='text-align: center;'>Projected Constructors Championship</h3>", unsafe_allow_html=True)
 
        alpine_only = combined[combined["Driver"].isin(alpine_drivers)]
        alpine_points = alpine_only["Points"].sum()

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
        
        **Records**:
        - Only driver in history to win Formula Renault, Formula 3, and Formula 2 championships in consecutive seasons
        - Sixth driver in history to win GP2/Formula 2 title in rookie season. 
        - Second highest points driver in their F1 rookie season (97 points, current record held by Lewis Hamilton at 105)

        **Fun Facts**:
        - Red Bull Racing principal Christian Horner has said he regrets not signing Piastri while he was running in Formula 4
        - McLaren and Alpine went to court fighting over Piastri after he was both a reserve driver for McLaren and a test driver for Alpine in 2022
        """,
    "Pierre Gasley": """
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

if option == "Interesting Factoid":
    text_input = st.text_input("enter a driver")
    driverstats = None
    AA23_valid_names = ("Alex Albon", "Albon", "alex albon", "albon", "23")
    AKA12_valid_names = ("Andrea Kimi Antonelli", "Antonelli", "Kimi Antonelli", "andrea kimi antonelli", "antonelli", "kimi antonelli", "12")
    CL16_valid_names = ("Charles Leclerc", "Leclerc", "charles leclerc", "leclerc", "16")
    CS55_valid_names = ("Carlos Sainz", "Sainz", "carlos Sainz", "Sainz", "55")
    EO31_valid_names = ("Esteban Ocon", "Ocon", "esteban ocon", "ocon", "31")
    FA14_valid_names = ("Fernando Alonso", "Alonso", "The Rookie", "Fernando", "fernando alonso", "alonso", "fernando", "the rookie", "14")
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
    OP81_valid_names = ("Oscar Piastri", "oscar piastri", "Piastri", "piastri", "Pastry", "pastry", "Great Barrier Chief", "great barrier chief", "Wizard of Aus", "wizard of aus", "81")
    PG10_valid_names = ("Pierre Gasley", "pierre gasley", "Gasley", "gasley", "10")
    YT22_valid_names = ("Yuki Tsunoda", "Tsunoda", "yuki tsunoda", "tsunoda", "22")
    valid_driver_names = set(AA23_valid_names + AKA12_valid_names + CL16_valid_names + CS55_valid_names + EO31_valid_names + FA14_valid_names + GB5_valid_names + GR63_valid_names + IH6_valid_names + JD7_valid_names + LH44_valid_names + LL30_valid_names + LN4_valid_names + LS18_valid_names + MV33_valid_names + NH27_valid_names + OB87_valid_names + OP81_valid_names + PG10_valid_names + YT22_valid_names)
    invalid_driver_names = set()

    if text_input is None:
        st.write("")
    if text_input in AA23_valid_names:
        driverstats = "Alex Albon"
    elif text_input in AKA12_valid_names:
        driverstats = "Andrea Kimi Antonelli"
    elif text_input in CL16_valid_names:
        driverstats = "Charles Leclerc"
    elif text_input in CS55_valid_names:
        driverstats = "Carlos Sainz"
    elif text_input in EO31_valid_names:
        driverstats = "Esteban Ocon"
    elif text_input in FA14_valid_names:
        driverstats = "Fernando Alonso"
    elif text_input in GB5_valid_names:
        driverstats = "Gabriel Bortoleto"
    elif text_input in GR63_valid_names:
        driverstats = "George Russell"
    elif text_input in IH6_valid_names:
        driverstats = "Isack Hadjar"
    elif text_input in JD7_valid_names:
        driverstats = "Jack Doohan"
    elif text_input in LH44_valid_names:
        driverstats = "Lewis Hamilton"
    elif text_input in LL30_valid_names:
        driverstats = "Liam Lawson"
    elif text_input in LN4_valid_names:
        driverstats = "Lando Norris" 
    elif text_input in LS18_valid_names:
        driverstats = "Lance Stroll"
    elif text_input in MV33_valid_names:
        driverstats = "Max Verstappen"
    elif text_input in NH27_valid_names:
        driverstats = "Nico Hulkenberg"
    elif text_input in OB87_valid_names:
        driverstats = "Oliver Bearman"
    elif text_input in OP81_valid_names:
        driverstats = "Oscar Piastri"
    elif text_input in PG10_valid_names:
        driverstats = "Pierre Gasley"
    elif text_input in YT22_valid_names:
        driverstats = "Yuki Tsunoda"

        
    if driverstats in driver_info:
        st.markdown(driver_info[driverstats], unsafe_allow_html=True)
    else:
        st.write("")

        
##TRACK INFORMATION

if option == "Track Information":

    track = st.selectbox("Choose a Circuit",
                 ["Australia",
                  "China",
                  "Japan",
                  "Bahrain",
                  "Saudi Arabia",
                  "Miami",
                  "Emilia-Romagna",
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
        st.image("/Users/kileytrombly/Desktop/Coding/formula-1-2025-tracker/Saudi_Arabia_Circuit.png")
        st.subheader("**Lap Record:** 1:30.734")
        st.subheader(f"**2024 Winner:** Max Verstappen")
        st.write("**Important Notes:**")
        st.write("Safety car occurance: 100%")
        st.write("Many corners are quite difficult because they're highspeed and blind, with legends like Schumacher even crashing")
        st.write("With three DRS zones and many high speed corners, there are many overtaking opportunities.")
        st.write("**Fun Moments:**")
        st.write("Ollie Bearman's 2024 F1 Debut: Ollie filled in for Carlos Sainz on Ferrari and placed p7 ahead of Lando Norris and Lewis Hamilton")
    else:
        st.write("be patient")

##CONSTRUCTION INFORMATION

constructor_info = {
    "Alpine": """
        info coming soon
        """,
    "Aston Martin": """
        info coming soon
        """,
    "Ferrari": """
        info coming soon
        """,
    "Haas": """
        info coming soon
        """,
    "Kick Sauber": """
        info coming soon
        """,
    "McLaren": """
        info coming soon
        """,
    "Mercedes": """
        info coming soon
        """,
    "Racing Bulls": """
        info coming soon
        """,
    "Red Bull Racing": """
        info coming soon
        """,
    "Williams": """
        info coming soon
        """,
}

if option == "Construction Information":
    text_input = st.text_input("enter a constructor")
    if text_input in constructor_info:
        st.markdown(constructor_info[text_input], unsafe_allow_html=True)
    else:
        st.write("")





