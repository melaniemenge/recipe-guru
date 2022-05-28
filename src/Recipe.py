#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Melanie Menge
# date: 2022-05-25
# description: gets, saves and displays recipe

from contextlib import nullcontext
import requests
import json

class Recipe:
    """
    Recipe class which gets, saves and displays recipe information
    --------------------------------------------------------------
    methods:

    findRecipes(filters)
        finds recipes in API with the set filters
    
    saveRecipe(recipeId)
        saves specific recipe

    getRecipe(recipeId)
        returns all information for a specific recipe

    getFavorites()
        returns all saved recipes as a list

    """

    URL = 'https://api.edamam.com/api/recipes/v2?app_id=dc4783f9&app_key=65a6ebb5c315e0c402346af6c4d22fba&type=public&q='
    recipes = {}
    response = None

    def findRecipes(self, filters:dict):
        q = ''
        for k in filters:
            if k == 'ingredients':
                for ing in filters[k]: 
                    q = q + ing + ' '
        
        if q != '':
            searchurl = self.URL + q
            r = requests.get(searchurl)
            if r.status_code == 200:
                self.response = r.json()
                self.recipes['count'] = self.response['count']
                if self.recipes['count'] > 0:
                    self.recipes['names'] = []
                for recipe in self.response['hits']:
                    self.recipes['names'].append(recipe['recipe']['label'])
        
        return json.dumps(self.recipes, indent=4)

    def saveRecipe(self, recipeId):
        pass

    def getRecipe(self, recipeId):
        pass

    def getFavorites(self):
        pass

