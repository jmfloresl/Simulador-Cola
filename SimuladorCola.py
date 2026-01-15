import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import simpy
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

#Inicia el programa
class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Colas con Prioridad")
        self.root.geometry("1000x800")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.create_widgets()
        
    #Crea la ventana de inicio con sus caracteristicas
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Bienvenido al Simulador de Colas con Prioridad", font=("Helvetica", 26)).pack(pady=20)
        #configuracion para el estilo de diseño de los botones
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 14))
            
        ttk.Button(frame, text="Entrar al Libre",  command=self.open_simulator).pack(fill="x", pady=10 )
        ttk.Button(frame, text="Entrar al Modelo",  command=self.open_simulator2).pack(fill="x", pady=10 )
        ttk.Button(frame, text="Instrucciones",command=self.show_documentation).pack(fill="x", pady=10)
        ttk.Button(frame, text="Salir",command=self.root.quit ).pack(fill="x", pady=10)
    #Ejecuta la venta del boton de "Entrar al simulador"
    def open_simulator(self):
        self.root.withdraw()  # Oculta la ventana de inicio
        simulator_window = tk.Toplevel(self.root)
        app = QueueSimulator(simulator_window)
        simulator_window.protocol("WM_DELETE_WINDOW", lambda: self.on_simulator_close(simulator_window))
        
    def open_simulator2(self):
        self.root.withdraw()  # Oculta la ventana de inicio
        simulator_window = tk.Toplevel(self.root)
        app = QueueSimulator2(simulator_window)
        simulator_window.protocol("WM_DELETE_WINDOW", lambda: self.on_simulator_close(simulator_window))
    #Devuelve al inicio al cerrar el simulador
    def on_simulator_close(self, simulator_window):
        simulator_window.destroy()
        self.root.deiconify()  # Muestra la ventana de inicio nuevamente
    #Ejecuta la venta del boton de "Documentacion"
    def show_documentation(self):
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Instrucciones")
        doc_window.geometry("1000x800")

        text_widget = tk.Text(doc_window, wrap="word", padx=10, pady=10,font=("Arial", 16) )
        text_widget.pack(expand=True, fill="both")

        scrollbar = ttk.Scrollbar(text_widget, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar.set)

        documentation = """
        ======================================================================================================================================
        Instrucciones:
        Este simulador es empleado para fines educativos tratando de representar el proceso de espera en colas de atención, este simulador
        consta de dos tipos de simuladores.
        
        
        ====================================================================================================================================== 
        Modelo: 
        En este simulador se le solicitara que selecciones uno de los tipos de cola utilizados, estos son M/M/1 y M/M/s con prioridad
        luego de seleccionar uno se le aparecerán nuevos campos para llenar, ambos comparten la solicitud de los siguientes campos:
            -Tasa de Llegadas: Se espera un valor decimal
            -Tasa de Servicio: Se espera un valor decimal
            -Tiempo Simulación: Se espera un valor decimal que será tratado a minutos
        
        Pero la selección de M/M/s con prioridad hará aparecer la solicitud de un campo adicional:
            -Número de Servidores: Se espera un valor entero
        
        Luego de llenados los datos, se pueden dar al botón de Ejecutar simulación, y dará al instante las acciones que transcurrieron en la ventana
        inferior, estas acciones incluyen los hechos de cuando un cliente fue servido y despachado, cuando fue rechazado y la cantidad de
        clientes atendidos en ese momento.
        
        En siguiente instancia aparecerá un gráfico lineal que analiza los patrones de salida y entrada de cada cliente en el tiempo que 
        ocurrió el evento.
        

        ======================================================================================================================================
        Libre: 
        En este simulador se podrá observar el movimiento de los clientes regulares y de prioridad entrando a las filas y ser atendidos 
        por las cajas. En este simulador el usuario tendrá acceso a una mayor amplitud de variables que el usuario puede trabajar:
            -Tiempo de Servicio: Se solicita un tiempo máximo de llegada el cual será filtrado. Se espera un valor decimal
            -Intervalo de Llegada: Se solicita un tiempo máximo de llegada el cual será filtrado. Se espera un valor decimal
            -Máximo de Clientes en Espera: Sirve para limitar el máximo de clientes que estarán en la sala de espera. Se espera un entero
            -Número de Cajas: Se asigna el número de cajas que procesaran a los clientes regulares. Se espera un entero
            -Cajas de Prioridad: Se asigna el número de cajas que procesaran a los clientes prioritarios. Se espera un entero
            -Proporción de Prioridad: Se asigna el valor porcentual de la aparición de clientes de prioridad. Se espera un valor decimal
            -Número de Filas: Se asigna el número de filas que procesaran a los clientes, se crea una prioritaria por defecto. 
            Se espera un entero
            -Duración de la Simulación: Se asigna el tiempo en minutos y se procesa en tiempo real. Se espera un valor decimal.
            
        Luego de que se den los datos si puede iniciar el simulador, este entonces desplegara en función tres ventanas las cuales demuestran
        los eventos de acción, el rendimiento de las cajas y la ventana que dibuja el movimiento de los clientes.
        
        El simulador también cuenta con los botones de pausar/reanudar la simulación, reiniciarla y un botón que despliega una ventana externa
        que demuestra los cálculos usando las formulas de la teoría de colas.
        
        
        ======================================================================================================================================
        Simulador de Colas con Prioridad

        Este simulador modela sistemas de colas con prioridad, aplicables a diversos escenarios como bancos, supermercados o centros de 
        atención al cliente.

        Teoría de Colas:
        La teoría de colas es una rama de la matemática aplicada que estudia y modela el comportamiento de las líneas de espera. 
        Se utiliza para analizar y optimizar sistemas donde la demanda de un servicio excede la capacidad de proporcionarlo inmediatamente.

        Elementos básicos de un sistema de colas:
            - Llegada de clientes: Proceso por el cual los clientes llegan al sistema.
            - Cola: Donde los clientes esperan antes de ser atendidos.
            - Servidores: Entidades que proporcionan el servicio a los clientes.
            - Disciplina de la cola: Reglas que determinan el orden en que se atienden los clientes.

        Modelos implementados:
        1) Modelo M/M/1:
            - Un solo servidor
            - Llegadas según distribución de Polisón (tasa λ)
            - Tiempo de servicio exponencial (tasa μ)
            - Fórmulas clave:
            * Utilización del sistema: ρ = λ/μ
            * Número promedio de clientes en cola: Lq = λ²/(μ(μ-λ))
            * Tiempo promedio en cola: Wq = Lq/λ

        2) Modelo M/M/s (con prioridad):
            - Múltiples servidores (s)
            - Llegadas según distribución de Polisón (tasa λ)
            - Tiempo de servicio exponencial (tasa μ)
            - Fórmulas clave:
            * Utilización del sistema: ρ = λ/(sμ)
            * Probabilidad de sistema vacío: P₀ = 1 / [Σ(λ/μ)ⁿ/n! + (λ/μ)ˢ/(s!(1-ρ))]
            * Número promedio de clientes en cola: Lq = (P₀(λ/μ)ˢρ) / (s!(1-ρ)²)

        Características del simulador:
            - Configuración flexible de número de servidores y colas
            - Simulación de clientes regulares y prioritarios
            - Visualización en tiempo real del estado del sistema
            - Cálculo y presentación de estadísticas de rendimiento

        Análisis de rendimiento:
            El simulador calcula y muestra métricas clave como:
            - Tiempo promedio de espera
            - Longitud promedio de la cola
            - Utilización de los servidores
            - Probabilidad de rechazo (cuando se implementa capacidad limitada)

        Aplicaciones prácticas:
            Este simulador puede utilizarse para:
            - Optimizar la asignación de recursos en sistemas de servicio
            - Analizar el impacto de diferentes configuraciones de servidores
            - Estudiar el efecto de la priorización en el rendimiento del sistema
            - Tomar decisiones basadas en datos para mejorar la eficiencia operativa

        Limitaciones y consideraciones:
            - El modelo asume distribuciones de llegada y servicio específicas
            - No considera factores externos que pueden afectar el rendimiento real
            - La simulación es una aproximación y los resultados pueden variar en situaciones del mundo real

        Se puede decir que este simulador proporciona una herramienta valiosa para entender y analizar sistemas de colas complejos, 
        permitiendo a los usuarios experimentar con diferentes configuraciones y parámetros para optimizar el rendimiento del sistema. 
        permite entender mejor la dinámica de los sistemas de colas con prioridad y cómo diferentes configuraciones afectan su rendimiento.
        
        ======================================================================================================================================
        """


        text_widget.insert(tk.END, documentation)
        text_widget.configure(state="disabled")  # Hace el texto de solo lectura

