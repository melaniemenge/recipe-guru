#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Melanie Menge
# date: 2022-05-24
# description: find recipes based on ingredients, allergies, intolerances or ecogolical impact

import json
from pprint import pprint
from syslog import LOG_DAEMON
from PyInquirer import prompt, Separator

from Recipe import Recipe
from Ingredients import Ingredients

from examples import custom_style_2

recipe = Recipe()
recipenames = []
continueoptions = []
ingredientslist = []
searchdict = {}

# get recipe names for selection
def recipeoptions(list, function):
    recipenames.clear()
    if function == 'recipes':
        for recipe in list['recipes']:
            recipenames.append(recipe[0])
        recipenames.append(Separator())
        recipenames.append('next 20 recipes')
        recipenames.append('back to main menu')
    else:
        for recipe in list:
            recipenames.append(recipe)

def setcontinueoptions(function):
    continueoptions.clear()
    if function == 'ingredients':
        lst = [
            'save recipe',
            'continue browsing recipes',
            'enter new search',
            'back to main menu',
            'exit'
        ]

        continueoptions.extend(lst)
    elif function == 'favorites':
        lst = [
            'delete recipe',
            'continue browsing saved recipes',
            'back to main menu',
            'exit'
        ]
        continueoptions.extend(lst)

# get ingredients from input
def get_input_ingredients():
    return prompt(ingredients,style=custom_style_2)

def show_recipe_info(r):
    # get Url for selected recipe to get the information
    recipeUrl = r[1]
    recipeInfo = recipe.getRecipe(recipeUrl)
    # show user information of recipe
    print(json.dumps(recipeInfo, indent=4))

# intro questions
questions = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            'Search for recipes',
            'Show saved recipes',
            'exit'
        ],
    },
]
searchtypes = [
    {
        'type': 'list',
        'name': 'searchtype',
        'message': 'What kind of search would you like to do?',
        'choices': [
            'Search with ingredients',
            'Search with diets',
            'Search with nutritients',
            'Search with max calories',
            'Search for recipe type'
        ],
    },
]

diets = [
    {
        'type':'list',
        'name':'diets',
        'message':'Which kind of diet do you want to search recipes for?',
        'choices': [
            'balanced',
            'high-fiber',
            'high-protein',
            'low-carb',
            'low-fat',
            'low-sodium',
            'None - return to menu'
        ],
    }
]

# selection for recipes
recipes = [
    {
        'type':'list',
        'name':'recipes',
        'message':'Select recipe for more information',
        'choices': recipenames,
    }
]

# entry for ingredients
ingredients = [ 
    {
        'type': 'input',
        'name': 'ingredients',
        'message': 'What ingredients are you looking for?',
        'filter': lambda val: val.lower()
    },
    {
        'type': 'confirm',
        'name': 'no-ingredient',
        'message': "Do you want to enter another ingredient?",
        'default': True
    }
]

cont = [
    {
        'type':'list',
        'name':'continue',
        'message':'action:',
        'choices': continueoptions,
    },
]

favorites = [
    {
        'type': 'list',
        'name': 'favorites',
        'message': "You're saved recipes:",
        'choices': recipenames
    }
]

def show_main_menu():
    exit = False 
    answers = prompt(questions,style=custom_style_2)
    if answers['action'] == 'exit':
        exit = True
    return answers, exit

def search_for_ingredients(exit):
    newingredientssearch = False
    # user selected 'search with ingredients', therefore, we're going to prompt the user for the ingredients 
    ingredients = get_input_ingredients()
    if not ingredients['no-ingredient'] :
            if ingredients['ingredients'] > '':
                ingredientslist.append(ingredients['ingredients'])
    while ingredients['ingredients'] != '' and ingredients['no-ingredient']:
        ingredientslist.append(ingredients['ingredients'])
        ingredients = get_input_ingredients()
        # if user does not want to add more ingredients the previously entered ingredient is added to the list as well (only if it's not an empty entry)
        if not ingredients['no-ingredient'] :
            if ingredients['ingredients'] > '':
                ingredientslist.append(ingredients['ingredients'])
            break
    if len(ingredientslist) > 0 :
        # after user enters ingredients we're going to find recipes with the selected ingredients 
        searchdict['ingredients'] = ingredientslist
        recipesresult = recipe.findRecipes(searchdict)
        while(len(recipesresult) > 0) and not exit and not newingredientssearch:
            recipeoptions(recipesresult,'recipes')
            # user can now decide if he wants to get more information for a recipe which is listed or look at the next 20 recipes
            selectedrecipe = prompt(recipes,style=custom_style_2)

            # see next 20 recipes
            if selectedrecipe['recipes'] == 'next 20 recipes':
                recipesresult = recipe.getNext20Recipes(recipesresult['next'])
            # go back to main menu
            elif selectedrecipe['recipes'] == 'back to main menu':
                recipesresult.clear()
                answers,exit = show_main_menu()
            # get information for recipe
            else:
                for r in recipesresult['recipes']:
                    if r[0] == selectedrecipe['recipes']:
                        recipeUrl = r[1]
                        show_recipe_info(r)
                        Separator()
                        # ask user what they want to do next (continue browsing recipes or go back to menu or exit)
                        setcontinueoptions('ingredients')
                        action = prompt(cont,style=custom_style_2)
                        if action['continue'] == 'continue browsing recipes':
                            pass
                        elif action['continue'] == 'back to main menu':
                            recipesresult.clear()
                            answers,exit = show_main_menu()
                        elif action['continue'] == 'enter new search':
                            newingredientssearch = True
                        elif action['continue'] == 'save recipe':
                            recipe.saveRecipe(selectedrecipe['recipes'],recipeUrl)
                        else:
                            exit = True
    else:
        answers,exit = show_main_menu()

    return answers,exit

def main():
    answers,exit = show_main_menu()
    while not exit:
        newingredientssearch = False
        if answers['action'] == 'Search for recipes':
            searchtype = prompt(searchtypes,style=custom_style_2)
            if searchtype['searchtype'] == 'Search with ingredients' or newingredientssearch:
                answers,exit = search_for_ingredients(exit)
            # user wants to search recipes for a specific diet
            elif answers['searchtype'] == 'Search with diets':
                diet = prompt(diets,style=custom_style_2)
                if diet['diets'] != 'None - return to menu':
                    #TODO
                    pass


        # show saved recipes and get information about them
        elif answers['action'] == 'Show saved recipes':
            favoriterecipes = recipe.getFavorites()
            favoritesnames = []
            deleted = False
            for f in favoriterecipes:
                favoritesnames.append(f[0])
            while (len(favoriterecipes)>0) and not deleted:
                recipeoptions(favoritesnames,'favorites')
                selectedfave = prompt(favorites,style=custom_style_2)
                for f in favoriterecipes:
                    if f[0] == selectedfave['favorites']:
                        show_recipe_info(f)
                        Separator()
                        setcontinueoptions('favorites')
                        action = prompt(cont,style=custom_style_2)
                        if action['continue'] == 'continue browsing saved recipes':
                            pass
                        elif action['continue'] == 'back to main menu':
                            answers,exit = show_main_menu()
                        elif action['continue'] == 'delete recipe':
                            recipe.deleteRecipe(selectedfave['favorites'])
                            deleted = True
                        else:
                            exit = True
            print('there are no saved recipes')
            answers,exit = show_main_menu()
        else:
            exit = True
        exit = True
        

if __name__ == '__main__':
    main()