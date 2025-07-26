# Import libraries
import streamlit as st
from streamlit_oauth import OAuth2Component
import os

st.title("🍳 SnapChef: Recipe Suggestion RAG")

# Load OAuth credentials from secrets 
client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
redirect_uri = "http://localhost:8501"  

token = None

# Initialize OAuth2Component for Google login
oauth2 = OAuth2Component(
    client_id=client_id,
    client_secret=client_secret,
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token"
)

# Handle login flow
if 'token' not in st.session_state:
    # If not, show authorize button
    result = oauth2.authorize_button("Log in using Google","http://localhost:8501", "openid email profile")
    if result and 'token' in result:
        # If authorization successful, save token in session state
        st.session_state.token = result.get('token')
        st.rerun()
else:
    # If token exists in session state, show the token
    token = st.session_state['token']


# Servings Input
st.markdown("### Servings")
serving_size = st.number_input(
    "Enter servings", min_value=1, max_value=15, value=2
)

# Cooking Time Input
st.markdown("### Cooking Time")
cooking_time = st.selectbox(
    "Select approximate cooking time",
    ["< 30 minutes", "30-60 minutes", "> 60 minutes"]
)

# Ingredients Input
st.markdown("### Ingredients")

# Initialize ingredients list in session state if not already present
if "ingredients_list" not in st.session_state:
    st.session_state["ingredients_list"] = []

# Define helper function to add ingredient to list when input changes
def add_ingredient():
    ingredient = st.session_state.ingredient_input
    if ingredient:
        st.session_state.ingredients_list.append(ingredient)
        st.session_state.ingredient_input = ""

# Text input for ingredient entry
st.text_input(
    "Add an ingredient",
    key="ingredient_input",
    on_change=add_ingredient
)

# Display current ingredients with option to remove 
remove_indices = []
for i, ing in enumerate(st.session_state["ingredients_list"]):
    col1, col2 = st.columns([5, 1])
    col1.write(f"- {ing}")
    if col2.button("❌", key=f"del_{i}"):
        remove_indices.append(i)
for i in sorted(remove_indices, reverse=True):
    st.session_state["ingredients_list"].pop(i)

# User Prompt / Preferences
st.markdown("### Preferences")
prompt = st.text_area("Describe preferences", placeholder="e.g., I want a spicy, low-oil recipe")

#  Final Recipe Generation 
if token and st.button("Generate Recipe"):
    st.session_state["serving_size"] = serving_size
    st.session_state["cooking_time"] = cooking_time
    st.session_state["prompt"] = prompt
    st.switch_page("pages/GenerateRecipe.py")