#-------------------------------------------------------------------------------------#

MAX_QUEUE_SIZE = 6
#M/M/c/inf/Fifo/k
class QueueSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Colas con Prioridad")
        #self.root.attributes('-fullscreen', True)
        # Variables por defecto
        self.max_waiting = tk.IntVar(value=10)
        self.num_boxes = tk.IntVar(value=4)
        self.priority_boxes_var = tk.IntVar(value=1)
        self.service_time = tk.DoubleVar(value=5)
        self.arrival_interval = tk.DoubleVar(value=3)
        self.priority_ratio = tk.DoubleVar(value=0.3)
        self.num_queues = tk.IntVar(value=2)  # Número de filas
        self.simulation_duration = tk.DoubleVar(value=2)  # Simulación en minutos     
        self.eventos = []
        
        self.int_validator = root.register(self.validate_int)
        self.double_validator = root.register(self.validate_double)        
        
        self.customers = []
        self.regular_customers = {i: [] for i in range(self.num_queues.get())}
        self.priority_customers = []
        self.waiting_room_customers = []
        self.counters = []
        self.simulation_paused = False  # Variable para controlar la pausa
        self.env = None  # Entorno de simulación
        self.simulation_end_time = None  # Tiempo de finalización de la simulación

        self.total_customers = 0
        self.total_wait_time = 0
        self.max_wait_time = 0
        self.wait_times = []


        self.create_widgets()

    def validate_int(self, value_if_allowed):
        """Validar que la entrada sea un entero mayor o igual a 1"""
        if value_if_allowed.isdigit() and int(value_if_allowed) >= 1:
            return True
        elif value_if_allowed == "":
            return True  # Permitir borrar el contenido
        else:
            return False

    def validate_double(self, value_if_allowed):
        """Validar que la entrada sea un número decimal mayor o igual a 0.1"""
        try:
            value = float(value_if_allowed)
            return value > 0
        except ValueError:
            return value_if_allowed == ""  # Permitir borrar el contenido


    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 14))

        style.configure("TEntry", font=("Helvetica", 14))
        style.configure("TButton", font=("Helvetica", 14))
        
        
        ttk.Label(frame, text="Tiempo de Servicio (s):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.service_time, validate="key", 
                  validatecommand=(self.double_validator, '%P')).grid(row=0, column=1, sticky=tk.E)

        ttk.Label(frame, text="Intervalo de Llegada (s):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.arrival_interval, validate="key", 
                  validatecommand=(self.double_validator, '%P')).grid(row=1, column=1, sticky=tk.E)        

        ttk.Label(frame, text="Máximo de Clientes en Espera:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.max_waiting, validate="key", 
                  validatecommand=(self.int_validator, '%P')).grid(row=3, column=1, sticky=tk.E)

        ttk.Label(frame, text="Número de Cajas:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.num_boxes, validate="key", 
                  validatecommand=(self.int_validator, '%P')).grid(row=2, column=1, sticky=tk.E)
        
        ttk.Label(frame, text="Cajas de Prioridad:").grid(row=4, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.priority_boxes_var, validate="key", 
                  validatecommand=(self.int_validator, '%P')).grid(row=4, column=1, sticky=tk.E)
        
        ttk.Label(frame, text="Proporción de Prioridad:").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.priority_ratio, validate="key", 
                  validatecommand=(self.double_validator, '%P')).grid(row=5, column=1, sticky=tk.E)
        
        ttk.Label(frame, text="Número de Filas:").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.num_queues, validate="key", 
                  validatecommand=(self.int_validator, '%P')).grid(row=6, column=1, sticky=tk.E)
        
        ttk.Label(frame, text="Duración de la Simulación (min):").grid(row=7, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.simulation_duration, validate="key", 
                  validatecommand=(self.double_validator, '%P')).grid(row=7, column=1, sticky=tk.E)

        self.start_button = ttk.Button(frame, text="Iniciar Simulación", command=self.start_simulation)
        self.start_button.grid(row=8, column=0, columnspan=2)

        self.pause_button = ttk.Button(frame, text="Detener/Reanudar Simulación", command=self.pause_simulation)
        self.pause_button.grid(row=9, column=0, columnspan=2)

        self.reset_button = ttk.Button(frame, text="Reiniciar Simulación", command=self.reset_simulation)
        self.reset_button.grid(row=10, column=0, columnspan=2)

        self.timer_label = ttk.Label(self.root, text="Tiempo restante: 00:00", font=("Helvetica", 16))
        self.timer_label.grid(row=1, column=0, pady=10)

        #---------------------------------------------
        self.canvas_frame_log = ttk.Frame(self.root)
        self.canvas_frame_log.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.canvas = tk.Canvas(self.canvas_frame_log, width=800, height=500, bg='white')
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.y_scrollbar = ttk.Scrollbar(self.canvas_frame_log, orient=tk.VERTICAL, command=self.canvas.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)

        self.canvas_content_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_content_frame, anchor=tk.NW)
        #---------------------------------------------
    
        #Este es el canvas del texto
        self.log_text = tk.Text(self.root, height=10, width=100)
        self.log_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    
        
        #-----------------------------------------------------------------------------------------------------------
        self.calcular_prob_button = ttk.Button(frame, text="Calcular Modelo Probabilístico", command=self.calcular_modelo_probabilistico)
        self.calcular_prob_button.grid(row=11, column=0, columnspan=2)

        #-----------------------------------------------------------------------------------------------------------
    def update_scrollregion(self):
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))   

    def reset_simulation(self):
        self.customers = []
        self.regular_customers = {i: [] for i in range(self.num_queues.get())}
        self.priority_customers = []
        self.waiting_room_customers = []
        self.counters = [0] * self.num_boxes.get()
        self.canvas.delete("all")
        self.env = None
        self.waiting_room = None
        self.boxes = None
        self.regular_boxes = None
        self.priority_boxes = None
        self.simulation_end_time = None
        self.simulation_paused = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.log_text.delete(1.0, tk.END)
        self.timer_label.config(text="Tiempo restante: 00:00")
        if hasattr(self, 'simulation_finished'):
            del self.simulation_finished

    def start_simulation(self):
        # Verifica que todos los campos estén llenos
        if not self.validate_fields():
            return

        self.reset_simulation()
        if hasattr(self, 'canvas_rendimiento'):
            self.canvas_widget_rendimiento.grid_forget()
            del self.fig_rendimiento
            del self.ax_rendimiento
            del self.canvas_rendimiento
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.env = simpy.Environment()
        self.waiting_room = simpy.Resource(self.env, capacity=self.max_waiting.get())
        self.boxes = [simpy.Resource(self.env, capacity=1) for _ in range(self.num_boxes.get())]

        priority_count = self.priority_boxes_var.get()
        self.regular_boxes = self.boxes[priority_count:]
        self.priority_boxes = self.boxes[:priority_count]

        self.simulation_end_time = self.simulation_duration.get() * 60

        self.env.process(self.customer_generator())
        self.update_timer()
        self.simulate_step()
        
    def validate_fields(self):
        """Verifica que todos los campos necesarios estén llenos y sean válidos."""
        if (self.service_time.get() <= 0 or
            self.arrival_interval.get() <= 0 or
            self.max_waiting.get() <= 0 or
            self.num_boxes.get() <= 0 or
            self.priority_boxes_var.get() < 0 or
            self.priority_ratio.get() < 0 or
            self.num_queues.get() <= 0 or
            self.simulation_duration.get() <= 0):
            
            messagebox.showwarning("Advertencia", "Por favor, asegúrese de que todos los campos estén llenos y sean válidos.")
            return False
        
        return True
        
    def simulate_step(self):
        if self.env is not None and not self.simulation_paused:
            self.env.run(until=self.env.now + 1)
            self.update_gui()
            self.mostrar_grafico_rendimiento()  # Añade esta línea
            if self.env.now < self.simulation_end_time:
                self.root.after(1000, self.simulate_step)
            elif not hasattr(self, 'simulation_finished'):
                self.simulation_finished = True
                self.start_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.log_text.insert(tk.END, "Simulación Finalizada\n")
                self.log_text.see(tk.END)
                self.print_statistics()
                self.mostrar_grafico_rendimiento()  # Actualiza una última vez al finalizar

    def customer_generator(self):
        while True:
            if self.env.now >= self.simulation_end_time:
                return
            yield self.env.timeout(random.expovariate(1.0 / self.arrival_interval.get())) #explota el tiempo de llegada
            priority = random.random() < self.priority_ratio.get()
            self.env.process(self.customer(priority))
            #self.env.process(self.customer_gen2(priority))
            
