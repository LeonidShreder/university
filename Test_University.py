class University:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.students = []
        self.professors = []
        self.courses = []
        self.departments = []
        self.library = None

    def enroll_student(self, student):
        self.students.append(student)

    def hire_professor(self, professor):
        self.professors.append(professor)

    def offer_course(self, course, professor):
        self.courses.append(course)
        course.set_professor(professor)
        professor.add_course(course)

    def set_library(self, library):
        self.library = library

    def list_books(self):
        if self.library is not None:
            print(f"{self.name} in {self.location} has access to the following books:")
            self.library.list_books()
        else:
            print(f"{self.name} in {self.location} does not have a library yet.")

    def add_department(self, department):
        self.departments.append(department)

    def assign_professor_to_department(self, professor, department):
        if department in self.departments:
            department.add_professor(professor)
        else:
            print(f"Error: {department.name} is not a valid department in {self.name}.")

    def assign_student_to_department(self, student, department):
        if department in self.departments:
            department.add_student(student)
        else:
            print(f"Error: {department.name} is not a valid department in {self.name}.")

    def assign_department(self, department):
        self.departments.append(department)
        for student in department.students:
            student.department = department
        for professor in department.professors:
            professor.department = department


class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.read_books = []

    def speak(self):
        pass

    def read_book(self, book):
        self.read_books.append(book)
        print(f"{self.name} is reading {book.title}.")

    def ask_question(self, recipient, question):
        print(f"{self.name} asks {recipient.name}: {question}")

    def answer_question(self, asker, question):
        print(f"{self.name} answers {asker.name}'s question: {question}")


class Student(Human):
    def __init__(self, name, age, student_id, specialization, required_courses, department):
        super().__init__(name, age)
        self.student_id = student_id
        self.specialization = specialization
        self.courses_enrolled = {}
        self.required_courses = required_courses
        self.department = None

    def register_for_course(self, course):
        self.courses_enrolled[course] = None
        course.enroll_student(self)

    def check_out_book(self, library, book):
        library.check_out_book(self, book)

    def return_book_to_library(self, library, book):
        if book in self.borrowed_books:
            library.add_book(book)
            self.borrowed_books.remove(book)

    def set_score(self, course, score):
        if course in self.courses_enrolled:
            self.courses_enrolled[course] = score

    def calculate_grade(self, course):
        score = self.courses_enrolled.get(course)
        if score is None:
            return "F"
        elif score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def has_honors_diploma(self):
        if not self.required_courses:
            return False

        a_count = sum(1 for course in self.courses_enrolled if self.calculate_grade(course) == "A")
        percentage_a = (a_count / len(self.required_courses)) * 100

        return percentage_a >= 75

    def retake_failed_courses(self):
        failed_courses = [course for course in self.courses_enrolled if self.calculate_grade(course) == "F"]

        for course in failed_courses:
            self.courses_enrolled.pop(course)

    def is_eligible_for_graduation(self):
        return all(course in self.courses_enrolled for course in self.required_courses)

    def graduate(self):
        if self.is_eligible_for_graduation():
            if not self.has_honors_diploma():
                print(f"{self.name} has successfully graduated in {self.specialization}.")
            else:
                print(f"{self.name} has graduated with honors in {self.specialization}.")
        else:
            print(f"{self.name} is not eligible for graduation. Retaking required courses...")
            self.retake_required_courses()

    def retake_required_courses(self):
        missing_courses = [course for course in self.required_courses if course not in self.courses_enrolled]

        for course in missing_courses:
            self.register_for_course(course)

    def ask_professor_for_recommendation(self, professor, book):
        professor.recommend_book(self, book)


class Course:
    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name
        self.students_enrolled = []
        self.recommended_literature = []

    def add_recommendation(self, book, library):
        self.recommended_literature.append(book)
        library.remove_book(book)

    def list_recommendations(self):
        if not self.recommended_literature:
            print(f"No recommended literature for {self.name}.")
        else:
            print(f"Recommended literature for {self.name}:")
            for book in self.recommended_literature:
                print(book.title)

    def enroll_student(self, student):
        self.students_enrolled.append(student)

    def set_professor(self, professor):
        self.professor = professor


class MathCourse(Course):
    def is_required_for_department(self, department):
        return department == "Mathematics"


class CSDataCourse(Course):
    def is_required_for_department(self, department):
        return department == "Computer Science and Data Science"


