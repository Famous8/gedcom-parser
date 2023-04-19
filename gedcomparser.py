from classes import Person, Family

# Creating GEDCOMParse class
class gedcomParse():
    def __init__(self, file):
        # Storing file contents
        self.fileContents = open(file, encoding="utf8").readlines()

        # Setting variables of class
        self.fullGedcom = []  # To store list of all people as objects
        self.familyList = []  # To store list of all families as objects

        self.familyIDList = []  # To store IDs of all families in GEDCOM (as string)
        self.familyStart = None  # To store which line the families begin to be defined

        person = Person()

        current_index = 0  # To store which line it is iterating over
        indi = False  # To define whether an individual has been identified yet

        while self.familyStart is None:
            line = self.fileContents[current_index]

            if line.startswith("0"):
                if "INDI" in line:
                    indi = True  # Individual has been identified
                    line_split = line.split("@")  # Separating ID from rest of text

                    if person.name != None:
                        self.fullGedcom.append(person)  # Appending person to list if person has a name stored

                    person = Person()  # Creating a new instance of a person
                    person.id = line_split[1]  # Setting Person's ID

            if line.startswith("1 FAMC"):  # Adding Person's birth family to variable
                line_split = line.split("@")
                person.familyChildID = line_split[1]

            elif line.startswith("1 FAMS"):  # Adding Person's family with Spouse to variable
                line_split = line.split("@")
                person.familySpouseIDs.append(line_split[1])

            elif line.startswith("1 NAME") and indi:  # Adding name to person, if they are an individual
                person.name = self.remExtra(line)

            elif line.startswith("2 GIVN"):  # Adding first name to person (Only on Ancestry)
                person.given = self.remExtra(line)

            elif line.startswith("2 SURN"):  # Adding surname to person (Only on Ancestry)
                person.surname = self.remExtra(line)

            elif line.startswith("1 SEX"):  # Adding Sex to Person
                sex = line.split("1 SEX ")[1]
                if sex == "M":
                    person.sex = sex

                elif sex == "F":
                    person.sex = sex

            elif line.startswith("1 BIRT"):  # Initialising birth
                birthdate = None
                birthlocation = None
                birthnotes = None

                if self.fileContents[current_index + 1].startswith("2 DATE"):  # Checking date of birth, as birth has been initialised
                    birthdate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):  # Checking location of birth, as birth has been initialised
                    birthlocation = self.remExtra(self.fileContents[current_index + 2])

                if self.fileContents[current_index + 3].startswith("2 NOTE"):  # Checking notes of birth, as birth has been initialised
                    birthnotes = self.remExtra(self.fileContents[current_index + 3])

                person.birth = (birthdate, birthlocation, birthnotes)  # Storing birth details in tuple
                current_index += len([x for x in person.birth if x is not None])  # Changing next line accordingly, checking how many lines it skipped

            elif line.startswith("1 DEAT"):  # Initialising death
                deathdate = None
                deathlocation = None
                deathnotes = None

                if self.fileContents[current_index + 1].startswith("2 DATE"):  # Checking date of death, as death has been initialised
                    deathdate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):  # Checking place of death, as death has been initialised
                    deathlocation = self.remExtra(self.fileContents[current_index + 2])

                if self.fileContents[current_index + 3].startswith("2 NOTE"):  # Checking notes of death, as death has been initialised
                    deathnotes = self.remExtra(self.fileContents[current_index + 3])

                person.death = (deathdate, deathlocation, deathnotes)  # Storing death details in tuple
                current_index += len([x for x in person.death if x is not None])  # Changing next line accordingly, checking how many lines it skipped

            elif line.startswith("3 PAGE"):  # Appending source to person's source list
                person.sources.append(self.remExtra(line))

            elif line.startswith("1 OCCU"):  # Initialising occupation
                occudate = None
                occulocation = None
                occunotes = self.remExtra(line)

                if self.fileContents[current_index + 1].startswith("2 DATE"):  # Checking for occupation date
                    occudate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):  # Checking for occupation location
                    occulocation = self.remExtra(self.fileContents[current_index + 2])

                occupation = (occunotes, occudate, occulocation)  # Storing occupation details in tuple

                person.occupations.append(occupation)  # Appending occupation to persons occupation list
                current_index += len([x for x in occupation if x is not None])  # Changing next line accordingly, checking how many lines it skipped

            elif line.startswith("1 EDUC"):  # Initialising education
                educdate = None
                educlocation = None
                educnotes = self.remExtra(line)

                if self.fileContents[current_index + 1].startswith("2 DATE"):  # Checking for education date
                    educdate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):  # Checking for education location
                    educlocation = self.remExtra(self.fileContents[current_index + 2])

                education = (educnotes, educdate, educlocation)  # Storing education details in tuple

                person.education.append(education)  # Appending education to persons education list
                current_index += len([x for x in education if x is not None])  # Changing next line accordingly, checking how many lines it skipped

            elif line.startswith("1 RESI"):  # Initialising residence
                residate = None
                resilocation = None
                resinotes = None

                if self.fileContents[current_index + 1].startswith("2 DATE"):  # Checking for residence date
                    residate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):  # Checking for residence location
                    resilocation = self.remExtra(self.fileContents[current_index + 2])

                if self.fileContents[current_index + 3].startswith("2 NOTE"):  # Checking  for residence notes
                    resinotes = self.remExtra(self.fileContents[current_index + 3])

                residence = (residate, resilocation, resinotes)  # Storing residence details in tuple

                person.residences.append(residence)  # Appending residence to persons residence list
                current_index += len([x for x in residence if x is not None])  # Changing next line accordingly, checking how many lines it skipped

            elif line.startswith("1 _WLNK"):  # Initialising Link (Ancestry Only)
                wlnktitle = None
                wlnklink = None

                if self.fileContents[current_index + 1].startswith("2 TITL"):  # Checking for link url
                    wlnktitle = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 NOTE"):  # Checking for link note
                    wlnklink = self.remExtra(self.fileContents[current_index + 2])

                wlnk = (wlnktitle, wlnklink)  # Storing link details in tuple

                person.links.append(wlnk)  # Appending residence to persons links list
                current_index += len([x for x in wlnk if x is not None])  # Changing next line accordingly, checking how many lines it skipped

            elif line.startswith("1 TITL"):  # Initialising Title
                title = self.remExtra(line)
                titledate = None
                titlelocation = None

                if self.fileContents[current_index + 1].startswith("2 DATE"):  # Checking for title date
                    titledate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):  # Checking for place
                    titlelocation = self.remExtra(self.fileContents[current_index + 2])

                titleentry = (title, titledate, titlelocation)  # Storing title details in tuple

                person.titles.append(titleentry)  # Appending title to persons title list
                current_index += len([x for x in titleentry if x is not None])  # Changing next line accordingly, checking how many lines it skipped

            elif line.startswith("2 NOTE"):  # Appending note
                person.notes.append(self.remExtra(line))

            if line.startswith("0 @F"):  # Setting where families are defined
                self.familyStart = current_index

            current_index += 1  # Going to the next line

        self.fullGedcom.append(person)  # Appending last person to list
        self.createFamilies()

    def findPersonByID(self, id):  # Returns persons object from their ID
        for person in self.fullGedcom:
            if person.id == id:
                return person

        return None

    def createFamilies(self):
        family = Family()

        for x in range(self.familyStart, len(self.fileContents)):  # Iterating from where families begin being defined to end of file
            line = self.fileContents[x]  # Defining line
            if line.startswith("0 @F"):  # Checking if new family is defined in GEDCOM
                if family.id is not None:  # Checking if current family has been defined in program
                    self.familyList.append(family)  # Appending family to family list
                    family = Family()
                    family.id = line.split("@")[1]  # Setting family ID

                family.id = line.split("@")[1]

            if line.startswith("1 HUSB"):  # Checking if Husband defined
                person = self.findPersonByID(line.split("@")[1])
                family.parentOne = person
                person.familySpouses.append(family)
                next = self.fileContents[x + 1]  # Setting next line

                if next.startswith("1 WIFE") or next.startswith("1 HUSB"):  # Checking if next line is another spouse
                    person = self.findPersonByID(next.split("@")[1])
                    family.parentTwo = person
                    person.familySpouses.append(family)  # Adding spouse to family

            elif line.startswith("1 WIFE") and family.parentOne is None:  # Checking if wife is only known spouse
                person = self.findPersonByID(line.split("@")[1])
                family.parentOne = person
                person.familySpouses.append(family)  # Adding wife as only known spouse and parent

            elif line.startswith("1 CHIL"):  # Checking if the person is a child 
                person = self.findPersonByID(line.split("@")[1])
                family.children.append(person)
                person.familyChild = family  # Adding child to family

        self.familyList.append(family)  # Appending family to family list

    def findFamily(self, id):  # Returns family object from its ID
        for family in self.familyList:
            if id == family.id:
                return family

        return None

    def remExtra(self, line):  # Removing all extra characters from line
        toRemove = ["\n", "/"]
        for char in toRemove:
            if char in line:
                line = line.replace(char, "")

        return line[7:]