#Clientes que llegan en un intervalo y son atendidos por Ws segun la           

    def customer_gen2(self, priority):
        with self.waiting_room.request() as req:
            yield req
            self.waiting_room_customers.append((priority, self.env.now))
            
            while True:
                if priority:
                    if len(self.priority_customers) < MAX_QUEUE_SIZE:
                        self.waiting_room_customers.pop(0)
                        self.priority_customers.append((priority, self.env.now))
                        box = random.choice(self.priority_boxes)
                        break
                else:
                    available_queues = [q for q, customers in self.regular_customers.items() if len(customers) < MAX_QUEUE_SIZE]
                    if available_queues:
                        chosen_queue = random.choice(available_queues)
                        self.waiting_room_customers.pop(0)
                        self.regular_customers[chosen_queue].append((priority, self.env.now))
                        box = random.choice(self.regular_boxes)
                        break
                yield self.env.timeout(1)  # Espera antes de intentar nuevamente

        with box.request() as req:
            yield req
            log_entry_message = f"Cliente {'Prioritario' if priority else 'Regular'} entró en Caja {self.boxes.index(box) + 1} a tiempo {self.env.now}\n"
            self.log_text.insert(tk.END, log_entry_message)
            self.log_text.see(tk.END)

            # Parámetros de la tasa de llegada y servicio (lambda y mu)
            tasa_llegada = self.arrival_interval  # Lambda, tasa de llegada de clientes
            tasa_servicio = self.service_time  # Mu, tasa de servicio de los clientes en la caja

            # Cálculo del valor esperado del tiempo en la cola (1 / (mu - lambda))
            if tasa_servicio > tasa_llegada:
                valor_esperado = 1 / (tasa_servicio - tasa_llegada)
            else:
                valor_esperado = 0.1  # Evitar división por cero o tasas de servicio muy bajas
            
            # Tiempo de salida aleatorio entre 0 y el valor esperado del tiempo en la cola
            salida_aleatoria = random.uniform(0, valor_esperado)
            yield self.env.timeout(salida_aleatoria)
            
            if priority:
                self.priority_customers.pop(0)
            else:
                self.regular_customers[chosen_queue].pop(0)
            self.counters[self.boxes.index(box)] += 1
            
            log_exit_message = f"Cliente {'Prioritario' if priority else 'Regular'} salió de Caja {self.boxes.index(box) + 1} a tiempo {self.env.now}\n"
            self.log_text.insert(tk.END, log_exit_message)
            self.log_text.see(tk.END)

     
