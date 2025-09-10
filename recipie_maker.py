import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random


# Download NLTK data (needed only the first time you run)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download("punkt_tab")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# --- Clean the words ---
def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t.isalpha() and t not in stop_words]
    return tokens

# --- Nutrition info (per 100g) ---
nutrition_db = {
    "chicken": {"calories": 239, "protein": 27},
    "rice": {"calories": 130, "protein": 2.7},
    "garlic": {"calories": 149, "protein": 6.4},
    "tomato": {"calories": 18, "protein": 0.9},
    "onion": {"calories": 40, "protein": 1.1},
    "egg": {"calories": 155, "protein": 13},
    "oil": {"calories": 884, "protein": 0}
}

# --- How to cook (random steps) ---
cooking_methods = ["chop", "boil", "fry", "mix", "grill", "bake"]

def generate_recipe(ingredients):
    steps = []
    for ing in ingredients:
        method = random.choice(cooking_methods)
        steps.append(f"{method.capitalize()} the {ing}.")
    steps.append("Finally, serve and enjoy your meal! 🍽️")
    return steps

# --- Count calories + protein ---
def calculate_nutrition(ingredients):
    total_calories = 0
    total_protein = 0
    missing = []
    for ing in ingredients:
        if ing in nutrition_db:
            total_calories += nutrition_db[ing]["calories"]
            total_protein += nutrition_db[ing]["protein"]
        else:
            missing.append(ing)
    return total_calories, total_protein, missing

# --- Streamlit App ---
st.set_page_config(page_title="NLP Recipe Maker", page_icon="🍳", layout="centered")

st.title("🍳 NLP Recipe Maker")
st.write("Type your ingredients and I’ll make a recipe + show calories and protein.")

user_input = st.text_input("What ingredients do you have? (e.g., chicken, rice, garlic)")

if st.button("Make Recipe"):
    if user_input.strip() == "":
        st.warning("Please enter some ingredients!")
    else:
        ingredients = preprocess(user_input)

        st.subheader("📋 Recipe Steps")
        recipe = generate_recipe(ingredients)
        for step in recipe:
            st.write("- " + step)

        calories, protein, missing = calculate_nutrition(ingredients)

        st.subheader("📊 Nutrition Info")
        st.write(f"**Total Calories:** {calories} kcal")
        st.write(f"**Total Protein:** {protein} g")

        if missing:
            st.info(f"No nutrition data available for: {', '.join(missing)}")
