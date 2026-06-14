import restaurant
import loadDataSet
import Model

#restaurant1 = restaurant("Burger Place", ["Best Hamburger Ever", "Cheddar Bacon Hamburger", "Cream Cheese-Jalapeño Hamburger", "Mushroom Veggie Burger"])
#restaurant2 = restaurant("Vegan Place", ["Mushroom Veggie Burger", "Caesar Salad", "Carrot Juice", "Water"])
#restaurant3 = restaurant("Seafood Place", ["Steamed Lobster Tails", "Grilled Tuna", "Broiled Scallops"])
    
def compare_two_recipes_ingredient_similarity(rec1, rec2):
    print(Model.check_words_similarity(rec1, rec2))
    # common_ingr = ingr1.intersection(ingr2)
    # total_ingr = ingr1.union(ingr2)
    # if len(total_ingr) == 0:
    #     return 0.0
    # similarity = len(common_ingr) / len(total_ingr)
    # return similarity

def compare_two_resturants_menu_similarity(rest1, rest2):
    menu1 = set(rest1.menuItems)
    menu2 = set(rest2.menuItems)
    common_items = menu1.intersection(menu2)
    commonItemsWeight = len(common_items)
    for i in range(len(rest1.menuItems)):
        for j in range(len(rest2.menuItems)):
            commonItemsWeight += Model.check_words_similarity(rest1.menuItems[i], rest2.menuItems[j]).item()
    return commonItemsWeight

# this function will print the recipe names:
# loadDataSet.find_recipes_by_name('Scallops')

compare_two_recipes_ingredient_similarity("Best Hamburger Ever", "Cheddar Bacon Hamburger")
compare_two_recipes_ingredient_similarity("Best Hamburger Ever", "Broiled Scallops")

