from datetime import datetime

class dateValidityUtility:

    def is_date1_greater_than_date2 (self, date1, date2):
        first_date = datetime.strptime(date1, '%d %b %Y')
        second_date = datetime.strptime(date2, '%d %b %Y')
        return first_date > second_date

    def is_birthdate_greater_than_death_date (self, birth_date, death_date):
        return is_date1_greater_than_date2(date1=birth_date, date2=death_date)

    def is_marriage_date_greater_than_divorce_date (self, marriage_date, divorce_date):
        return is_date1_greater_than_date2(date1=marriage_date, date2=divorce_date)



