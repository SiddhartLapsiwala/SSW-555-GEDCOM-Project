"""
=============================================================================
 |   Assignment:  Sprint 4
 |       Author:  Siddhart Lapsiwala, Dariel Bobadilla, Tom Joseph, Michael Kim
 |       Grader:  James Rowland
 |       Course:  SW555 - Agile Methods of Software Dev.
 |   Instructor:  James Rowland
 |     Due Date:  Sunday (08/05/2018) 10pm
 |     Language:  Python
 | Ex. Packages:  N/A
 | Deficiencies:  None
 ===========================================================================
"""

import unittest
from prettytable import PrettyTable
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict, Counter


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
        return [self.id, self.name, self.gender, self.birthday, self.age, self.alive, self.death, self.child,
                self.spouse]


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
        self.duplicated_individual = []
        self.duplicated_family = []

    def add_individual(self, level, argument, tag):
        if argument in self.individual.keys():
            self.duplicated_individual.append(argument)
        self.individual[argument] = Individual(argument)

    def add_family(self, level, argument, tag):
        if argument in self.family.keys():
            self.duplicated_family.append(argument)
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
                    print(
                        "Error: INDIVIDUAL : US01 : " + key + " : Birthday " + individual.birthday + " occurs in future")
                    result = True
                if individual.death > today_date:
                    print("Error: INDIVIDUAL : US01 : " + key + " : Death " + individual.birthday + " occurs in future")
                    result = True
        for key, family in self.family.items():
            if family.marriage != 'NA' or family.divorced != 'NA':
                if family.marriage > today_date:
                    print("Error: FAMILY : US01 : " + key + " : Marriage Date " + family.marriage + " occurs in future")
                    result = True
                if family.divorced > today_date:
                    print("Error: FAMILY : US01 : " + key + " : Divorced Date " + family.divorced + " occurs in future")
                    result = True
        return result

    def validate_birth_before_marriage(self):
        """US02 - TJ Birth before marriage of Individual"""
        result = False
        for key, family in self.family.items():
            if family.marriage != "NA":
                if family.marriage < self.individual[list(family.husband_id)[0]].birthday:
                    print("Error: FAMILY : US02 : " + key + " Birth " + self.individual[list(family.husband_id)[
                        0]].birthday + " of husband should occur before marriage " + family.marriage)
                    result = True
                if family.marriage < self.individual[list(family.wife_id)[0]].birthday:
                    print("Error: FAMILY : US02 : " + key + " Birth " + self.individual[list(family.wife_id)[
                        0]].birthday + " of wife should occur before marriage " + family.marriage)
                    result = True
        return result

    def validate_death_after_birth(self):
        """US03 - TJ Birth before Death of Individual"""
        result = False
        for key, individual in self.individual.items():
            if individual.birthday != 'NA' or individual.death != 'NA':
                if individual.birthday > individual.death:
                    print(
                        "Error: Individual: US03: " + key + " Birth " + individual.birthday + "should occur before death " + individual.death)
                    result = True
        return result

    def validate_family_marriage_before_divorce(self):
        """US04	Marriage before divorce"""
        result = False
        for key, family in self.family.items():
            if family.marriage < family.divorced:
                print(
                    "Error: FAMILY : US04 : " + key + " Marriage " + family.marriage + " should occur before divorce " + family.divorced)
                result = True
        return result

    def validate_family_marriage_before_death(self):
        """US05	Marriage before death"""
        result = False
        for key, family in self.family.items():
            if family.marriage > self.individual[list(family.husband_id)[0]].death:
                print("Error: FAMILY : US05 : " + key + " Marriage " + family.marriage + " should occur before death " +
                      self.individual[list(family.husband_id)[0]].death + " of either spouse")
                result = True
            if family.marriage > self.individual[list(family.wife_id)[0]].death:
                print("Error: FAMILY : US05 : " + key + " Marriage " + family.marriage + " should occur before death " +
                      self.individual[list(family.wife_id)[0]].death + "of either spouse")
                result = True
        return result

    def validate_family_divorce_before_death(self):
        """US06	Divorce before death"""
        result = False
        for key, family in self.family.items():
            if family.divorced > self.individual[list(family.husband_id)[0]].death:
                print("Error: FAMILY : US06 : " + key + " Divorce " + family.divorced + " should occur before death " +
                      self.individual[list(family.husband_id)[0]].death + " of either spouse")
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
                    print(
                        "Error: INDIVIDUAL : US07 : " + key + " Individual should be less than 150 years after birth date " + individual.birthday)
                    result = True
                else:
                    print(
                        "Error: INDIVIDUAL : US07 : " + key + " Individual should be less than 150 years after birth date " + individual.birthday)
                    result = True
        return result

    def validate_childbirth_after_marriage_parents(self):
        """US08 - Birth after Marriage of Parents"""
        result = False
        for key, family in self.family.items():
            listofchildren = list(family.children)
            for child in listofchildren:
                if family.marriage > self.individual[child].birthday:
                    print(
                        "Error: FAMILY : US08 : " + key + " Children " + child + " should be born after marriage of parents ")
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
        return abs((date1 - date2).days / standardunit[unit]) >= limit

    def check_all_elements_equal(self, list):
        if list[1:] == list[:-1]:
            return True

    def validate_childbirth_before_death_parents(self):
        """US09 - Birth before death of parents"""
        result = False
        for key, family in self.family.items():
            list_of_children = list(family.children)
            for child in list_of_children:
                if self.individual[list(family.wife_id)[0]].death < self.individual[child].birthday:
                    print("Error: FAMILY : US09 : " + key + " Child "
                          + child + " should be born before death of mother")
                    result = True
                elif self.individual[list(family.husband_id)[0]].death != 'NA':
                    father_death = datetime.strptime(self.individual[list(family.husband_id)[0]].death, '%Y-%m-%d')
                    child_date = datetime.strptime(self.individual[child].birthday, '%Y-%m-%d')
                    if ((father_death + relativedelta(months=+9)) - child_date).days < 0:
                        print("Error: FAMILY : US09 : " + key + " Child "
                              + child + " should be born before 9 months after death of father")
                        result = True
        return result

    def validate_family_marriage_after_14(self):
        """US10	Marriage after 14"""
        result = False
        for key, family in self.family.items():
            husband_birthday = datetime.strptime(self.individual[list(family.husband_id)[0]].birthday, '%Y-%m-%d')
            wife_birthday = datetime.strptime(self.individual[list(family.wife_id)[0]].birthday, '%Y-%m-%d')
            marriage = datetime.strptime(family.marriage, '%Y-%m-%d')
            if (wife_birthday + relativedelta(years=+14)) > marriage:
                print("Error: FAMILY : US10: " + key + " Marriage " + family.marriage
                      + " should occur at least 14 years after birth of wife " + list(family.wife_id)[0])
                result = True
            if (husband_birthday + relativedelta(years=+14)) > marriage:
                print("Error: FAMILY : US10: " + key + " Marriage " + family.marriage
                      + " should occur at least 14 years after birth of husband " + list(family.husband_id)[0])
                result = True
        return result

    def validate_no_bigamy(self):
        """US11 - Marriage should not occur during marriage to another spouse"""
        result = False
        husband_in_multiple_family = defaultdict(list)
        for key, family in self.family.items():
            husid = ",".join(family.husband_id)
            """I01:{F23,F24}"""
            """I02:{F36,F37}"""
            husband_in_multiple_family[husid].append(key)
        for key, value in husband_in_multiple_family.items():
            if len(value) >= 2:
                divorce_date = self.family[value[0]].divorced
                if divorce_date != 'NA':
                    for id in range(1, len(value)):
                        if divorce_date > self.family[value[id]].marriage:
                            print("Error: FAMILY: US11:", value[id],
                                  " : " + key + ": Marriage should not occur during marriage to another spouse ")
                            result = True
        return result

    def validate_parents_not_too_old(self):
        """US12 - Mother should be less than 60 years older than her children and father should be less than 80 years older than his children"""
        result = False
        for key, family in self.family.items():
            listofchildren = list(family.children)
            mother = list(family.wife_id)[0]
            father = list(family.husband_id)[0]
            for child in listofchildren:
                if self.date_diff(self.convert_to_date(self.individual[mother].birthday),
                                  self.convert_to_date(self.individual[child].birthday), 60, "year"):
                    print(
                        "Error: FAMILY : US12 : " + key + " : Mother " + mother + " should not be less than 60 years older than her child " + child)
                    result = True
                if self.date_diff(self.convert_to_date(self.individual[father].birthday),
                                  self.convert_to_date(self.individual[child].birthday), 80, "year"):
                    print(
                        "Error: FAMILY : US12 : " + key + " : Father " + father + " should not be less than 80 years older than his child " + child)
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
                    sib_birthday_month = datetime.today().strptime(self.individual[each_sibiling].birthday,
                                                                   '%Y-%m-%d').month
                    sib_birthday_day = datetime.today().strptime(self.individual[each_sibiling].birthday,
                                                                 '%Y-%m-%d').day
                    sibday.append(sib_birthday_day)
                    sibmonth.append(sib_birthday_month)
                    for each_month_element in range(len(sibmonth) - 1):
                        month_diff = sibmonth[each_month_element + 1] - sibmonth[each_month_element]
                        if month_diff > 8:
                            result = True
                        else:
                            print(
                                "Error: FAMILY : US13: Family sibiling spacing should be more than 8 months apart or less than 2 days apart",
                                key)

                    for each_day_element in range(len(sibday) - 1):
                        day_diff = sibday[each_day_element + 1] - sibday[each_day_element]
                        if day_diff < 2:
                            result = True
                        else:
                            print(
                                "Error: FAMILY : US13: Family sibiling spacing should be more than 8 months apart or less than 2 days apart",
                                key)
        return result

    def validate_multiple_births(self):
        """US14 - Multiple births <= 5"""
        result = False
        for key, family in self.family.items():
            birthday_list = list()
            list_of_children = family.children
            for child in list_of_children:
                birthday_list.append(self.individual[child].birthday)
            count_dict = dict((i, birthday_list.count(i)) for i in birthday_list)
            list_birthdays = count_dict.values()
            if max(list_birthdays) <= 5:
                result = True
            else:
                print(
                    "Error: FAMILY : US14: " + key + "Number of children born in a single birth should not be greater than 5")
        return result

    def validate_maximum_number_of_siblings(self):
        """US15 -Fewer than 15 siblings"""
        result = False
        for key, family in self.family.items():
            if len(family.children) < 15:
                print(
                    "Error: FAMILY : US15: " + key + "Total Number of children born in the family should be less than 15")
                result = True
        return result

    def validate_male_last_names(self):
        """US16 - All male members of a family should have the same last name"""
        listofmalemember = dict()
        result = False
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

    def validate_no_marriages_to_desendants(self):
        """US17 - Parents should not marry any of their descendants"""
        result = False
        for key, family in self.family.items():
            listofchildren = list(family.children)
            husband_id = list(family.husband_id)
            wife_id = list(family.wife_id)

            hubbyid = " ".join(husband_id)
            wifeyid = " ".join(wife_id)

            for wfe_id in wife_id:
                for i in listofchildren:
                    if i in wfe_id:
                        if hubbyid not in listofchildren:
                            print("Error: FAMILY: US17 : Husband:", hubbyid,
                                  "parent should not marry their descendants", i)
                            result = True
            for hsb_id in husband_id:
                for i in listofchildren:
                    if i in hsb_id:
                        if wifeyid not in listofchildren:
                            print("Error: FAMILY: US17 : Wife:", wifeyid, "parent should not marry their deccendants",
                                  i)
                            result = True
        return result

    def validate_siblings_should_not_marry(self):
        """US18 - Siblings should not marry one another"""
        result = False
        hubby_list = []
        wifey_list = []
        for key, family in self.family.items():
            sibiling_list = list(family.children)
            husband_id = list(family.husband_id)
            wife_id = list(family.wife_id)

            for wfe_id in wife_id:
                for i in sibiling_list:
                    if i in wfe_id:
                        wifey_list.append(i)

            for hsb_id in husband_id:
                for i in sibiling_list:
                    if i in hsb_id:
                        hubby_list.append(i)

            hubby_id = " ".join(list(set(hubby_list)))
            wifey_id = " ".join(list(set(wifey_list)))

            marriage_list = wifey_list + hubby_list
            if set(marriage_list) == set(sibiling_list):
                print("Error: FAMILY: US18 : Brother:", hubby_id, "sibling should not marry Sister:", wifey_id)
                result = True

        return result

    def validate_correct_gender_by_role(self):
        """US21 Husband in family should be male and wife in family should be female"""
        result = False
        for key, family in self.family.items():
            husband_gender = self.individual[list(family.husband_id)[0]].gender
            wife_gender = self.individual[list(family.wife_id)[0]].gender
            if husband_gender != 'M':
                print("Error: FAMILY : US21: " + list(family.husband_id)[
                    0] + " Husband in family " + key + " should be male")
                result = True
            if wife_gender != 'F':
                print("Error: FAMILY : US21: " + list(family.wife_id)[
                    0] + " Wife in family " + key + " should be female")
                result = True
        return result

    def validate_unique_ids(self):
        """US22 All individual IDs should be unique and all family IDs should be unique"""
        result = False
        for item in self.duplicated_individual:
            print("Error: INDIVIDUAL : US22: Non unique individual ID: " + item)
            result = True

        for item in self.duplicated_family:
            print("Error: FAMILY : US22: Non unique family ID: " + item)
            result = True

        return result

    def validate_unique_name_and_birth(self):
        """US23 No more than one individual with the same name and birth date should appear in a GEDCOM file"""
        result = False
        count = Counter([individual.name + " " + individual.birthday for individual in self.individual.values()])
        for duplicated, value in count.items():
            if value > 1:
                print("Error: INDIVIDUAL : US23: Non unique individual name and birthday: " + duplicated)
                result = True
        return result

    def validate_unique_families_by_spouses(self):
        """US24 No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file"""
        result = False
        unique_family = list()  # defaultdict(lambda: 1)
        for key, family in self.family.items():
            wife_name = self.individual[list(family.wife_id)[0]].name
            marriage_date = family.marriage
            current_tuple = (wife_name, marriage_date)
            unique_family.append(current_tuple)
        family_dic = {x: unique_family.count(x) for x in unique_family}
        for family_dic_key, family_dic_value in family_dic.items():
            if family_dic_value > 1:
                print("Error: FAMILY : US24: " + "More than one family with the same spouses by name " + family_dic_key[
                    0] + " and the same marriage date " + family_dic_key[1])
                result = True
        return result
    '''
    def validate_unique_first_names_and_birthdays(self):
        """US 25: No more than one child with same name and birthday should present in a family"""
        listofchildren = dict()
        result = True
        for key, family in self.family.items():
            listofchildren = list(family.children)
            for idx,child in enumerate(listofchildren):
                for index, child1 in enumerate(listofchildren):
                    if self.individual[child1].birthday == self.individual[child].birthday and self.individual[child1].name.split("/")[0] == self.individual[child].name.split("/")[0] and idx != index:
                        result = False
                        print("Error: FAMILY : US25: " + "More than one child with same name and birthday are present in family " +
                              family.id)
                        return result
        if result:
            print("FAMILY: US25: No families in the given file have more than one child with same name and birthday")
    '''

    def list_all_deceased(self):
        """US 29: List all deceased individuals in a GEDCOM file"""
        result = []
        for key, individual in self.individual.items():
            if individual.death != 'NA':
                print("FAMILY : US 29: Deceased idividual name - " + individual.name)
                result.append(individual)
        if len(result) > 0:
            print("FAMILY : US 29: " + str(len(result)) + " individuals are deceased in the given file")
        else:
            print("FAMILY : US 29 : No deceased individuals exist in the given file")
        return result

    def validate_list_living_married(self):
        """US 30: List all living married people in a GEDCOM File"""
        married_id = []
        cmarried_id = []
        family_id = []
        alivemarriedid = []

        result = True

        for key, individual in self.individual.items():
            if individual.spouse != "NA" and individual.death == "NA":
                married_id.append(individual.spouse)

        for s in married_id:
            cmarried_id.append(','.join(s))

        for key, family in self.family.items():
            family_id.append(family.id)

        for i in family_id:
            for c in cmarried_id:
                if c in i:
                    alivemarriedid.append(c)

        alivemarriedcouple = [var for var in alivemarriedid if var]
        nbalivemarriedcouple = ''.join(alivemarriedcouple)

        for key, family in self.family.items():
            if family.id == nbalivemarriedcouple:
                print("Living & Married: ", nbalivemarriedcouple, family.husband_name, "married to", family.wife_name)
                print("List Living Singles:", family.husband_name, ",", family.wife_name)

        return result

    def validate_list_living_single(self):
        """US 31: List all living people over 30 who have never been married in a GEDCOM file"""
        overthirty = []
        result = True
        for key, individual in self.individual.items():
            if individual.age > 30 and individual.spouse == set():
                overthirty.append(individual.name)
        print("List all Living people over 30 who have never been married: ", overthirty)
        return result

    def list_upcoming_birthday(self):
        result = False
        list_result = list()
        today_date = datetime.today().strftime('%m-%d');
        today_date_plus30 = datetime.now() + relativedelta(days=30)
        today_date_plus30 = today_date_plus30.strftime('%m-%d')
        for key, individual in self.individual.items():
            if individual.death == 'NA':
                birthday = datetime.strptime(individual.birthday, '%Y-%m-%d')
                birthday = birthday.strftime('%m-%d')
                if today_date < birthday < today_date_plus30:
                    list_result.append("Name: " + individual.name + " Birthday: " + individual.birthday)
                    result = True;
        print("List of upcoming birthday :")
        print('\n'.join(str(p) for p in list_result))
        return result

    def list_upcoming_anniversaries(self):
       result = False
       list_result = list()
       today_date = datetime.today().strftime('%m-%d');
       today_date_plus30 = datetime.now() + relativedelta(days=30)
       today_date_plus30 = today_date_plus30.strftime('%m-%d')
       for key,family  in self.family.items():
           if family.divorced == 'NA':
               marriage_date = datetime.strptime(family.marriage, '%Y-%m-%d')
               marriage_date = marriage_date.strftime('%m-%d')
               if today_date < marriage_date < today_date_plus30:
                   list_result.append("Husband ID: " + list(family.husband_id)[0] + " Husband Name: " + family.husband_name + " Wife ID: " + list(family.wife_id)[0] + " Wife Name: " + family.wife_name)
                   result = True;
       print("List of upcoming Anniversaries :")
       print('\n'.join(str(p) for p in list_result))
       return result


