import json
import argparse
import os
import sys
from Model import model, get_embedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# def get_embedding(text):
#     """Mock embedding function for testing without the model loaded."""
#     # In a real implementation, this would call the actual embedding model.
#     # Here we return a random vector for demonstration.
#     print(f"Generating embedding for: {text}")
#     return np.random.rand(768)  # Assuming 768-dimensional embeddings


def clear_embeddings(embds):
    embeddings = [emb for emb in embds[1:] if emb is not None and isinstance(emb, np.ndarray)]
    if embeddings:
        avg_emb = np.mean(embeddings, axis=0)
        return avg_emb
    return 0.0

def generate_restaurant_embedding(restaurant_name, menu_items):
    # menu_items in the form of [[itemName, [ingredient1, ingredient2, ...]], ...]
    #returns a list in the form of [restaurantName, res1item1_emb, res1item1_ingredients_emb, ...]
    restaurant_embedding = [restaurant_name]
    # print(f"Generating embeddings for restaurant: {restaurant_name}")
    # print(f"Menu items: {menu_items}")

    # Generate embeddings for each item and its ingredients
    for item in menu_items:
        # print(f"Processing menu item: {item}")
        if item is None:
            continue

        # Process Item Name
        item_name = item[0]
        
        if item_name:
            # 1. Get embedding for the item name
            item_embedding = get_embedding(item_name)
            restaurant_embedding.append(item_embedding)
            
            # 2. Get embedding for all ingredients combined
            ingredients = item[1]
            if isinstance(ingredients, list) and len(ingredients) > 0:
                ingredients_text = ", ".join(ingredients)
                ingredients_embedding = get_embedding(ingredients_text)
                restaurant_embedding.append(ingredients_embedding)
            else:
                # will notify the developer
                print(f"The menu item {item_name} doesnt have a list of ingredients")
        else:
            print(f"Skipping menu item with no name: {item}")

    print(f"Successfully processed {len(restaurant_embedding)} items.")
    return [restaurant_embedding[0], clear_embeddings(restaurant_embedding[1:])]

def load_restaurants(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def pair_restaurants(restaurant_names, restaurant_embeddings):
    #prints  a list of pairs of restaurants with their similarity scores
     # 1. Compute similarity matrix
    if len(restaurant_embeddings) > 1:
        sim_matrix = cosine_similarity(restaurant_embeddings)
        
        # 2. Group into pairs
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
    
def find_most_similar_restaurant(restaurant, restaurant_names, restaurant_embeddings):
    #returns a list of other restaurants sorted by similarity to the given restaurant (list has the restaurant names and similarity scores)
    if len(restaurant_embeddings) > 1:
        sim_matrix = cosine_similarity(restaurant_embeddings)
        index = restaurant_names.index(restaurant)
        similarities = sim_matrix[index]
        sorted_indices = np.argsort(similarities)[::-1]  # Sort in descending order
        sorted_restaurants = [(restaurant_names[i], similarities[i]) for i in sorted_indices if restaurant_names[i] != restaurant]
        return sorted_restaurants


def extract_item_name(item):
    if isinstance(item, dict):
        return item.get('name') or item.get('item_name') or item.get('title') or item.get('menu_item') or 'Unnamed item'
    return str(item)
def main():
   
    test_data_path = 'testing_data_V1.0.json'

    if not os.path.exists(test_data_path):
        print('Input file not found:', test_data_path, file=sys.stderr)
        sys.exit(2)

    data = load_restaurants(test_data_path)

    restaurant_list = []

    print("Generating embeddings for restaurant menus...")
    for restaurant in data:
        restaurant_name = restaurant.get('restaurant_name') or restaurant.get('name') or 'Unnamed'
        menu_items_dict = restaurant.get('menu', [])
        menu_items = []
        for item in menu_items_dict:
            if item is None:
                continue
            # Process Item Name
            item_name = item.get('item') if isinstance(item, dict) else str(item)
            ingredients = item.get('ingredients', [])
            menu_items.append([item_name, ingredients])

        restaurant_value = generate_restaurant_embedding(restaurant_name, menu_items)
        restaurant_list.append(restaurant_value)

    # 1. Calculate a single representative vector for each restaurant
    restaurant_embeddings = []
    restaurant_names = []

    for restaurant in restaurant_list:
        restaurant_embeddings.append(restaurant[1])
        restaurant_names.append(restaurant[0])
    
    # pairs restaurants by similarity
    # pair_restaurants(restaurant_names, restaurant_embeddings)
    
    # returns a list of other restaurants sorted by similarity to the given restaurant (list has the restaurant names and similarity scores)
    similar_restaurants = find_most_similar_restaurant(restaurant_names[0], restaurant_names, restaurant_embeddings)
    print(f"Most similar restaurants to {restaurant_names[0]}:")
    for name, similarity in similar_restaurants:
        print(f"  {name}: {similarity:.4f}")

                            





if __name__ == '__main__':
    main()
