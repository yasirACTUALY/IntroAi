import tkinter as tk
from tkinter import ttk
import prototype1_test
import evaluate
import sys
import os
import numpy as np
import load_dataset
from sklearn.metrics.pairwise import cosine_similarity

root = tk.Tk();
root.title("Restaurant Recommender");
root.geometry("800x600");

exitbutton = tk.Button(root, text="Exit", width = 25, command=root.destroy);
exitbutton.pack(side="bottom");

label = tk.Label(root, text = "Recommending based on: ");
label.pack(pady = 10);

def select(event):
    selected_item = combo_box.get();
    label.config(text="Recommending based on: " + selected_item);

combo_box = ttk.Combobox(
    root,
    values = ["Restaurant Name", "Cuisine Type", "Flavor"],
    state = "readonly"
)
combo_box.pack(pady=5);
combo_box.set("Restaurant Name");
combo_box.bind("<<ComboboxSelected>>", select);

recEntry = tk.Entry(root);
recEntry.pack();

dietary_label = tk.Label(root, text="Dietary Restrictions (Leave Blank if None):");
dietary_label.pack();

dietary_entry = tk.Entry(root);
dietary_entry.pack();

confirmbutton = tk.Button(root, text="Get Recommendations", width=25);
confirmbutton.pack(pady=10);



test_data_path = 'testing_data_V1.0.json'

if not os.path.exists(test_data_path):
    print('Input file not found:', test_data_path, file=sys.stderr)
    sys.exit(2)

data = evaluate.load_restaurants(test_data_path)

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
        ingredients = load_dataset.get_ingredients_by_recipe_name(item_name)
        menu_items.append([item_name, ingredients])
   
restaurant_value = evaluate.generate_restaurant_embedding(restaurant_name, menu_items)
restaurant_list.append(restaurant_value)

restaurant_embeddings = []
restaurant_names = []

for restaurant in restaurant_list:
    restaurant_embeddings.append(restaurant[1])
    restaurant_names.append(restaurant[0])

def recommend():
    print("Generating recommendations...")
    inputRestaurant = recEntry.get();
    inputIndex = -1;
    for name in restaurant_names:
        if name == inputRestaurant:
            inputIndex = restaurant_names.index(name)
            break
    else:
        print("Input restaurant not found.")
        return
    similar_restaurants = evaluate.find_most_similar_restaurant(restaurant_names[inputIndex], restaurant_names, restaurant_embeddings)


        
        
        



        

root.mainloop();