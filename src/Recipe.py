#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Melanie Menge
# date: 2022-05-25
# description: gets, saves and displays recipe

from contextlib import nullcontext
import requests
import re

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

    def createRecipeDict(self,response):
        self.response = response.json()
        self.recipes['count'] = self.response['count']
        self.recipes['next'] = self.response['_links']['next']['href']
        if self.recipes['count'] > 0:
            self.recipes['recipes'] = []
        for recipe in self.response['hits']:
            self.recipes['recipes'].append((recipe['recipe']['label'],recipe['_links']['self']['href']))
        
        return self.recipes

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
                return self.createRecipeDict(r)
    


    def getNext20Recipes(self,href):
        r = requests.get(href)
        return self.createRecipeDict(r)

    def saveRecipe(self, recipeId):
        pass

    def getRecipe(self, recipeUrl):
        r = requests.get(recipeUrl)
        response = r.json()
        recipe = {}
        makros = {}
        if r.status_code == 200:
            recipe['recipe_name'] = response['recipe']['label'] 
            recipe['source'] = response['recipe']['source'] 
            recipe['source_url'] = response['recipe']['url'] 
            recipe['ingredients'] = response['recipe']['ingredientLines'] 
            recipe['calories'] = response['recipe']['calories']
            recipe['yield'] = response['recipe']['yield']
            makros['fat'] = response['recipe']['totalNutrients']['FAT']
            makros['carbs'] = response['recipe']['totalNutrients']['CHOCDF']
            makros['sugar'] = response['recipe']['totalNutrients']['SUGAR']
            makros['protein'] = response['recipe']['totalNutrients']['PROCNT']
            recipe['makros'] = makros
            
        return recipe

    def getFavorites(self):
        pass

