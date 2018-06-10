"""
=============================================================================
 |   Assignment:  Project 2  (To convert from Fahrenheit to Celsius)
 |       Author:  Siddhart Lapsiwala (slapsiwa@stevens.edu)
 |       Grader:  James Rowland
 |       Course:  SW555 - Agile Methods of Software Dev.
 |   Instructor:  James Rowland
 |     Due Date:  Wednesday (06/03/2018) 10pm
 |     Language:  Python
 | Ex. Packages:  N/A
 | Deficiencies:  None
 |    Functions:  1. file_reader(path)
 ===========================================================================
"""


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


def main():
    path = 'proj02test.ged' #input("Enter file name with extension: ")
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
        else:
            result.append(level)
            result.append(argument)
            result.append("N")
            result.append(tag)
        print("|".join(result))


if __name__ == '__main__':
    main()
