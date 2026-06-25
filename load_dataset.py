import pandas as pd

# Load dataset
def load_dataset(filepath):
    """Load dataset from CSV file"""
    try:
        # choose reader based on file extension
        if filepath.lower().endswith('.csv'):
            data = pd.read_csv(filepath)
        elif filepath.lower().endswith('.json'):
            # try newline-delimited JSON first, fall back to regular JSON
            try:
                data = pd.read_json(filepath, lines=True)
            except ValueError:
                data = pd.read_json(filepath)
        else:
            # default: try CSV then JSON
            try:
                data = pd.read_csv(filepath)
            except Exception:
                data = pd.read_json(filepath)
        print(f"Dataset loaded successfully: {filepath}")
        print(f"Shape: {data.shape}")
        # print(f"\nFirst few rows:\n{data.head()}")
        return data
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return None
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None


def search_data(column, value):
    """Search rows in a dataframe by column value."""
    if data is None:
        return None
    if column not in data.columns:
        print(f"Error: Column '{column}' not found")
        return None
    result = data[data[column].astype(str).str.contains(str(value), case=False, na=False)]
    print(f"Found {len(result)} matching rows")
    return result


def get_column_data( column):
    """Access a single column from the dataset."""
    if data is None:
        return None
    if column not in data.columns:
        print(f"Error: Column '{column}' not found")
        return None
    return data[column]


def get_row_by_index(index):
    """Access a single row from the dataset by index."""
    if data is None:
        return None
    try:
        return data.iloc[index]
    except Exception as e:
        print(f"Error accessing row {index}: {e}")
        return None


def find_recipes_by_name( word):
    """Find all recipes that contain a word in their name."""
    if data is None:
        print(f"Error: Data not loaded")
        return None
    if 'recipe_title' not in data.columns:
        print(f"Error: 'recipe_title' column not found")
        return None
    result = data[data['recipe_title'].astype(str).str.contains(word, case=False, na=False)]
    if result.empty:
        print(f"Found 0 recipes containing '{word}'")
        return None
    print(f"Found {len(result)} recipes containing '{word}'")
    for idx, row in result.iterrows():
        print(f"  - {row['recipe_title']}")
    # return result.loc[result['recipe_title'].astype(str).str.len().idxmin()]
    
def get_ingredients_by_recipe_name( word):
    """Find all recipes that contain a word in their name."""
    if data is None:
        return None
    if 'recipe_title' not in data.columns:
        print(f"Error: 'recipe_title' column not found")
        return None
    result = data[data['recipe_title'].astype(str).str.contains(word, case=False, na=False)]
    if result.empty:
        print(f"Found 0 recipes containing '{word}'")
        return None
   #print(f"Found {len(result)} recipes containing '{word}'")
    return result;
    for idx, row in result.iterrows():
        print(f"  - {row['ingredients_canonical']}")

data = load_dataset('dataset/recipes_extended.json')
# Example usage
if __name__ == "__main__":
    # Load dataset/recipes_extended.json by default
    dataset = load_dataset('dataset/recipes_extended.json')
    if dataset is not None:
        # print(f"\nDataset Info:")
        # print(dataset.info())
        # Example usage:
        print(find_recipes_by_name(dataset, 'Hamburger'))
        # print(get_column_data(dataset, 'recipe_title').head())
        # print(get_row_by_index(dataset, 0))
