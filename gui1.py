import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEvent, QThread, Signal
from PySide6.QtWidgets import QApplication, QGridLayout, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QButtonGroup, QCheckBox, QFileDialog ,QLineEdit,QHBoxLayout, QStackedWidget, QStackedLayout
from PySide6.QtGui import QPixmap, QIcon, Qt, QColor, QIntValidator
import pandas as pd
import random

class Customer():
    def __init__(self, demand):
        self.demand = demand
class Producent():
    def __init__(self, quantity, price):
        self.price = price
        self.quantity = quantity

class Bee():
    def __init__(self, product, matrix_producents, matrix_customers, number_products, number_customers, number_bees, number_observator, restricition, producents, price, distance):
        self.product = product
        self.matrix_producents = matrix_producents
        self.matrix_customers = matrix_customers
        self.number_products = number_products
        self.number_customers = number_customers
        self.number_bees = number_bees
        self.number_observator = number_observator
        self.restricition = restricition #Wektor klientow posiadajacych zapotrzebowanie na produkt X
        self.producents = producents  #Wektor producentow produkujacych produkt X
        self.price = price
        self.distance = distance

    def function(self, distribuation):
            k = self.product - 1
            m = len(self.matrix_producents[0])
            n = len(distribuation[0])
            value = 0
            matrix = [[0] * m for i in range(n)]
            for i in range(n):
                for j in range(m):
                    if distribuation[i][j] >= 0.1 * self.matrix_producents[j][k]:
                        matrix[i][j] = distribuation[i][j] * self.price[j][k]
                    else:
                        matrix[i][j] = distribuation[i][j] * self.price[j][k] + 0.45 * self.distance[i][j]
                    value += matrix[i][j]
                    value = round(value, 5)
            return value
    
    def function_efficency(self, value):
            value_eff = 1 / (1 + value)
            value_eff = round(value_eff, 5)
                    
            return value_eff
        

    def correct_position(self, new_bee):
            
            counter=0
            kolumny = np.sum(new_bee, axis=0)
            wiersze = np.sum(new_bee, axis=1)
            
            while not(np.all(self.restricition == wiersze) and np.all(kolumny <= self.producents)):
                a=np.shape(new_bee)[0]
                b=np.shape(new_bee)[1]
                for i in range(a):
                    for j in range(b):
                        k=random.randint(0,b-1)
                        roz=np.abs(self.restricition[i]-wiersze[i])
                        value=random.randint(0,roz)
                        if self.restricition[i] >= wiersze[i]:
                            if np.sum(new_bee,axis=0)[k]+value <= self.producents[k]:
                                new_bee[i, k] = new_bee[i, k] + value
                                kolumny = np.sum(new_bee, axis=0)
                                wiersze=np.sum(new_bee,axis=1)
                                break
                        if self.restricition[i]< wiersze[i]:
                            if new_bee[i,k]-value > 0:
                                new_bee[i, k] = new_bee[i, k] - value
                                kolumny = np.sum(new_bee, axis=0)
                                wiersze=np.sum(new_bee,axis=1)
                                break
                counter += 1
                kolumny = np.sum(new_bee, axis=0)
                wiersze=np.sum(new_bee,axis=1)
                if counter >= 10:
                    new_bee,correct_value,correct_eff = self.generate_matrix_production(new_bee, 1)
                    new_bee=np.squeeze(new_bee)
                    return new_bee
            return new_bee
        
        
    def generate_matrix_production(self, producents, n):

            matrixes = []
            vector = []
            vector_eff = []

            while len(matrixes) < n:
                matrix = np.zeros((self.number_customers, self.number_products), dtype=int)

                for j in range(self.number_customers):
                    value = self.restricition[j]
                    for i in range(self.number_products):
                        if i == self.number_products - 1:
                            a = self.producents[i] - np.sum(matrix[:j, i])
                            if value <= a:
                                matrix[j, i] = value
                            else:
                                break  # Przerwanie pętli w przypadku braku dopuszczalnej macierzy
                        else:
                            x = random.randint(0, min(value, self.producents[i] - np.sum(matrix[:j, i])))
                            matrix[j, i] = x
                            value -= x
                    else:
                        continue
                    break

                else:
                    # Ta część kodu zostanie wykonana, jeśli pętla zakończy się naturalnie (bez przerwania)
                    matrixes.append(matrix)
            for i in range(len(matrixes)):
                vector.append(self.function(matrixes[i]))
                vector_eff.append(self.function_efficency(vector[i]))

            return matrixes, vector, vector_eff    
        
        
    def generate_neighbours(self, matrix):
        n = len(matrix)
        neighbours_matrix = np.zeros(np.shape(matrix))
        fi = np.random.randint(0, 2, size=np.shape(matrix))
        neighbours_matrix = matrix + fi
        corrected_neighbour = self.correct_position(neighbours_matrix)
        return corrected_neighbour

    def employee_bees(self, matrixes, vector, eff):
            counter_list = [0 for i in range(len(matrixes))]
            list_neighbours = [0 for i in range(len(matrixes))]
            for i in range(len(matrixes)):
                neighbour_matrix = self.generate_neighbours(matrixes[i])
                new_value = self.function(neighbour_matrix)
                if new_value < vector[i]:
                    list_neighbours[i] = neighbour_matrix
                    vector[i] = new_value
                    eff[i] = self.function_efficency(new_value)
                else:
                    list_neighbours[i] = matrixes[i]
                    counter_list[i] += 1
            matrixes = list_neighbours
            return matrixes, vector, eff, counter_list
        
    def onlooker_bees(self, matrixes, vector, eff, counter_list, ob):
            counter = 0
            counter_help = 0
            matrixes1 = np.array(matrixes[0])
            if ob < len(eff):
                list_position = [np.zeros(np.shape(matrixes1)) for i in range(len(eff))]
                list_value = [0 for i in range(len(eff))]
                list_efficency = [0 for i in range(len(eff))]
            else:
                list_position = [np.zeros(np.shape(matrixes1)) for i in range(ob)]
                list_value = [0 for i in range(ob)]
                list_efficency = [0 for i in range(ob)]
            
            list_probability = [0 for i in range(len(eff))]
            for i in range(len(eff)):
                list_probability[i] = eff[i] / np.sum(eff)
            while counter < ob:
                for i in range(ob):
                    for j in range(len(matrixes)):
                        r = random.uniform(0, 1)
                        if r < list_probability[j]:
                            if np.array_equal(list_position[i], np.zeros(np.shape(matrixes1))):
                                list_position[i] = self.generate_neighbours(matrixes[j])
                                list_value[i] = self.function(list_position[i])
                                list_efficency[i] = self.function_efficency(list_value[i])
                                if vector[j] > list_value[i]:
                                    matrixes[j] = list_position[i]
                                    vector[j] = list_value[i]
                                    eff[j] = list_efficency[i]
                                    counter_list[j] = 0
                                counter += 1
                                break
            return matrixes, vector, eff, counter_list    

    def scout_bees(self, matrixes,vector, eff, counter_list, limit):
            matrixes1 = np.array(matrixes[0])
            list_position = [np.zeros(np.shape(matrixes1)) for i in range(len(matrixes))]
            for i in range(len(matrixes)):
                if counter_list[i] > limit:
                    matrix, vec, eff1 = self.generate_matrix_production(self.matrix_producents, 1)
                    matrix = np.squeeze(np.array(matrix))
                    matrixes[i] = matrix
                    vector[i] = vec
                    eff[i] = eff1
                    counter_list[i] = 0
                
            return matrixes, np.squeeze(vector), np.squeeze(eff), counter_list
        

    def ABC(self, limit, limit_iter):
            population, vec, vec_eff = self.generate_matrix_production(self.matrix_producents, self.number_bees)
            vector_best = []
            counter = 0
            while counter < limit_iter:
                print(f" Mati to szef zapamiętaj to po raz  {counter}")
                population, vec, vec_eff, counter_list= self.employee_bees(population, vec, vec_eff)
                population, vec, vec_eff, counter_list = self.onlooker_bees(population, vec, vec_eff, counter_list, self.number_observator)
                population, vec, vec_eff, counter_list = self.scout_bees(population, vec, vec_eff, counter_list, limit)
                vector_best.append(min(vec))
                counter += 1

            fitness_index = np.argmin(vec)
            fitness_value = vec[fitness_index]
            population_best = population[fitness_index]

            return population_best, vector_best, fitness_value

