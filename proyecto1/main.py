import time
from protocolos.utopiaprotocol import UtopiaProtocol
from protocolos.linkprotocol import LinkProtocol
from capas.networklayer import NetworkLayer
from capas.physicallayer import PhysicalLayer
from simulador.simulator import Simulator
from modelos.packet import Packet
import threading

# Crea instancias de capa de red
network_layer_A = NetworkLayer()
network_layer_B = NetworkLayer()

# Crea los protocolos de enlace
link_protocol_A = None
link_protocol_B = None

# Crea instancias de capa fisica
physical_layer_A = PhysicalLayer(error_rate=0.1)
physical_layer_B = PhysicalLayer(error_rate=0.1)

# Conecta los componentes entre sí
physical_layer_A.set_receptor(physical_layer_B)
physical_layer_B.set_receptor(physical_layer_A)

def menu():
    global link_protocol_A, link_protocol_B
    while True:
        print("\n===========================================================")
        print("Menu de Procolos de Enlace\n")
        print("0. Link")
        print("1. Utopia")
        print("2. Stop and Wait")
        print("3. PAR")
        print("4. Sliding Window de 1 bit")
        print("5. Go-Back-N")
        print("6. Selective-Repeat")

        opcion = input("\nIngrese una opcion: ")
        if opcion == "0":
            #Link
            link_protocol_A = LinkProtocol('A')
            link_protocol_B = LinkProtocol('B')
            break
        if opcion == "1":
            #Utopia
            break
        elif opcion == "2":
            #Stop and Wait
            break
        elif opcion == "3":
            #PAR
            break
        elif opcion == "4":
            #Sliding Window de 1 bit
            break
        elif opcion == "5":
            #Go-Back-N
            break
        elif opcion == "6":
            #Selective-Repeat
            break
        else:
            print("\nOpcion invalida\n")

    return

def simulation():
    global network_layer_A, link_protocol_A, physical_layer_A, network_layer_B, link_protocol_B, physical_layer_B
    menu()

    print("\nSimulacion Iniciada\n")
    time.sleep(1)

    # Inicializa el simulador con los componentes para A y B
    simulator_A = Simulator(link_protocol_A, network_layer_A, physical_layer_A)
    simulator_B = Simulator(link_protocol_B, network_layer_B, physical_layer_B)
    # Crear los threads e iniciarlos
    thread_A = threading.Thread(target=simulator_A.run_simulation)
    thread_B = threading.Thread(target=simulator_B.run_simulation)
    thread_A.start()
    thread_B.start()
        

if __name__ == "__main__":
    # Inicializa la simulacion
    simulation()