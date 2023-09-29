import time
import threading
from protocolos.linkprotocol import LinkProtocol
from capas.networklayer import NetworkLayer
from capas.physicallayer import PhysicalLayer
from protocolos.utopiaprotocol import UtopiaProtocol
from protocolos.stopandwaitprotocol import StopAndWait
from protocolos.parprotocol import ParProtocol
from simulador.simulator import Simulator

# Mantén un registro de todos los hilos de la simulación
simulator_threads = []

# Variable de control para pausar la simulación
pausa_simulacion = False

# Variable de control para finalizar la simulación
finalizar_simulacion = False

# Crea instancias de capa de red
network_layer_A = NetworkLayer()
network_layer_B = NetworkLayer()

# Crea los protocolos de enlace
link_protocol_A = None
link_protocol_B = None

# Crea instancias de capa física
physical_layer_A = PhysicalLayer(error_rate=0.1)
physical_layer_B = PhysicalLayer(error_rate=0.1)

# Conecta los componentes entre sí
physical_layer_A.set_receptor(physical_layer_B)
physical_layer_B.set_receptor(physical_layer_A)

def menu_pausa(simulator_A, simulator_B):
    global pausa_simulacion, finalizar_simulacion
    while not finalizar_simulacion:
        opcion = input("\nPresiona 'p' para pausar la simulación, 'r' para reanudar o 't' para terminar: \n\n")
        if opcion.lower() == 'p':
            pausa_simulacion = True
            simulator_A.pause = pausa_simulacion
            simulator_B.pause = pausa_simulacion
            print("Eventos cliente A: \n")
            simulator_A.link_protocol.print_events()
            print("\nEventos cliente B: \n")
            simulator_B.link_protocol.print_events()
        elif opcion.lower() == 'r':
            pausa_simulacion = False
            simulator_A.pause = pausa_simulacion
            simulator_B.pause = pausa_simulacion
        elif opcion.lower() == 't':
            finalizar_simulacion = True
            simulator_A.running = False
            simulator_B.running = False
            break
        else:
            print("\nOpción no válida\n")

def menu():
    global link_protocol_A, link_protocol_B
    while True:
        print("\n===========================================================")
        print("Menu de Protocolos de Enlace\n")
        print("0. Link")
        print("1. Utopia")
        print("2. Stop and Wait")
        print("3. PAR")
        print("4. Sliding Window de 1 bit")
        print("5. Go-Back-N")
        print("6. Selective-Repeat")

        opcion = input("\nIngrese una opción: ")
        if opcion == "0":
            # Link
            link_protocol_A = LinkProtocol('A')
            link_protocol_B = LinkProtocol('B')
            link_protocol_A.set_physical_layer(physical_layer_A)
            link_protocol_B.set_physical_layer(physical_layer_B)
            break
        if opcion == "1":
            # Utopia
            link_protocol_A = UtopiaProtocol('A')
            link_protocol_B = UtopiaProtocol('B')
            link_protocol_A.set_physical_layer(physical_layer_A)
            link_protocol_B.set_physical_layer(physical_layer_B)
            break
        elif opcion == "2":
            # Stop and Wait
            link_protocol_A = StopAndWait('A')
            link_protocol_B = StopAndWait('B')
            link_protocol_A.set_physical_layer(physical_layer_A)
            link_protocol_B.set_physical_layer(physical_layer_B)
            break
        elif opcion == "3":
            # PAR
            link_protocol_A = ParProtocol('A')
            link_protocol_B = ParProtocol('B')
            link_protocol_A.set_physical_layer(physical_layer_A)
            link_protocol_B.set_physical_layer(physical_layer_B)
            break
        elif opcion == "4":
            # Sliding Window de 1 bit
            break
        elif opcion == "5":
            # Go-Back-N
            break
        elif opcion == "6":
            # Selective-Repeat
            break
        else:
            print("\nOpción inválida\n")

def simulation():
    global network_layer_A, link_protocol_A, physical_layer_A, network_layer_B, link_protocol_B, physical_layer_B
    menu()

    print("\nSimulación Iniciada\n")
    time.sleep(1)

    # Inicializa el simulador con los componentes para A y B
    simulator_A = Simulator(link_protocol_A, network_layer_A, physical_layer_A)
    simulator_B = Simulator(link_protocol_B, network_layer_B, physical_layer_B)

    # Crea y arranca un hilo para el control de pausa
    pausa_thread = threading.Thread(target=menu_pausa, args=(simulator_A, simulator_B))
    pausa_thread.start()

    # Crear los threads e iniciarlos
    thread_A = threading.Thread(target=simulator_A.run_simulation)
    thread_B = threading.Thread(target=simulator_B.run_simulation)
    simulator_threads.append(thread_A)
    simulator_threads.append(thread_B)
    thread_A.start()
    thread_B.start()

    # Espera a que se finalice la simulación
    while not finalizar_simulacion:
        pass
    
    for thread in simulator_threads:
            thread.join()

if __name__ == "__main__":
    # Inicializa la simulación
    simulation()
