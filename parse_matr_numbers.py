import csv
from termcolor import colored
import pandas as pd
import sys

def find_student_and_give_point(evaluation_df, matricle_number, name):
    # Iterate over evaluation file and look for matriculation number
    for index, row in evaluation_df.iterrows():
        matricle_number_to_compare = row[2].strip()
        if len(matricle_number_to_compare) != 8 or not matricle_number_to_compare.isdigit():
            continue
        if matricle_number_to_compare == matricle_number:
            text_1 = f"{colored('Match:', 'green')} \t{row[0]} {row[1]}"
            print(text_1, " " * max(55 - len(text_1), 0), f" == {name}")
            if row[5] == '-':
                row[5] = 1
            else:
                print(colored(f"Points already set to: {row[5]}", 'yellow'))
            return
    print(colored(f"No match for: {name} matr number: {matricle_number}", 'red'))


def main():
    attendance = pd.read_csv(ATTENDANCE_PATH, sep=',', converters={i: str for i in range(100)})
    evaluation = pd.read_csv(EVALUATION_PATH, sep=',', converters={i: str for i in range(100)})

    # Iterate over attendance table
    for index, row in attendance.iterrows():
        name = row[1].strip()
        matricle_number = row[2].strip()

        # Make sure matricle number is ok
        if len(matricle_number) == 7:
            matricle_number = '0' + matricle_number
        if len(matricle_number) != 8 or not matricle_number.isdigit():
            print(colored('Wrong matr number in attendance file please check:', 'red'),
                  f"Name: {name} \tMatriculation Number: {matricle_number}")
            continue

        find_student_and_give_point(evaluation, matricle_number, name)
    # Drop Rows with empty matriculation number
    evaluation = evaluation.drop(evaluation[evaluation["Matrikelnummer"] == ""].index)
    # Write back to csv file
    evaluation.to_csv('output.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    print("Done.")


if __name__ == '__main__':
    print(f"Arguments count: {len(sys.argv)}")
    assert len(sys.argv)==3
    
    ATTENDANCE_PATH = sys.argv[1]
    EVALUATION_PATH = sys.argv[2]

    main()
