"""
=============================================================================
 |   Assignment:  Project 3
 |       Author:  Siddhart Lapsiwala (slapsiwa@stevens.edu)
 |       Grader:  James Rowland
 |       Course:  SW555 - Agile Methods of Software Dev.
 |   Instructor:  James Rowland
 |     Due Date:  Wednesday (06/10/2018) 10pm
 |     Language:  Python
 | Ex. Packages:  N/A
 | Deficiencies:  None
 |    Functions:  1. file_reader(path)
 ===========================================================================
"""

from prettytable import PrettyTable
from datetime import datetime


def file_reader(path):
    """Read the contains of file"""
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("File not found : ", path)
    except IOError:
        raise IOError("Error opening file : ", path)
    else:
        with fp:
            for line_num, line in enumerate(fp):
                fields = line.strip().split()
                if len(fields) >= 3:
                    fields = line.strip().split(" ",2)
                elif len(fields) < 1:
                    raise ValueError("Excepted number of fields is not present in row.")
                else:
                    fields = line.strip().split()
                    fields.append("")
                yield fields


class Individual:
    """Single Individual"""
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.gender = ''
        self.birthday = ''
        self.age = ''
        self.alive = 'TRUE'
        self.death = 'NA'
        self.child = set()
        self.spouse = set()

    def add_name(self, name):
        self.name = name

    def add_gender(self, gender):
        self.gender = gender

    def add_birthday(self,birthday):
        self.birthday = birthday

    def add_age(self,flag,current_tagdate):
        if flag == 'Death':
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
            end_date = datetime.strptime(current_tagdate, '%Y-%m-%d')
        else:
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
            end_date = datetime.today()
        age = end_date.year - birthday.year - ((end_date.month, end_date.day) < (birthday.month, birthday.day))
        self.age = age

    def add_death(self, death):
        self.death = death

    def add_alive(self,alive):
        self.alive = alive

    def add_child(self, id):
        self.child.add(id)

    def add_spouse(self, id):
        self.spouse.add(id)

    def pt_row(self):
        if len(self.child) == 0:
            self.child = "NA"
        if len(self.spouse) == 0:
            self.spouse = "NA"
        return [self.id, self.name, self.gender, self.birthday, self.age, self.alive, self.death, self.child, self.spouse]


class Family:
    """Single Family"""
    def __init__(self, id):
        self.id = id
        self.marriage = 'NA'
        self.divorced = 'NA'
        self.husband_id = set()
        self.husband_name = 'NA'
        self.wife_id = set()
        self.wife_name = 'NA'
        self.children = set()

    def add_marriage(self, marriage):
        self.marriage = marriage

    def add_divorce(self, divorced):
        self.divorced = divorced

    def add_husband_id(self, id):
        self.husband_id.add(id)

    def add_husband_name(self,name):
        self.husband_name = name

    def add_wife_id(self, id):
        self.wife_id.add(id)

    def add_wife_name(self,name):
        self.wife_name = name

    def add_children(self, id):
        self.children.add(id)

    def pt_row(self):
        if len(self.children) == 0:
            self.children = 'NA'
        return [self.id, self.marriage, self.divorced, self.husband_id, self.husband_name, self.wife_id,
               self.wife_name, self.children]


class Repository:

    def __init__(self):
        """All information about Individual and Family"""
        self.individual = dict()
        self.family = dict()

    def add_individual(self,level,argument,tag):
        self.individual[argument] = Individual(argument)

    def add_family(self,level,argument,tag):
        self.family[argument] = Family(argument)

    def individual_table(self):
        pt = PrettyTable(
            field_names=['ID', 'Name', 'Gender', 'Birthday', 'Age','Alive','Death','Child','Spouse'])
        for key in sorted(self.individual.keys()):
            pt.add_row(self.individual[key].pt_row())
        print(pt)

    def family_table(self):
        pt = PrettyTable(
            field_names=['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID','Wife Name','Children'])
        for key in sorted(self.family.keys()):
            pt.add_row(self.family[key].pt_row())
        print(pt)


def main():
    path = 'proj03test.ged' #input("Enter file name with extension: ")
    repo = Repository()
    for level, tag, argument in file_reader(path):
        print(level, tag, argument)
        result = list()
        valid_tags = {'NAME': '1', 'SEX': '1','MARR': '1',
                      'BIRT': '1', 'DEAT': '1', 'FAMC': '1', 'FAMS': '1',
                      'HUSB': '1', 'WIFE': '1', 'CHIL': '1',
                      'DIV': '1', 'DATE': '2', 'HEAD': '0', 'TRLR': '0', 'NOTE': '0'}
        special_valid_tags = {'INDI': '0','FAM': '0'}

        valid_tag_level = False
        if argument in ['INDI', 'FAM']:
            special_tags = True
            for current_tag, current_level in special_valid_tags.items():
                if level == current_level and argument == current_tag:
                    valid_tag_level = True
                    break
        else:
            special_tags = False
            for current_tag, current_level in valid_tags.items():
                if level == current_level and tag == current_tag:
                    valid_tag_level = True
                    break

        if valid_tag_level and special_tags:
            result.append(level)
            result.append(argument)
            result.append("Y")
            result.append(tag)
            if argument in ["INDI"]:
                repo.add_individual(level,tag,argument)
                current_id = tag
            else:
                repo.add_family(level,tag,argument)
                current_id = tag
        elif not valid_tag_level and not special_tags:
            result.append(level)
            result.append(tag)
            result.append("N")
            result.append(argument)
        elif valid_tag_level and not special_tags:
            result.append(level)
            result.append(tag)
            result.append("Y")
            result.append(argument)
            if tag == "NAME":
                repo.individual[current_id].add_name(argument)
            elif tag == "SEX":
                repo.individual[current_id].add_gender(argument)
            elif tag == "FAMC":
                repo.individual[current_id].add_child(argument)
            elif tag == "FAMS":
                repo.individual[current_id].add_spouse(argument)
            elif tag in "HUSB":
                repo.family[current_id].add_husband_id(argument)
                repo.family[current_id].add_husband_name(repo.individual[argument].name)
            elif tag in "WIFE":
                repo.family[current_id].add_wife_id(argument)
                repo.family[current_id].add_wife_name(repo.individual[argument].name)
            elif tag in "CHIL":
                repo.family[current_id].add_children(argument)
            elif tag in ["BIRT", "DEAT", "DIV", "MARR"]:
                check_date_tag = True
                previous_tag = tag
            elif tag == "DATE" and check_date_tag == True:
                argument = datetime.strptime(argument, '%d %b %Y').strftime('%Y-%m-%d')
                if previous_tag == "BIRT":
                    repo.individual[current_id].add_birthday(argument)
                    repo.individual[current_id].add_age('Birth',argument)
                elif previous_tag == "DEAT":
                    repo.individual[current_id].add_death(argument)
                    repo.individual[current_id].add_alive("False")
                    repo.individual[current_id].add_age('Death',argument)
                elif previous_tag == "MARR":
                    repo.family[current_id].add_marriage(argument)
                elif previous_tag == "DIV":
                    repo.family[current_id].add_divorse(argument)

        else:
            result.append(level)
            result.append(argument)
            result.append("N")
            result.append(tag)
        print("|".join(result))

    print("\n Individual Summary")
    repo.individual_table()

    print("\n Family Summary")
    repo.family_table()


if __name__ == '__main__':
    main()
