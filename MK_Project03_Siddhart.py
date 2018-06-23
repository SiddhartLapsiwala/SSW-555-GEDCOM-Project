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
import unittest

birthdate = []
marrdate = []
divdate = []
deathdate = []
alldates = birthdate + marrdate + divdate + deathdate

todaysdate = datetime.today().strftime('%Y-%m-%d')


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
        self.birthday = 'NA'
        self.age = 'NA'
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
                    repo.individual[current_id].add_age('Birth', argument)
                    if argument < todaysdate:
                        birthdate.append(argument)
                    else:
                        repo.individual[current_id].add_birthday("Invalid Birthday")
                elif previous_tag == "DEAT":
                    repo.individual[current_id].add_death(argument)
                    repo.individual[current_id].add_alive("False")
                    repo.individual[current_id].add_age('Death', argument)
                    if argument < todaysdate:
                        deathdate.append(argument)
                    else:
                        repo.individual[current_id].add_death("Invalid Death day")
                elif previous_tag == "MARR":
                    repo.family[current_id].add_marriage(argument)
                    if argument < todaysdate:
                        marrdate.append(argument)
                    else:
                        repo.individual[current_id].add_marriage("Invalid Marriage day")
                elif previous_tag == "DIV":
                    repo.family[current_id].add_divorse(argument)
                    if argument < todaysdate:
                        divdate.append(argument)
                    else:
                        repo.individual[current_id].add_divorse("Invalid Divorce day")


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


def before_current_date(date1, date2):
    """MK Test Function"""
    firstdate = datetime.strptime(date1,'%Y-%m-%d')
    seconddate =datetime.strptime(date2,'%Y-%m-%d')
    if firstdate <= seconddate:
        return True
    else:
        return False


class DateTestCase(unittest.TestCase):
    """ MK Test for Sprint 1"""
    """US01 Dates before Current Date"""
    def test_birth_dates_before_current(self):
        individual = Individual("I01")
        individual.add_birthday("1960-07-15")
        future_date = "2500-06-23"
        self.assertTrue(individual.id == "I01")
        self.assertTrue(individual.birthday == "1960-07-15")
        self.assertTrue(before_current_date(individual.birthday, todaysdate))
        self.assertFalse(before_current_date(future_date, individual.birthday))

    def test_death_dates_before_current(self):
        """ MK Test for Sprint 1"""
        """US01 Dates before Current Date"""
        individal = Individual("I01")
        individal.add_death("2013-12-31")
        self.assertTrue(individal.death == "2013-12-31")
        self.assertTrue(before_current_date(individal.death, todaysdate))

    def test_married_dates_before_current(self):
        """ MK Test for Sprint 1"""
        """US01 Dates before Current Date"""
        family = Family("I01")
        family.add_marriage("1980-02-14")
        self.assertTrue(family.marriage == "1980-02-14")
        self.assertTrue(before_current_date(family.marriage, todaysdate))

    def test_divorce_dates_before_current(self):
        """ MK Test for Sprint 1"""
        """US01 Dates before Current Date"""
        family = Family("I01")
        family.add_divorce("1982-02-15")
        self.assertTrue(family.divorced == "1982-02-15")
        self.assertTrue(before_current_date(family.divorced, todaysdate))

    def test_all_dates(self):
        """ MK Test for Sprint 1"""
        """US01 Dates before Current Date"""
        for eadates in alldates:
            self.assertTrue(eadates < todaysdate)

    def test_birth_before_marriage(self):
        """MK Test for sprint 1"""
        """US08 Birth Before Marriage of Parents"""
        family = Family("F23")
        individual = Individual("I19")
        family.add_marriage("1980-02-14")
        individual.add_birthday("1981-02-13")
        self.assertTrue(before_current_date(family.marriage, individual.birthday))
        self.assertFalse(before_current_date(individual.birthday, family.marriage))


if __name__ == '__main__':
    main()
    unittest.main(exit=False, verbosity=2)