def main():
    path = 'proj03test.ged'  # input("Enter file name with extension: ")
    repo = Repository()
    repo.read_file(path)

    print("\n Individual Summary")
    repo.individual_table()

    print("\n Family Summary")
    repo.family_table()

    """US01"""
    repo.validate_before_current_date_individual()
    """US02"""
    repo.validate_birth_before_marriage()
    """US03"""
    repo.validate_death_after_birth()
    """US04"""
    repo.validate_family_marriage_before_divorce()
    """US05"""
    repo.validate_family_marriage_before_death()
    """US06"""
    repo.validate_family_divorce_before_death()
    """US07"""
    repo.validate_less_150_years_old()
    """US08"""
    repo.validate_childbirth_after_marriage_parents()
    """US09"""
    repo.validate_childbirth_before_death_parents()
    """US10"""
    repo.validate_family_marriage_after_14()
    """US11"""
    repo.validate_no_bigamy()
    """US12"""
    repo.validate_parents_not_too_old()
    """US13"""
    repo.validate_sibiling_spacing()
    """US14"""
    repo.validate_multiple_births()
    """US15"""
    repo.validate_maximum_number_of_siblings()
    """US16"""
    repo.validate_male_last_names()
    """US17"""
    repo.validate_no_marriages_to_desendants()
    """US18"""
    repo.validate_siblings_should_not_marry()
    """US21"""
    repo.validate_correct_gender_by_role()
    """US22"""
    repo.validate_unique_ids()
    """US23"""
    repo.validate_unique_name_and_birth()
    """US24"""
    repo.validate_unique_families_by_spouses()
    """US25"""
    # repo.validate_unique_first_names_and_birthdays()
    """US29"""
    repo.list_all_deceased()
    """US30"""
    repo.validate_list_living_married()
    """US31"""
    repo.validate_list_living_single()
    """US38"""
    repo.list_upcoming_birthday()
    """US39"""
    repo.list_upcoming_anniversaries()

