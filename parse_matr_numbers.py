import csv
import pandas as pd
import sys
import os.path

def find_student_and_give_point(evaluation_df, matricle_number, name):
    # Iterate over evaluation file and look for matriculation number
    for index, row in evaluation_df.iterrows():
        matricle_number_to_compare = row[2].strip()
        if len(matricle_number_to_compare) != 8 or not matricle_number_to_compare.isdigit():
            continue
        if matricle_number_to_compare == matricle_number:
            text_1 = f"Match: \t{row[0]} {row[1]}"
            print(text_1, " " * max(55 - len(text_1), 0), f" == {name}")
            if row[5] == '-':
                row[5] = 1
            else:
                print(f"Points already set to: {row[5]}")
            return
    print(f"No match for: {name} matr number: {matricle_number}")


if __name__ == '__main__':

    # Check inputs
    if len(sys.argv)!=3:
    	print("Please give the file paths as arguments like this: \n'python parse_matr_numbers.py [path to attendance_file] [path to evaluation_file]'")
    	sys.exit()
    
    ATTENDANCE_PATH = sys.argv[1]
    EVALUATION_PATH = sys.argv[2]
    
    if not os.path.isfile(ATTENDANCE_PATH):
    	print("No file at path: "+ ATTENDANCE_PATH)
    	sys.exit()
    	
    if not os.path.isfile(EVALUATION_PATH):
    	print("No file at path: "+ EVALUATION_PATH)
    	sys.exit()

    # Read csv tables
    attendance = pd.read_csv(ATTENDANCE_PATH, sep=',', converters={i: str for i in range(100)})
    evaluation = pd.read_csv(EVALUATION_PATH, sep=',', converters={i: str for i in range(100)})

    # Iterate over attendance table
    for index, row in attendance.iterrows():
        name = row[1].strip()
        matricle_number = row[2].strip()

        # Make sure matricle number is ok
        if len(matricle_number) == 7:
            matricle_number = '0' + matricle_number # Try to fix with initial zero
        if len(matricle_number) != 8 or not matricle_number.isdigit():
            print('Wrong matr number in attendance file please check:',
                  f"Name: {name} \tMatriculation Number: {matricle_number}")
            continue

        find_student_and_give_point(evaluation, matricle_number, name)
    # Drop Rows with empty matriculation number
    evaluation = evaluation.drop(evaluation[evaluation["Matrikelnummer"] == ""].index)
    # Write result to new csv file
    evaluation.to_csv('output.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    print("Done.")
