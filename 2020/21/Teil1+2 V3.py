import sys
import re
import itertools
import functools
import collections

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesex='''
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
'''[1:-1].split('\n')   # split example in lines, keep line endings


# -------- parse and perform some first analysis that can be done on the fly -----------

possiblyInIngredients = dict()  # for a ingredient, which allergens could be in it
allIngredients = set()  # all ingredients that are part of food
ingredientOccurs = collections.defaultdict(int)  # how often occurs the ingredient in the food info?

for s in lines:
    # parse line
    food = s.rstrip('\n')

    ingredients, allergens = food.split(" (contains ")
    allergens = allergens[0:-1]

    ingredients = ingredients.split(" ")
    allergens = allergens.split(", ")

    # generate results
    for ingredient in ingredients:
        allIngredients.add(ingredient)
        ingredientOccurs[ingredient] = ingredientOccurs[ingredient] + 1

    for allergen in allergens:
        # if an allergen is mentioned for several food items, it can only be
        # in those ingredients, that are part of all these food items, since
        # there are no two different ingredients that have the same allergens.
        if allergen not in possiblyInIngredients:
            possiblyInIngredients[allergen] = set(ingredients)
        else:
            apif = possiblyInIngredients[allergen]
            apif = apif.intersection(set(ingredients))
            possiblyInIngredients[allergen] = apif

#print(possiblyInIngredients)


# -------- part 1 -----------

# Start with all allergens, for that we know the ingredient exactly
allergens = possiblyInIngredients.keys()
solvedAllergensToLearnFrom = [allergen for allergen in allergens
                                 if len(possiblyInIngredients[allergen]) == 1]
while len(solvedAllergensToLearnFrom) > 0:
    allergen = solvedAllergensToLearnFrom.pop()
    ingredient = next(iter(possiblyInIngredients[allergen]))  # get the only ingredient
    for otherAllergen in allergens:
        if otherAllergen != allergen and ingredient in possiblyInIngredients[otherAllergen]:
            # another allergen for that we held ingredient for possible so far
            ingredients = possiblyInIngredients[otherAllergen]
            ingredients.remove(ingredient)  # "my" ingredient cannot be responsible for the other allergen any more
            possiblyInIngredients[otherAllergen] = ingredients
            if len(ingredients) == 1:  # ingredient for the other allergen has been identified
                solvedAllergensToLearnFrom.append(otherAllergen)
print("Identified allergen for each ingredient:", possiblyInIngredients)
if len([allergen for allergen in allergens if len(possiblyInIngredients[allergen])!=1]) >0:
    raise RuntimeError("could not solve puzzle")


# create output for solution of part 1

ingredientsWithoutAllergens = allIngredients
for allergen in possiblyInIngredients:
    ingredientsWithoutAllergens = ingredientsWithoutAllergens.difference(possiblyInIngredients[allergen])
#print("ingredients without allergens", ingredientsWithoutAllergens)
occurs = 0
for ingredient in ingredientsWithoutAllergens:
    occurs += ingredientOccurs[ingredient]
print("Result of part 1:", occurs)
#1913


# ---------------------- part 2 ---------------------

allergensAndTheirIngredients = [ (allergen, next(iter(possiblyInIngredients[allergen])) ) for allergen in possiblyInIngredients]
allergensAndTheirIngredients = sorted(allergensAndTheirIngredients)
print("allergens and their ingredients, sorted by allergen:", allergensAndTheirIngredients)

res = functools.reduce ( lambda a, b: a + "," + b,
                         [ingredient for (allergen, ingredient) in allergensAndTheirIngredients] )
print("Result of part 2:", res)
#gpgrb,tjlz,gtjmd,spbxz,pfdkkzp,xcfpc,txzv,znqbr
