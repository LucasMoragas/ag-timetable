from dataclasses import dataclass
from typing import Optional

from ag_timetable.CourseSubject import CourseSubject

@dataclass
class ClassSlot:
    term: int                  # 1 to 6 (period/semester)
    day: int                   # 1 to 5 (Monday to Friday)
    slot: int                  # 1 to 4 (class period in the day)
    subject: Optional[CourseSubject] = None  # Will be assigned later
