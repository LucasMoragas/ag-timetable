from dataclasses import dataclass, field
from typing import List
from collections import defaultdict
import random

from ag_timetable.CourseSubject import CourseSubject
from ag_timetable.ClassSlot import ClassSlot

@dataclass
class WeeklySchedule:
    slots: List[ClassSlot] = field(default_factory=list)

    def __post_init__(self):
        # Inicializa 6 períodos × 5 dias × 4 aulas = 120 slots semanais
        for term in range(1, 7):           # Períodos de 1 a 6
            for day in range(1, 6):        # Dias úteis (1 a 5)
                for slot in range(1, 5):   # 4 horários por dia
                    self.slots.append(ClassSlot(term=term, day=day, slot=slot))

    def assign_subjects_randomly(self, subjects: List[CourseSubject]):
        """
        Distribui aleatoriamente as disciplinas em seus respectivos períodos,
        respeitando o número de aulas semanais (lecture_count) de cada uma.
        """
        for term in range(1, 7):
            term_subjects = [s for s in subjects if s.term == term]
            term_slots = [s for s in self.slots if s.term == term and s.subject is None]
            random.shuffle(term_slots)

            for subject in term_subjects:
                assigned_count = 0
                for slot in term_slots:
                    if slot.subject is None:
                        slot.subject = subject
                        assigned_count += 1
                        if assigned_count == subject.lecture_count:
                            break
                if assigned_count < subject.lecture_count:
                    raise ValueError(f"Not enough available slots to assign '{subject.subject_name}' in term {term}.")

    def count_schedule_conflicts(self) -> int:
        """
        Retorna a quantidade de conflitos de horário, ou seja, quando o mesmo professor
        está alocado para disciplinas diferentes no mesmo dia e horário, mas em períodos distintos.
        """
        conflict_count = 0
        grouped_by_time = defaultdict(list)

        # Agrupa todos os slots pelo horário (dia e slot)
        for s in self.slots:
            if s.subject is not None:
                key = (s.day, s.slot)
                grouped_by_time[key].append(s)

        # Verifica se o mesmo professor aparece mais de uma vez no mesmo horário
        for (day, slot), slots in grouped_by_time.items():
            prof_counts = defaultdict(list)
            for s in slots:
                prof_counts[s.subject.instructor].append(s)

            for instructor, prof_slots in prof_counts.items():
                if len(prof_slots) > 1:
                    conflict_count += len(prof_slots) - 1  # N conflitos = N - 1 pares simultâneos

        return conflict_count

    def count_double_aggregations(self) -> int:
        """
        Conta quantas vezes uma disciplina aparece em dois slots consecutivos
        no mesmo dia (ex: slots 1 e 2).
        """
        aggregation_count = 0
        subject_slots = defaultdict(list)

        # Agrupa os slots por disciplina
        for s in self.slots:
            if s.subject is not None:
                key = (s.term, s.subject.subject_name)
                subject_slots[key].append(s)

        # Verifica aglutinações duplas por dia
        for (term, subject_name), slots in subject_slots.items():
            slots_by_day = defaultdict(list)
            for s in slots:
                slots_by_day[s.day].append(s.slot)

            for day, slot_list in slots_by_day.items():
                slot_list.sort()
                for i in range(len(slot_list) - 1):
                    if slot_list[i + 1] == slot_list[i] + 1:
                        aggregation_count += 1

        return aggregation_count

    def count_triple_aggregations(self) -> int:
        """
        Conta quantas vezes uma disciplina aparece em três slots consecutivos
        no mesmo dia (ex: slots 1, 2, 3).
        """
        aggregation_count = 0
        subject_slots = defaultdict(list)

        for s in self.slots:
            if s.subject is not None:
                key = (s.term, s.subject.subject_name)
                subject_slots[key].append(s)

        for (term, subject_name), slots in subject_slots.items():
            slots_by_day = defaultdict(list)
            for s in slots:
                slots_by_day[s.day].append(s.slot)

            for day, slot_list in slots_by_day.items():
                slot_list.sort()
                for i in range(len(slot_list) - 2):
                    if (slot_list[i + 1] == slot_list[i] + 1 and
                        slot_list[i + 2] == slot_list[i] + 2):
                        aggregation_count += 1

        return aggregation_count

    def count_quadruple_aggregations(self) -> int:
        """
        Conta quantas vezes uma disciplina aparece em quatro slots consecutivos
        no mesmo dia (ex: slots 1, 2, 3, 4).
        """
        aggregation_count = 0
        subject_slots = defaultdict(list)

        for s in self.slots:
            if s.subject is not None:
                key = (s.term, s.subject.subject_name)
                subject_slots[key].append(s)

        for (term, subject_name), slots in subject_slots.items():
            slots_by_day = defaultdict(list)
            for s in slots:
                slots_by_day[s.day].append(s.slot)

            for day, slot_list in slots_by_day.items():
                slot_list.sort()
                for i in range(len(slot_list) - 3):
                    if (slot_list[i + 1] == slot_list[i] + 1 and
                        slot_list[i + 2] == slot_list[i] + 2 and
                        slot_list[i + 3] == slot_list[i] + 3):
                        aggregation_count += 1

        return aggregation_count

    def free_class_slots_status(self) -> List[ClassSlot]:
        free_slots = [s for s in self.slots if s.subject.subject_name == "Free"]
        
        if free_slots[0].day == free_slots[1].day:
            if free_slots[0].slot == 1 and free_slots[1].slot == 2:
                return 1
            elif free_slots[0].slot == 3 and free_slots[1].slot == 4:
                return 1
            elif free_slots[0].slot == 1 and free_slots[1].slot == 4:
                return 1
            if free_slots[1].slot == 1 and free_slots[0].slot == 2:
                return 1
            elif free_slots[1].slot == 3 and free_slots[0].slot == 4:
                return 1
            elif free_slots[1].slot == 1 and free_slots[0].slot == 4:
                return 1
            else:
                return 0
        else:
            if free_slots[0].slot == 1 and free_slots[1].slot == 4:
                return 1
            elif free_slots[1].slot == 1 and free_slots[0].slot == 4:
                return 1
            else:
                return 0