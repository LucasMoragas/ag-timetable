import tkinter as tk
from tkinter import BooleanVar, Frame, Label, Entry, Button, Checkbutton, LEFT, RIGHT, BOTH, Y, X, TOP, BOTTOM, DISABLED, NORMAL
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from concurrent.futures import ThreadPoolExecutor

from ag_timetable.ScheduleGA import ScheduleGA
from ag_timetable.CourseSubject import CourseSubject

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

class ScheduleGAInterface:
    def __init__(self, root):
        """
        GUI Interface for the Schedule Genetic Algorithm.

        Top frame: form for GA parameters and plot side by side.
        Bottom frame: pivot table showing the best schedule.
        """
        self.root = root
        self.root.title("Schedule GA Explorer")
        self.root.geometry("1000x750")
        self.root.configure(bg="#2E2E2E")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Executor for background GA runs
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.ga = None
        self.future = None

        self.create_frames()
        self.create_form()
        self.create_plot()
        self.create_table()

    def create_frames(self):
        # Top container for form and plot
        self.frame_top = Frame(self.root, bg="#2E2E2E")
        self.frame_top.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        # Form frame on left
        self.frame_left = Frame(self.frame_top, bg="#2E2E2E", width=300)
        self.frame_left.pack(side=LEFT, fill=Y, padx=(0,10))

        # Plot frame on right
        self.frame_right = Frame(self.frame_top, bg="#2E2E2E")
        self.frame_right.pack(side=RIGHT, fill=BOTH, expand=True)

        # Bottom frame for schedule table
        self.frame_bottom = Frame(self.root, bg="#2E2E2E")
        self.frame_bottom.pack(side=BOTTOM, fill=BOTH, expand=True, padx=10, pady=(0,10))

    def create_form(self):
        Label(self.frame_left, text="Schedule GA", bg="#2E2E2E", fg="white",
              font=("Verdana", 16, "bold")).pack(pady=10)
        fields = [
            ("Population Size:", "pop_size"),
            ("Generations:", "generations"),
            ("Crossover Prob:", "cx_prob"),
            ("Mutation Rate:", "mu_rate"),
            ("Elitism Size:", "elitism_size"),
            ("Tournament Size:", "tournament_size"),
        ]
        self.entries = {}
        for label_text, var_name in fields:
            Label(self.frame_left, text=label_text, bg="#2E2E2E", fg="white",
                  font=("Verdana", 12)).pack(anchor="w", pady=5)
            entry = Entry(self.frame_left, bg="#555555", fg="white", insertbackground="white",
                          font=("Verdana", 12))
            entry.pack(fill="x", pady=2)
            self.entries[var_name] = entry
        defaults = {'pop_size':'50','generations':'100','cx_prob':'0.9','mu_rate':'0.1','elitism_size':'2','tournament_size':'3'}
        for k,v in defaults.items(): self.entries[k].insert(0, v)
        self.tournament_var = BooleanVar(value=True)
        Checkbutton(self.frame_left, text="Tournament Selection", variable=self.tournament_var,
                    bg="#2E2E2E", fg="white", selectcolor="#2E2E2E",
                    font=("Verdana", 12)).pack(anchor="w", pady=10)
        self.run_button = Button(self.frame_left, text="Run GA", bg="#555555", fg="white",
                                 font=("Verdana", 12, "bold"), command=self.on_run)
        self.run_button.pack(pady=10)
        self.result_label = Label(self.frame_left, text="Best Fitness: N/A", bg="#2E2E2E", fg="white",
                                   font=("Verdana", 12))
        self.result_label.pack(pady=5)

    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.fig.patch.set_facecolor("#2E2E2E")
        self.ax.set_facecolor("#2E2E2E")
        self.ax.set_title("Best Fitness over Generations", color="white")
        self.ax.tick_params(colors="white")
        self.ax.set_xlabel("Generation", color="white")
        self.ax.set_ylabel("Fitness", color="white")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_right)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        self.canvas.draw()

    def create_table(self):
        # Style configuration for gridlines and headers
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview',
                        font=('Verdana', 10),
                        rowheight=60,
                        bordercolor='#616161',
                        borderwidth=1,
                        relief='solid',
                        background='#2E2E2E',
                        foreground='white',
                        gridcolor='#444444')
        style.configure('Treeview.Heading',
                        font=('Verdana', 10, 'bold'),
                        background='#444444',
                        foreground='white',
                        bordercolor='#666666',
                        borderwidth=1,
                        relief='solid')
        style.map('Treeview.Heading',
                  background=[('active', '#555555')])

        Label(self.frame_bottom, text="Best Schedule (Periods x Day-Slot)", bg="#2E2E2E", fg="white",
              font=("Verdana", 14, "bold")).pack(anchor="w", pady=(5,0))
        # Columns: Day1 Slot1 ... Day5 Slot4
        self.days = range(1,6)
        self.slots = range(1,5)
        cols = [f"D{d}_S{s}" for d in self.days for s in self.slots]
        headers = [f"Day {d} Slot {s}" for d in self.days for s in self.slots]
        self.tree = ttk.Treeview(self.frame_bottom, columns=cols, show='headings')
        self.tree.pack(fill=BOTH, expand=True, pady=5)

        for col, head in zip(cols, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=90, anchor="center", stretch=True)

    def on_run(self):
        self.run_button.config(state=DISABLED)
        self.result_label.config(text="Best Fitness: Running...")
        self.tree.delete(*self.tree.get_children())
        params = {
            'subjects': course_schedule,
            'pop_size': int(self.entries['pop_size'].get()),
            'generations': int(self.entries['generations'].get()),
            'use_tournament': self.tournament_var.get(),
            'crossover_prob': float(self.entries['cx_prob'].get()),
            'elitism_size': int(self.entries['elitism_size'].get()),
            'mutation_rate': float(self.entries['mu_rate'].get()),
            'tournament_size': int(self.entries['tournament_size'].get()),
        }
        self.ga = ScheduleGA(**params)
        self.future = self.executor.submit(self.ga.run)
        self.root.after(100, self.check_future)

    def check_future(self):
        if self.future.done():
            best_sched = self.future.result()
            fitness = self.ga._fitness(best_sched)
            gens, bests = self.ga.export_history()
            self.update_plot(gens, bests)
            self.result_label.config(text=f"Best Fitness: {fitness:.4f}")
            self.update_table(best_sched)
            self.run_button.config(state=NORMAL)
        else:
            self.root.after(100, self.check_future)

    def update_plot(self, x, y):
        self.ax.clear()
        self.ax.set_facecolor("#2E2E2E")
        self.ax.plot(x, y, color="cyan", label="Best Fitness")
        self.ax.set_title("Best Fitness over Generations", color="white")
        self.ax.tick_params(colors="white")
        self.ax.set_xlabel("Generation", color="white")
        self.ax.set_ylabel("Fitness", color="white")
        self.ax.legend(facecolor="#2E2E2E", edgecolor="white", labelcolor="white")
        self.canvas.draw()

    def update_table(self, sched):
        self.tree.delete(*self.tree.get_children())
        # Map (term,day,slot)->subject
        sched_map = {(slot.term, slot.day, slot.slot):
                     (slot.subject.subject_name if slot.subject else 'Free')
                     for slot in sched.slots}
        # Insert a row per term
        for term in range(1,7):
            row = []
            for d in self.days:
                for s in self.slots:
                    row.append(sched_map.get((term, d, s), ''))
            self.tree.insert('', 'end', values=row, tags=('row',))

    def on_close(self):
        self.executor.shutdown(wait=False)
        self.root.quit()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    ScheduleGAInterface(root)
    root.mainloop()
