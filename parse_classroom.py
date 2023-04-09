import statistics


SIMPLE_CLASSROOM_PATH = "classroom_simple.txt"
COMPLEX_CLASSROOM_PATH = "classroom_complex.txt"


# SIMPLE CLASSROOM - STEP 1
def format_simple_raw(student_raw_data):
    """Take student_raw_data as string and returns it as student dictionary
    with these keys: 'name', 'country', and 'grades' as a list of ints
    """
    name, country, grade1, grade2, grade3 = \
        [line for line in student_raw_data.split('\n') if line]

    return {
        'name': name,
        'country': country,
        'grades': [int(grade1), int(grade2), int(grade3)]
    }


def parse_simple_classroom(file_path):
  """Parse classroom file that is given in `file_path` parameter.
  Returns a list of dictionaries describing the students in the classroom,
  each student is described with the dictionary (Ver 1): {
    'name': ...,
    'country': ...,
    'grades': [...]
    }
  """
  # Get file raw contents, skip first line and split to students
  with open(file_path, 'r') as fileobj:
    fileobj.readline()
    raw_students_list = fileobj.read().split('###\n')

  students_list = []
  for raw_student_data in raw_students_list:
    # For each student in the list, format and append dict to list
    student_dict = format_simple_raw(raw_student_data)
    students_list.append(student_dict)

  return students_list


# STEP 2
def student_avg(students_list, student_name):
  """Takes a students list and a str with student name, and returns
  the average of the student's grades. If student doesn't exist in
  list returns None. (Ver 1)
  """
  # Create dict with student name: grades_list to check if student exists
  students_names_grades_dict = {student['name'].lower(): student['grades']
                                for student in students_list}
  if student_name not in students_names_grades_dict:
    return None

  # Calculate avg grade of student's grades
  sum_grades = sum(students_names_grades_dict[student_name])
  return sum_grades / len(students_names_grades_dict[student_name])


# BONUS STEPS - COMPLEX CLASSROOM
def parse_complex_classroom(file_path):
  """Parse classroom file (can handle either simple or complex files)
  that is given in `file_path` parameter. Returns a dictionary
  describing the students in the classroom, which contain pairs of
  student name as key and student data as value in dictionary format.
  each student data is described with the dictionary: {
    'name': ...,
    'country': ...,
    'optional_attribute_1': ...,
    'optional_attribute_2': ...,
    'grades': [...]
    }
  """
  # Get file raw contents, skip first line and split to students
  with open(file_path, 'r') as fileobj:
    fileobj.readline()
    raw_students_list = fileobj.read().split('###\n')

  students_dict = {}
  for raw_student_data in raw_students_list:
    # For each student in the list, format and add student_data dict
    # to the students_dict
    student_dict = format_complex_raw(raw_student_data)
    students_dict[student_dict['name'].lower()] = student_dict

  return students_dict


def format_complex_raw(student_raw_data):
  """Take student_raw_data as string and returns it as student dictionary
  with the following keys: 'name', 'country', 'grades', 'notes', 'average',
  and any other optional attributes
  """
  student_raw_list = [line for line in student_raw_data.split('\n') if line]
  name = student_raw_list[0]
  country = student_raw_list[1]

  student_data = {
    'name': name,
    'country': country,
    'notes': [],
    'grades': [],
    'average': ''
  }

  for line in student_raw_list[2:]:
    # Loop every item in student_raw_list, check if there is a note,
    # Or optional attribute or a grade and add it to the student_data
    if "note=" in line:
      note_content = line.split('=')[1]
      student_data['notes'].append(note_content)
    elif "=" in line:
      opt_attribute_key, opt_attribute_value = line.split('=')
      student_data[opt_attribute_key] = opt_attribute_value
    elif line.isnumeric():
      student_data['grades'].append(int(line))

  student_data['average'] = calc_student_avg_grade(student_data['grades'])
  if not student_data['notes']:
    del student_data['notes']

  return student_data


def calc_student_avg_grade(grades_list):
  """Takes grades_list then calculate and return the average grade"""
  sum_student_grades = sum(grades_list)
  return sum_student_grades / len(grades_list)


def get_student_avg(students_dict, student_name):
  """Checks if student_name exists in students_dict, if it does, returns
  the average of the student's grades. Otherwise, returns None.
  """
  if student_name not in students_dict:
    return None
  return students_dict[student_name]['average']


def students_statistics(students_dict):
  """Calculates the average grades of the classroom, the median grade
  and sorts the students by average grade from highest to lowest.
  Returns a dictionary with all the stats.
  """
  # Get all grades of all students to calculate the statistics
  total_grades = [grade for student_data in students_dict.values()
                  for grade in student_data['grades']]
  total_average = sum(total_grades) / len(total_grades)
  median_grade = statistics.median(total_grades)
  sorted_dict = sorted(students_dict.items(), key=lambda x: x[1]['average'],
                       reverse=True)

  return {"total average": total_average,
    "median grade": median_grade,
    "sorted dict": sorted_dict
  }


def main():
  """Initiating Main function with tests"""
  student_name = input("Please write student's name: ").lower()

  # Test step 1-2
  print("Testing Simple Classroom file:")
  students_list = parse_simple_classroom(SIMPLE_CLASSROOM_PATH)
  avg = student_avg(students_list, student_name)
  if avg is None:
    print("Student doesn't exists in the classroom_simple file.\n")
  else:
    print(f"{student_name.capitalize()}'s average grade is {avg:.2f}\n")

  # Test bonus steps - with edited complex classroom file
  print("Testing Complex Classroom file:")
  students_dict = parse_complex_classroom(COMPLEX_CLASSROOM_PATH)
  avg2 = get_student_avg(students_dict, student_name)
  if avg2 is None:
    print("Student doesn't exists in the classroom_complex file.\n")
  else:
    print(f"{student_name.capitalize()}'s average grade is {avg2:.2f}\n")

  # Get the classroom stats from students dict and print the results
  stats = students_statistics(students_dict)
  print(f"Classroom Statistics (Complex Classroom File)\n"
        f"Total average: {stats['total average']:.2f}\n"
        f"Median grade: {stats['median grade']}\n\n"
        f"Students sorted by average grade from highest to lowest:")
  for i, student in enumerate(stats['sorted dict'], start=1):
    print(f"{i}. {student[1]['name']}, average grade: "
          f"{student[1]['average']:.2f}")


if __name__ == '__main__':
  main()