#Clientes que son atendidos por un intervalo aleatorio             
    def customer(self, priority):
        with self.waiting_room.request() as req:
            yield req
            self.waiting_room_customers.append((priority, self.env.now))
            
            while True:
                if priority:
                    if len(self.priority_customers) < MAX_QUEUE_SIZE:
                        self.waiting_room_customers.pop(0)
                        self.priority_customers.append((priority, self.env.now))
                        box = random.choice(self.priority_boxes)
                        break
                else:
                    available_queues = [q for q, customers in self.regular_customers.items() if len(customers) < MAX_QUEUE_SIZE]
                    if available_queues:
                        chosen_queue = random.choice(available_queues)
                        self.waiting_room_customers.pop(0)
                        self.regular_customers[chosen_queue].append((priority, self.env.now))
                        box = random.choice(self.regular_boxes)
                        break
                yield self.env.timeout(1)  # Espera antes de intentar nuevamente

        with box.request() as req:
            yield req
            log_entry_message = f"Cliente {'Prioritario' if priority else 'Regular'} entró en Caja {self.boxes.index(box) + 1} a tiempo {self.env.now}\n"
            self.log_text.insert(tk.END, log_entry_message)
            self.log_text.see(tk.END)
            
            # Tiempo de salida aleatorio entre 0 y 30 segundos
            salida_aleatoria = random.uniform(0, 0.5) * 60
            yield self.env.timeout(salida_aleatoria)
            
            if priority:
                self.priority_customers.pop(0)
            else:
                self.regular_customers[chosen_queue].pop(0)
            self.counters[self.boxes.index(box)] += 1
            log_exit_message = f"Cliente {'Prioritario' if priority else 'Regular'} salió de Caja {self.boxes.index(box) + 1} a tiempo {self.env.now}\n"
            self.log_text.insert(tk.END, log_exit_message)
            self.log_text.see(tk.END)
    
    def update_gui(self):
        self.canvas.delete("all")

        # Dibujar la sala de espera
        x_waiting = 50
        y_waiting = 50
        self.canvas.create_rectangle(x_waiting - 20, y_waiting, x_waiting + 80, y_waiting + 280, outline='black')
        self.canvas.create_text(x_waiting + 30, y_waiting - 10, text="Sala de Espera", fill="black")
        for i, customer in enumerate(self.waiting_room_customers):
            color = 'red' if customer[0] else 'green'
            self.canvas.create_oval(x_waiting, y_waiting + (i * 30), x_waiting + 20, y_waiting + (i * 30) + 20, fill=color)

        # Dibujar las cajas y sus cuadrados de atención
        for i, box in enumerate(self.boxes):
            x = 700
            y = 50 + i * 80
            color = 'red' if box in self.priority_boxes else 'blue'
            self.canvas.create_rectangle(x, y, x + 60, y + 60, fill=color)
            self.canvas.create_text(x + 30, y - 10, text=f"Caja {i + 1}", fill="black")
            if self.counters[i] > 0:
                self.canvas.create_text(x + 30, y + 30, text=f"{self.counters[i]}", fill="white")

        # Dibujar las filas y los clientes en ellas
        for q in range(self.num_queues.get()):
            x = 400
            y_start = 50 + (q * 200)
            self.canvas.create_rectangle(x - 20, y_start, x + 80, y_start + 180, outline='blue')
            self.canvas.create_text(x + 30, y_start - 10, text=f"Fila {q + 1}", fill="black")
            for i, customer in enumerate(self.regular_customers[q][:MAX_QUEUE_SIZE]):
                self.canvas.create_oval(x, y_start + (i * 30), x + 20, y_start + (i * 30) + 20, fill='green')

        # Dibujar la fila prioritaria
        x = 550
        y_start = 50
        self.canvas.create_rectangle(x - 20, y_start, x + 80, y_start + 180, outline='red')
        self.canvas.create_text(x + 30, y_start - 10, text="Fila Prioritaria", fill="black")
        for i, customer in enumerate(self.priority_customers[:MAX_QUEUE_SIZE]):
            self.canvas.create_oval(x, y_start + (i * 30), x + 20, y_start + (i * 30) + 20, fill='red')
        self.update_scrollregion()
        
    def update_timer(self):
        if self.env is None or self.simulation_end_time is None:
            return
        remaining_time = max(0, self.simulation_end_time - self.env.now)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        self.timer_label.config(text=f"Tiempo restante: {minutes:02}:{seconds:02}")
        if self.env.now < self.simulation_end_time and not self.simulation_paused:
            self.root.after(1000, self.update_timer)

    def pause_simulation(self):
        self.simulation_paused = not self.simulation_paused
        if not self.simulation_paused:
            self.simulate_step()
            self.update_timer()
    #------------------------------------------------------------------------------------------------
    def calcular_modelo_probabilistico(self):
        lamda = self.arrival_interval.get()
        mu = self.service_time.get()
        s = self.num_boxes.get()

        if lamda >= mu * s:
            messagebox.showwarning("Advertencia", "La tasa de llegada no puede ser mayor o igual que la tasa de servicio multiplicada por el número de servidores.")
            return

        results = self.mms_model(lamda, mu, s)
        self.mostrar_resultados_probabilisticos(results)

    def mms_model(self, lamda, mu, s):
        rho = lamda / (s * mu)
        sumatoria = sum([(lamda / mu)**n / math.factorial(n) for n in range(s)])
        P_0 = 1 / (sumatoria + ((lamda / mu)**s / (math.factorial(s) * (1 - rho))))
        L_q = (P_0 * (lamda / mu)**s * rho) / (math.factorial(s) * (1 - rho)**2)
        L_s = s * rho
        L_w = L_q + L_s
        W_q = L_q / lamda
        W_s = 1 / mu
        W_w = W_q + W_s
        return {"rho": rho, "P_0": P_0, "L_q": L_q, "L_s": L_s, "L_w": L_w, "W_q": W_q, "W_s": W_s, "W_w": W_w}

    def mostrar_resultados_probabilisticos(self, results):
        # Crear una nueva ventana para mostrar los resultados
        results_window = tk.Toplevel(self.root)
        results_window.title("Resultados del Modelo Probabilístico")
        ttk.Label(results_window, font=("Helvetica", 16, "bold"), text='Modelo de resultados probalisticos del sistema de colas').pack(side="top")
        ttk.Label(results_window, text=f"Probabilidad de Zero Clientes: {results['P_0']:.4f}").pack()
        ttk.Label(results_window, text=f"Tasa de uso del sistema: {results['rho']:.4f}").pack()
        ttk.Label(results_window, text=f"Tasa de ocio del sistema: {1 - results['rho']:.4f}").pack()
        ttk.Label(results_window, text=f"Número esperado de clientes en la cola (Lq): {results['L_q']:.4f}").pack()
        ttk.Label(results_window, text=f"Número esperado de clientes recibiendo servicio (Ls): {results['L_s']:.4f}").pack()
        ttk.Label(results_window, text=f"Número esperado de clientes en el sistema de colas (Lw): {results['L_w']:.4f}").pack()
        ttk.Label(results_window, text=f"Valor esperado del tiempo en la cola (Wq): {results['W_q']:.4f} minutos").pack()
        ttk.Label(results_window, text=f"Valor esperado del tiempo en el servicio (Ws): {results['W_s']:.4f} minutos").pack()
        ttk.Label(results_window, text=f"Valor esperado del tiempo en el sistema (Ww): {results['W_w']:.4f} minutos").pack()
                            
    def mostrar_grafico_rendimiento(self):
        if not hasattr(self, 'fig_rendimiento'):
            self.fig_rendimiento, self.ax_rendimiento = plt.subplots(figsize=(8, 4))
            self.canvas_rendimiento = FigureCanvasTkAgg(self.fig_rendimiento, master=self.root)
            self.canvas_widget_rendimiento = self.canvas_rendimiento.get_tk_widget()
            self.canvas_widget_rendimiento.grid(row=0, column=1, columnspan=1)

        self.ax_rendimiento.clear()
        box_numbers = range(1, len(self.counters) + 1)
        self.ax_rendimiento.bar(box_numbers, self.counters)

        self.ax_rendimiento.set_xlabel('Número de Caja')
        self.ax_rendimiento.set_ylabel('Clientes Atendidos')
        self.ax_rendimiento.set_title('Rendimiento de Cajas durante la Simulación')
        self.ax_rendimiento.set_xticks(box_numbers)

        for i, v in enumerate(self.counters):
            self.ax_rendimiento.text(i + 1, v, str(v), ha='center', va='bottom')

        self.canvas_rendimiento.draw()
