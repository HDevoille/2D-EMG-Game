import socket
from pylsl import StreamInlet, resolve_stream
import tkinter as tk
import threading

class GUI:

    def __init__(self):
        self.inlet = None
        self.max_strength = 0 
        self.root = tk.Tk()
        
        self.root.geometry("500x300")
        self.root.title("2D EMG Game Acquisition")

        self.label = tk.Label(self.root,text = "Console :")
        self.label.pack(padx=20,pady=10)

        self.console = tk.Text(self.root,height=6)
        self.console.pack(padx=20,pady=10)

        self.buttonFindStream = tk.Button(self.root,text="Find Stream",command=threading.Thread(target=self.open_stream).start)
        self.buttonFindStream.pack(padx=20,pady=10)

        self.buttonCalibration = tk.Button(self.root,text="Launch Calibration",command = threading.Thread(target=self.calibration).start)
        self.buttonCalibration.pack(padx=20,pady=10)

        self.buttonStart = tk.Button(self.root, text="Start Server", command = threading.Thread(target = self.start_server).start)
        self.buttonStart.pack(padx=20,pady=10)

        self.root.mainloop()


    def recv_data(self):
        sample,timestamp = self.inlet.pull_sample()
        return abs(sample[1])

    def calibration(self):
        self.console.delete(1.0,tk.END)
        self.console.insert(tk.END,"Squeeze to full strength \n")
        n = 0
        calibration_data = []
        while n < 500:
            sample = self.recv_data()
            calibration_data.append(sample)
            n+=1
        maxstrength = max(calibration_data)
        self.max_strength = maxstrength
        self.console.insert(tk.END,"Max Strength = " + str(self.max_strength)+"\n")

    def traitement_data(self):
        last_sample = self.recv_data()
        if last_sample > self.max_strength/2:
            return last_sample

    def start_server(self):
        self.console.delete(1.0,tk.END)
        # Créer un socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Attacher le socket à une adresse et un port spécifiques
        server_socket.bind(('localhost', 12345))
        
        # Commencer à écouter pour les connexions entrantes
        server_socket.listen(1)
        self.console.insert(tk.END,"Server started and listening on localhost:12345 \n")

        while True:
            # Accepter une connexion entrante
            client_socket, addr = server_socket.accept()
            self.console.insert(tk.END,f"Connection from {addr} has been established! \n")

            while True:

                try:
                    # Envoyer un message au client
                    message = str(self.traitement_data())
                    client_socket.send(bytes(message+",", "utf-8"))
                    self.console.insert(tk.END,message+"\n")
                except:
                    self.console.insert(tk.END,"Client has disconnected \n")
                    break  # sortir de la boucle interne si le client est déconnecté

            # Fermer le socket client
            client_socket.close()

    def open_stream(self):
        self.console.delete(1.0,tk.END)
        self.console.insert(tk.END,"Looking for OpenSignals stream ...")
        os_stream = resolve_stream("name","OpenSignals")
        self.inlet = StreamInlet(os_stream[0])
        self.console.insert(tk.END,"Stream found !")

"""
def recv_data(inlet):
        sample,timestamp = inlet.pull_sample()
        return abs(sample[1])

def calibration(inlet):
    n = 0
    calibration_data = []
    while n < 1000:
        sample = recv_data(inlet)
        calibration_data.append(sample)
        n+=1
    maxstrength = max(calibration_data)
    print(maxstrength)
    return maxstrength

def traitement_data(maxstrength,inlet):
    last_sample = recv_data(inlet)
    if last_sample > maxstrength/2:
        return last_sample

def start_server(maxstrength,inlet):
    # Créer un socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # Attacher le socket à une adresse et un port spécifiques
    server_socket.bind(('localhost', 12345))
        
    # Commencer à écouter pour les connexions entrantes
    server_socket.listen(1)
    #self.console.insert(tk.END,"Server started and listening on localhost:12345")
    print("Server Started")

    while True:
        # Accepter une connexion entrante
        client_socket, addr = server_socket.accept()
        #self.console.insert(tk.END,f"Connection from {addr} has been established!")
        print(f"Connection from {addr} has been established!")

        while True:
            try:
            # Envoyer un message au client
                client_socket.send(bytes(str(traitement_data(maxstrength,inlet))+",", "utf-8"))
            except:
                #self.console.insert(tk.END,"Client has disconnected")
                print("Client disconnected")
                break  # sortir de la boucle interne si le client est déconnecté

        # Fermer le socket client
        client_socket.close()
"""

if __name__ == "__main__":
    GUI()

    # inlet = open_stream()
    # maxstrength = calibration(inlet)
    # start_server(maxstrength, inlet)