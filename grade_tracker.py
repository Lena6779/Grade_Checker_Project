import csv  # Built in python module

subjects = ["math", "science", "english", "history"] # Wanted to define "subjects" first before getting deeper into the code

# Function to read student data from already created CSV
def load_students():
    students = []
    try:
        with open("data\students.csv", "r") as file:
            reader = csv.DictReader(file)  # Reads each row as a dictionary using the header as keys
            for row in reader:
                try:
                    for subject in subjects:
                        if row[subject]:
                            row[subject] = int(row[subject])
                    students.append(row)
                except (ValueError, KeyError) as error:
                    print(f"Skipping malformed row {row}: {error}")
    except FileNotFoundError:
                    print("Error: students.csv not found.")
                    print("Please try again with the correct file path.")  # Comment to help user if file not found error
    return students

# Grade and letter function calculations below 
def get_letter_grade(average): # The plus and negative grading scale is not being used here so I have this instead
    if average is None:
        return "N/A"
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F" # All other grades just gets labeled as an "F" if not meeting above criteria

def calculate_average(grades):
    if not grades:
        return None
    return round(sum(grades) / len(grades), 1) # Rounds to 1 decimal place

def calculate_student_average(students, subjects):
    for student in students:
        grades = [student[subject] for subject in subjects if isinstance(student[subject], int)]
        avg = calculate_average(grades)
        student["average"] = avg
        student["grade"] = get_letter_grade(avg)

# Function to calculate the top 5 students 
def get_average(student):
    return student["average"]
def get_top_five_students(students):
    valid_students = [student for student in students if student["average"] is not None]
    valid_students.sort(key=get_average, reverse=True)
    return valid_students[:5]

# The following 3 functions are similar as using the report dictionary created. But each function plays a part!
def generate_report(students):  # Builds the student data
    student_summary_report = {
        "total_number_of_students": len(students)
    }

    class_averages = [student["average"] for student in students if student["average"] is not None]
    student_summary_report["average_class_score"] = round(sum(class_averages) / len(class_averages), 1) if class_averages else None

    if class_averages:
        student_summary_report["highest_average"] = max(class_averages)
        student_summary_report["lowest_average"] = min(class_averages)
    else:
        student_summary_report["highest_average"] = None
        student_summary_report["lowest_average"] = None
    
    student_summary_report["individual_reports"] = {
        student["student_name"]: {"average": student["average"], "grade": student["grade"]}
        for student in students
        }   
    counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0, "N/A": 0} # To help count how many scores fall into each grade category 
    for student in students:
        grade = student["grade"]
        counts[grade] += 1
    student_summary_report["grade_distribution"] = counts
    return student_summary_report

def write_report(report, filepath): # Saves report to a file 
    with open(filepath, "w") as file:
        file.write("=" * 40 + "\n")
        file.write("Student Report With Stats!\n")
        file.write("=" * 40 + "\n")
        file.write(f"Total Students: {report['total_number_of_students']}\n")
        file.write("=" * 40 + "\n")
        file.write("Grade Statistics\n")
        file.write("=" * 40 + "\n")
        file.write(f"Average Class Score: {report['average_class_score']}\n")
        file.write(f"Highest Average: {report['highest_average']}\n")
        file.write(f"Lowest Average: {report['lowest_average']}\n")
        file.write("=" * 40 + "\n")
        file.write("Grade Distribution:\n")
        for grade, count in report["grade_distribution"].items():
            file.write(f"  {grade}: {count}\n")
        file.write("=" * 40 + "\n")
        file.write("Individual Reports:\n")
        file.write("=" * 40 + "\n")
        for name, info in report["individual_reports"].items():
            file.write(f"  {name}: Average={info['average']}, Grade={info['grade']}\n")
        file.write("=" * 40 + "\n")    

   
def print_report(report): # Prints it to the terminal for displaying purposes
    print("=" * 40)
    print("Student Report With Stats!")
    print("=" * 40)
    print(f"Total Students: {report['total_number_of_students']}")
    print(f"Average Class Score: {report['average_class_score']}")
    print(f"Highest Average: {report['highest_average']}")
    print(f"Lowest Average: {report['lowest_average']}")
    print("=" * 40)
    print("Grade Distribution:")
    for grade, count in report["grade_distribution"].items():
        print(f"  {grade}: {count}")
    print("=" * 40)
    print("Individual Reports:")
    for name, info in report["individual_reports"].items():
        print(f"  {name}: Average={info['average']}, Grade={info['grade']}")
    print("=" * 40)

# main() PLEASE DO NOT MODIFY!
def main():
    students = load_students()
    calculate_student_average(students, subjects)
    report = generate_report(students)
    print_report(report) # Decided on this to make the terminal output look neat and organized instead of a super long dictionary
    write_report(report, "grade_report.txt")
    top_five = get_top_five_students(students)
    print("Top 5 Students are:")
    print(f"{'Name':<20}{'Average':<10}{'Grade':<6}")
    print("-" * 36)
    for student in top_five:
        print(f"{student['student_name']:<20}{student['average']:<10}{student['grade']:<6}")
    print()
    print("Summary report written to a text file called 'grade_report'!")

if __name__ == "__main__":
    main()