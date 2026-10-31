import json
import os
from abc import ABC, abstractmethod


# ==========================================================
# USER CLASSES
# ==========================================================

class User(ABC):
    """
    Abstract base class for all users of the system.
    """

    def __init__(self, user_id, name, username, password):
        self.__user_id = user_id
        self.__name = name
        self.__username = username
        self.__password = password

    # Encapsulation using properties
    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self.__name

    @property
    def username(self):
        return self.__username

    def check_password(self, password):
        return self.__password == password

    @abstractmethod
    def dashboard(self):
        pass


# ==========================================================
# STUDENT CLASS - INHERITANCE
# ==========================================================

class Student(User):

    def __init__(self, user_id, name, username, password, student_id):
        super().__init__(user_id, name, username, password)
        self.student_id = student_id

    def dashboard(self):
        print(f"\nWelcome, Student {self.name}!")
        print("You can take examinations and view your results.")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "username": self.username,
            "student_id": self.student_id
        }


# ==========================================================
# TEACHER CLASS - INHERITANCE
# ==========================================================

class Teacher(User):

    def __init__(self, user_id, name, username, password, teacher_id):
        super().__init__(user_id, name, username, password)
        self.teacher_id = teacher_id

    def dashboard(self):
        print(f"\nWelcome, Teacher {self.name}!")
        print("You can create examinations and view student results.")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "username": self.username,
            "teacher_id": self.teacher_id
        }


# ==========================================================
# QUESTION CLASS
# ==========================================================

class Question:

    def __init__(self, question_id, text, options, correct_answer, marks):
        self.question_id = question_id
        self.text = text
        self.options = options
        self.correct_answer = correct_answer.upper()
        self.marks = marks

    def display(self):
        print(f"\n{self.question_id}. {self.text}")

        for key, value in self.options.items():
            print(f"   {key}. {value}")

    def check_answer(self, answer):
        return answer.upper() == self.correct_answer

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "text": self.text,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "marks": self.marks
        }


# ==========================================================
# EXAM CLASS
# ==========================================================

class Exam:

    def __init__(self, exam_id, title, subject, duration):
        self.exam_id = exam_id
        self.title = title
        self.subject = subject
        self.duration = duration

        # List data structure
        self.questions = []

        # Set prevents a student from taking the same exam twice
        self.completed_students = set()

    def add_question(self, question):
        self.questions.append(question)

    def total_marks(self):
        return sum(question.marks for question in self.questions)

    def is_completed_by(self, student_id):
        return student_id in self.completed_students

    def mark_completed(self, student_id):
        self.completed_students.add(student_id)

    def display_exam(self):
        print("\n" + "=" * 60)
        print(f"EXAM: {self.title}")
        print(f"Subject: {self.subject}")
        print(f"Duration: {self.duration} minutes")
        print(f"Total Questions: {len(self.questions)}")
        print(f"Total Marks: {self.total_marks()}")
        print("=" * 60)

    def to_dict(self):
        return {
            "exam_id": self.exam_id,
            "title": self.title,
            "subject": self.subject,
            "duration": self.duration,
            "questions": [q.to_dict() for q in self.questions],
            "completed_students": list(self.completed_students)
        }


# ==========================================================
# RESULT CLASS
# ==========================================================

class Result:

    def __init__(self, student_id, student_name, exam_id,
                 exam_title, score, total_marks):
        self.student_id = student_id
        self.student_name = student_name
        self.exam_id = exam_id
        self.exam_title = exam_title
        self.score = score
        self.total_marks = total_marks

        self.percentage = self.calculate_percentage()
        self.grade = self.calculate_grade()
        self.status = self.calculate_status()

    def calculate_percentage(self):
        if self.total_marks == 0:
            return 0

        return (self.score / self.total_marks) * 100

    def calculate_grade(self):
        percentage = self.percentage

        if percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        else:
            return "F"

    def calculate_status(self):
        return "PASS" if self.percentage >= 50 else "FAIL"

    def display(self):
        print("\n" + "=" * 50)
        print("EXAMINATION RESULT")
        print("=" * 50)
        print(f"Student ID : {self.student_id}")
        print(f"Student    : {self.student_name}")
        print(f"Exam       : {self.exam_title}")
        print(f"Score      : {self.score}/{self.total_marks}")
        print(f"Percentage : {self.percentage:.2f}%")
        print(f"Grade      : {self.grade}")
        print(f"Status     : {self.status}")
        print("=" * 50)

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "student_name": self.student_name,
            "exam_id": self.exam_id,
            "exam_title": self.exam_title,
            "score": self.score,
            "total_marks": self.total_marks,
            "percentage": round(self.percentage, 2),
            "grade": self.grade,
            "status": self.status
        }


