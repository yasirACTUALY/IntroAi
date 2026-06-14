from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-mpnet-base-v2')

def check_words_similarity(words1, words2):
    emb1 = model.encode(words1)
    emb2 = model.encode(words2)
    return util.cos_sim(emb1, emb2)

# Example usage
if __name__ == "__main__":
    Categories = ['Spicy', 'Sweet', 'Sour', 'Salty', 'Bitter']
    Testcases = ['Lasagna', 'Chocolate Cake', 'Lemonade', 'Pretzels', 'Black Coffee', 'Mexican Tacos', 'Glazed Donuts', 'Sour Candy', 'Salty Chips', 'Bitter Melon', 'Sweetbreads']

    # Embedding each word and for each word find the rank the category which is closest to it
    for testcase in Testcases:
        testcase_embedding = model.encode(testcase)
        category_embeddings = model.encode(Categories)

        # Calculate cosine similarity between the testcase and each category
        similarities = [util.cos_sim(testcase_embedding, category_embedding).item() for category_embedding in category_embeddings]

        # Rank categories from most similar to least similar
        ranked_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)

        print(f"Category ranking for '{testcase}':")
        for rank, idx in enumerate(ranked_indices, start=1):
            print(f"{rank}. {Categories[idx]} ({similarities[idx]:.4f})")