#------------------------------------------------------------------------------------------------------

        
        
#------------------------------------------------------------------------------------------------------
class QueueSimulator2:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Colas")

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Selección de Modelo
        self.modelo_var = tk.StringVar()
        ttk.Label(self.frame, text="Selecciona el Modelo de Cola:").grid(row=0, column=0, sticky=tk.W)
        self.menu_modelo = ttk.Combobox(self.frame, textvariable=self.modelo_var, values=["M/M/1", "M/M/s con Prioridad"])
        self.menu_modelo.grid(row=0, column=1, sticky=(tk.W, tk.E))

        # Entradas de Parámetros
        self.frame_params = ttk.Frame(self.frame)
        self.frame_params.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.frame_params.grid_forget()  # Ocultar inicialmente

        ttk.Label(self.frame_params, text="Tasa de Llegadas:").grid(row=0, column=0, sticky=tk.W)
        self.entrada_tasa_llegadas = ttk.Entry(self.frame_params)
        self.entrada_tasa_llegadas.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.frame_params, text="Tasa de Servicio:").grid(row=1, column=0, sticky=tk.W)
        self.entrada_tasa_servicio = ttk.Entry(self.frame_params)
        self.entrada_tasa_servicio.grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.frame_params, text="Tiempo de Simulación(min):").grid(row=2, column=0, sticky=tk.W)
        self.entrada_tiempo_simulacion = ttk.Entry(self.frame_params)
        self.entrada_tiempo_simulacion.grid(row=2, column=1, sticky=(tk.W, tk.E))

        self.entrada_tiempo_servidores = ttk.Label(self.frame_params, text="Número de Servidores (para M/M/s):")
        self.entrada_tiempo_servidores.grid(row=3, column=0, sticky=tk.W)
        self.entrada_tiempo_servidores.grid_forget()
        self.entrada_servidores = ttk.Entry(self.frame_params)
        self.entrada_servidores.grid(row=3, column=1, sticky=(tk.W, tk.E))
        self.entrada_servidores.grid_forget()  # Ocultar inicialmente

        ttk.Button(self.frame, text="Ejecutar Simulación", command=self.ejecutar_simulacion).grid(row=2, column=0, columnspan=2, pady=10)

        # Área de texto para el log
        self.texto_log = tk.Text(self.frame, height=10, width=60)
        self.texto_log.grid(row=3, column=0, columnspan=2, pady=10)
        self.texto_log.config(state=tk.DISABLED)

        self.menu_modelo.bind("<<ComboboxSelected>>", self.actualizar_frame_params)

    def actualizar_frame_params(self, event):
        modelo = self.modelo_var.get()
        if modelo == "M/M/1":
            self.entrada_servidores.grid_forget()
            self.entrada_tiempo_servidores.grid_forget()
            
        elif modelo == "M/M/s con Prioridad":
            self.entrada_servidores.grid(row=3, column=1, sticky=(tk.W, tk.E))
            self.entrada_tiempo_servidores.grid(row=3, column=0, sticky=tk.W)
        self.frame_params.grid()

    def ejecutar_simulacion(self):
        modelo = self.modelo_var.get()
        tasa_llegadas = float(self.entrada_tasa_llegadas.get())
        tasa_servicio = float(self.entrada_tasa_servicio.get())
        tiempo_simulacion = float(self.entrada_tiempo_simulacion.get())

        if modelo == "M/M/1":
            self.simular_mm1(tasa_llegadas, tasa_servicio, tiempo_simulacion)
        elif modelo == "M/M/s con Prioridad":
            num_servidores = int(self.entrada_servidores.get())
            self.simular_mms_con_prioridad(tasa_llegadas, tasa_servicio, tiempo_simulacion, num_servidores)

    def simular_mm1(self, tasa_llegadas, tasa_servicio, tiempo_simulacion):
        cola = ColaMM1(tasa_llegadas, tasa_servicio, tiempo_simulacion)
        eventos = cola.simular()
        cola.imprimir_estadisticas(self.texto_log)
        self.graficar_eventos(eventos)
        self.iniciar_simulacion_visual(tasa_llegadas, tasa_servicio, tiempo_simulacion)

    def simular_mms_con_prioridad(self, tasa_llegadas, tasa_servicio, tiempo_simulacion, num_servidores):
        cola = ColaMMSConPrioridad(tasa_llegadas, tasa_servicio, tiempo_simulacion, num_servidores)
        eventos = cola.simular()
        cola.imprimir_estadisticas(self.texto_log)
        self.graficar_eventos(eventos)
        self.iniciar_simulacion_visual(tasa_llegadas, tasa_servicio, tiempo_simulacion, num_servidores)

    def graficar_eventos(self, eventos):
        llegadas = [evento[1] for evento in eventos if 'llegada' in evento[0]]
        salidas = [evento[1] for evento in eventos if 'salida' in evento[0]]

        fig, ax = plt.subplots()
        ax.plot(llegadas, np.arange(len(llegadas)), 'bo-', label='Llegadas')
        ax.plot(salidas, np.arange(len(salidas)), 'ro-', label='Salidas')
        ax.set_xlabel('Tiempo(min)')
        ax.set_ylabel('Número de clientes')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

        # Cerrar la figura después de mostrarla
        plt.close(fig)

    def iniciar_simulacion_visual(self, tasa_llegadas, tasa_servicio, tiempo_simulacion, num_servidores=1):
        self.env = simpy.Environment()
        self.tasa_llegadas = tasa_llegadas
        self.tasa_servicio = tasa_servicio
        self.tiempo_simulacion = tiempo_simulacion
        self.num_servidores = num_servidores

        self.waiting_room = simpy.Resource(self.env, capacity=1)
        self.priority_customers = []
        self.regular_customers = {i: [] for i in range(self.num_servidores)}
        self.priority_boxes = [simpy.Resource(self.env, capacity=1) for _ in range(num_servidores)]
        self.regular_boxes = [simpy.Resource(self.env, capacity=1) for _ in range(num_servidores)]
        self.counters = [0] * num_servidores

        self.env.process(self.customer_generator())
        self.env.run(until=self.tiempo_simulacion)

    def customer_generator(self):
        while True:
            yield self.env.timeout(random.expovariate(1.0 / self.tasa_llegadas))
            priority = random.random() < 0.5
            self.env.process(self.handle_customer(priority))

    def handle_customer(self, priority):
        chosen_queue = None
        if priority:
            if len(self.priority_customers) < self.num_servidores:
                self.priority_customers.append((priority, self.env.now))
            else:
                self.log_text_insert("Cliente de prioridad rechazado\n")
        else:
            if sum(len(queue) for queue in self.regular_customers.values()) < self.num_servidores * 2:
                chosen_queue = random.choice(list(self.regular_customers.keys()))
                self.regular_customers[chosen_queue].append((priority, self.env.now))
            else:
                self.log_text_insert("Cliente regular rechazado\n")

        with self.waiting_room.request() as req:
            yield req
            self.log_text_insert(f"Cliente {'prioritario' if priority else 'regular'} en sala de espera\n")
            yield self.env.timeout(random.expovariate(1.0 / self.tasa_servicio))
            self.log_text_insert(f"Cliente {'prioritario' if priority else 'regular'} movido a cola\n")
            self.move_to_box(priority, chosen_queue if not priority else None)

    def log_text_insert(self, message):
        self.texto_log.config(state=tk.NORMAL)
        self.texto_log.insert(tk.END, f'{self.env.now:.2f}: {message}')
        self.texto_log.config(state=tk.DISABLED)

    def move_to_box(self, priority, chosen_queue):
        if priority:
            if self.priority_customers:
                for i, box in enumerate(self.priority_boxes):
                    if box.count == 0:
                        self.priority_customers.pop(0)
                        self.env.process(self.serve_customer(box, i))
                        break
        else:
            if chosen_queue is not None and self.regular_customers[chosen_queue]:
                self.regular_customers[chosen_queue].pop(0)
                self.env.process(self.serve_customer(self.regular_boxes[chosen_queue], chosen_queue))

    def serve_customer(self, box, queue_index):
        with box.request() as req:
            yield req
            self.log_text_insert(f"Cliente atendido en caja {queue_index + 1}\n")
            yield self.env.timeout(random.expovariate(1.0 / self.tasa_servicio))
            self.log_text_insert(f"Cliente sale de la caja {queue_index + 1}\n")

