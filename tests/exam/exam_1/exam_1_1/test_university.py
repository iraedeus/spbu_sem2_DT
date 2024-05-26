import pytest

from src.exam.exam_1.exam_1_1.university import *


def abitura():
    unty = University("first")
    for i in range(6):
        unty.add_student(str(i), i, [])
    for i in range(6):
        unty.add_teacher(str(i), i, [])

    unty.add_subject("math", [3, 5], [1, 2, 5])
    unty.add_subject("physics", [1, 2, 5], [1, 4])
    unty.add_subject("biology", [1, 3], [5])

    return unty


def session(unty: University):
    for i in range(0, 6, 2):
        unty.add_score(1, "biology", i)
    for i in range(4):
        unty.add_score(3, "math", 5)

    return unty


class TestUniversityAdd:
    def test_add_subject(self):
        unty = University("test")
        unty.add_subject("math", [], [])
        unty.add_subject("physics", [], [])

        assert set(unty.subjects.keys()) == {"math", "physics"}
        assert unty.subjects["math"].students == []
        assert unty.subjects["physics"].students == []

    def test_add_student(self):
        unty = University("test")
        unty.add_student("1", 1, [])
        unty.add_student("2", 2, [])

        assert set(unty.students.keys()) == {1, 2}
        assert unty.students[1].subjects == {}
        assert unty.students[2].subjects == {}

    def test_add_student_and_subject(self):
        unty = University("test")
        unty.add_student("1", 1, [])
        unty.add_student("2", 2, [])
        unty.add_subject("math", [1], [])
        unty.add_subject("physics", [1, 2], [])

        assert unty.students[1].subjects == {"math": [], "physics": []}
        assert unty.students[2].subjects == {"physics": []}
        assert unty.subjects["math"].students == [1]
        assert unty.subjects["physics"].students == [1, 2]

    def test_add_teacher(self):
        unty = University("test")
        unty.add_teacher("1", 1, [])
        unty.add_teacher("2", 2, [])

        assert set(unty.teachers.keys()) == {1, 2}
        assert unty.teachers[1].subjects == []
        assert unty.teachers[2].subjects == []

    def test_add_teacher_and_subject(self):
        unty = University("test")
        unty.add_teacher("1", 1, [])
        unty.add_teacher("2", 2, [])
        unty.add_subject("math", [], [1, 2])
        unty.add_subject("physics", [], [1, 2])

        assert set(unty.teachers[1].subjects) == {"math", "physics"}
        assert set(unty.teachers[2].subjects) == {"math", "physics"}
        assert unty.subjects["math"].teachers == [1, 2]
        assert unty.subjects["physics"].teachers == [1, 2]

    def test_add_all(self):
        unty = University("test")
        unty.add_teacher("1", 1, [])
        unty.add_teacher("2", 2, [])
        unty.add_student("1", 1, [])
        unty.add_student("2", 2, [])
        unty.add_subject("math", [], [1, 2])
        unty.add_subject("physics", [1, 2], [1, 2])

        assert set(unty.teachers[1].subjects) == {"math", "physics"}
        assert set(unty.teachers[2].subjects) == {"math", "physics"}
        assert unty.students[1].subjects == {"physics": []}
        assert unty.students[2].subjects == {"physics": []}
        assert unty.subjects["math"].teachers == [1, 2]
        assert unty.subjects["physics"].teachers == [1, 2]
        assert unty.subjects["math"].students == []
        assert unty.subjects["physics"].students == [1, 2]


class TestUniversityAPI:
    unty = abitura()
    unty = session(unty)

    def test_get_score(self):
        assert self.unty.get_score(1, "biology") == [0, 2, 4]
        assert self.unty.get_score(3, "math") == [5, 5, 5, 5]

    def test_get_average(self):
        assert self.unty.get_average(1, "biology") == 2.0
        assert self.unty.get_average(3, "math") == 5.0

    def test_get_teachers(self):
        assert self.unty.get_all_teachers("math") == [
            self.unty.teachers[1],
            self.unty.teachers[2],
            self.unty.teachers[5],
        ]
        assert self.unty.get_all_teachers("biology") == [self.unty.teachers[5]]

    def test_get_students(self):
        assert self.unty.get_all_students("math") == [self.unty.students[3], self.unty.students[5]]
        assert self.unty.get_all_students("biology") == [self.unty.students[1], self.unty.students[3]]

    def test_get_subjects_from_student(self):
        assert self.unty.get_all_subjects_from_student("1") == [
            self.unty.subjects["physics"],
            self.unty.subjects["biology"],
        ]
        assert self.unty.get_all_subjects_from_student("3") == [
            self.unty.subjects["math"],
            self.unty.subjects["biology"],
        ]

    def test_get_subjects_from_teacher(self):
        assert self.unty.get_all_subjects_from_teacher("1") == [
            self.unty.subjects["math"],
            self.unty.subjects["physics"],
        ]
        assert self.unty.get_all_subjects_from_teacher("3") == []
