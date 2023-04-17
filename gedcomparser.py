from person import Person

class gedcomParse():
    def __init__(self, file):
        self.fileContents = open(file).readlines()
        self.fullGedcom = []

        person = Person()
        current_index = 0

        while current_index < len(self.fileContents):
            line = self.fileContents[current_index]
            if line.startswith("0"):
                if "INDI" in line:
                    line_split = line.split("@")
                    self.fullGedcom.append(person)
                    person = Person()
                    person.id = line_split[1]

            if line.startswith("1 FAMC"):
                line_split = line.split("@")
                person.familyChild.append(line_split[1])

            elif line.startswith("1 FAMS"):
                line_split = line.split("@")
                person.familySpouse.append(line_split[1])

            elif line.startswith("1 NAME"):
                person.name = self.remExtra(line)

            elif line.startswith("2 GIVN"):
                person.given = self.remExtra(line)

            elif line.startswith("2 SURN"):
                person.surname = self.remExtra(line)

            elif line.startswith("1 SEX"):
                sex = line.split("1 SEX ")[1]
                if sex == "M":
                    person.sex = sex

                elif sex == "F":
                    person.sex = sex

            elif line.startswith("1 BIRT"):
                birthdate = None
                birthlocation = None
                birthnotes = None

                if self.fileContents[current_index + 1].startswith("2 DATE"):
                    birthdate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):
                    birthlocation = self.remExtra(self.fileContents[current_index + 2])

                if self.fileContents[current_index + 3].startswith("2 NOTE"):
                    birthnotes = self.remExtra(self.fileContents[current_index + 3])

                person.birth = (birthdate, birthlocation, birthnotes)
                current_index += len([x for x in person.birth if x is not None])

            elif line.startswith("1 DEAT"):
                deathdate = None
                deathlocation = None
                deathnotes = None

                if self.fileContents[current_index + 1].startswith("2 DATE"):
                    deathdate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):
                    deathlocation = self.remExtra(self.fileContents[current_index + 2])

                if self.fileContents[current_index + 3].startswith("2 NOTE"):
                    deathnotes = self.remExtra(self.fileContents[current_index + 3])

                person.death = (deathdate, deathlocation, deathnotes)
                current_index += len([x for x in person.death if x is not None])

            elif line.startswith("3 PAGE"):
                person.sources.append(self.remExtra(line))

            elif line.startswith("1 OCCU"):
                occudate = None
                occulocation = None
                occunotes = self.remExtra(line)

                if self.fileContents[current_index + 1].startswith("2 DATE"):
                    occudate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):
                    occulocation = self.remExtra(self.fileContents[current_index + 2])

                occupation = (occunotes, occudate, occulocation)

                person.occupations.append(occupation)
                current_index += len([x for x in occupation if x is not None])

            elif line.startswith("1 EDUC"):
                educdate = None
                educlocation = None
                educnotes = self.remExtra(line)

                if self.fileContents[current_index + 1].startswith("2 DATE"):
                    educdate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):
                    educlocation = self.remExtra(self.fileContents[current_index + 2])

                education = (educnotes, educdate, educlocation)

                person.education.append(education)
                current_index += len([x for x in education if x is not None])

            elif line.startswith("1 RESI"):
                residate = None
                resilocation = None
                resinotes = None

                if self.fileContents[current_index + 1].startswith("2 DATE"):
                    residate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):
                    resilocation = self.remExtra(self.fileContents[current_index + 2])

                if self.fileContents[current_index + 3].startswith("2 NOTE"):
                    resinotes = self.remExtra(self.fileContents[current_index + 3])

                residence = (residate, resilocation, resinotes)

                person.residences.append(residence)
                current_index += len([x for x in residence if x is not None])

            elif line.startswith("1 _WLNK"):
                wlnktitle = None
                wlnklink = None

                if self.fileContents[current_index + 1].startswith("2 TITL"):
                    wlnktitle = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 NOTE"):
                    wlnklink = self.remExtra(self.fileContents[current_index + 2])

                wlnk = (wlnktitle, wlnklink)

                person.links.append(wlnk)
                current_index += len([x for x in wlnk if x is not None])

            elif line.startswith("1 TITL"):
                title = self.remExtra(line)
                titledate = None
                titlelocation = None

                if self.fileContents[current_index + 1].startswith("2 DATE"):
                    titledate = self.remExtra(self.fileContents[current_index + 1])

                if self.fileContents[current_index + 2].startswith("2 PLAC"):
                    titlelocation = self.remExtra(self.fileContents[current_index + 2])

                titleentry = (title, titledate, titlelocation)

                person.residences.append(titleentry)
                current_index += len([x for x in titleentry if x is not None])

            elif line.startswith("2 NOTE"):
                person.notes.append(self.remExtra(line))

            current_index += 1

    def remExtra(self, line):
        toRemove = ["\n", "/"]
        for char in toRemove:
            if char in line:
                line = line.replace(char, "")

        return line[7:]
