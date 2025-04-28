from api import mongo

class Movie():
    def __init__(self, title, desscription, year):
        self.title = title
        self.description = desscription
        self.year = year