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

    def validate_family_marriage_before_divorce(self):
        """US04	Marriage before divorce"""
        result = False
        for key, family in self.family.items():
            if family.marriage > family.divorced:
                print("Error Marriage should occur before divorce of spouses for Family having ID " + key)
                result = True
        return result

    def validate_family_marriage_before_death(self):
        """US05	Marriage before death"""
        result = False
        for key, family in self.family.items():
            if family.marriage > self.individual[list(family.husband_id)[0]].death:
                print("Error Marriage should occur before death of either spouse ID: " + list(family.husband_id)[0])
                result = True
            if family.marriage > self.individual[list(family.wife_id)[0]].death:
                print("Error Marriage should occur before death of either spouse ID: " + list(family.wife_id)[0])
                result = True
        return result

    def validate_family_divorce_before_death(self):
        """US06	Divorce before death"""
        result = False
        for key, family in self.family.items():
            if family.divorced > self.individual[list(family.husband_id)[0]].death:
                print("Error Divorce should occur before death of either spouse ID: " + list(family.husband_id)[0])
                result = True
            if family.divorced > self.individual[list(family.wife_id)[0]].death:
                print("Error Divorce should occur before death of either spouse ID: " + list(family.wife_id)[0])
                result = True
        return result

    def validate_less_150_years_old(self):
        """US07	Less than 150 years old"""
        result = False
        for key, individual in self.individual.items():
            if individual.age >= 150:
                if individual.death == 'NA':
                    print("Error Current date should be less than 150 years after birth ID: " + individual.id)
                    result = True
                else:
                    print("Error Death should be less than 150 years after birth ID: " + individual.id)
                    result = True
        return result

    def validate_before_current_date_individual(self):
        """US01 - Date before current date Individual: Birthday & Death Date"""
        today_date = datetime.today().strftime('%Y-%m-%d')
        result = False
        for key, individual in self.individual.items():
            if individual.death == 'NA':
                print("Please Check Death day for birth ID: " + individual.id)
            if individual.birthday < today_date:
                result = True
            if individual.death < today_date:
                result = True
            else:
                print("Error the date should be before the current date. Please check Birthday or Death date under Individual!")
        return result

    def validate_before_current_date_family(self):
        """US01 - Date before current date Family: Marriage & Divorce"""
        today_date = datetime.today().strftime('%Y-%m-%d')
        result = False
        for key, family in self.family.items():
            if family.marriage < today_date:
                result = True
            if family.divorced < today_date:
                result = True
            else:
                print("Error the date should be before the current date. Please check Marriage or Divorced date under family!")
        return result

    def validate_childbirth_after_marriage_parents(self):
        """US08 - Birth after Marriage of Parents"""
        result = False
        for key, family in self.family.items():
            if self.individual[list(family.children)[0]].id in family.children:
                if family.marriage < self.individual[list(family.children)[0]].birthday:
                    return True
                if (family.divorced + relativedelta(month=9)) - family.divorced > 9:
                    return False
                else:
                    print("Please check if birthday is greater than marriage date")
            else:
                print("Please check if family has children")
        return result

    def validate_death_after_birth(self):
        """US03 - TJ Birth after Death of Individual"""
        result = False
        for key, individual in self.individual.items():
            if individual.birthday < individual.death:
                print("Error Birth should occur before death of Individual having ID " + key)
                result = True
        return result

    def validate_divorce_after_marriage(self):
        """US03 - TJ Divorce after marriage of Individual"""
        result = False
        for key, family in self.family.items():
            if family.marriage > family.divorced:
                print("Error Marriage should occur before divorce of Family having ID " + key)
                result = True
        return result

    def validate_no_bigamy(self):
        """US11 - Marriage should not occur during marriage to another spouse"""
        result = False
        for key, family in self.family.items():
            if family.marriage is not "" and family.divorced < family.marriage:
                print("Error Marriage should not occur during marriage to another spouse " + key)
                result = True
        return result

    def validate_sibiling_spacing(self):
        """US13 - Birth Dates of Sibilings should be more than 8 months apart or less than 2 days apart"""
        result = False
        sibday = []
        sibmonth = []
        for key, family in self.family.items():
            children_list = list(family.children)
            if self.individual[list(family.children)[0]].id in family.children:
                for each_sibiling in children_list:
                    sib_birthday_month = datetime.today().strptime(self.individual[each_sibiling].birthday, '%Y-%m-%d').month
                    sib_birthday_day = datetime.today().strptime(self.individual[each_sibiling].birthday,  '%Y-%m-%d').day
                    sibday.append(sib_birthday_day)
                    sibmonth.append(sib_birthday_month)
                    for each_month_element in range(len(sibmonth)-1):
                        month_diff = sibmonth[each_month_element+1]-sibmonth[each_month_element]
                        if month_diff > 8:
                            result = True
                    for each_day_element in range(len(sibday)-1):
                        day_diff = sibday[each_day_element+1]-sibday[each_day_element]
                        if day_diff < 2:
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

    repo.validate_family_marriage_before_divorce()
    repo.validate_family_marriage_before_death()
    repo.validate_family_divorce_before_death()
    repo.validate_less_150_years_old()


