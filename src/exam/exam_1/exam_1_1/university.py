from src.homework.homework_1.registry import Registry


class University:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.subjects: dict[str, Subject] = {}
        self.teachers: dict[int, Teacher] = {}
        self.students: dict[int, Student] = {}

    def add_subject(self, subject_title: str, students_id: list[int], teachers_id: list[int]) -> None:
        if subject_title in self.subjects.keys():
            raise KeyError(f"The subject {subject_title} already exists in {self.name} university")

        new_subject = register_subjects.dispatch(subject_title)()
        self.subjects[subject_title] = new_subject

        for student_id in students_id:
            if student_id in self.students.keys():
                self.bind_student_and_subject(subject_title, student_id)
            else:
                raise KeyError(f"The student with id {student_id} doesn't exist in {self.name} university")

        for teacher_id in teachers_id:
            if teacher_id in self.teachers.keys():
                self.bind_teacher_and_subject(subject_title, teacher_id)
            else:
                raise KeyError(f"The teacher with id {teacher_id} doesn't exist in {self.name} university")

    def add_student(self, student_name: str, student_id: int, subjects_title: list[str]) -> None:
        new_student = Student(student_name)
        self.students[student_id] = new_student

        for subject_title in subjects_title:
            if subject_title in self.subjects.keys():
                self.bind_student_and_subject(subject_title, student_id)
            else:
                raise KeyError(f"The subject {subject_title} doesn't exist in {self.name} university")

    def bind_student_and_subject(self, subject_title: str, student_id: int) -> None:
        student = self.students[student_id]
        student.subjects[subject_title] = []

        subject = self.subjects[subject_title]
        subject.students.append(student_id)

    def add_teacher(self, teacher_name: str, teacher_id: int, subjects_title: list[str]) -> None:
        new_teacher = Teacher(teacher_name)
        self.teachers[teacher_id] = new_teacher

        for subject_title in subjects_title:
            if subject_title in self.subjects.keys():
                self.bind_teacher_and_subject(subject_title, teacher_id)
            else:
                raise KeyError(f"The subject {subject_title} doesn't exist in {self.name} university")

    def bind_teacher_and_subject(self, subject_title: str, teacher_id: int) -> None:
        teacher = self.teachers[teacher_id]
        teacher.subjects.append(subject_title)

        subject = self.subjects[subject_title]
        subject.teachers.append(teacher_id)

    def add_score(self, student_id: int, subject_title: str, new_score: int) -> None:
        if not (0 <= new_score <= 5):
            raise AttributeError("The score for the subject should be from 0 to 5")
        if student_id not in self.students.keys():
            raise KeyError(f"The student with id {student_id} doesn't exist in {self.name} university")
        if subject_title not in self.subjects.keys():
            raise KeyError(f"The subject {subject_title} doesn't exist in {self.name} university")

        student = self.students[student_id]
        student.subjects[subject_title].append(new_score)

    def get_score(self, student_id: int, subject_title: str) -> list[int]:
        if student_id not in self.students.keys():
            raise KeyError(f"The student with id {student_id} doesn't exist in {self.name} university")
        if subject_title not in self.subjects.keys():
            raise KeyError(f"The subject {subject_title} doesn't exist in {self.name} university")

        student = self.students[student_id]
        return student.subjects[subject_title]

    def get_average(self, student_id: int, subject_title: str) -> float:
        if student_id not in self.students.keys():
            raise KeyError(f"The student with id {student_id} doesn't exist in {self.name} university")
        if subject_title not in self.subjects.keys():
            raise KeyError(f"The subject {subject_title} doesn't exist in {self.name} university")

        student = self.students[student_id]
        scores = student.subjects[subject_title]
        return sum(scores) / len(scores)

    def get_all_teachers(self, subject_title: str) -> list["Teacher"]:
        if subject_title not in self.subjects.keys():
            raise KeyError(f"The subject {subject_title} doesn't exist in {self.name} university")

        subject = self.subjects[subject_title]
        return [self.teachers[teacher_id] for teacher_id in subject.teachers]

    def get_all_students(self, subject_title: str) -> list["Student"]:
        if subject_title not in self.subjects.keys():
            raise KeyError(f"The subject {subject_title} doesn't exist in {self.name} university")

        subject = self.subjects[subject_title]
        return [self.students[student_id] for student_id in subject.students]

    def get_all_subjects_from_student(self, student_name: str) -> list["Subject"] | list[list["Subject"]]:
        students_subjects_titles = []
        for student in self.students.values():
            if student.name == student_name:
                students_subjects_titles.append(student.subjects.keys())
        if len(students_subjects_titles) == 0:
            raise KeyError(f"The student with name {student_name} doesn't exist in {self.name} university")
        elif len(students_subjects_titles) == 1:
            return [self.subjects[title] for title in students_subjects_titles[0]]
        else:
            return [[self.subjects[title] for title in smh] for smh in students_subjects_titles]

    def get_all_subjects_from_teacher(self, teacher_name: str) -> list["Subject"] | list[list["Subject"]]:
        teachers_subjects_titles = []
        for teacher in self.teachers.values():
            if teacher.name == teacher_name:
                teachers_subjects_titles.append(teacher.subjects)

        if len(teachers_subjects_titles) == 0:
            raise KeyError(f"The teacher with name {teacher_name} doesn't exist in {self.name} university")
        elif len(teachers_subjects_titles) == 1:
            return [self.subjects[title] for title in teachers_subjects_titles[0]]
        else:
            return [[self.subjects[title] for title in smh] for smh in teachers_subjects_titles]


class Teacher:
    def __init__(self, name: str) -> None:
        self.subjects: list[str] = []
        self.name: str = name


class Student:
    def __init__(self, name: str) -> None:
        self.subjects: dict[str, list[int]] = {}
        self.name: str = name


class Subject:
    def __init__(self) -> None:
        self.students: list[int] = []
        self.teachers: list[int] = []


register_subjects = Registry[Subject](None)


@register_subjects.register("math")
class Math(Subject):
    def __init__(self) -> None:
        super().__init__()


@register_subjects.register("biology")
class Biology(Subject):
    def __init__(self) -> None:
        super().__init__()


@register_subjects.register("physics")
class Physics(Subject):
    def __init__(self) -> None:
        super().__init__()


@register_subjects.register("english")
class EnglishLanguage(Subject):
    def __init__(self) -> None:
        super().__init__()


if __name__ == "__main__":
    pass
