#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Melanie Menge
# date: 2022-05-24
# description: find recipes based on ingredients, allergies, intolerances or ecogolical impact

import json
from pprint import pprint
from tkinter.tix import Tree
from unittest import result
from PyInquirer import prompt, Separator
import keyboard

from Recipe import Recipe
from Ingredients import Ingredients

from examples import custom_style_2

recipe = Recipe()
recipenames = []


# get recipe names for selection
def recipeoptions(reciperesult):
    recipenames.clear()
    for recipe in reciperesult['recipes']:
        recipenames.append(recipe[0])
    recipenames.append(Separator())
    recipenames.append('next 20 recipes')
    recipenames.append('back to main menu')

# get ingredients from input
def get_input_ingredients():
    return prompt(ingredients,style=custom_style_2)


# intro questions
questions = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            'Search for recipes',
            'Show favorite recipes',
            'exit'
        ],
    },
    {
        'type': 'list',
        'name': 'searchtype',
        'message': 'What kind of search would you like to do?',
        'choices': [
            'Search with ingredients',
            'Search with keywords',
            'Search with nutritients',
            'Search for recipe type'
        ],
        'when': lambda answers: answers['action'] == 'Search for recipes'
    },
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
        'message': "Are you sure you don't want to enter another ingredient?",
        'when': lambda ing: ing['ingredients'] == ''
    }
]

cont = [
    {
        'type': 'confirm',
        'name': 'continue',
        'message': 'Do you want to continue browsing recipes?'
    },
    {
        'type': 'confirm',
        'name': 'menu',
        'message': 'Do you want to return to main menu?',
        'when': lambda cont: not cont['continue']
    }

]

def main():
    # get initial searchtype from user
    exit = False
    answers = prompt(questions,style=custom_style_2)
    if answers['action'] == 'exit':
        exit = True
    while not exit:
        ingredientslist = []
        searchdict = {}
        if answers['searchtype'] == 'Search with ingredients':
            # user selected 'search with ingredients' therefore, we're going to prompt the user for the ingredients 
            ingredients = get_input_ingredients()
            while ingredients['ingredients'] > '':
                ingredientslist.append(ingredients['ingredients'])
                ingredients = get_input_ingredients()
            if len(ingredientslist) > 0 :
                # after user enters ingredients we're going to find recipes with the selected ingredients 
                searchdict['ingredients'] = ingredientslist
                recipesresult = recipe.findRecipes(searchdict)
                while(len(recipesresult) > 0) and not exit:
                    print('im here')
                    recipeoptions(recipesresult)
                    # user can now decide if he wants to get more information for a recipe which is listed or look at the next 20 recipes
                    selectedrecipe = prompt(recipes,style=custom_style_2)

                    # see next 20 recipes
                    if selectedrecipe['recipes'] == 'next 20 recipes':
                        recipesresult = recipe.getNext20Recipes(recipesresult['next'])
                    # go back to main menu
                    elif selectedrecipe['recipes'] == 'back to main menu':
                        recipesresult.clear()
                        answers = prompt(questions,style=custom_style_2)
                    else:
                        # get Url for selected recipe to get the information
                        for r in recipesresult['recipes']:
                            if r[0] == selectedrecipe['recipes']:
                                recipeUrl = r[1]
                                recipeInfo = recipe.getRecipe(recipeUrl)
                                print(json.dumps(recipeInfo, indent=4))
                                Separator()
                                action = prompt(cont,style=custom_style_2)
                                if action['continue']:
                                    pass
                                elif action['menu']:
                                    recipesresult.clear()
                                    answers = prompt(questions,style=custom_style_2)
                                else:
                                    exit = True
            else:
                answers = prompt(questions,style=custom_style_2)
                                    
        

if __name__ == '__main__':
    main()