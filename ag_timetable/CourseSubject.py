from dataclasses import dataclass

@dataclass
class CourseSubject:
    term: int               # ex: 1st or 2nd semester
    subject_name: str       # ex: "Algorithms"
    instructor: str         # ex: "Ernani Borges"
    lecture_count: int      # number of scheduled classes