class Test(unittest.TestCase):
    """US01"""

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

    """US02"""

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

    """US03"""

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

    """US04"""

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

    """US05"""

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

    """US06"""

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

    """US07"""

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

    """US08"""

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

    """US09"""

    def test_validate_childbirth_before_death_parents(self):
        """US09 Birth before death of parents"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_childbirth_before_death_parents(), True)
        self.assertNotEqual(repo.validate_childbirth_before_death_parents(), False)
        self.assertTrue(repo.validate_childbirth_before_death_parents())
        self.assertIsNotNone(repo.validate_childbirth_before_death_parents())
        self.assertIsNot(repo.validate_childbirth_before_death_parents(), '')

        repo1 = Repository()
        repo1.add_individual('', 'I01', '')
        repo1.individual['I01'].add_death('1970-01-01')

        repo1.add_individual('', 'I02', '')
        repo1.individual['I02'].add_death('1970-01-01')

        repo1.add_individual('', 'I03', '')
        repo1.individual['I03'].add_birthday('1969-01-01')

        repo1.add_family('', 'F01', '')
        repo1.family['F01'].add_husband_id('I01')
        repo1.family['F01'].add_wife_id('I01')
        repo1.family['F01'].add_divorce('1960-01-01')
        repo1.family['F01'].add_children('I03')
        self.assertFalse(repo1.validate_childbirth_before_death_parents())

        repo1.add_individual('', 'I04', '')
        repo1.individual['I04'].add_birthday('1971-01-01')
        repo1.family['F01'].add_children('I04')
        self.assertTrue(repo1.validate_childbirth_before_death_parents())

    """US10"""

    def test_validate_family_marriage_after_14(self):
        """US10 Marriage after 14"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_family_marriage_after_14(), True)
        self.assertNotEqual(repo.validate_family_marriage_after_14(), False)
        self.assertTrue(repo.validate_family_marriage_after_14())
        self.assertIsNotNone(repo.validate_family_marriage_after_14())
        self.assertIsNot(repo.validate_family_marriage_after_14(), '')

        repo1 = Repository()
        repo1.add_individual('', 'I01', '')
        repo1.individual['I01'].add_death('1970-01-01')
        repo1.individual['I01'].add_birthday('1970-01-01')

        repo1.add_individual('', 'I02', '')
        repo1.individual['I02'].add_death('1970-01-01')
        repo1.individual['I02'].add_birthday('1970-01-01')

        repo1.add_family('', 'F01', '')
        repo1.family['F01'].add_husband_id('I01')
        repo1.family['F01'].add_wife_id('I01')
        repo1.family['F01'].add_divorce('1990-01-01')
        repo1.family['F01'].add_marriage('1984-01-02')
        self.assertFalse(repo1.validate_family_marriage_after_14())

        repo1.family['F01'].add_marriage('1983-12-31')
        self.assertTrue(repo1.validate_family_marriage_after_14())

    """US11"""

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

    """US12"""

    def test_validate_parents_not_too_old(self):
        """US12 - Mother should be less than 60 years older than her children and father should be less than
         80 years older than his children"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_parents_not_too_old(), True)
        self.assertNotEqual(repo.validate_parents_not_too_old(), False)
        self.assertTrue(repo.validate_parents_not_too_old())
        self.assertIsNotNone(repo.validate_parents_not_too_old())
        self.assertIsNot(repo.validate_parents_not_too_old(), '')

    """US13"""

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

    """US14"""

    def test_validate_multiple_births(self):
        """US14 - Multiple births <= 5"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_multiple_births(), True)
        self.assertNotEqual(repo.validate_multiple_births(), False)
        self.assertTrue(repo.validate_multiple_births())
        self.assertIsNotNone(repo.validate_multiple_births())
        self.assertIsNot(repo.validate_multiple_births(), '')

    """US15"""

    def test_validate_maximum_number_of_siblings(self):
        """US15 -Fewer than 15 siblings"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_maximum_number_of_siblings(), True)
        self.assertNotEqual(repo.validate_maximum_number_of_siblings(), False)
        self.assertTrue(repo.validate_maximum_number_of_siblings())
        self.assertIsNotNone(repo.validate_maximum_number_of_siblings())
        self.assertIsNot(repo.validate_maximum_number_of_siblings(), '')

    """US16"""

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

    """US17"""

    def test_validate_no_marriages_to_descendants(self):
        """US17 - Parents should not marry any of their descendants"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_no_marriages_to_desendants(), True)
        self.assertNotEqual(repo.validate_no_marriages_to_desendants(), False)
        self.assertTrue(repo.validate_no_marriages_to_desendants())
        self.assertIsNotNone(repo.validate_no_marriages_to_desendants())
        self.assertIsNot(repo.validate_no_marriages_to_desendants(), '')

    """US18"""

    def test_validate_sibilings_should_not_marry(self):
        """US18 - Siblings should not marry one another"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_siblings_should_not_marry(), True)
        self.assertNotEqual(repo.validate_siblings_should_not_marry(), False)
        self.assertTrue(repo.validate_siblings_should_not_marry())
        self.assertIsNotNone(repo.validate_siblings_should_not_marry())
        self.assertIsNot(repo.validate_siblings_should_not_marry(), '')

    """US21"""

    def test_validate_correct_gender_by_role(self):
        """US21 - Correct gender for role"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_correct_gender_by_role(), True)
        self.assertNotEqual(repo.validate_correct_gender_by_role(), False)
        self.assertTrue(repo.validate_correct_gender_by_role())
        self.assertIsNotNone(repo.validate_correct_gender_by_role())
        self.assertIsNot(repo.validate_correct_gender_by_role(), '')

    """US22"""

    def test_validate_unique_ids(self):
        """US22 - All individual IDs should be unique and all family IDs should be unique"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_unique_ids(), True)
        self.assertNotEqual(repo.validate_unique_ids(), False)
        self.assertTrue(repo.validate_unique_ids())
        self.assertIsNotNone(repo.validate_unique_ids())
        self.assertIsNot(repo.validate_unique_ids(), '')

    """US23"""

    def test_validate_unique_name_and_birth(self):
        """US23 - No more than one individual with the same name and birth date should appear in a GEDCOM file"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_unique_name_and_birth(), True)
        self.assertNotEqual(repo.validate_unique_name_and_birth(), False)
        self.assertTrue(repo.validate_unique_name_and_birth())
        self.assertIsNotNone(repo.validate_unique_name_and_birth())
        self.assertIsNot(repo.validate_unique_name_and_birth(), '')

    """US24"""

    def test_validate_unique_families_by_spouses(self):
        """US24 - Unique families by spouses"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_unique_families_by_spouses(), True)
        self.assertNotEqual(repo.validate_unique_families_by_spouses(), False)
        self.assertTrue(repo.validate_unique_families_by_spouses())
        self.assertIsNotNone(repo.validate_unique_families_by_spouses())
        self.assertIsNot(repo.validate_unique_families_by_spouses(), '')

        """US25"""

    '''
    def test_validate_unique_first_names_and_birthdays(self):
        """US25 - No more than one child with same first name and birthday should present in a family"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_unique_first_names_and_birthdays(), True)
        self.assertNotEqual(repo.validate_unique_first_names_and_birthdays(), False)
        self.assertTrue(repo.validate_unique_first_names_and_birthdays())
        self.assertIsNotNone(repo.validate_unique_first_names_and_birthdays())
        self.assertIsNot(repo.validate_unique_first_names_and_birthdays(), '')
    '''

    def test_list_all_deceased(self):
        """US 29: List all deceased individuals in a GEDCOM file"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(len(repo.list_all_deceased()), 1)
        self.assertNotEqual(len(repo.list_all_deceased()), 10)
        self.assertTrue(len(repo.list_all_deceased()) > 0)

    def test_validate_list_living_married(self):
        """US30 - List Living Married"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_list_living_married(), True)
        self.assertNotEqual(repo.validate_list_living_married(), False)
        self.assertTrue(repo.validate_list_living_married())
        self.assertIsNotNone(repo.validate_list_living_married())
        self.assertIsNot(repo.validate_list_living_married(), '')

    def test_validate_list_living_single(self):
        """US31 - List Living Single"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.validate_list_living_single(), True)
        self.assertNotEqual(repo.validate_list_living_single(), False)
        self.assertTrue(repo.validate_list_living_single())
        self.assertIsNotNone(repo.validate_list_living_single())
        self.assertIsNot(repo.validate_list_living_single(), '')

    """US38"""
    def test_list_upcoming_birthday(self):
        """US38 - List all living people in a GEDCOM file whose birthdays occur in the next 30 days"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.list_upcoming_birthday(), True)
        self.assertNotEqual(repo.list_upcoming_birthday(), False)
        self.assertTrue(repo.list_upcoming_birthday())
        self.assertIsNotNone(repo.list_upcoming_birthday())
        self.assertIsNot(repo.list_upcoming_birthday(), '')

    """US39"""
    def test_list_upcoming_anniversaries(self):
        """US39 - List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days"""
        path = 'proj03test.ged'
        repo = Repository()
        repo.read_file(path)
        self.assertEqual(repo.list_upcoming_anniversaries(), True)
        self.assertNotEqual(repo.list_upcoming_anniversaries(), False)
        self.assertTrue(repo.list_upcoming_anniversaries())
        self.assertIsNotNone(repo.list_upcoming_anniversaries())
        self.assertIsNot(repo.list_upcoming_anniversaries(), '')


if __name__ == '__main__':
    main()
    # unittest.main(verbosity=2)