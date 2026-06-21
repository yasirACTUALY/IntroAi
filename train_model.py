import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import loadDataSet
import Model
from loadDataSet import data
from Model import model

# Prepare the data
# Combine recipe title and ingredients as input
data['combined_input'] = data['recipe_title'] + " " + data['ingredients_canonical'].apply(lambda x: " ".join(x))

# Filter out rows with missing taste data
model_data = data[['combined_input', 'primary_taste']].dropna()

# 80-20 split
train_df, val_df = train_test_split(model_data, test_size=0.8, random_state=42)

# Map labels to integers
unique_labels = model_data['primary_taste'].unique().tolist()
label_2_id = {label: i for i, label in enumerate(unique_labels)}

# Convert to SentenceTransformer InputExamples
# SoftmaxLoss expects at least two texts. For classification, we repeat the input.
train_examples = [
    InputExample(texts=[row['combined_input'], row['combined_input']], label=label_2_id[row['primary_taste']]) 
    for _, row in train_df.iterrows()
]

# Create DataLoader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

# Define loss (using the updated embedding dimension method name)
train_loss = losses.SoftmaxLoss(
    model=model, 
    embedding_dimension=model.get_embedding_dimension(), 
    num_labels=len(unique_labels)
)

# Fine-tune the model
print("Starting fine-tuning with corrected input format...")
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=1,
    warmup_steps=100,
    show_progress_bar=True
)

print("Fine-tuning complete.")