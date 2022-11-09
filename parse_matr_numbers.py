import csv

import pandas as pd


def find_student_and_give_point(evaluation_df, matricle_number, name):
    # Iterate over evaluation file and look for matriculation number
    for index, row in evaluation_df.iterrows():
        matricle_number_to_compare = row[2].strip()
        if len(matricle_number_to_compare) != 8 or not matricle_number_to_compare.isdigit():
            continue
        if matricle_number_to_compare == matricle_number:
            print(f"Found match for: {row[0]} should be: {name}")
            if row[5] == '-':
                row[5] = 1
            else:
                print("Points already set to: ", row[5])
            return
    print(f"No match for: {name} matr number: {matricle_number}")


def main():
    attendance = pd.read_csv(ATTENDANCE_PATH, sep=',')
    evaluation = pd.read_csv(EVALUATION_PATH, sep=',', converters={i: str for i in range(100)})

    # Iterate over attendance table
    for index, row in attendance.iterrows():
        name = row[1].strip()
        matricle_number = row[2].strip()

        # If matriculation number not ok skip and print error message
        if len(matricle_number) != 8 or not matricle_number.isdigit():
            print(
                f"Wrong matr number in attendance file please check: Name: {name} \tMatriculation Number: {matricle_number}")
            continue

        find_student_and_give_point(evaluation, matricle_number, name)
    # Drop Rows with empty matriculation number
    evaluation = evaluation.drop(evaluation[evaluation["Matrikelnummer"] == ""].index)
    # Write back to csv file
    evaluation.to_csv('output.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
    print("Done.")


if __name__ == '__main__':
    ATTENDANCE_PATH = "02_Lecture/Lecture 02 Attendance.csv"
    EVALUATION_PATH = "02_Lecture/Overcoming Obst 950636118 (W2223) Bewertungen-20221108_1833-comma_separated.csv"

    main()