class Professor(Human):
    def __init__(self, name, age, employee_id, department, experience, salary):
        super().__init__(name, age)
        self.employee_id = employee_id
        self.department = department
        self.experience = experience
        self.salary = salary
        self.courses_taught = []

    def teach(self, course):
        print(f"Professor {self.name} is teaching {course.name} in the {self.department} department.")

    def get_experience(self):
        return self.experience

    def set_experience(self, years):
        self.experience = years

    def promote(self, years):
        self.experience += years
        print(f"Professor {self.name} has been promoted and now has {self.experience} years of experience.")

    def get_salary(self):
        return self.salary

    def set_salary(self, salary):
        self.salary = salary

    def recommend_book(self, student, book):
        print(f"{self.name} recommends {book.title} to {student.name}.")
        student.read_book(book)

    def teach_course(self, course):
        self.courses_taught.append(course)

    def add_course(self, course):
        self.courses_taught.append(course)
        course.set_professor(self)


class Department:
    def __init__(self, department_id, name):
        self.department_id = department_id
        self.name = name
        self.professors = []
        self.courses_offered = []
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def add_professor(self, professor):
        self.professors.append(professor)

    def add_course(self, course):
        self.courses_offered.append(course)

    def get_required_courses_for_specialization(self, specialization):
        required_courses = []
        for course in self.courses_offered:
            if course.is_required_for_department(self.name):
                required_courses.append(course)
        return required_courses


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"{book.title} has been added to {self.name}.")

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            print(f"{book.title} has been removed from {self.name}.")
        else:
            print(f"{book.title} is not in {self.name}.")

    def list_books(self):
        if not self.books:
            print(f"{self.name} has no books.")
        else:
            print(f"Books in {self.name}:")
            for book in self.books:
                print(book.title)

    def check_out_book(self, student, book):
        if book in self.books:
            self.books.remove(book)
            student.borrowed_books.append(book)
            print(f"{student.name} has checked out {book.title}.")
        else:
            print(f"{book.title} is not available in {self.name}.")

    def return_book(self, student, book):
        self.books.append(book)


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"


if __name__ == "__main__":
    # Create a University
    my_university = University("My University", "City")

    # Create Students
    student1 = Student("Alice", 20, "S001", "Computer Science", ["Math", "Programming"], 'computer_science_department')
    student2 = Student("Bob", 22, "S002", "Physics", ["Physics", "Math"], 'physics_department')
    student3 = Student("Charlie", 21, "S003", "History", ["History", "English"], 'history_department')

    # Create departments
    computer_science_department = Department(1, "Computer Science")
    physics_department = Department(2, "Physics")
    history_department = Department(3, "History")

    # Assign students to their respective departments
    my_university.assign_student_to_department(student1, computer_science_department)
    my_university.assign_student_to_department(student2, physics_department)
    my_university.assign_student_to_department(student3, history_department)

    # Create Professors
    professor1 = Professor("Dr. Smith", 45, "P001", "Computer Science", 15, 75000)
    professor2 = Professor("Dr. Johnson", 55, "P002", "Physics", 20, 90000)
    professor3 = Professor("Dr. Davis", 50, "P003", "History", 18, 80000)

    student1.ask_question(professor1, "Could you explain this concept?")
    professor1.answer_question(student1, "Certainly, here's how it works.")

    # Enroll Students and Hire Professors
    my_university.enroll_student(student1)
    my_university.enroll_student(student2)
    my_university.enroll_student(student3)

    my_university.hire_professor(professor1)
    my_university.hire_professor(professor2)
    my_university.hire_professor(professor3)

    # Offer Courses
    course1 = Course("CSCI101", "Introduction to Computer Science")
    course2 = Course("PHYS101", "Introduction to Physics")
    course3 = Course("HIST101", "Introduction to History")

    # Offer Courses (pass course and professor objects, not strings)
    my_university.offer_course(course1, professor1)
    my_university.offer_course(course2, professor2)
    my_university.offer_course(course3, professor3)

    library = Library("My Library")

    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald")
    book2 = Book("To Kill a Mockingbird", "Harper Lee")
    book3 = Book("1984", "George Orwell")

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    library.list_books()

    # Print Information
    print(f"{my_university.name} in {my_university.location} has the following students:")
    for student in my_university.students:
        print(f"Student: {student.name}, ID: {student.student_id}, Specialization: {student.specialization}")

    print(f"\n{my_university.name} in {my_university.location} has the following professors:")
    for professor in my_university.professors:
        print(f"Professor: {professor.name}, ID: {professor.employee_id}, Department: {professor.department}")

    print(f"\n{my_university.name} in {my_university.location} offers the following courses:")
    for course in my_university.courses:
        print(f"Course: {course.name}, ID: {course.course_id}")

    # Print Library Information
    my_university.list_books()
