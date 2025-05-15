from ag_timetable.CourseSubject import CourseSubject
from ag_timetable.WeeklySchedule import WeeklySchedule

course_schedule = [
    # Term 1
    CourseSubject(1, "Algorithms", "Ernani Borges", 8),
    CourseSubject(1, "F. WEB Design", "Marco Maciel", 2),
    CourseSubject(1, "Mathematics", "Jorge", 6),
    CourseSubject(1, "Extension 1", "Aline", 1),
    CourseSubject(1, "Architecture", "Rogélio", 3),

    # Term 2
    CourseSubject(2, "Logic", "Marcelo Barreiro", 3),
    CourseSubject(2, "Data Structures (E.D.)", "Alexandre", 6),
    CourseSubject(2, "Database Modeling (Mod. B.D.)", "Camilo", 2),
    CourseSubject(2, "Operating Systems (S.O.)", "Gustavo Bota", 4),
    CourseSubject(2, "Extension 2", "Rogélio", 1),
    CourseSubject(2, "Web Scripting", "Aline", 2),
    CourseSubject(2, "Free", "Unknow", 2),

    # Term 3
    CourseSubject(3, "OOP (P.O.O.)", "Eduardo Silvestre", 6),
    CourseSubject(3, "Extension 3", "Camilo", 1),
    CourseSubject(3, "O.O. (P.O.)", "Hugo", 5),
    CourseSubject(3, "Databases (B.D.)", "Rogério Costa", 6),
    CourseSubject(3, "Interface", "Lídia", 2),

    # Term 4
    CourseSubject(4, "Project Development and Management (P.D.M.)", "Jefferson", 8),
    CourseSubject(4, "Web Application Development I (D.A.W.1)", "Rafael Godoi", 4),
    CourseSubject(4, "Software Engineering (Esof)", "Mauro", 4),
    CourseSubject(4, "Networks", "Frederico", 4),

    # Term 5
    CourseSubject(5, "Software Engineering Lab (LabEsof)", "Mauro", 6),
    CourseSubject(5, "Project Planning (P.P.)", "Marco Maciel", 2),
    CourseSubject(5, "Web Application Development II (DAW 2)", "Lídia", 4),
    CourseSubject(5, "Probability", "Alef", 2),
    CourseSubject(5, "Ethics", "Ana Lúcia", 2),
    CourseSubject(5, "Server Deployment", "Gustavo Bota", 4),
    
    # Term 6
    CourseSubject(6, "Project Management (GeProj)", "Marco Maciel", 4),
    CourseSubject(6, "Information Security", "Elson", 4),
    CourseSubject(6, "Extension 6", "Ademir", 2),
    CourseSubject(6, "Entrepreneurship", "Ana Lúcia", 2),
    CourseSubject(6, "Data Science", "Marcelo Barreiro", 4),
    CourseSubject(6, "Computer Intelligence", "José Ricardo", 4),
]

schedule = WeeklySchedule()
schedule.assign_subjects_randomly(course_schedule)

print("Conflicts:", schedule.count_schedule_conflicts())
print("Double aggregations:", schedule.count_double_aggregations())
print("Triple aggregations:", schedule.count_triple_aggregations())
print("Quadruple aggregations:", schedule.count_quadruple_aggregations())
