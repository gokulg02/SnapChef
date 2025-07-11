import streamlit as st
import requests
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


if "chat_history" in st.session_state:
    del st.session_state["chat_history"]

st.title("👩‍🍳 SnapChef: Generating Your Recipe")

# Check if inputs are present
required_keys = ["serving_size", "cooking_time", "prompt", "ingredients_list"]
for k in required_keys:
    if k not in st.session_state:
        st.warning("Incomplete input. Please go back to the home page.")
        st.stop()

serving_size = st.session_state["serving_size"]
cooking_time = st.session_state["cooking_time"]
prompt_text = st.session_state["prompt"]
ingredients_list = st.session_state["ingredients_list"]

llm = ChatOpenAI(
    openai_api_key="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",
    model="gpt-4o"
)

# Use a single memory instance in session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# ConversationChain automatically includes the full history
conversation = ConversationChain(
    llm=llm,
    memory=st.session_state.memory
)

with st.spinner("Generating your recipe using RAG + LLM..."):
    query = f"{prompt_text} that can be made with {', '.join(ingredients_list)} and takes {cooking_time}."
    response = requests.get(
        "http://127.0.0.1:5000/search",
        params={"query": query, "n": 5}
    )
    if response.ok:
        api_response = response.json()
    else:
        st.error(f"API error {response.status_code}: {response.text}")
        st.stop()

    recipe_summary = ""
    for i, recipe in enumerate(api_response, 1):
        title = recipe.get("name", "Untitled")
        servings = recipe.get("servings", "N/A")
        desc = recipe.get("description", "")
        ingredients = recipe.get("ingredients_raw", [])
        if isinstance(ingredients, str):
            ingredients = [ingredients]
        ingredients_fmt = ", ".join(ingredients) if ingredients else "Not specified"
        steps = recipe.get("steps", "") or "No steps provided."
        recipe_summary += (
            f"{i}. {title} — serves {servings}\n"
            f"   Description: {desc}\n"
            f"   Ingredients: {ingredients_fmt}\n"
            f"   Steps: {steps}\n\n"
        )

    user_intent = prompt_text if prompt_text else "Find a recipe"
    ingredients_display = ", ".join(ingredients_list)

    llm_prompt = f"""
        The user describes the dish they would like to have as "{user_intent}".
        Here is a summary of the top 5 recipes that match users interest:
        {recipe_summary}

        Using this information, suggest the best recipe that fits user's requirements of:
        - Time available: {cooking_time}
        - Ingredients available: {st.session_state['ingredients_list']}

        The suggested recipe should have the following:
        1. Dish name
        2. Approximate Cook time
        3. Ingridients for {serving_size} servings
        4. Cooking steps in bullet points

        Feel free to adapt the recipe according to the user needs and the ingredients user has. 
        """
    
#     llm_prompt = f"""
# You are a helpful AI chef assistant.

# User Intent: "{user_intent}"
# Available Ingredients: {ingredients_display}
# Desired Cooking Time: {cooking_time}
# Desired Servings: {serving_size}

# Top 5 Retrieved Recipes:
# {recipe_summary}

# Please reason step by step:
# Step 1: Identify best recipes matching ingredients, time, and servings.
# Step 2: Suggest substitutions if ingredients missing.
# Step 3: Adjust quantities for {serving_size} servings.
# Step 4: Write clear, bullet-point instructions.
# Step 5: Give a brief explanation if needed.

# Finally, present *only*:
# - Dish Name
# - Estimated Cook Time
# - Ingredients for {serving_size} servings
# - Step-by-step instructions
# """

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI chef."),
        ("human", "{topic}")
    ])
    # chain = prompt_template | llm

    # llm_response = chain.invoke({"topic": llm_prompt})

    if "recipe_generated" not in st.session_state:
        llm_response = conversation.invoke({"input": llm_prompt})
        st.session_state.recipe_generated = llm_response["response"]
        st.markdown(st.session_state.recipe_generated)
    else:
        st.markdown(st.session_state.recipe_generated)

# Optional: Follow-up Q&A
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# user_followup = st.text_input("Ask SnapChef follow-up questions (optional):")

# if user_followup:
#     followup_prompt = f"""
# User follow-up: "{user_followup}"
# Given the previous recipe, update the recipe according to the follow-up and print the updated recipe.
# """
#     followup_response = chain.invoke({"topic": followup_prompt})
#     st.session_state["chat_history"].append((user_followup, followup_response.content))

# for idx, (q, a) in enumerate(st.session_state["chat_history"]):
#     st.markdown(f"*User:* {q}")
#     st.markdown(f"*SnapChef:* {a}")

user_followup = st.text_input("Ask SnapChef follow-up questions to customize recipe further (optional):")

if st.button("Add Follow-up") and user_followup:
    followup_response = conversation.invoke({"input": user_followup})
    st.session_state["chat_history"].append((user_followup, followup_response["response"]))

# Display chat history
for q, a in st.session_state["chat_history"]:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**SnapChef:** {a}")