# Clases para M/M/1 y M/M/s con Prioridad
class ColaMM1:
    def __init__(self, tasa_llegadas, tasa_servicio, tiempo_simulacion):
        self.tasa_llegadas = tasa_llegadas
        self.tasa_servicio = tasa_servicio
        self.tiempo_simulacion = tiempo_simulacion

    def simular(self):
        eventos = []
        tiempo_actual = 0
        while tiempo_actual < self.tiempo_simulacion:
            tiempo_llegada = random.expovariate(self.tasa_llegadas)
            tiempo_salida = random.expovariate(self.tasa_servicio)
            tiempo_actual += tiempo_llegada
            eventos.append(('llegada', tiempo_actual))
            tiempo_actual += tiempo_salida
            eventos.append(('salida', tiempo_actual))
        return eventos

    def imprimir_estadisticas(self, texto_log):
        texto_log.config(state=tk.NORMAL)
        texto_log.insert(tk.END, "Estadísticas M/M/1:\n")
        texto_log.insert(tk.END, f"Tasa de Llegadas: {self.tasa_llegadas}\n")
        texto_log.insert(tk.END, f"Tasa de Servicio: {self.tasa_servicio}\n")
        texto_log.insert(tk.END, f"Tiempo Simulación(min): {self.tiempo_simulacion}\n")
        texto_log.config(state=tk.DISABLED)

