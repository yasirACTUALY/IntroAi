import tkinter as tk
from tkinter import ttk
import prototype1_test
import sys
import os
import numpy as np
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

def recommend():
    inputText = recEntry.get();
    recBy = combo_box.get();
    test_data_path = 'testing_data_V1.0.json';
    if(recBy == "Restaurant Name"):
        test_data_path = 'testing_data_V1.0.json'
        if not os.path.exists(test_data_path):
            print('Input file not found:', test_data_path, file=sys.stderr)
            sys.exit(2)
        data = prototype1_test.load_data(test_data_path);
        restaurant_list = prototype1_test.restaurant_to_list(data);
        restaurant_embeddings = []
        restaurant_names = [];
        inputIndex = -1;
        i = 0;

        restaurant_list = prototype1_test.restaurant_to_list(data)
        for restaurant in restaurant_list:
            
            name = restaurant[0]
            if name == inputText:
                inputIndex = i;
            # Extract all embeddings (skipping the name and any None values)
            embeddings = [emb for emb in restaurant[1:] if emb is not None and isinstance(emb, np.ndarray)]
        
            if embeddings:
                avg_emb = np.mean(embeddings, axis=0)
                restaurant_embeddings.append(avg_emb)
                restaurant_names.append(name)
            i += 1;
        if inputIndex != -1:
            if len(restaurant_embeddings) > 1:
                sim_matrix = cosine_similarity(restaurant_embeddings)


        
        
        



        


root.mainloop();