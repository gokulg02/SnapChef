import streamlit as st

st.title("🍳 SnapChef: Recipe Suggestion RAG")

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

# Navigate to generation page
if st.button("Generate Recipe"):
    st.session_state["serving_size"] = serving_size
    st.session_state["cooking_time"] = cooking_time
    st.session_state["prompt"] = prompt
    st.switch_page("pages/GenerateRecipe.py")