class ColaMMSConPrioridad:
    def __init__(self, tasa_llegadas, tasa_servicio, tiempo_simulacion, num_servidores):
        self.tasa_llegadas = tasa_llegadas
        self.tasa_servicio = tasa_servicio
        self.tiempo_simulacion = tiempo_simulacion
        self.num_servidores = num_servidores

    def simular(self):
        eventos = []
        tiempo_actual = 0
        while tiempo_actual < self.tiempo_simulacion:
            tiempo_llegada = random.expovariate(self.tasa_llegadas)
            tiempo_salida = random.expovariate(self.tasa_servicio)
            tiempo_actual += tiempo_llegada
            eventos.append(('llegada', tiempo_actual))
            tiempo_actual += tiempo_salida
            eventos.append(('salida', tiempo_actual))
        return eventos

    def imprimir_estadisticas(self, texto_log):
        texto_log.config(state=tk.NORMAL)
        texto_log.insert(tk.END, "Estadísticas M/M/s con Prioridad:\n")
        texto_log.insert(tk.END, f"Tasa de Llegadas: {self.tasa_llegadas}\n")
        texto_log.insert(tk.END, f"Tasa de Servicio: {self.tasa_servicio}\n")
        texto_log.insert(tk.END, f"Tiempo Simulación(min): {self.tiempo_simulacion}\n")
        texto_log.config(state=tk.DISABLED)

#------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = StartWindow(root)
    root.mainloop()

