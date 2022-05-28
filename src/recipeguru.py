#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Melanie Menge
# date: 2022-05-24
# description: find recipes based on ingredients, allergies, intolerances or ecogolical impact

from pprint import pprint
from unittest import result
from PyInquirer import prompt

from Recipe import Recipe
from Ingredients import Ingredients

from examples import custom_style_2

recipe = Recipe()

def getMostCommonIngredients():
    return Ingredients.getMostCommonIngredients

questions = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            'Search for recipes',
            'Show favorite recipes'
        ]
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
        ]
    },
]


ingredients = [ 
    {
        'type': 'input',
        'name': 'ingredients',
        'message': 'What ingredients are you looking for?',
        'filter': lambda val: val.lower()
    },
]

def get_input_ingredients():
    return prompt(ingredients,style=custom_style_2)

def main():
    answers = prompt(questions,style=custom_style_2)
    ingredientslist = []
    searchdict = {}
    result = None
    if answers['searchtype'] == 'Search with ingredients':
        ingredients = get_input_ingredients()
        while ingredients['ingredients'] != '':
            ingredientslist.append(ingredients['ingredients'])
            ingredients = get_input_ingredients()
        if len(ingredientslist) > 0:
            searchdict['ingredients'] = ingredientslist
            result = recipe.findRecipes(searchdict)
            print(result)
                    
        

if __name__ == '__main__':
    main()