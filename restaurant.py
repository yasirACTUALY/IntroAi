class restaurant:
    def __init__(self, name, menuItems):
        self.name = name
        self.menuItems = menuItems
    def compare_item(self, otherRestaurant, selfIndex, otherIndex):
        selfItem = self.menuItems[selfIndex]
        otherItem = otherRestaurant.menuItems[otherIndex]
        



# Each recipe now includes:

#     🍽️ Cuisine detection (multi-label: Italian, Indian, Mediterranean, etc.)
#     🧁 Course classification (main, dessert, side, drink, etc.)
#     🌶️ Taste profile (sweet, savory, sour, spicy, umami, bitter, neutral)
#     🌿 Dietary tags (vegan, vegetarian, halal, gluten-free)
#     ⏱️ Estimated preparation and cooking times (auto-derived from text actions)
#     ⚙️ Difficulty level (easy / medium / hard based on steps and ingredients)
#     ❤️ Healthiness score (computed using nutrient-related ingredients)
#     🍗 Main ingredient detection (chicken, tofu, lentils, etc.)
#     📄 Enriched textual features for NLP and recommendation systems

#  0   recipe_title           62126 non-null  str   
#  1   category               62126 non-null  str   
#  2   subcategory            62126 non-null  str   
#  3   description            62126 non-null  str   
#  4   ingredients            62126 non-null  object
#  5   directions             62126 non-null  object
#  6   num_ingredients        62126 non-null  int64 
#  7   num_steps              62126 non-null  int64 
#  8   ingredient_text        62126 non-null  str   
#  9   directions_text        62126 non-null  str   
#  10  combined_text          62126 non-null  str   
#  11  ingredients_raw        62126 non-null  object
#  12  directions_raw         62126 non-null  object
#  13  ingredients_canonical  62126 non-null  object
#  14  cuisine_list           62126 non-null  object
#  15  course_list            62126 non-null  object
#  16  tastes                 62126 non-null  object
#  17  primary_taste          62126 non-null  str   
#  18  secondary_taste        62126 non-null  str   
#  19  fast_hits              62126 non-null  int64 
#  20  slow_hits              62126 non-null  int64 
#  21  medium_hits            62126 non-null  int64 
#  22  cook_speed             62126 non-null  str   
#  23  est_prep_time_min      62126 non-null  int64 
#  24  est_cook_time_min      62126 non-null  int64 
#  25  difficulty             62126 non-null  str   
#  26  is_vegan               62126 non-null  bool  
#  27  is_vegetarian          62126 non-null  bool  
#  28  is_halal               62126 non-null  bool  
#  29  is_kosher              62126 non-null  bool  
#  30  is_nut_free            62126 non-null  bool  
#  31  is_dairy_free          62126 non-null  bool  
#  32  is_gluten_free         62126 non-null  bool  
#  33  dietary_profile        62126 non-null  object
#  34  healthiness_score      62126 non-null  int64 
#  35  health_flags           62126 non-null  object
#  36  main_ingredient        62126 non-null  str   
#  37  health_level           62126 non-null  str 
