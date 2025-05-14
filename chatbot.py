import streamlit as st
import fastf1
import fastf1.plotting
import seaborn as sns
fastf1.Cache.enable_cache('/workspaces/formula1forthegirlies/__pycache__') 
import matplotlib.pyplot as plt

AA23_valid_names = ("Alex Albon", "Albon", "alex albon", "albon", "23")
AKA12_valid_names = ("Andrea Kimi Antonelli", "Antonelli", "Kimi Antonelli", "andrea kimi antonelli", "antonelli", "kimi antonelli", "12")
CL16_valid_names = ("Charles Leclerc", "Leclerc", "charles leclerc", "leclerc", "16")
CS55_valid_names = ("Carlos Sainz", "carlos sainz", "Sainz", "carlos Sainz", "Sainz", "55")
EO31_valid_names = ("Esteban Ocon", "Ocon", "esteban ocon", "ocon", "31")
FA14_valid_names = ("Fernando Alonso", "Alonso", "The Rookie", "Fernando", "fernando alonso", "alonso", "fernando", "the rookie", "14")
FC43_valid_names = ("Franco Colapinto", "Colapinto", "franco colapinto", "colapinto")
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
OB87_valid_names = ("Oliver Bearman", "oliver bearman", "Ollie Bearman", "ollie bearman", "Ollie in the Wallie", "ollie in the wallie","Bearman", "87")
OP81_valid_names = ("Oscar Piastri", "oscar piastri", "Piastri", "piastri", "Pastry", "pastry", "Great Barrier Chief", "great barrier chief", "Wizard of Aus", "wizard of aus", "oscar", "Oscar", "81")
PG10_valid_names = ("Pierre Gasley", "pierre gasley", "Gasley", "gasley", "10", "Pierre Gasly", "pierre gasly", "gasly")
YT22_valid_names = ("Yuki Tsunoda", "Tsunoda", "yuki tsunoda", "tsunoda", "22")
valid_driver_names = set(AA23_valid_names + AKA12_valid_names + CL16_valid_names + CS55_valid_names + EO31_valid_names + FA14_valid_names + GB5_valid_names + GR63_valid_names + IH6_valid_names + JD7_valid_names + LH44_valid_names + LL30_valid_names + LN4_valid_names + LS18_valid_names + MV33_valid_names + NH27_valid_names + OB87_valid_names + OP81_valid_names + PG10_valid_names + YT22_valid_names)

# map names to driver codes
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
                st.error(f"An error occured: {e}")

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
                st.error(f"An error occurred: {e}")
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
                st.error(f"An error occurred: {e}")

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
                st.error(f"error: {str(e)}")