class WorkerThread(QThread):
    finished = Signal()

    def __init__(self, iteration, criterium, product, matrix_producents_app, matrix_clients_app, number_producents, number_clients, employee_bee, observator_bee, production, restriction, matrix_price_app, matrix_distance_app):
        super().__init__()
        self.iteration = iteration
        self.criterium = criterium
        self.product = product
        self.matrix_producents_app = matrix_producents_app
        self.matrix_clients_app = matrix_clients_app
        self.number_producents = number_producents
        self.number_clients = number_clients
        self.employee_bee = employee_bee
        self.observator_bee = observator_bee
        self.production = production
        self.restriction = restriction
        self.matrix_price_app = matrix_price_app
        self.matrix_distance_app = matrix_distance_app
        self.population_best = None
        self.vector_best = None
        self.fitness_value = None
        self.iteration_list = []

    def run(self):
        bee = Bee(
            self.product, self.matrix_producents_app, self.matrix_clients_app,
            self.number_producents, self.number_clients,
            self.employee_bee, self.observator_bee,
            self.production, self.restriction,
            self.matrix_price_app, self.matrix_distance_app
        )
        self.opulation_best, self.vector_best, self.fitness_value = bee.ABC(self.criterium, self.iteration)
        self.iteration_list = [i+1 for i in range(self.iteration)]
        self.finished.emit()
        print(population_best)
        print(vector_best)
        print(fitness_value)


class Canvas(FigureCanvas):
    def __init__(self, vector, iteration):
        self.vector = vector
        self.iteration = iteration
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        


        self.ax.plot(self.iteration, self.vector)
        self.ax.set(xlabel='Liczba iteracji', ylabel='Wartosc funkcji celu', title='Wykres funkcji celu')
        self.ax.grid()


