import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


greeting_data = [
    ("hi!", "hey there!"),
    ("hello", "what can i do ya for"),
    ("hey", "hi!"),
    ("what's up", "hello! do you like the cars? the cars that go vroom?"),
    ("howdy", "howdy partner!"),
    ("good morning", "hidy ho!"),
    ("goodbye", "later skater!"),
    ("bye", "bye bye!"),
    ("sorry", "no worries, pal"),
    ("tell me about", "what do you want to know? i'm very smart"),
    ("what", "sorry, i dont understand. can you rephrase that?"),
    ("i asked about something else", "sorry, i mustve gotten things mixed up. can you ask again?"),

    # Car-related questions
    ("tell me about the car", "F1 cars are built for speed and downforce. Want tech details?"),
    ("how fast is the car", "F1 cars can exceed 220 mph with immense cornering grip."),
    ("what is the car made of", "Carbon fiber composites make F1 cars strong and super light."),
    ("is the car electric", "Not fully — they're hybrids with electric power + internal combustion."),
    ("describe the aerodynamics", "F1 cars use wings and diffusers to create downforce and reduce drag."),
    ("how heavy is the car", "An F1 car weighs at least 798 kg including the driver."),
    ("how do the tires work", "Different compounds provide grip depending on track temperature and wear."),
    ("does DRS affect the car", "Yes, DRS opens the rear wing to reduce drag and boost top speed."),

    #mclaren related questions
    ("what's cool about the mclaren MCL39?", "i LOVE the mclaren car. i think the coolest feature was actually on their car from 2024, the MCL38. that car had a spike on the front wing to gently discourage people from bumping them"),
    ("describe the mclaren car", "it's really designed for aerodynamics, with arguably one of the best rear wings in the game. the mclaren car is so good this year, that red-bull team principal has already accused them of cheating, twice!"),
    ("what makes the mclaren car so good?", "part of the reason the mclaren car is performing so well is because of their rear tyre managment. no one quite knows how (yet), but their rear tyres just dont overheat as fast as everyone elses"),
    ("is the mclaren car legal?", "while redbull has accused mclaren of cheating several times already in 2025, the mclaren car is currently up to code!"),
    ("why was mclaren accused of cheating?", "redbull thought that mclaren was possibly still using mini-DRS in the 2025 season, which would be against FIA regulations"),
    ("is a car spike legal?", "not anymore. however, in 2024, when mclaren implimented it for the first time, it was within regulations"),
    ("mclaren MCL39 suspension", "mclaren uses a pull-rod front suspension and a push-rod rear suspension"),

    #redbull related questions
    ("what's cool about the redbull?", "nothing, its dogwater")
]


X = [item[0] for item in greeting_data]  # input phrases
y = [item[1] for item in greeting_data]  # appropriate responses

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

def get_best_response(user_input):
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X_vec)
    best_match_index = similarities.argmax()
    return y[best_match_index]

st.title("Revvy")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("i love talking about f1!")

#response
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = get_best_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

#chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])



