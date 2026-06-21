import json
import argparse
import os
import sys
from Model import model, get_embedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



def load_restaurants(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def extract_item_name(item):
    if isinstance(item, dict):
        return item.get('name') or item.get('item_name') or item.get('title') or item.get('menu_item') or 'Unnamed item'
    return str(item)

def restaurant_to_list(data):
    # a list in the form of [[restrurantName, res1item1_emb, res1item1_ingredients_emb, ...], ...]
    restaurant_list = []

    print("Generating embeddings for restaurant menus...")
    for restaurant in data:
        restaurant_name = restaurant.get('restaurant_name') or restaurant.get('name') or 'Unnamed'
        menu_items = restaurant.get('menu', [])

        # Initialize the row with the name
        current_restaurant_entry = [restaurant_name]

        # Generate embeddings for each item and its ingredients
        for item in menu_items:
            if item is None:
                continue

            # Process Item Name
            item_name = item.get('item') if isinstance(item, dict) else str(item)
            
            if item_name:
                # 1. Get embedding for the item name
                item_embedding = get_embedding(item_name)
                current_restaurant_entry.append(item_embedding)
                
                # 2. Get embedding for all ingredients combined
                ingredients = item.get('ingredients', [])
                if isinstance(ingredients, list) and len(ingredients) > 0:
                    ingredients_text = ", ".join(ingredients)
                    ingredients_embedding = get_embedding(ingredients_text)
                    current_restaurant_entry.append(ingredients_embedding)
                else:
                    # item without ingredients
                    current_restaurant_entry.append(None)
                    # will notify the developer
                    print(f"The menu item {item_name} doesnt have a list of ingredients")

        restaurant_list.append(current_restaurant_entry)
    print(f"Successfully processed {len(restaurant_list)} restaurants.")
    return restaurant_list


def main():
    test_data_path = 'testing_data_V1.0.json'

    if not os.path.exists(test_data_path):
        print('Input file not found:', test_data_path, file=sys.stderr)
        sys.exit(2)

    data = load_restaurants(test_data_path)

    # 1. Calculate a single representative vector for each restaurant
    restaurant_embeddings = []
    restaurant_names = []

    restaurant_list = restaurant_to_list(data)
    for restaurant in restaurant_list:
        name = restaurant[0]
        # Extract all embeddings (skipping the name and any None values)
        embeddings = [emb for emb in restaurant[1:] if emb is not None and isinstance(emb, np.ndarray)]
        
        if embeddings:
            avg_emb = np.mean(embeddings, axis=0)
            restaurant_embeddings.append(avg_emb)
            restaurant_names.append(name)

    # 2. Compute similarity matrix
    if len(restaurant_embeddings) > 1:
        sim_matrix = cosine_similarity(restaurant_embeddings)
        
        # 3. Group into pairs
        paired = set()
        groups = []
        
        # Sort similarities to find best matches
        for i in range(len(restaurant_names)):
            if i in paired:
                continue
            
            # Find most similar that isn't already paired
            current_sims = sim_matrix[i].copy()
            current_sims[i] = -1  # Don't match with self
            
            # Zero out already paired indices
            for p_idx in paired:
                current_sims[p_idx] = -1
                
            best_match_idx = np.argmax(current_sims)
            
            if current_sims[best_match_idx] > -1:
                groups.append((restaurant_names[i], restaurant_names[best_match_idx], current_sims[best_match_idx]))
                paired.add(i)
                paired.add(best_match_idx)

        print("\n--- Restaurant Groups (Pairs by Similarity) ---")
        for r1, r2, sim in groups:
            print(f"{r1} & {r2} (Similarity: {sim:.4f})")
    else:
        print("Not enough restaurants to form pairs.")
                            





if __name__ == '__main__':
    main()