# ==========================================================
# DIGITAL EXAM MANAGEMENT SYSTEM
# ==========================================================

class DigitalExamSystem:

    def __init__(self):
        # Dictionary data structures
        self.students = {}
        self.teachers = {}
        self.exams = {}
        self.results = []

        self.data_file = "exam_system_data.json"

        self.load_data()

        # Create sample data if the system is empty
        if not self.students and not self.teachers:
            self.create_sample_data()

    # ------------------------------------------------------
    # SAMPLE DATA
    # ------------------------------------------------------

    def create_sample_data(self):

        student = Student(
            "U001",
            "Joshua Bangura",
            "joshua",
            "1234",
            "ST001"
        )

        teacher = Teacher(
            "U002",
            "Mr. Kamara",
            "teacher",
            "1234",
            "TE001"
        )

        self.students[student.username] = student
        self.teachers[teacher.username] = teacher

        exam = Exam(
            "EX001",
            "Introduction to Computer Science",
            "Computer Science",
            30
        )

        exam.add_question(
            Question(
                1,
                "What does CPU stand for?",
                {
                    "A": "Central Processing Unit",
                    "B": "Computer Personal Unit",
                    "C": "Central Program Utility",
                    "D": "Computer Processing User"
                },
                "A",
                10
            )
        )

        exam.add_question(
            Question(
                2,
                "Which language is commonly used for OOP?",
                {
                    "A": "HTML",
                    "B": "Python",
                    "C": "CSS",
                    "D": "SQL"
                },
                "B",
                10
            )
        )

        exam.add_question(
            Question(
                3,
                "Which of these is a database?",
                {
                    "A": "MySQL",
                    "B": "Python",
                    "C": "Windows",
                    "D": "Chrome"
                },
                "A",
                10
            )
        )

        self.exams[exam.exam_id] = exam

        self.save_data()

    # ------------------------------------------------------
    # STUDENT REGISTRATION
    # ------------------------------------------------------

    def register_student(self):

        print("\n--- STUDENT REGISTRATION ---")

        name = input("Enter full name: ").strip()
        username = input("Create username: ").strip()

        if username in self.students or username in self.teachers:
            print("Username already exists.")
            return

        password = input("Create password: ").strip()

        student_id = f"ST{len(self.students) + 1:03d}"
        user_id = f"U{len(self.students) + len(self.teachers) + 1:03d}"

        student = Student(
            user_id,
            name,
            username,
            password,
            student_id
        )

        self.students[username] = student

        self.save_data()

        print("\nRegistration successful!")
        print(f"Your Student ID is: {student_id}")

    # ------------------------------------------------------
    # TEACHER REGISTRATION
    # ------------------------------------------------------

    def register_teacher(self):

        print("\n--- TEACHER REGISTRATION ---")

        name = input("Enter full name: ").strip()
        username = input("Create username: ").strip()

        if username in self.students or username in self.teachers:
            print("Username already exists.")
            return

        password = input("Create password: ").strip()

        teacher_id = f"TE{len(self.teachers) + 1:03d}"
        user_id = f"U{len(self.students) + len(self.teachers) + 1:03d}"

        teacher = Teacher(
            user_id,
            name,
            username,
            password,
            teacher_id
        )

        self.teachers[username] = teacher

        self.save_data()

        print("\nTeacher registration successful!")

    # ------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------

    def login(self):

        print("\n--- LOGIN ---")

        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username in self.students:
            user = self.students[username]

            if user.check_password(password):
                self.student_menu(user)
                return

        elif username in self.teachers:
            user = self.teachers[username]

            if user.check_password(password):
                self.teacher_menu(user)
                return

        print("Invalid username or password.")

    # ------------------------------------------------------
    # STUDENT MENU
    # ------------------------------------------------------

    def student_menu(self, student):

        while True:

            student.dashboard()

            print("\n1. View Available Exams")
            print("2. Take Exam")
            print("3. View My Results")
            print("4. Logout")

            choice = input("Select option: ").strip()

            if choice == "1":
                self.view_exams()

            elif choice == "2":
                self.take_exam(student)

            elif choice == "3":
                self.view_student_results(student)

            elif choice == "4":
                print("Logging out...")
                break

            else:
                print("Invalid option.")

    # ------------------------------------------------------
    # TEACHER MENU
    # ------------------------------------------------------

    def teacher_menu(self, teacher):

        while True:

            teacher.dashboard()

            print("\n1. Create Exam")
            print("2. View Exams")
            print("3. View All Results")
            print("4. Logout")

            choice = input("Select option: ").strip()

            if choice == "1":
                self.create_exam()

            elif choice == "2":
                self.view_exams()

            elif choice == "3":
                self.view_all_results()

            elif choice == "4":
                print("Logging out...")
                break

            else:
                print("Invalid option.")

    # ------------------------------------------------------
    # CREATE EXAM
    # ------------------------------------------------------

    def create_exam(self):

        print("\n--- CREATE EXAM ---")

        exam_id = f"EX{len(self.exams) + 1:03d}"

        title = input("Exam title: ").strip()
        subject = input("Subject: ").strip()

        while True:
            try:
                duration = int(input("Duration in minutes: "))

                if duration <= 0:
                    print("Duration must be greater than zero.")
                else:
                    break

            except ValueError:
                print("Enter a valid number.")

        exam = Exam(
            exam_id,
            title,
            subject,
            duration
        )

        while True:

            print("\n--- ADD QUESTION ---")

            text = input("Question: ").strip()

            options = {}

            for letter in ["A", "B", "C", "D"]:
                options[letter] = input(
                    f"Option {letter}: "
                ).strip()

            while True:
                correct = input(
                    "Correct answer (A/B/C/D): "
                ).upper().strip()

                if correct in options:
                    break

                print("Please enter A, B, C, or D.")

            while True:
                try:
                    marks = int(input("Marks: "))

                    if marks <= 0:
                        print("Marks must be greater than zero.")
                    else:
                        break

                except ValueError:
                    print("Enter a valid number.")

            question_id = len(exam.questions) + 1

            question = Question(
                question_id,
                text,
                options,
                correct,
                marks
            )

            exam.add_question(question)

            another = input(
                "Add another question? (y/n): "
            ).lower()

            if another != "y":
                break

        self.exams[exam_id] = exam

        self.save_data()

        print("\nExam created successfully!")
        print(f"Exam ID: {exam_id}")

    # ------------------------------------------------------
    # VIEW EXAMS
    # ------------------------------------------------------

    def view_exams(self):

        print("\n--- AVAILABLE EXAMS ---")

        if not self.exams:
            print("No exams available.")
            return

        for exam in self.exams.values():

            print(
                f"\nID: {exam.exam_id}"
                f"\nTitle: {exam.title}"
                f"\nSubject: {exam.subject}"
                f"\nQuestions: {len(exam.questions)}"
                f"\nTotal Marks: {exam.total_marks()}"
                f"\nDuration: {exam.duration} minutes"
            )

    # ------------------------------------------------------
    # TAKE EXAM
    # ------------------------------------------------------

    def take_exam(self, student):

        self.view_exams()

        if not self.exams:
            return

        exam_id = input("\nEnter Exam ID: ").upper().strip()

        if exam_id not in self.exams:
            print("Exam not found.")
            return

        exam = self.exams[exam_id]

        if exam.is_completed_by(student.student_id):
            print("You have already completed this examination.")
            return

        exam.display_exam()

        confirm = input(
            "Are you ready to start? (y/n): "
        ).lower()

        if confirm != "y":
            print("Exam cancelled.")
            return

        score = 0

        for question in exam.questions:

            question.display()

            while True:

                answer = input(
                    "Your answer: "
                ).upper().strip()

                if answer in ["A", "B", "C", "D"]:
                    break

                print("Please enter A, B, C, or D.")

            if question.check_answer(answer):
                score += question.marks

        exam.mark_completed(student.student_id)

        result = Result(
            student.student_id,
            student.name,
            exam.exam_id,
            exam.title,
            score,
            exam.total_marks()
        )

        self.results.append(result)

        self.save_data()

        print("\nExam submitted successfully!")

        result.display()

    # ------------------------------------------------------
    # VIEW STUDENT RESULTS
    # ------------------------------------------------------

    def view_student_results(self, student):

        print("\n--- MY RESULTS ---")

        found = False

        for result in self.results:

            if result.student_id == student.student_id:
                result.display()
                found = True

        if not found:
            print("You have no examination results yet.")

    # ------------------------------------------------------
    # VIEW ALL RESULTS
    # ------------------------------------------------------

    def view_all_results(self):

        print("\n--- ALL STUDENT RESULTS ---")

        if not self.results:
            print("No results available.")
            return

        for result in self.results:
            result.display()

    # ======================================================
    # SAVE DATA TO JSON
    # ======================================================

    def save_data(self):

        data = {
            "students": [
                student.to_dict()
                for student in self.students.values()
            ],

            "teachers": [
                teacher.to_dict()
                for teacher in self.teachers.values()
            ],

            "exams": [
                exam.to_dict()
                for exam in self.exams.values()
            ],

            "results": [
                result.to_dict()
                for result in self.results
            ]
        }

        try:

            with open(
                self.data_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

        except Exception as error:
            print(f"Error saving data: {error}")

    # ======================================================
    # LOAD DATA FROM JSON
    # ======================================================

    def load_data(self):

        if not os.path.exists(self.data_file):
            return

        try:

            with open(
                self.data_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            # Load students
            for item in data.get("students", []):

                student = Student(
                    item["user_id"],
                    item["name"],
                    item["username"],
                    "",
                    item["student_id"]
                )

                self.students[student.username] = student

            # Load teachers
            for item in data.get("teachers", []):

                teacher = Teacher(
                    item["user_id"],
                    item["name"],
                    item["username"],
                    "",
                    item["teacher_id"]
                )

                self.teachers[teacher.username] = teacher

            # Load exams
            for item in data.get("exams", []):

                exam = Exam(
                    item["exam_id"],
                    item["title"],
                    item["subject"],
                    item["duration"]
                )

                for q in item.get("questions", []):

                    question = Question(
                        q["question_id"],
                        q["text"],
                        q["options"],
                        q["correct_answer"],
                        q["marks"]
                    )

                    exam.add_question(question)

                exam.completed_students = set(
                    item.get("completed_students", [])
                )

                self.exams[exam.exam_id] = exam

            # Load results
            for item in data.get("results", []):

                result = Result(
                    item["student_id"],
                    item["student_name"],
                    item["exam_id"],
                    item["exam_title"],
                    item["score"],
                    item["total_marks"]
                )

                self.results.append(result)

        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"Could not load saved data: {error}")


# ==========================================================
# MAIN PROGRAM
# ==========================================================

def main():

    system = DigitalExamSystem()

    while True:

        print("\n")
        print("=" * 60)
        print("       DIGITAL EXAM AND RESULTS MANAGEMENT SYSTEM")
        print("=" * 60)

        print("\n1. Student Registration")
        print("2. Teacher Registration")
        print("3. Login")
        print("4. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            system.register_student()

        elif choice == "2":
            system.register_teacher()

        elif choice == "3":
            system.login()

        elif choice == "4":
            system.save_data()
            print("\nThank you for using the Digital Exam System!")
            break

        else:
            print("Invalid option. Please try again.")


# ==========================================================
# PROGRAM START
# ==========================================================

if __name__ == "__main__":
    main()