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

    def connect(self):
        client = MongoClient("mongodb://localhost:27017")
        self.db = client.recipe_database



