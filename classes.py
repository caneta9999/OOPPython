import pandas as pd
import csv
from json import loads
from random import randint, shuffle

class Person:
    instances = []
    def __init__(self, name: str, age: int):
        self.name = name
        className = self.__class__.__name__
        self.__profession = className if className != "Person" else ""
        self.age = age
        Person.instances.append(self)
        
    #getters
    @property
    def name(self):
        return self.__name
    @property
    def age(self):
        return self.__age
    @property
    def adult(self):
        return self.__adult
    @property
    def profession(self):
        return self.__profession
    
    #setters
    @name.setter
    def name(self,value):
        if len(value) < 1:
            raise Exception("The name is too short!")
        elif len(value) > 100:
            raise Exception("The name is too long!")
        else:
            self.__name = value
    @age.setter
    def age(self, value):
        if value > 150 or value < 0:
            raise Exception("Invalid age!")
        elif self.profession and not Person.isadult(value):
            raise Exception("Must be over 18!")
        else:
            self.__age = value
            self.__adult = Person.isadult(self.__age)
    
    @staticmethod
    def isadult(age):
        return True if age >= 18 else False

    @classmethod
    def export_to_csv(cls):
        people = {'name': [], 'age': [], "profession" : [], "otherAttributes": []}
        for instance in Person.instances:
           people['name'].append(instance.name)
           people['age'].append(instance.age)
           people['profession'].append(instance.profession)
           people['otherAttributes'].append({key: value for key, value in instance.__dict__.items() if "_Person" not in key})
        pd.DataFrame(people).to_csv('.\People.csv')
    @classmethod
    def import_from_csv(cls):
        with open('People.csv', 'r') as f:
            reader = csv.DictReader(f)
            people = list(reader)
        for person in people:
            profession = person.get('profession')
            if not profession:
                Person(name=person.get('name'),age=int(person.get('age')))
            else:
                if profession == "SoccerPlayer":
                    SoccerPlayer(name=person.get('name'),age=int(person.get('age')), otherAttributes=loads(person.get('otherAttributes').replace("\'", "\"")))
                elif profession == "Author":
                    Author(name=person.get('name'),age=int(person.get('age')), otherAttributes=loads(person.get('otherAttributes').replace("\'", "\"")))
    @classmethod
    def random_person(cls):
        quantityPeople = len(Person.instances)
        return Person.instances[randint(0,quantityPeople-1)]
    @classmethod
    def print_allpeople(cls):
        for person in Person.instances:
            print(person)
        
    def __str__(self):
        string = f'My name is {self.name} and i am {self.age} years old.'
        string += f' I work as {self.profession}.' if self.profession else ""
        return string
    def __len__(self):
        return len(self.name)

class SoccerPlayer(Person):
    __positions = ["Goalkeeper", "Defence", "Midfield", "Attack"]
    def __init__(self, name: str, age: int, position = "Attack", goals = 0, otherAttributes = {}):
        super().__init__(
            name, age
        )
        if otherAttributes:
            self.goals = otherAttributes['_SoccerPlayer__goals']
            self.position = otherAttributes['_SoccerPlayer__position']
        else:
            self.goals = goals
            self.position = position
    @property
    def goals(self):
        return self.__goals
    @property
    def position(self):
        return self.__position
    
    @goals.setter
    def goals(self, value):
        if value < 0:
            raise Exception("Invalid number of goals")
        else:
            self.__goals = value
    @position.setter
    def position(self, value):
        if value not in SoccerPlayer.__positions:
            raise Exception("Invalid position!")
        else:
            self.__position = value
            
    @classmethod
    def print_positions(cls):
        print("The possible positions are: ")
        for position in SoccerPlayer.__positions:
            print(f'{position}')            

    def __str__(self):
        string = super().__str__()
        string += f' My position is {self.position}'
        string += f' and I have already scored {self.goals} goals in my career' if self.goals > 0 else ""
        return string
    def __add__(self, goals):
        self.goals += goals
        return self

class Author(Person):
    def __init__(self, name: str, age: int, writtenBooks = [], otherAttributes = {}):
        super().__init__(
            name, age
        )
        if otherAttributes:
            self.writtenBooks = otherAttributes['_Author__writtenBooks']
        else:
            self.writtenBooks = writtenBooks
    @property
    def writtenBooks(self):
        return self.__writtenBooks
    
    @writtenBooks.setter
    def writtenBooks(self, value):
        if type(value) != list:
            print("The collection of written books must be a list!")
        else:
            self.__writtenBooks = value

    @staticmethod
    def shuffle_books(books, max_books=3):
        shuffled_books = []
        n_books = 0
        if books:
            shuffled_books = books.copy()
            shuffle(shuffled_books)
            if len(books) > max_books:
                n_books = max_books
            else:
                n_books = len(books)
        return shuffled_books, n_books

    def __str__(self):
        string = super().__str__()
        books, n_books = Author.shuffle_books(self.__writtenBooks)
        string += ' Some of my books are: ' if books else ''
        for i in range(0,n_books):
            string += books[i]
            if (n_books - i) > 1:
                if (n_books - i) > 2:
                    string += ', '
                elif (n_books - i) == 2:
                    string += ' and '
        return string
    def __contains__(self, book):
        return book in self.writtenBooks