class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.menu_width = 200
        self.animation_duration = 200
        self.setStyleSheet('background-color:#211B1B')

        self.Icon = QIcon('icons8-bee-100.png')
        self.setWindowIcon(self.Icon)
        self.setWindowTitle("Algorytm ABC")


        self.central_widget = QWidget(self)
        self.main_page = QWidget(self)
        
        self.demand_page = QWidget(self)
        self.parameters_page = QWidget(self)
        self.price_page = QWidget(self)
        self.distance_page = QWidget(self)



        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setStyleSheet("background-color: blue;")
        




        # self.setStyleSheet("""
        # QWidget {
        #     background-color: blue;  /* Kolor tła ramki okna */
        #     border: 2px solid black;  /* Grubość obramowania */ fajne ramki
        #     border-radius: 5px;  /* Zakrzywienie narożników */
        # }
        #  """)
        self.setup()
        
    def setup(self):
        
        self.setGeometry(100, 100, 800, 600)

        #ustawienie layoutów####
        self.layoutV1 = QVBoxLayout()
        self.layoutH1 = QHBoxLayout()
        self.layoutH2 = QHBoxLayout()
        self.layoutH3 = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.layoutV1.addLayout(self.layoutH1)
        self.layoutV1.addLayout(self.layoutH2)
        self.layoutV1.addLayout(self.layoutH3)
        self.main_layout.addLayout(self.layoutV1)
        self.setLayout(self.main_layout)

        self.central_widget.installEventFilter(self)
        
        self.stack_main_widget = QStackedWidget(self.central_widget)
        self.stack_main_widget.addWidget(self.main_page)
        
        self.stack_main_widget.addWidget(self.parameters_page)
        self.stack_main_widget.addWidget(self.distance_page)
        self.stack_main_widget.addWidget(self.price_page)
        self.stack_main_widget.addWidget(self.demand_page)
        self.main_layout.addWidget(self.stack_main_widget)


        ##########

        #ustawienie przycisku menu######
        self.menu_btn = QPushButton(self)
        self.menu_pixmap = QPixmap('icons8-menu-64.png')
        self.menu_btn.setIcon(QIcon(self.menu_pixmap))
        self.menu_btn.setIconSize(self.menu_btn.size())
        self.menu_btn.setFlat(True)
        self.menu_btn.clicked.connect(self.slidemenu)
        self.menu_btn.raise_()
        self.layoutH1.addWidget(self.menu_btn, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layoutH1.addStretch(20)

        
        ##########

        self.import_btn = QPushButton(self)
        self.import_pixmap = QPixmap('icons8-import-64.png')
        self.import_btn.setIcon(QIcon(self.import_pixmap))
        self.import_btn.setIconSize(self.import_btn.size())
        self.import_btn.setFlat(True)
        self.import_btn.raise_()
        self.layoutH1.addWidget(self.import_btn, alignment=Qt.AlignTop | Qt.AlignRight)
        self.import_btn.clicked.connect(self.Import)
        


        #ustawienie ikonki na srodku#######
        self.bee_label = QLabel(self)
        self.icon_bee = QPixmap('bee_noc.png')
        self.icon_bee_scaled = self.icon_bee.scaled(self.icon_bee.width()//2, self.icon_bee.height()//2, Qt.KeepAspectRatio)
        self.bee_label.setPixmap(self.icon_bee_scaled)
        self.layoutH2.addWidget(self.bee_label, alignment = Qt.AlignCenter)
        ############

        #Slide menu##########





        self.menu_frame = QFrame(self)
        self.menu_frame.setGeometry(QRect(-self.menu_width, 100, self.menu_width, self.height()))
        self.menu_frame.setStyleSheet("background-color:#151318")
        

        self.menu_layout = QVBoxLayout(self.menu_frame)

        
            #przyciski w slidemenu

        self.parameters = QPushButton("Parametery", self.menu_frame)
        self.parameters_label = QLabel(self)
        self.parameters_label.setPixmap(QPixmap('icons8-queen-bee-48.png'))
        self.parameters.clicked.connect(self.parameters_ui)

        self.diagram = QPushButton("Wykres funkcji celu", self.menu_frame)
        self.diagram_label = QLabel(self)
        self.diagram_label.setPixmap(QPixmap('icons8-coordinate-system-48.png'))
        self.diagram.clicked.connect(self.diagram_ui)

        self.demand = QPushButton("Producenci i odbiorcy", self.menu_frame)
        self.demand_label = QLabel(self)
        self.demand_label.setPixmap(QPixmap('icons8-customers-40.png'))
        self.demand.clicked.connect(self.demand_ui)

        self.price = QPushButton("Ceny produktow", self.menu_frame)
        self.price_label = QLabel(self)
        self.price_label.setPixmap(QPixmap('icons8-price-48.png'))
        self.price.clicked.connect(self.price_ui)

        self.distance = QPushButton("Ustalenie dystansow", self.menu_frame)
        self.distance_label = QLabel(self)
        self.distance_label.setPixmap(QPixmap('icons8-distance-48.png'))
        self.distance.clicked.connect(self.distance_ui)

        self.main_prev = QPushButton("Menu główne", self.menu_frame)
        self.main_prev_label = QLabel(self)
        self.main_prev_label.setPixmap(QPixmap('icons8-home-page-40.png'))
        self.main_prev.clicked.connect(self.main_prev_ui)
    
        self.parameters.setStyleSheet('background-color:darkviolet; color: white')
        self.diagram.setStyleSheet('background-color:darkviolet; color: white')
        self.distance.setStyleSheet('background-color:darkviolet; color: white')
        self.demand.setStyleSheet('background-color:darkviolet; color: white')
        self.price.setStyleSheet('background-color:darkviolet; color: white')
        self.main_prev.setStyleSheet('background-color:darkviolet; color: white')
        
        
        self.layout_menuH1 = QHBoxLayout()
        self.layout_menuH2 = QHBoxLayout()
        self.layout_menuH3 = QHBoxLayout()
        self.layout_menuH4 = QHBoxLayout()
        self.layout_menuH5 = QHBoxLayout()
        self.layout_menuH6 = QHBoxLayout()


        self.layout_menuH1.addWidget(self.parameters_label)
        self.layout_menuH1.addWidget(self.parameters)
        self.layout_menuH1.addStretch(20)
        
        self.layout_menuH2.addWidget(self.diagram_label)
        self.layout_menuH2.addWidget(self.diagram)
        self.layout_menuH2.addStretch(20)
        
        self.layout_menuH3.addWidget(self.demand_label)
        self.layout_menuH3.addWidget(self.demand)
        self.layout_menuH3.addStretch(20)

        self.layout_menuH4.addWidget(self.price_label)
        self.layout_menuH4.addWidget(self.price)
        self.layout_menuH4.addStretch(20)

        self.layout_menuH5.addWidget(self.distance_label)
        self.layout_menuH5.addWidget(self.distance)
        self.layout_menuH5.addStretch(20)

        self.layout_menuH6.addWidget(self.main_prev_label)
        self.layout_menuH6.addWidget(self.main_prev)
        self.layout_menuH6.addStretch(20)
        

        self.menu_layout.addLayout(self.layout_menuH1)
        self.menu_layout.addLayout(self.layout_menuH2)
        self.menu_layout.addLayout(self.layout_menuH3)
        self.menu_layout.addLayout(self.layout_menuH4)
        self.menu_layout.addLayout(self.layout_menuH5)
        self.menu_layout.addLayout(self.layout_menuH6)
        

#Ustawienie stron###########################################################
        self.parameters_page = QWidget(self)
        self.parameters_frame = QFrame(self.parameters_page)
        self.parameters_layout = QVBoxLayout(self.parameters_page)
        self.parameters_frame.setStyleSheet('background-color: #211B1B')
        self.parameters_layout.addWidget(self.parameters_frame)
        self.stack_main_widget.addWidget(self.parameters_page)
        self.counter_parameters = 1
        
    
        self.demand_page = QWidget(self)
        self.demand_frame = QFrame(self.demand_page)
        self.demand_layout = QVBoxLayout(self.demand_page)
        self.demand_frame.setStyleSheet('background-color: #211B1B')
        self.demand_layout.addWidget(self.demand_frame)
        self.stack_main_widget.addWidget(self.demand_page)
        self.counter_demand = 1

        self.distance_page = QWidget(self)
        self.distance_frame = QFrame(self.distance_page)
        self.distance_layout = QVBoxLayout(self.distance_page)
        self.distance_frame.setStyleSheet('background-color: #211B1B')
        self.distance_layout.addWidget(self.distance_frame)
        self.stack_main_widget.addWidget(self.distance_page)
        self.counter_distance = 1

        self.price_page = QWidget(self)
        self.price_frame = QFrame(self.price_page)
        self.price_layout = QVBoxLayout(self.price_page)
        self.price_frame.setStyleSheet('background-color: #211B1B')
        self.price_layout.addWidget(self.price_frame)
        self.stack_main_widget.addWidget(self.price_page)
        self.counter_price = 1


        self.diagram_page = QWidget(self)
        self.diagram_frame = QFrame(self.diagram_page)
        self.diagram_layout = QVBoxLayout(self.diagram_page)
        self.diagram_frame.setStyleSheet('background-color: #211B1B')
        self.diagram_layout.addWidget(self.diagram_frame)
        self.counter_diagram = 1
        self.stack_main_widget.addWidget(self.diagram_page)
        self.menu_btn.raise_()
        

        

            ##########


######### parameters page #######
        self.parameters_layoutH = QHBoxLayout()
        self.parameters_layoutH1 = QHBoxLayout()
        self.parameters_layoutH2 = QHBoxLayout()
        self.parameters_layoutH3 = QHBoxLayout()
        self.parameters_layoutH4 = QHBoxLayout()
        self.parameters_frame_layout = QVBoxLayout(self.parameters_frame)



        

        self.validator = QIntValidator(self)


        self.bee_employee = QLabel("Wpisz liczbe pszczol pracujacych", self.parameters_page)
        self.bee_employee.setStyleSheet('color:white')
        self.parameters_layoutH1.addWidget(self.bee_employee, alignment  = Qt.AlignTop)
        self.set_employee_bee = QLineEdit(self.parameters_page)
        self.set_employee_bee.setStyleSheet('background-color: white')
        self.set_employee_bee.setValidator(self.validator)
        self.parameters_layoutH1.addWidget(self.set_employee_bee, alignment=Qt.AlignTop)

        self.observator_employee = QLabel("Wpisz liczbe obserwatorow", self.parameters_page)
        self.observator_employee.setStyleSheet('color:white')
        self.parameters_layoutH2.addWidget(self.observator_employee, alignment  = Qt.AlignTop)
        self.set_observator_bee = QLineEdit(self.parameters_page)
        self.set_observator_bee.setStyleSheet('background-color: white')
        self.set_observator_bee.setValidator(self.validator)
        self.parameters_layoutH2.addWidget(self.set_observator_bee, alignment=Qt.AlignTop)

        self.criterium = QLabel("Wpisz ilosc iteracji przed porzuceniem", self.parameters_page)
        self.criterium.setStyleSheet('color:white')
        self.parameters_layoutH3.addWidget(self.criterium, alignment  = Qt.AlignTop)
        self.set_criterium = QLineEdit(self.parameters_page)
        self.set_criterium.setStyleSheet('background-color: white')
        self.set_criterium.setValidator(self.validator)
        self.parameters_layoutH3.addWidget(self.set_criterium, alignment=Qt.AlignTop)

        self.iteration = QLabel("Wpisz ilosc iteracji", self.parameters_page)
        self.iteration.setStyleSheet('color:white')
        self.parameters_layoutH4.addWidget(self.iteration, alignment  = Qt.AlignTop)
        self.set_iteration = QLineEdit(self.parameters_page)
        self.set_iteration.setStyleSheet('background-color: white')
        self.set_iteration.setValidator(self.validator)
        self.parameters_layoutH4.addWidget(self.set_iteration, alignment=Qt.AlignTop)
        

        self.parameters_frame_layout.addLayout(self.parameters_layoutH)
        self.parameters_frame_layout.addLayout(self.parameters_layoutH1)
        self.parameters_frame_layout.addLayout(self.parameters_layoutH2)
        self.parameters_frame_layout.addLayout(self.parameters_layoutH3)
        self.parameters_frame_layout.addLayout(self.parameters_layoutH4)
        self.parameters_frame_layout.addStretch(100)
        self.parameters_page.setLayout(self.parameters_frame_layout)
        
###############################
######diagram_page######

        self.diagram_frame_layout = QVBoxLayout(self.diagram_frame)
        self.diagram_layoutH1 = QHBoxLayout()
        self.diagram_layoutH2 = QHBoxLayout()
        self.diagram_layoutH3 = QHBoxLayout()
        self.diagram_layoutH4 = QHBoxLayout()
        self.diagram_layoutH5 = QHBoxLayout()
        self.diagram_layoutH6 = QHBoxLayout()
        self.diagram_layoutH7 = QHBoxLayout()
        self.diagram_button_generate = QPushButton("Generuj rozwiazanie", self.diagram_frame)
        self.diagram_button_generate.setStyleSheet('background-color: white')
        self.diagram_frame_layout.addWidget(self.diagram_button_generate, alignment=Qt.AlignTop)
        self.diagram_button_generate.clicked.connect(self.Generate_ABC)
        


        self.diagram_Employee = QLabel("Wpisana liczba pszczół pracowniczych", self.diagram_frame)
        self.diagram_Employee.setStyleSheet('color: white')
        self.diagram_layoutH1.addWidget(self.diagram_Employee, alignment=Qt.AlignRight)
        self.diagram_text_E = QLabel(self.diagram_frame)
        self.diagram_layoutH1.addWidget(self.diagram_text_E, alignment=Qt.AlignRight)
        self.set_employee_bee.textChanged.connect(self.update_text_E)
        self.diagram_text_E.setStyleSheet('color:white')

        self.diagram_Observator = QLabel("Wpisana liczba pszczół obserwatorów", self.diagram_frame)
        self.diagram_Observator.setStyleSheet('color: white')
        self.diagram_layoutH2.addWidget(self.diagram_Observator, alignment=Qt.AlignRight)
        self.diagram_text_O = QLabel(self.diagram_frame)
        self.diagram_layoutH2.addWidget(self.diagram_text_O, alignment=Qt.AlignRight)
        self.set_observator_bee.textChanged.connect(self.update_text_O)
        self.diagram_text_O.setStyleSheet('color:white')

        self.diagram_iteration = QLabel("Wpisana liczba iteracji", self.diagram_frame)
        self.diagram_iteration.setStyleSheet('color: white')
        self.diagram_layoutH3.addWidget(self.diagram_iteration, alignment=Qt.AlignRight)
        self.diagram_text_I = QLabel(self.diagram_frame)
        self.diagram_layoutH3.addWidget(self.diagram_text_I, alignment=Qt.AlignRight)
        self.set_iteration.textChanged.connect(self.update_text_I)
        self.diagram_text_I.setStyleSheet('color:white')

        self.diagram_criterium = QLabel("Wpisane kryterium porzucenia", self.diagram_frame)
        self.diagram_criterium.setStyleSheet('color: white')
        self.diagram_layoutH4.addWidget(self.diagram_criterium, alignment=Qt.AlignRight)
        self.diagram_text_C = QLabel(self.diagram_frame)
        self.diagram_layoutH4.addWidget(self.diagram_text_C, alignment=Qt.AlignRight)
        self.set_criterium.textChanged.connect(self.update_text_C)
        self.diagram_text_C.setStyleSheet('color:white')

        
        self.checkboxes = []
        


        self.diagram_check = QLabel("Zaznacz produkt do optymalizacji", self.diagram_frame)
        self.diagram_check.setStyleSheet('color: white')
        self.diagram_layoutH5.addWidget(self.diagram_check)
        self.diagram_layoutH1.addStretch(20)
        self.diagram_layoutH2.addStretch(20)
        self.diagram_layoutH3.addStretch(20)
        self.diagram_layoutH4.addStretch(20)

        self.diagram_production = QLabel("Produkcja wybranego produktu", self.diagram_page)
        self.diagram_restriction = QLabel("Zapotrzebowanie na dany produkt", self.diagram_page)
        self.diagram_production.setStyleSheet('color: white')
        self.diagram_restriction.setStyleSheet('color: white')
        self.diagram_layoutH6.addWidget(self.diagram_production)
        self.diagram_layoutH7.addWidget(self.diagram_restriction)

        

        

        self.diagram_frame_layout.addLayout(self.diagram_layoutH1)
        self.diagram_frame_layout.addLayout(self.diagram_layoutH2)
        self.diagram_frame_layout.addLayout(self.diagram_layoutH3)
        self.diagram_frame_layout.addLayout(self.diagram_layoutH4)
        self.diagram_frame_layout.addLayout(self.diagram_layoutH5)
        self.diagram_frame_layout.addLayout(self.diagram_layoutH6)
        self.diagram_frame_layout.addLayout(self.diagram_layoutH7)
        self.diagram_page.setLayout(self.diagram_frame_layout)
        

        ############

        ####prodyucneci page
        self.demand_frame_layout = QVBoxLayout(self.demand_frame)
        self.demand_layoutH1 = QHBoxLayout()
        self.demand_layoutH2 = QHBoxLayout()
        self.demand_layoutH3 = QHBoxLayout()
        self.demand_layoutH4 = QHBoxLayout()
        self.demand_layoutH5 = QHBoxLayout()
        self.demand_layoutH6 = QHBoxLayout()
        self.demand_layoutH7 = QHBoxLayout()
        self.demand_layoutH8 = QHBoxLayout()
        self.demand_grid_layout = QGridLayout(self.demand_page)
        self.demand_grid_layout2 = QGridLayout(self.demand_page)
        self.demand_text = QLabel("Uzupełnij macierz zaoptrzebowania klientów", self.demand_frame)
        self.demand_text.setStyleSheet('color:white')
        self.demand_layoutH1.addWidget(self.demand_text)
        self.demand_production = QLabel("Uzupełnij macierz produkcji", self.demand_frame)
        self.demand_production.setStyleSheet("color: white")
        self.demand_layoutH4.addWidget(self.demand_production)
        self.demand_producents = QLabel("Wpisz liczbe producentów", self.demand_frame)
        self.demand_clients = QLabel("Wpisz liczbę klientów", self.demand_frame)
        self.demand_producents_edit = QLineEdit(self.demand_frame)
        self.demand_clients_edit = QLineEdit(self.demand_frame)
        self.demand_producents.setStyleSheet('color:white')
        self.demand_clients.setStyleSheet('color: white')
        self.demand_producents_edit.setStyleSheet('background-color: white')
        self.demand_clients_edit.setStyleSheet('background-color: white')
        self.demand_layoutH2.addWidget(self.demand_producents)
        self.demand_layoutH2.addWidget(self.demand_producents_edit)
        self.demand_layoutH3.addWidget(self.demand_clients)
        self.demand_layoutH3.addWidget(self.demand_clients_edit)

        self.set_text = QLabel("Wpisz ilosc produktow", self.demand_page)
        self.set_text.setStyleSheet('color: white')
        self.demand_layoutH6.addWidget(self.set_text, alignment=Qt.AlignTop)


        
        self.set_product = QLineEdit(self.demand_page)
        self.set_product.setStyleSheet('background-color: white')
        self.validator = QIntValidator(self)
        self.set_product.setValidator(self.validator)
        self.demand_layoutH6.addWidget(self.set_product, alignment=Qt.AlignTop)
        self.set_product.textChanged.connect(self.upgrade_product)
        



        self.demand_producents_edit.textChanged.connect(self.update_matrix)
        self.demand_clients_edit.textChanged.connect(self.update_matrix)

    


        self.demand_frame_layout.addLayout(self.demand_layoutH6)
        self.demand_frame_layout.addLayout(self.demand_layoutH3)
        self.demand_frame_layout.addLayout(self.demand_layoutH2)
        self.demand_frame_layout.addLayout(self.demand_layoutH5)
        self.demand_frame_layout.addLayout(self.demand_layoutH4)
        self.demand_frame_layout.addLayout(self.demand_grid_layout)
        self.demand_frame_layout.addLayout(self.demand_layoutH1)
        self.demand_frame_layout.addLayout(self.demand_grid_layout2)
        self.demand_frame_layout.addStretch(100)
        self.demand_page.setLayout(self.demand_frame_layout)

        #######
        #####price page###
        self.price_frame_layout = QVBoxLayout(self.price_frame)
        self.price_layoutH1 = QHBoxLayout()
        self.price_layoutH2 = QHBoxLayout()
        self.price_layoutH3 = QHBoxLayout()
        self.price_layoutH4 = QHBoxLayout()
        self.price_grid_layout = QGridLayout(self.price_frame)



        self.price_text = QLabel("Uzupełnij macierz kosztów", self.price_frame)
        self.price_text.setStyleSheet('color: white')
        self.price_layoutH2.addWidget(self.price_text)

        self.price_frame_layout.addLayout(self.price_layoutH1)
        self.price_frame_layout.addLayout(self.price_layoutH2)
        self.price_frame_layout.addLayout(self.price_layoutH3)
        self.price_frame_layout.addLayout(self.price_layoutH4)
        self.price_frame_layout.addLayout(self.price_grid_layout)
        self.price_frame_layout.addStretch(100)
        self.price_page.setLayout(self.price_frame_layout)

#######
        self.lineedit_demand_producents = []
        self.lineedit_demand_clients = []
        self.lineedit_price = []
        self.lineedit_distance = []

##### distance page

        self.distance_frame_layout = QVBoxLayout(self.distance_frame)
        self.distance_layoutH1 = QHBoxLayout()
        self.distance_layoutH2 = QHBoxLayout()
        self.distance_layoutH3 = QHBoxLayout()
        self.distance_layoutH4 = QHBoxLayout()
        self.distance_grid_layout = QGridLayout(self.distance_frame)


        self.distance_text = QLabel("Uzupełnij macierz dystansów", self.distance_frame)
        self.distance_text.setStyleSheet('color: white')
        self.distance_layoutH2.addWidget(self.distance_text)

        self.distance_frame_layout.addLayout(self.distance_layoutH1)
        self.distance_frame_layout.addLayout(self.distance_layoutH2)
        self.distance_frame_layout.addLayout(self.distance_layoutH3)
        self.distance_frame_layout.addLayout(self.distance_layoutH4)
        self.distance_frame_layout.addLayout(self.distance_grid_layout)
        self.distance_frame_layout.addStretch(100)
        self.distance_page.setLayout(self.distance_frame_layout)




        self.menu_animation = QPropertyAnimation(self.menu_frame, b"geometry")
        self.menu_animation.setDuration(self.animation_duration)
        self.main_layout.addWidget(self.stack_main_widget)
        
            
        self.show()
    def get_restriction(self, customers, producents, k):
        help_customers = np.transpose(customers)
        help_producents = np.transpose(producents)
        producents = help_producents[k - 1]
        restricition = help_customers[k - 1]
        return producents, restricition
    def Generate_ABC(self):
        k = 0
        product = 0
        for check in self.checkboxes:
            self.list_check[k] = check.isChecked()
            k+=1
        for check in self.list_check:
            if check == True:
                product = self.list_check.index(check)
        product += 1
        k = 0
        production, restriction = self.get_restriction(self.matrix_clients_app, self.matrix_producents_app, product)
        number_producents = int(self.demand_producents_edit.text())
        number_clients = int(self.demand_clients_edit.text())
        employee_bee = int(self.set_employee_bee.text())
        observator_bee = int(self.set_observator_bee.text())
        criterium = int(self.set_criterium.text())
        iteration = int(self.set_iteration.text())
        print(product)
       # print(product, self.matrix_producents_app, self.matrix_clients_app, number_producents, number_clients, employee_bee, observator_bee, production, restriction, self.matrix_price_app, self.matrix_distance_app)
        self.thread = WorkerThread(iteration, criterium, product, self.matrix_producents_app, self.matrix_clients_app, number_producents, number_clients, employee_bee, observator_bee, production, restriction, self.matrix_price_app, self.matrix_distance_app)
        self.thread.finished.connect(self.thread_finished)
        self.thread.start()
    def thread_finished(self):
        print("Thread finished.")
        print(self.thread.vector_best, self.thread.iteration_list)
        self.diagram = Canvas(self.thread.vector_best, self.thread.iteration_list)
        self.diagram.show()

    def slidemenu(self):
        if self.menu_animation.state() == QPropertyAnimation.Running:
            self.menu_animation.stop()

        if self.menu_frame.geometry().x() == -self.menu_width:
            self.menu_animation.setStartValue(QRect(0, 0, 0, self.height()))
            self.menu_animation.setEndValue(QRect(0, 0, self.menu_width, self.height()))
        else:
            self.menu_animation.setStartValue(QRect(0, 0, self.menu_width, self.height()))
            self.menu_animation.setEndValue(QRect(-self.menu_width, 0, 0, self.height()))
        self.menu_btn.raise_()
        self.menu_animation.start()

    def parameters_ui(self):
        if self.stack_main_widget.currentWidget != self.parameters_page:
            self.bee_label.hide()
            self.stack_main_widget.setCurrentWidget(self.parameters_page)
        else:
            self.bee_label.show()
            self.stack_main_widget.setCurrentWidget(self.main_page)
        self.counter_parameters += 1
        self.number_products = self.set_employee_bee.text()
        print(self.number_products)
    def demand_ui(self):
        if self.stack_main_widget.currentWidget != self.demand_page:
            self.bee_label.hide()
            self.stack_main_widget.setCurrentWidget(self.demand_page)
        else:
            self.bee_label.show()
            self.stack_main_widget.setCurrentWidget(self.main_page)
        self.counter_demand += 1
        print("clicked!")
    def price_ui(self):
        if self.stack_main_widget.currentWidget != self.price_page:
            self.bee_label.hide()
            self.stack_main_widget.setCurrentWidget(self.price_page)
        else:
            self.bee_label.show()
            self.stack_main_widget.setCurrentWidget(self.main_page)
        self.counter_price += 1
        print("clicked!")
    def distance_ui(self):
        if self.stack_main_widget.currentWidget != self.distance_page:
            self.bee_label.hide()
            self.stack_main_widget.setCurrentWidget(self.distance_page)
        else:
            self.bee_label.show()
            self.stack_main_widget.setCurrentWidget(self.main_page)
        self.counter_distance += 1
        print("clicked!")
    def diagram_ui(self):
        # self.diagram_class = Canvas()
        # self.diagram_class.show()
        if self.stack_main_widget.currentWidget != self.diagram_page:
            self.bee_label.hide()
            self.stack_main_widget.setCurrentWidget(self.diagram_page)
        else:
            self.bee_label.show()
            self.stack_main_widget.setCurrentWidget(self.main_page)
        self.counter_diagram += 1
    def main_prev_ui(self):
        if self.stack_main_widget.currentWidget != self.main_page:
            self.bee_label.show()
            self.stack_main_widget.setCurrentWidget(self.main_page)
        
        print("clicked!")
    def update_text_E(self, text):

        self.diagram_text_E.setText(text)
    def update_text_O(self, text):
        self.diagram_text_O.setText(text)
    def update_text_I(self, text):
        self.diagram_text_I.setText(text)
    def update_text_C(self, text):
        self.diagram_text_C.setText(text)
    def upgrade_product(self, text):
        self.number_check = int(text)
        self.button_group= QButtonGroup()

        for checkbox in self.checkboxes:
            checkbox.setParent(None)
            checkbox.deleteLater()
        self.list_check = [0 for i in range(self.number_check)]
        self.checkboxes = [QCheckBox(f'Produkt{i+1}') for i in range(self.number_check)]
        k = 0
        for checkbox in self.checkboxes:
            checkbox.setStyleSheet('color: white')
            self.button_group.addButton(checkbox)
            self.button_group.setExclusive(True)
            self.list_check[k]= checkbox.isChecked()
            self.diagram_layoutH5.addWidget(checkbox)
            k +=1
        k = 0
        print(self.list_check)

        # for lineedit in self.lineedit:
        #     lineedit.setParent(None)
        #     lineedit.deleteLater()
        # self.lineedit = [QLineEdit(self.demand_page) for i in range(self.number_check)]
        # self.demandH = [QHBoxLayout() for i in range(self.number_check)]
        # for lineedit in self.lineedit:
        #     lineedit.setStyleSheet('background-color: white')
        #     self.demandH[lineedit].addWidget(lineedit)
        #     self.demand_frame_layout.addLayout(self.demandH[lineedit])

    def update_matrix(self, flag = 0, matrix_producents = 0, matrix_clients  = 0, matrix_price  = 0, matrix_distance  = 0):
        self.lineedit_demand_producents = []
        self.lineedit_demand_clients = []
        self.lineedit_price = []
        self.lineedit_distance = []
        for i in reversed(range(self.demand_grid_layout.count())):
            item = self.demand_grid_layout.itemAt(i)
            widget = item.widget()
            self.demand_grid_layout.removeItem(item)
            widget.setParent(None)
        for i in reversed(range(self.demand_grid_layout2.count())):
            item = self.demand_grid_layout2.itemAt(i)
            widget = item.widget()
            self.demand_grid_layout2.removeItem(item)
            widget.setParent(None)
        for i in reversed(range(self.price_grid_layout.count())):
            item = self.price_grid_layout.itemAt(i)
            widget = item.widget()
            self.price_grid_layout.removeItem(item)
            widget.setParent(None)
        for i in reversed(range(self.distance_grid_layout.count())):
            item = self.distance_grid_layout.itemAt(i)
            widget = item.widget()
            self.distance_grid_layout.removeItem(item)
            widget.setParent(None)

        # Pobierz wartości x i y
        z_text = self.set_product.text()
        x_text = self.demand_producents_edit.text()
        y_text = self.demand_clients_edit.text()

        if not x_text or not y_text or not z_text:
            return

        z = int(z_text)
        x = int(x_text)
        y = int(y_text)
        
        for i in range(x):
            for j in range(z):
                lineedit = QLineEdit(self.demand_frame)
                validator = QIntValidator()
                lineedit.setValidator(validator)
                lineedit.setStyleSheet('background-color: white')
                if flag == 1:
                    lineedit.setText(str(matrix_producents[i][j]))
                else:
                    lineedit.setText('0')
                self.lineedit_demand_producents.append(lineedit)
                self.demand_grid_layout.addWidget(lineedit, i, j)
        
        for i in range(y):
            for j in range(z):
                lineedit = QLineEdit(self.demand_frame)
                validator = QIntValidator()
                lineedit.setValidator(validator)
                lineedit.setStyleSheet('background-color: white')
                if flag == 1:
                    lineedit.setText(str(matrix_clients[i][j]))
                else:
                    lineedit.setText('0')
                self.lineedit_demand_clients.append(lineedit)
                self.demand_grid_layout2.addWidget(lineedit, i, j)
        for i in range(x):
            for j in range(z):
                lineedit = QLineEdit(self.price_frame)
                validator = QIntValidator()
                lineedit.setValidator(validator)
                lineedit.setStyleSheet('background-color: white')
                if flag == 1:
                    lineedit.setText(str(matrix_clients[i][j]))
                else:
                    lineedit.setText('0')
                self.lineedit_price.append(lineedit)
                self.price_grid_layout.addWidget(lineedit, i, j)
        for i in range(y):
            for j in range(x):
                lineedit = QLineEdit(self.distance_frame)
                validator = QIntValidator()
                lineedit.setValidator(validator)
                lineedit.setStyleSheet('background-color: white')
                if flag == 1:
                    lineedit.setText(str(matrix_distance[i][j]))
                else:
                    lineedit.setText('0')
                self.lineedit_distance.append(lineedit)
                self.distance_grid_layout.addWidget(lineedit, i, j)
 
        for edit in self.lineedit_demand_producents:
            edit.textChanged.connect(self.update_edit)
        for edit in self.lineedit_demand_clients:
            edit.textChanged.connect(self.update_edit)
        for edit in self.lineedit_price:
            edit.textChanged.connect(self.update_edit)
        for edit in self.lineedit_distance:
            edit.textChanged.connect(self.update_edit)
    def Import(self):
        try:
            self.response = QFileDialog.getOpenFileName(parent=self, caption='Wybierz plik')
        except FileNotFoundError:
            return
        if (self.response):
            self.flag = 1
        self.object = pd.read_csv(self.response[0])
        self.object_producents = self.object["producenci"]
        self.object_producents = self.object["producenci"].to_numpy()
        self.object_producents_size = len(self.object_producents)
        self.len_producents = len(self.object_producents)
        self.len_sqrt = int(np.sqrt(self.len_producents))
        self.rows_producents = int(self.len_producents / self.len_sqrt)
        self.cols_producents = int(self.len_sqrt)
        self.matrix_producents_app = self.object_producents.reshape((self.rows_producents, self.cols_producents))

        self.set_product.setText(str(len(self.matrix_producents_app[0])))
        self.tr = np.transpose(self.matrix_producents_app)
        self.demand_producents_edit.setText(str(len(self.tr[0])))

        self.object_clients = self.object["klienci"]
        self.object_clients = self.object["klienci"].to_numpy()
        self.object_clients_size = len(self.object_clients)
        self.len_clients = len(self.object_clients)
        self.len_sqrt = int(np.sqrt(self.len_clients))
        self.rows_clients = int(self.len_clients / self.len_sqrt)
        self.cols_clients = int(self.len_sqrt)
        self.matrix_clients_app = self.object_clients.reshape((self.rows_clients, self.cols_clients))

        self.tr = np.transpose(self.matrix_clients_app)
        self.demand_clients_edit.setText(str(len(self.tr[0])))

        self.object_price = self.object["cena"]
        self.object_price = self.object["cena"].to_numpy()
        self.object_price_size = len(self.object_price)
        self.len_price = len(self.object_price)
        self.len_sqrt = int(np.sqrt(self.len_price))
        self.rows_price = int(self.len_price / self.len_sqrt)
        self.cols_price = int(self.len_sqrt)
        self.matrix_price_app = self.object_price.reshape((self.rows_price, self.cols_price))

        self.object_distance = self.object["dystans"]
        self.object_distance = self.object["dystans"].to_numpy()
        self.object_distance_size = len(self.object_distance)
        self.len_distance = len(self.object_distance)
        self.len_sqrt = int(np.sqrt(self.len_distance))
        self.rows_distance = int(self.len_distance / self.len_sqrt)
        self.cols_distance = int(self.len_sqrt)
        self.matrix_distance_app = self.object_distance.reshape((self.rows_distance, self.cols_distance))

        self.update_matrix(self.flag, self.matrix_producents_app, self.matrix_clients_app, self.matrix_price_app, self.matrix_distance_app)
        
        
    


    def eventFilter(self, obj, event):
        if obj == self.central_widget and event.type() == QEvent.MouseButtonPress:
            if self.menu_frame.isVisible() and self.menu_frame.geometry().contains(event.globalPos()):
                self.slidemenu()
                return True  # Dodaj to, aby zatrzymać dalsze przetwarzanie zdarzenia
        return super().eventFilter(obj, event)

    def update_edit(self):
        z_text = self.set_product.text()
        x_text = self.demand_producents_edit.text()
        y_text = self.demand_clients_edit.text()

        if not x_text or not y_text or not z_text:
            return

        z = int(z_text)
        x = int(x_text)
        y = int(y_text)
        self.matrix_demand_producents = [[0]*self.number_check for i in range(self.number_check)]
        self.matrix_demand_clients = [[0]*self.number_check for i in range(self.number_check)]
        self.matrix_price_app = [[0]*self.number_check for i in range(self.number_check)]
        self.matrix_distance_app = [[0] * self.number_check for i in range(self.number_check)]
        k = 0
        for i in range(x):
            for j in range(z):
                self.matrix_demand_producents[i][j] = self.lineedit_demand_producents[k].text()
                k += 1
        k = 0
        for i in range(x):
            for j in range(z):
                self.matrix_demand_clients[i][j] = self.lineedit_demand_clients[k].text()
                k += 1
        k = 0
        for i in range(x):
            for j in range(z):
                self.matrix_price_app[i][j] = self.lineedit_price[k].text()
                k += 1
        k = 0
        for i in range(x):
            for j in range(z):
                self.matrix_distance_app[i][j] = self.lineedit_distance[k].text()
                k += 1
        
                
        for row in self.matrix_demand_clients:
            print(row)
            
    
        

app = QApplication([])

login = Application()
app.exec()