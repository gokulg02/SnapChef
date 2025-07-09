import streamlit as st
import requests

st.title("SnapChef: Recipe Suggestion RAG")


#Servings Selection
st.markdown(
    "<p style='font-size: 18px; font-weight: bold;'>Servings</p>",
    unsafe_allow_html=True
)

serving_size = st.number_input(
    "Enter the number of servings you want", min_value=1, max_value=15, value=2, step=1,
    help="Enter the number of servings you want"
)


# Cooking Time Selection
st.markdown(
    "<p style='font-size: 18px; font-weight: bold;'>Cooking Time</p>",
    unsafe_allow_html=True
)

cooking_time = st.selectbox(
    "Select approximate cooking time",
    options=["< 30 minutes", "30-60 minutes", "> 60 minutes"],
    index=0,
    help="Select approximate cooking time"
)


# Ingredients Input
st.markdown(
    "<p style='font-size: 18px; font-weight: bold;'>Ingredients</p>",
    unsafe_allow_html=True
)

if "ingredients_list" not in st.session_state:
    st.session_state["ingredients_list"] = []

def add_ingredient():   # Function to clear input after adding
    ingredient = st.session_state.ingredient_input
    if ingredient:
        st.session_state.ingredients_list.append(ingredient)
        st.session_state.ingredient_input = ""  # This clears the input

st.text_input(
    "Add an ingredient and press Enter",
    key="ingredient_input",
    on_change=add_ingredient
)

remove_indices = []
for i, ingredient in enumerate(st.session_state["ingredients_list"]):
    col1, col2 = st.columns([5, 1])
    col1.write(f"- {ingredient}")
    if col2.button("❌", key=f"del_{i}"):
        remove_indices.append(i)

for i in sorted(remove_indices, reverse=True):
    st.session_state["ingredients_list"].pop(i)


# Prompt Input
st.markdown(
    "<p style='font-size: 18px; font-weight: bold;'>Prompt</p>",
    unsafe_allow_html=True
)

prompt = st.text_area(
    "Enter a description and preferences for your recipe",
    placeholder="e.g., I want a spicy, low-oil recipe",
    help="Optionally add any preferences or additional instructions"
)


# Generate and Output Recipe 
if st.button("Generate Recipe"):
    with st.spinner("Generating your recipe using RAG model..."):
        query = f"{prompt} that can be made with {', '.join(st.session_state['ingredients_list'])} and takes {cooking_time}."
        response = requests.get(
            "http://127.0.0.1:5000/search",
            params={"query": query, "n": 5}
        )
        
        if response.ok:
            api_response = response.json()
        else:
            api_response = f"API returned error {response.status_code}: {response.text}"


        # ingredients_display = ", ".join(st.session_state["ingredients_list"])
        # output_recipe = (
        #     f"### Suggested Recipe\n"
        #     f"- **Serving Size:** {serving_size}\n"
        #     f"- **Cooking Time:** {cooking_time}\n"
        #     f"- **Ingredients:** {ingredients_display}\n"
        #     f"- **Prompt:** {prompt}\n\n"
        #     "**Instructions:**\n"
        #     "1. Prepare your ingredients.\n"
        #     "2. Follow your preferred cooking method based on the time and ingredients.\n"
        #     "3. Enjoy your customized recipe!"
        # )

        output_recipe = (
            f"### DB query\n"
            f"{query}\n"
            f"### API response\n"
            f"{api_response}\n"
        )
        # output_recipe = (query)
        st.markdown(output_recipe)
