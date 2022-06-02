#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Melanie Menge
# date: 2022-05-25
# description: connection to MongoDB

from contextlib import nullcontext
from pymongo import MongoClient

class Database:
    
    STATUS = ''
    db = None

    def __init__(self):
        client = MongoClient("mongodb://localhost:27017")
        self.db = client.recipe_database

    def insert(self,recipe,url):
        favorites = self.db['favorites']
        favorite_recipe = {
            'name': recipe,
            'url': url
        }

        favorites.insert_one(favorite_recipe)

    def get_list_of_favorites(self):
        favorites = self.db['favorites']
        favoriterecipes = favorites.find()
        favoriteslist = []
        for fave in favoriterecipes:
            favoriteslist.append((fave['name'],fave['url']))
        return favoriteslist