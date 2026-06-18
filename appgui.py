import tkinter as tk

root = tk.Tk();
root.title("Restaurant Recommender");
root.geometry("800x600");

button = tk.Button(root, text="Stop", width = 25, command=root.destroy);
button.pack(side="bottom");

root.mainloop();