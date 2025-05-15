import random
import copy
from typing import List, Tuple
from ag_timetable.WeeklySchedule import WeeklySchedule
from ag_timetable.CourseSubject import CourseSubject

class ScheduleGA:
    """
    Genetic Algorithm for generating optimal weekly schedules for course subjects.

    Attributes:
        subjects (List[CourseSubject]): List of course subjects to schedule.
        pop_size (int): Number of individuals in the population.
        generations (int): Number of generations to run.
        use_tournament (bool): If True, use tournament selection; if False, use roulette selection.
        crossover_prob (float): Probability of performing crossover between two parents.
        elitism_size (int): Number of top individuals to carry over unchanged each generation.
        mutation_rate (float): Probability of applying mutation to a child.
        tournament_size (int): Number of competitors in tournament selection.
        population (List[WeeklySchedule]): Current population of schedules.
        history_gens (List[int]): Generation indices recorded during evolution.
        history_best (List[float]): Best fitness values per generation.
    """
    def __init__(
        self,
        subjects: List[CourseSubject],
        pop_size: int = 50,
        generations: int = 100,
        use_tournament: bool = True,
        crossover_prob: float = 0.9,
        elitism_size: int = 2,
        mutation_rate: float = 0.1,
        tournament_size: int = 3
    ):
        """
        Initialize the genetic algorithm with given parameters.

        Args:
            subjects: list of CourseSubject instances to schedule.
            pop_size: population size.
            generations: number of iterations to evolve.
            use_tournament: True for tournament selection, False for roulette.
            crossover_prob: probability of performing crossover between parents.
            elitism_size: number of best individuals preserved each generation.
            mutation_rate: chance of mutating a newly created child.
            tournament_size: number of individuals in tournament selection.
        """
        self.subjects = subjects
        self.pop_size = pop_size
        self.generations = generations
        self.use_tournament = use_tournament
        self.crossover_prob = crossover_prob
        self.elitism_size = elitism_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        # initialize population with random schedules
        self.population: List[WeeklySchedule] = [self._random_individual() for _ in range(self.pop_size)]
        # history for plotting
        self.history_gens: List[int] = []
        self.history_best: List[float] = []

    def _random_individual(self) -> WeeklySchedule:
        """
        Create a new random WeeklySchedule individual by assigning subjects randomly.

        Returns:
            A WeeklySchedule populated with randomly assigned subjects.
        """
        sched = WeeklySchedule()
        sched.assign_subjects_randomly(self.subjects)
        return sched

    def _fitness(self, sched: WeeklySchedule) -> float:
        """
        Calculate the fitness of a WeeklySchedule based on contiguous lectures and conflicts.

        Fitness = (20*doubles + 30*triples + 40*quadruples) / (100 * conflicts),
        where doubles, triples, quadruples are counts of adjacent lecture slots and
        conflicts is the number of scheduling conflicts.

        Args:
            sched: WeeklySchedule to evaluate.
        Returns:
            A float fitness score (higher is better).
        """
        d = sched.count_double_aggregations()
        t = sched.count_triple_aggregations()
        q = sched.count_quadruple_aggregations()
        c = sched.count_schedule_conflicts()
        return (20 * d + 30 * t + 40 * q) / max(1, 100 * c)

    def _select_parent(self) -> WeeklySchedule:
        """
        Select a parent individual from the population based on the selection flag.

        Returns:
            A selected WeeklySchedule from the population.
        """
        if self.use_tournament:
            # Tournament selection: choose the best of a random sample
            competitors = random.sample(self.population, self.tournament_size)
            return max(competitors, key=self._fitness)
        else:
            # Fitness proportionate selection (roulette wheel)
            fits = [self._fitness(ind) for ind in self.population]
            total = sum(fits)
            pick = random.uniform(0, total)
            current = 0.0
            for ind, fit in zip(self.population, fits):
                current += fit
                if current >= pick:
                    return ind
            return self.population[-1]

    def _crossover(self, p1: WeeklySchedule, p2: WeeklySchedule) -> WeeklySchedule:
        """
        Perform term-level crossover between two parent schedules.

        A cut point is chosen among terms, and all slots for terms <= cut come from p1,
        while the remaining terms come from p2.

        Args:
            p1: first parent WeeklySchedule.
            p2: second parent WeeklySchedule.
        Returns:
            A new WeeklySchedule offspring.
        """
        child = WeeklySchedule()
        child.slots.clear()
        terms = sorted({slot.term for slot in p1.slots})
        cut_index = random.randint(1, len(terms) - 1)
        for term in terms:
            source = p1 if term <= terms[cut_index - 1] else p2
            block = [copy.deepcopy(slot) for slot in source.slots if slot.term == term]
            child.slots.extend(block)
        return child

    def _mutate(self, sched: WeeklySchedule):
        """
        Mutate a schedule by swapping two slots within the same term to maintain validity.

        Args:
            sched: WeeklySchedule to mutate in place.
        """
        idx1, idx2 = random.sample(range(len(sched.slots)), 2)
        slot1 = sched.slots[idx1]
        slot2 = sched.slots[idx2]
        if slot1.term == slot2.term:
            slot1.subject, slot2.subject = slot2.subject, slot1.subject

    def run(self) -> WeeklySchedule:
        """
        Execute the genetic algorithm over the specified number of generations.

        Returns:
            The best WeeklySchedule found.
        """
        for gen in range(self.generations):
            # Sort population by descending fitness
            sorted_pop = sorted(self.population, key=self._fitness, reverse=True)
            # Carry over elites unchanged
            new_population = sorted_pop[:self.elitism_size]
            # Fill the rest of the new population
            while len(new_population) < self.pop_size:
                parent1 = self._select_parent()
                parent2 = self._select_parent()
                if random.random() < self.crossover_prob:
                    child = self._crossover(parent1, parent2)
                else:
                    child = copy.deepcopy(parent1)
                if random.random() < self.mutation_rate:
                    self._mutate(child)
                new_population.append(child)
            self.population = new_population
            # record history for plotting
            best_ind = max(self.population, key=self._fitness)
            best_fit = self._fitness(best_ind)
            self.history_gens.append(gen)
            self.history_best.append(best_fit)
        # Return the best schedule from the final population
        return max(self.population, key=self._fitness)

    def export_history(self) -> Tuple[List[int], List[float]]:
        """
        Export the recorded history of best fitness per generation.

        Returns:
            A tuple (generations, best_fitness_values).
        """
        return self.history_gens, self.history_best
    
    def export_best(self) -> WeeklySchedule:
        """
        Export the best individual (WeeklySchedule) from the current population.

        Returns:
            The WeeklySchedule with highest fitness from the final population.
        """
        return max(self.population, key=self._fitness)


if __name__ == "__main__":
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

    # Initialize the genetic algorithm with example parameters
    ga = ScheduleGA(
        subjects=course_schedule,
        pop_size=20,
        generations=50,
        use_tournament=True,  # True for tournament, False for roulette
        crossover_prob=0.8,
        elitism_size=2,
        mutation_rate=0.1,
        tournament_size=3
    )

    # Run the algorithm and retrieve the best schedule
    best_schedule = ga.run()
    fitness = ga._fitness(best_schedule)
    print(f"Best fitness: {fitness:.4f}")

    # Display the resulting schedule slots
    for slot in best_schedule.slots:
        subj_name = slot.subject.subject_name if slot.subject else 'Free'
        print(f"Term {slot.term} Day {slot.day} Slot {slot.slot}: {subj_name}")


    # Run the algorithm and retrieve the best schedule
    best_schedule = ga.run()
    fitness = ga._fitness(best_schedule)
    print(f"Best fitness: {fitness:.4f}")
    print("Conflicts:", best_schedule.count_schedule_conflicts())
    print("Double aggregations:", best_schedule.count_double_aggregations())
    print("Triple aggregations:", best_schedule.count_triple_aggregations())
    print("Quadruple aggregations:", best_schedule.count_quadruple_aggregations())
    
