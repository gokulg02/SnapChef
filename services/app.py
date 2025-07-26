# Import libraries
from flask import Flask, request, jsonify
import pandas as pd
import chromadb

# Load dataset
csv_path = "services/ChromaDB/recipes.csv"
RECIPES_DF = pd.read_csv(csv_path)
chroma_client = chromadb.PersistentClient(path="services/ChromaDB/dataset")
collection = chroma_client.get_or_create_collection(name="my_collection")

# Initialize Flask app
app = Flask(__name__)

# Define function to query chroma and get recipes
def query_chroma(
    query_texts,
    n_results=5
):
    # Query Chroma for similar IDs
    results = collection.query(
        query_texts=query_texts,
        n_results=n_results
    )

    # Flatten and convert IDs to int
    ids = [int(i) for i in results['ids'][0]]
    print("ids",ids)

    # Filter global DataFrame instead of reading CSV each time
    matched_df = RECIPES_DF[RECIPES_DF['id'].isin(ids)]

    # Return rows as list of dicts
    return matched_df.to_dict(orient="records")

# Flask GET route
@app.route('/search', methods=['GET'])
def search():
    # Get query params
    query_text = request.args.get('query')
    n_results = int(request.args.get('n', 10))

    if not query_text:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    # Run query
    recipes = query_chroma(
        query_texts=[query_text],
        n_results=n_results
    )

    return jsonify(recipes)


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)