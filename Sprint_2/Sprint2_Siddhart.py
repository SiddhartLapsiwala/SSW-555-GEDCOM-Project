"""
=============================================================================
 |   Assignment:  Sprint 1
 |       Author:  Siddhart Lapsiwala, Dariel Bobadilla, Tom Joseph, Michael Kim
 |       Grader:  James Rowland
 |       Course:  SW555 - Agile Methods of Software Dev.
 |   Instructor:  James Rowland
 |     Due Date:  Sunday (06/24/2018) 10pm
 |     Language:  Python
 | Ex. Packages:  N/A
 | Deficiencies:  None
 ===========================================================================
"""

import unittest
from prettytable import PrettyTable
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
                    fields = line.strip().split(" ", 2)
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

    def add_birthday(self, birthday):
        self.birthday = birthday

    def add_age(self, flag, current_tagdate):
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

    def add_alive(self, alive):
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

    def add_husband_name(self, name):
        self.husband_name = name

    def add_wife_id(self, id):
        self.wife_id.add(id)

    def add_wife_name(self, name):
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

    def add_individual(self, level, argument, tag):
        self.individual[argument] = Individual(argument)

    def add_family(self, level, argument, tag):
        self.family[argument] = Family(argument)

    def individual_table(self):
        pt = PrettyTable(
            field_names=['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])
        for key in sorted(self.individual.keys()):
            pt.add_row(self.individual[key].pt_row())
        print(pt)

    def family_table(self):
        pt = PrettyTable(
            field_names=['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])
        for key in sorted(self.family.keys()):
            pt.add_row(self.family[key].pt_row())
        print(pt)

    def read_file(self, path):
        for level, tag, argument in file_reader(path):
            # print(level, tag, argument)
            result = list()
            valid_tags = {'NAME': '1', 'SEX': '1', 'MARR': '1',
                          'BIRT': '1', 'DEAT': '1', 'FAMC': '1', 'FAMS': '1',
                          'HUSB': '1', 'WIFE': '1', 'CHIL': '1',
                          'DIV': '1', 'DATE': '2', 'HEAD': '0', 'TRLR': '0', 'NOTE': '0'}
            special_valid_tags = {'INDI': '0', 'FAM': '0'}

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
                    self.add_individual(level, tag, argument)
                    current_id = tag
                else:
                    self.add_family(level, tag, argument)
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
                    self.individual[current_id].add_name(argument)
                elif tag == "SEX":
                    self.individual[current_id].add_gender(argument)
                elif tag == "FAMC":
                    self.individual[current_id].add_child(argument)
                elif tag == "FAMS":
                    self.individual[current_id].add_spouse(argument)
                elif tag in "HUSB":
                    self.family[current_id].add_husband_id(argument)
                    self.family[current_id].add_husband_name(self.individual[argument].name)
                elif tag in "WIFE":
                    self.family[current_id].add_wife_id(argument)
                    self.family[current_id].add_wife_name(self.individual[argument].name)
                elif tag in "CHIL":
                    self.family[current_id].add_children(argument)
                elif tag in ["BIRT", "DEAT", "DIV", "MARR"]:
                    check_date_tag = True
                    previous_tag = tag
                elif tag == "DATE" and check_date_tag is True:
                    argument = datetime.strptime(argument, '%d %b %Y').strftime('%Y-%m-%d')
                    if previous_tag == "BIRT":
                        self.individual[current_id].add_birthday(argument)
                        self.individual[current_id].add_age('Birth', argument)
                    elif previous_tag == "DEAT":
                        self.individual[current_id].add_death(argument)
                        self.individual[current_id].add_alive("False")
                        self.individual[current_id].add_age('Death', argument)
                    elif previous_tag == "MARR":
                        self.family[current_id].add_marriage(argument)
                    elif previous_tag == "DIV":
                        self.family[current_id].add_divorce(argument)

            else:
                result.append(level)
                result.append(argument)
                result.append("N")
                result.append(tag)
            # print("|".join(result))

    def validate_before_current_date_individual(self):
        """US01 - Date before current date Individual and Family: Birthday, Death, Marriage and Divorced Date"""
        result = False
        today_date = datetime.today().strftime('%Y-%m-%d')
        for key, individual in self.individual.items():
            if individual.death != 'NA' or individual.death != 'NA':
                if individual.birthday > today_date:
                    print("Error: INDIVIDUAL : US01 : " + key + " : Birthday " + individual.birthday +" occurs in future")
                    result = True
                if individual.death > today_date:
                    print("Error: INDIVIDUAL : US01 : " + key + " : Death " + individual.birthday + " occurs in future")
                    result = True
        for key, family in self.family.items():
            if family.marriage != 'NA' or family.divorced != 'NA':
                if family.marriage > today_date:
                    print(
                        "Error: FAMILY : US01 : " + key + " : Marriage Date " + family.marriage + " occurs in future")
                    result = True
                if family.divorced > today_date:
                    print( "Error: FAMILY : US01 : " + key + " : Divorced Date " + family.divorced + " occurs in future")
                    result =  True
        return result

    def validate_birth_before_marriage(self):
        """US02 - TJ Birth before marriage of Individual"""
        result = False
        for key, family in self.family.items():
            if family.marriage !="NA":
                if family.marriage < self.individual[list(family.husband_id)[0]].birthday:
                    print(
                        "Error: FAMILY : US02 : " + key + " Birth " + self.individual[list(family.husband_id)[0]].birthday + " of husband should occur before marriage " + family.marriage)
                    result = True
                if family.marriage < self.individual[list(family.wife_id)[0]].birthday:
                    print(
                        "Error: FAMILY : US02 : " + key + " Birth " + self.individual[list(family.wife_id)[0]].birthday + " of wife should occur before marriage " + family.marriage)
                    result = True
        return result

    def validate_death_after_birth(self):
        """US03 - TJ Birth before Death of Individual"""
        result = False
        for key, individual in self.individual.items():
            if individual.birthday != 'NA' or individual.death!='NA':
                if individual.birthday > individual.death:
                    print("Error: Individual: US03: " + key + " Birth " + individual.birthday + "should occur before death " + individual.death)
                    result = True
        return result

    def validate_family_marriage_before_divorce(self):
        """US04	Marriage before divorce"""
        result = False
        for key, family in self.family.items():
            if family.marriage > family.divorced:
                print("Error: FAMILY : US04 : " + key + " Marriage "+family.marriage+" should occur before divorce "+family.divorced)
                result = True
        return result

    def validate_family_marriage_before_death(self):
        """US05	Marriage before death"""
        result = False
        for key, family in self.family.items():
            if family.marriage > self.individual[list(family.husband_id)[0]].death:
                print("Error: FAMILY : US05 : " +key+ " Marriage " +family.marriage + " should occur before death " + self.individual[list(family.husband_id)[0]].death + " of either spouse")
                result = True
            if family.marriage > self.individual[list(family.wife_id)[0]].death:
                print("Error: FAMILY : US05 : " +key+ " Marriage " +family.marriage + " should occur before death "+ self.individual[list(family.wife_id)[0]].death+"of either spouse")
                result = True
        return result

    def validate_family_divorce_before_death(self):
        """US06	Divorce before death"""
        result = False
        for key, family in self.family.items():
            if family.divorced > self.individual[list(family.husband_id)[0]].death:
                print("Error: FAMILY : US06 : " +key + " Divorce "+family.divorced+" should occur before death " +self.individual[list(family.husband_id)[0]].death+" of either spouse")
                result = True
            if family.divorced > self.individual[list(family.wife_id)[0]].death:
                print("Error: FAMILY : US06 : " + key + " Divorce " + family.divorced + " should occur before death " +
                      self.individual[list(family.wife_id)[0]].death + " of either spouse")
                result = True
        return result

    def validate_less_150_years_old(self):
        """US07	Less than 150 years old"""
        result = False
        for key, individual in self.individual.items():
            if individual.age >= 150:
                if individual.death == 'NA':
                    print("Error: INDIVIDUAL : US07 : " +key+ " Individual should be less than 150 years after birth date " + individual.birthday )
                    result = True
                else:
                    print("Error: INDIVIDUAL : US07 : " +key+ " Individual should be less than 150 years after birth date " + individual.birthday )
                    result = True
        return result

    def validate_childbirth_after_marriage_parents(self):
        """US08 - Birth after Marriage of Parents"""
        for key, family in self.family.items():
            listofchildren = list(family.children)
            for child in listofchildren:
                if family.marriage > self.individual[child].birthday:
                    print("Error: FAMILY : US08 : " + key + " Children " + child + " should be born after marriage of parents ")
                    result = True
                elif family.divorced != 'NA':
                    divorced = datetime.strptime(family.divorced, '%Y-%m-%d')
                    childdate = datetime.strptime(self.individual[child].birthday, '%Y-%m-%d')
                    if abs((divorced + relativedelta(month=9)) - childdate).days > 270:
                        print(
                            "Error: FAMILY : US08 : " + key + " Children " + child + " should be born with in 9 months after divorced of parents ")
                        result = True
        return result

    def convert_to_date(self, value):
        """Function to convert string to date having format as YYYY-MM-DD"""
        value = datetime.strptime(value, '%Y-%m-%d')
        return value

    def date_diff(self, date1, date2, limit, unit):
        """Function to check dates are in given range(limit)"""
        standardunit = {'days': 1, 'months': 30.4, 'year': 365.25}
        return abs((date1-date2).days/standardunit[unit]) >= limit

    def validate_parents_not_too_old(self):
        """US12 - Mother should be less than 60 years older than her children and father should be less than 80 years older than his children"""
        for key, family in self.family.items():
            listofchildren = list(family.children)
            mother = list(family.wife_id)[0]
            father = list(family.husband_id)[0]
            for child in listofchildren:
                if self.date_diff(self.convert_to_date(self.individual[mother].birthday),self.convert_to_date(self.individual[child].birthday),60,"year"):
                        print("Error: FAMILY : US12 : " + key + " : Mother " + mother + " should not be less than 60 years older than her child " + child)
                        result = True
                if self.date_diff(self.convert_to_date(self.individual[father].birthday),self.convert_to_date(self.individual[child].birthday),80,"year"):
                        print("Error: FAMILY : US12 : " +key + " : Father " + father +" should not be less than 80 years older than his child " + child)
                        result = True
        return result

    def check_all_elements_equal(self,list):
        if list[1:] == list[:-1]:
            return True

    def validate_male_last_names(self):
        """US16 - All male members of a family should have the same last name"""
        listofmalemember = dict()
        for key, family in self.family.items():
            listofchildren = list(family.children)
            father = list(family.husband_id)[0]
            listofmalemember[father] = self.individual[father].name.split("/")[1]
            for child in listofchildren:
                if self.individual[child].gender == "M":
                    listofmalemember[child] = self.individual[child].name.split("/")[1]
            if self.check_all_elements_equal(list(listofmalemember.values())):
                result = False
            else:
                print(
                    "Error: FAMILY : US16 : " + key + " All male members should have the same last name ")
                result = True
        return result


def main():
    path = 'proj03test.ged'  # input("Enter file name with extension: ")
    repo = Repository()
    repo.read_file(path)

    print("\n Individual Summary")
    repo.individual_table()

    print("\n Family Summary")
    repo.family_table()

    repo.validate_before_current_date_individual()
    repo.validate_birth_before_marriage()
    repo.validate_death_after_birth()
    repo.validate_family_marriage_before_divorce()
    repo.validate_family_marriage_before_death()
    repo.validate_family_divorce_before_death()
    repo.validate_less_150_years_old()
    repo.validate_childbirth_after_marriage_parents()
    repo.validate_parents_not_too_old()
    repo.validate_male_last_names()


class Test(unittest.TestCase):
    def test_validate_before_current_date_individual(self):
        """US01 - Date before current date Individual and Family: Birthday, Death, Marriage and Divorced Date"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertTrue(repo.validate_before_current_date_individual(), True)
        self.assertNotEqual(repo.validate_before_current_date_individual(), False)
        self.assertTrue(repo.validate_before_current_date_individual())
        self.assertIsNotNone(repo.validate_before_current_date_individual())
        self.assertIsNot(repo.validate_before_current_date_individual(), '')

    def test_validate_birth_before_marriage(self):
        """US02 - TJ Birth before marriage of Individual"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertTrue(repo.validate_birth_before_marriage(), True)
        self.assertNotEqual(repo.validate_birth_before_marriage(), False)
        self.assertTrue(repo.validate_birth_before_marriage())
        self.assertIsNotNone(repo.validate_birth_before_marriage())
        self.assertIsNot(repo.validate_birth_before_marriage(), '')

    def test_validate_death_after_birth(self):
        """US03 - TJ Birth before Death of Individual"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_death_after_birth(), True)
        self.assertNotEqual(repo.validate_death_after_birth(), False)
        self.assertTrue(repo.validate_death_after_birth())
        self.assertIsNotNone(repo.validate_death_after_birth())
        self.assertIsNot(repo.validate_death_after_birth(), '')

    def test_validate_family_marriage_before_divorce(self):
        """US04	Marriage before divorce"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_family_marriage_before_divorce(), True)
        self.assertNotEqual(repo.validate_family_marriage_before_divorce(), False)
        self.assertTrue(repo.validate_family_marriage_before_divorce())
        self.assertIsNotNone(repo.validate_family_marriage_before_divorce())
        self.assertIsNot(repo.validate_family_marriage_before_divorce(), '')

    def test_validate_family_marriage_before_death(self):
        """US05	Marriage before death"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_family_marriage_before_death(), True)
        self.assertNotEqual(repo.validate_family_marriage_before_death(), False)
        self.assertTrue(repo.validate_family_marriage_before_death())
        self.assertIsNotNone(repo.validate_family_marriage_before_death())
        self.assertIsNot(repo.validate_family_marriage_before_death(), '')

    def test_validate_family_divorce_before_death(self):
        """US06	Divorce before death"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_family_divorce_before_death(), True)
        self.assertNotEqual(repo.validate_family_divorce_before_death(), False)
        self.assertTrue(repo.validate_family_divorce_before_death())
        self.assertIsNotNone(repo.validate_family_divorce_before_death())
        self.assertIsNot(repo.validate_family_divorce_before_death(), '')

    def test_validate_less_150_years_old(self):
        """US07	Less than 150 years old"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_less_150_years_old(), True)
        self.assertNotEqual(repo.validate_less_150_years_old(), False)
        self.assertTrue(repo.validate_less_150_years_old())
        self.assertIsNotNone(repo.validate_less_150_years_old())
        self.assertIsNot(repo.validate_less_150_years_old(), '')

    def test_validate_childbirth_after_marriage_parents(self):
        """US08 Birth after marriage of parents"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_childbirth_after_marriage_parents(), True)
        self.assertNotEqual(repo.validate_childbirth_after_marriage_parents(), False)
        self.assertTrue(repo.validate_childbirth_after_marriage_parents())
        self.assertIsNotNone(repo.validate_childbirth_after_marriage_parents())
        self.assertIsNot(repo.validate_childbirth_after_marriage_parents(), '')

    def test_validate_parents_not_too_old(self):
        """US12 - Mother should be less than 60 years older than her children and father should be less than 80 years older than his children"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_parents_not_too_old(), True)
        self.assertNotEqual(repo.validate_parents_not_too_old(), False)
        self.assertTrue(repo.validate_parents_not_too_old())
        self.assertIsNotNone(repo.validate_parents_not_too_old())
        self.assertIsNot(repo.validate_parents_not_too_old(), '')

    def test_validate_male_last_names(self):
        """US16 - All male members of a family should have the same last name"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_male_last_names(), True)
        self.assertNotEqual(repo.validate_male_last_names(), False)
        self.assertTrue(repo.validate_male_last_names())
        self.assertIsNotNone(repo.validate_male_last_names())
        self.assertIsNot(repo.validate_male_last_names(), '')


if __name__ == '__main__':
    main()
    #unittest.main(exit=False, verbosity=2)
