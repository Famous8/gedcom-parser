class Person:
    def __init__(self):
        self.name = None
        self.given = None
        self.surname = None
        self.sex = None
        self.birth = ()
        self.death = ()
        self.sources = []
        self.notes = []
        self.occupations = []
        self.education = []
        self.residences = []
        self.titles = []
        self.links = []
        self.id = None
        self.familyChildID = None
        self.familySpouseIDs = []
        self.familyChild = None
        self.familySpouses = []

class Family:
    def __init__(self):
        self.id = None
        self.members = []
        self.parentOne = None
        self.parentTwo = None
        self.wife = None
        self.children = []
