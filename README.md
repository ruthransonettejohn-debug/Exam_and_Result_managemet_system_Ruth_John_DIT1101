Exam and Result Management System
​A robust, object-oriented console-based application written in Python for managing digital examinations, student registrations, teacher controls, automated grading, and JSON-based persistence.
​Features
​Role-Based Authentication & Dashboards: Separate workflows and access privileges for Students and Teachers through a polymorphic user structure.
​Dynamic Exam Creation: Teachers can build custom multiple-choice exams with specified durations, mark distributions, and multiple option sets (A, B, C, D).
​Automated Scoring & Grading: Instantly grades completed exams, calculates percentage scores, assigns academic letter grades (A–F), and tracks pass/fail statuses.
​Prevent Duplicate Submissions: Utilizes Python set data structures to ensure students can only take any given examination once.
​Persistent Data Storage: Automatically saves and loads all system entities (students, teachers, exams, questions, and historical results) to and from a local JSON file (exam_system_data.json).
​Class Architecture & Components

​1. User (ABC)
​Purpose: Serves as an abstract base class for all system users, enforcing encapsulation and shared attributes.
​Attributes: __user_id, __name, __username, __password (private attributes accessed via properties).
​Methods:
​check_password(password): Verifies user login credentials.
​dashboard() (Abstract): Forces subclasses to implement a custom dashboard view.

​2. Student (Inherits from User)
​Purpose: Represents a student entity capable of participating in exams and reviewing performance.
​Additional Attributes: student_id.
​Methods:
​dashboard(): Displays the student welcome message and available navigation.
​to_dict(): Serializes student attributes into a dictionary format for JSON export.

​3. Teacher (Inherits from User)
​Purpose: Represents an instructor or administrative user capable of creating exams and auditing results.
​Additional Attributes: teacher_id.
​Methods:
​dashboard(): Displays the teacher welcome message and available navigation.
​to_dict(): Serializes teacher attributes into a dictionary format for JSON export.

​4. Question
​Purpose: Manages individual examination questions, options, correct choices, and assigned marks.
​Attributes: question_id, text, options (dictionary), correct_answer, marks.
​Methods:
​display(): Renders the formatted question text and multiple-choice options to the console.
​check_answer(answer): Validates a student's answer against the stored correct choice.
​to_dict(): Serializes the question data structure.

​5. Exam
​Purpose: Manages an entire examination package, including questions, time limits, and tracking tracking for completed attempts.
​Attributes: exam_id, title, subject, duration, questions (list), completed_students (set).
​Methods:
​add_question(question): Appends a Question instance to the exam question list.
​total_marks(): Computes the aggregate points possible for the exam.
​is_completed_by(student_id): Checks if a student has already taken this exam using the internal set structure.
​mark_completed(student_id): Records a student ID into the completed set.
​display_exam(): Prints exam metadata (title, subject, duration, questions count).
​to_dict(): Serializes the exam and its nested questions/completed student records.

​6. Result
​Purpose: Computes and stores performance metrics for a completed examination attempt.
​Attributes: student_id, student_name, exam_id, exam_title, score, total_marks, percentage, grade, status.
​Methods:
​calculate_percentage(): Computes the score percentage ratio.
​calculate_grade(): Maps percentage ranges to letter grades (80%+ = A, 70%+ = B, 60%+ = C, 50%+ = D, <50 = F).
​calculate_status(): Determines "PASS" or "FAIL" status based on a 50% threshold.
​display(): Formats and prints a detailed score report card.
​to_dict(): Serializes result metrics for storage.

​7. DigitalExamSystem
​Purpose: Acts as the core controller managing collections, menus, and file input/output operations.
​Dictionaries & Lists:
​self.students: Maps usernames to Student instances.
​self.teachers: Maps usernames to Teacher instances.
​self.exams: Maps exam IDs to Exam instances.
​self.results: Stores historical Result instances in a list.
​Core Methods:
​register_student() / register_teacher(): Handles user onboarding and dynamic ID generation.
​login(): Authenticates credentials and routes users to their respective menus.
​create_exam(): Interactive prompt for instructors to generate new tests and questions.
​take_exam(student): Manages the active examination session, captures inputs, grades answers, and logs results.
​save_data() / load_data(): Manages reading and writing application state to exam_system_data.json.

​How to Run
Ensure you have Python 3 installed on your system.
Save the code into a file named main.py.
Open your terminal or command prompt in the script's directory and execute:
