import streamlit as st
from streamlit_oauth import OAuth2Component
import os

st.title("🍳 SnapChef: Recipe Suggestion RAG")

client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
redirect_uri = "http://localhost:8501"  

token = None

# Initialize OAuth component
oauth2 = OAuth2Component(
    client_id=client_id,
    client_secret=client_secret,
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token"
)

# Trigger auth
# token = oauth2.authorize_button(
#     name="Continue with Google",
#     redirect_uri=redirect_uri,
#     scope="openid email profile",
#     key="google_login"
# )
# # token = True

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
    st.json(token)
    # if st.button("Refresh Token"):
    #     # If refresh token button is clicked, refresh the token
    #     token = oauth2.refresh_token(token)
    #     st.session_state.token = token
    #     st.rerun()


# Servings
st.markdown("### Servings")
serving_size = st.number_input(
    "Enter servings", min_value=1, max_value=15, value=2
)

# Cooking Time
st.markdown("### Cooking Time")
cooking_time = st.selectbox(
    "Select approximate cooking time",
    ["< 30 minutes", "30-60 minutes", "> 60 minutes"]
)

# Ingredients
st.markdown("### Ingredients")
if "ingredients_list" not in st.session_state:
    st.session_state["ingredients_list"] = []

def add_ingredient():
    ingredient = st.session_state.ingredient_input
    if ingredient:
        st.session_state.ingredients_list.append(ingredient)
        st.session_state.ingredient_input = ""

st.text_input(
    "Add an ingredient",
    key="ingredient_input",
    on_change=add_ingredient
)

# Remove buttons
remove_indices = []
for i, ing in enumerate(st.session_state["ingredients_list"]):
    col1, col2 = st.columns([5, 1])
    col1.write(f"- {ing}")
    if col2.button("❌", key=f"del_{i}"):
        remove_indices.append(i)
for i in sorted(remove_indices, reverse=True):
    st.session_state["ingredients_list"].pop(i)

# Prompt
st.markdown("### Preferences")
prompt = st.text_area("Describe preferences", placeholder="e.g., I want a spicy, low-oil recipe")

if token and st.button("Generate Recipe"):
    st.session_state["serving_size"] = serving_size
    st.session_state["cooking_time"] = cooking_time
    st.session_state["prompt"] = prompt
    st.switch_page("pages/GenerateRecipe.py")
