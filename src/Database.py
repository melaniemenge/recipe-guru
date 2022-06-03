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
    favorites = None

    def __init__(self):
        client = MongoClient("mongodb://localhost:27017")
        self.db = client.recipe_database
        self.favorites = self.db['favorites']

    def insert(self,recipe,url):
        favorite_recipe = {
            'name': recipe,
            'url': url
        }

        self.favorites.insert_one(favorite_recipe)

    def delete(self, name):
        to_delete = {'name': name}
        self.favorites.delete_one(to_delete)

    def get_list_of_favorites(self):
        favorites = self.db['favorites']
        favoriterecipes = favorites.find()
        favoriteslist = []
        for fave in favoriterecipes:
            favoriteslist.append((fave['name'],fave['url']))
        return favoriteslist