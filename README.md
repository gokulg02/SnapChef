## Demo

![SnapChef Demo](/Assets/Demo2x.gif)

*Figure 1: Live demo of SnapChef generating a recipe based on user input.*

---

## Software Architecture

![SnapChef Architecture](/Assets/Software_Arch.png)

*Figure 2: Block diagram of SnapChef's Retrieval-Augmented Generation (RAG) pipeline.*

---

## Features

* **User Authentication**: Secure login using Google OAuth.
* **Personalized Recipe Suggestions**: Get recipe ideas based on:
    * Serving size
    * Cooking time
    * Available ingredients
    * Specific preferences (e.g., spicy, low-oil)
* **AI-Powered Recipe Generation**: Utilizes a powerful language model (GPT-4o) to generate detailed recipes, including dish name, cook time, ingredients, and step-by-step instructions.
* **Interactive Q&A**: Ask follow-up questions to customize the recipe further.
* **RAG Architecture**: The application uses a backend API to retrieve relevant recipes from a database, which are then used to inform the language model's response.

---

## How It Works

SnapChef is comprised of a Streamlit frontend and a Flask backend:

1.  **Frontend (Streamlit)**:
    * The user logs in via Google OAuth to start.
    * The user inputs their desired serving size, cooking time, available ingredients, and any other preferences on the **Home** page.
    * Upon clicking "Generate Recipe," the application sends a request to the backend API with the user's query.
    * The top 5 recipe results from the API are then passed to a language model (GPT-4o).
    * The language model generates a detailed recipe that is displayed to the user.
    * The user can then ask follow-up questions to further refine the recipe.

2.  **Backend (Flask)**:
    * The backend is a simple Flask server with a `/search` endpoint.
    * This endpoint receives a query from the frontend and uses a ChromaDB vector database to find the most relevant recipes from its dataset.
    * The matched recipes are then returned to the frontend.

---

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/gokulg02/snapchef.git](https://github.com/gokulg02/snapchef.git)
    cd snapchef
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up environment variables:**
    * You will need to create a `secrets.toml` file in the `apps/.streamlit/` directory.
    * This file should contain your Google Client ID, Google Client Secret, and your OpenAI API key.
        ```toml
        GOOGLE_CLIENT_ID = "your_google_client_id"
        GOOGLE_CLIENT_SECRET = "your_google_client_secret"
        OPEN_AI_API_KEY = "your_openai_api_key"
        ```
4.  **Run the backend server:**
    ```bash
    python services/app.py
    ```
5.  **Run the Streamlit app:**
    ```bash
    streamlit run apps/Home.py
    ```

---

##  Usage

1.  Open your web browser and navigate to the Streamlit app's URL (usually `http://localhost:8501`).
2.  Log in with your Google account.
3.  Enter your desired serving size, cooking time, and ingredients.
4.  Add any other preferences in the text area.
5.  Click "Generate Recipe" to get your customized recipe.
6.  Use the text input to ask follow-up questions and further tailor the recipe to your needs.