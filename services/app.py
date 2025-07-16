# app.py

from flask import Flask, request, jsonify
import pandas as pd
import chromadb

# ------------------------------
# Load your CSV ONCE at startup
# ------------------------------
CSV_PATH = "ChromaDB/recipes.csv"
RECIPES_DF = pd.read_csv(CSV_PATH)
chroma_client = chromadb.PersistentClient(path="dataset")
collection = chroma_client.get_or_create_collection(name="my_collection")

# ------------------------------
# Initialize Flask app
# ------------------------------
app = Flask(__name__)

# ------------------------------
# Function: Query Chroma + Get Recipes
# ------------------------------
def query_chroma_and_get_recipes(
    query_texts,
    n_results=5
):

    # 2) Query Chroma for similar IDs
    results = collection.query(
        query_texts=query_texts,
        n_results=n_results
    )

    # 3) Flatten and convert IDs to int
    ids = [int(i) for i in results['ids'][0]]
    print("ids",ids)
    # 4) Filter global DataFrame instead of reading CSV each time
    matched_df = RECIPES_DF[RECIPES_DF['id'].isin(ids)]

    # 5) Return rows as list of dicts
    return matched_df.to_dict(orient="records")

# ------------------------------
# Flask GET route
# ------------------------------
@app.route('/search', methods=['GET'])
def search():
    # Get query params
    query_text = request.args.get('query')
    n_results = int(request.args.get('n', 10))

    if not query_text:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    # Run query
    recipes = query_chroma_and_get_recipes(
        query_texts=[query_text],
        n_results=n_results
    )

    return jsonify(recipes)

# ------------------------------
# Run the app
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
