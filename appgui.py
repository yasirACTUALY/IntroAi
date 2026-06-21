import tkinter as tk
from tkinter import ttk

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
    if(recBy == "Restaurant Name"):


    if(recBy == "Cuisine Type"):

    
    if(recBy == "Flavor"):
        


root.mainloop();