class Test(unittest.TestCase):
    def test_individual_dates_before_current(self):
        """US01 Individual: Birthday or Death Day before current(MK)"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertTrue(repo.validate_before_current_date_individual(), True)
        self.assertNotEqual(repo.validate_before_current_date_individual(), False)
        self.assertTrue(repo.validate_before_current_date_individual())
        self.assertIsNotNone(repo.validate_before_current_date_individual())
        self.assertIsNot(repo.validate_before_current_date_individual(), '')

    def test_family_dates_before_current(self):
        """US01 Family: Divorced or Marriage before current(MK)"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertTrue(repo.validate_before_current_date_family(), True)
        self.assertNotEqual(repo.validate_before_current_date_family(), False)
        self.assertTrue(repo.validate_before_current_date_family())
        self.assertIsNotNone(repo.validate_before_current_date_family())
        self.assertIsNot(repo.validate_before_current_date_family(), '')

    def test_validate_individual_birth_before_death(self):
        """US03	Death before birth"""
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
        self.assertTrue(repo.validate_family_divorce_before_death())

        repo1 = Repository()
        repo1.add_individual('', 'I01', '')
        repo1.individual['I01'].add_death('1970-01-01')

        repo1.add_individual('', 'I02', '')
        repo1.individual['I02'].add_death('1970-01-01')

        repo1.add_family('', 'F01', '')
        repo1.family['F01'].add_husband_id('I01')
        repo1.family['F01'].add_wife_id('I01')
        repo1.family['F01'].add_divorce('1960-01-01')
        self.assertFalse(repo1.validate_family_divorce_before_death())

        repo1.family['F01'].add_divorce('1980-01-01')
        self.assertTrue(repo1.validate_family_divorce_before_death())

    def test_validate_less_150_years_old(self):
        """US07	Less than 150 years old"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertFalse(repo.validate_less_150_years_old())

        repo1 = Repository()
        repo1.add_individual('', 'I01', '')
        repo1.individual['I01'].add_birthday('1970-01-01')
        repo1.individual['I01'].add_age('', '')

        repo1.add_individual('', 'I02', '')
        repo1.individual['I02'].add_birthday('1770-01-01')
        repo1.individual['I02'].add_age('Death', '1780-01-01')
        self.assertFalse(repo1.validate_less_150_years_old())

        repo2 = Repository()
        repo2.add_individual('', 'I01', '')
        repo2.individual['I01'].add_birthday('1850-01-01')
        repo2.individual['I01'].add_age('', '')
        self.assertTrue(repo2.validate_less_150_years_old())

    def test_childbirth_after_marriage(self):
        """US08 Birth after marriage of parents"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_childbirth_after_marriage_parents(), True)
        self.assertNotEqual(repo.validate_childbirth_after_marriage_parents(), False)
        self.assertTrue(repo.validate_childbirth_after_marriage_parents())
        self.assertIsNotNone(repo.validate_childbirth_after_marriage_parents())
        self.assertIsNot(repo.validate_childbirth_after_marriage_parents(), '')

    def test_validate_no_bigamy(self):
        """US11 - Marriage should not occur during marriage to another spouse"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_no_bigamy(), True)
        self.assertNotEqual(repo.validate_no_bigamy(), False)
        self.assertTrue(repo.validate_no_bigamy())
        self.assertIsNotNone(repo.validate_no_bigamy())
        self.assertIsNot(repo.validate_no_bigamy(), '')

    def test_validate_sibling_spacing(self):
        """US13 - Birth Dates of Sibilings should be more than 8 months apart or less than 2 days apart"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_sibiling_spacing(), True)
        self.assertNotEqual(repo.validate_sibiling_spacing(), False)
        self.assertTrue(repo.validate_sibiling_spacing())
        self.assertIsNotNone(repo.validate_sibiling_spacing())
        self.assertIsNot(repo.validate_sibiling_spacing(), '')


if __name__ == '__main__':
    main()
    unittest.main(exit=False, verbosity=2)
