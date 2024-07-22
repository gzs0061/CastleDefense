import requests
import json
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer
import threading
import sys


class GameController(QMainWindow):
    def __init__(self):
        super(GameController, self).__init__()
        self.initUI()
        self.place_objects_flag = True

    def initUI(self):
        self.setGeometry(200, 200, 800, 800)
        self.setWindowTitle("Game Controller")

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Up")
        self.b1.setGeometry(QtCore.QRect(QtCore.QPoint(300, 100), QtCore.QSize(200, 50)))
        self.b1.clicked.connect(self.northSlot)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Down")
        self.b2.setGeometry(QtCore.QRect(QtCore.QPoint(300, 300), QtCore.QSize(200, 50)))
        self.b2.clicked.connect(self.southSlot)

        self.b3 = QtWidgets.QPushButton(self)
        self.b3.setText("Right")
        self.b3.setGeometry(QtCore.QRect(QtCore.QPoint(550, 200), QtCore.QSize(200, 50)))
        self.b3.clicked.connect(self.eastSlot)

        self.b4 = QtWidgets.QPushButton(self)
        self.b4.setText("Left")
        self.b4.setGeometry(QtCore.QRect(QtCore.QPoint(50, 200), QtCore.QSize(200, 50)))
        self.b4.clicked.connect(self.westSlot)

        self.b5 = QtWidgets.QPushButton(self)
        self.b5.setText("Reset")
        self.b5.setGeometry(QtCore.QRect(QtCore.QPoint(500, 500), QtCore.QSize(200, 100)))
        self.b5.clicked.connect(self.resetSlot)

        self.b6 = QtWidgets.QPushButton(self)
        self.b6.setText("Start")
        self.b6.setGeometry(QtCore.QRect(QtCore.QPoint(100, 500), QtCore.QSize(200, 100)))
        self.b6.clicked.connect(self.startSlot)


    def northSlot(self):
        print("north")
        self.set_direction("Defender", "simulation_target", "Path Point/north")

    def eastSlot(self):
        print("east")
        self.set_direction("Defender", "simulation_target", "Path Point/east")

    def westSlot(self):
        print("west")
        self.set_direction("Defender", "simulation_target", "Path Point/west")

    def southSlot(self):
        print("south")
        self.set_direction("Defender", "simulation_target", "Path Point/south")

    def resetSlot(self):
        print("reset")
        self.reset("Game Controller", "controller", "reset", "true")
        #stop placing objects once pressed
        self.place_objects_flag = True

    def reset(self, object_type, object_name, property, new_prop_val):
        # print("Setting " + property + " for " + name)

        url = "http://"+ "localhost" +"/SmartSpaceApi/api/ObjectProperties/" + object_type + '/' + object_name + '/' + property
        request_body = '"' + new_prop_val + '"'
        headers = {"Content-Type": "application/json"}
        response_code = requests.put(url, data=request_body, headers=headers)
        print(response_code)  # response code: 200=success, 400=prop could not be set
        return response_code

    def startSlot(self):
        print("start")
        try:
            self.object_names = [str(i) for i in range(1, 31)]

            # Start a separate thread for placing objects
            self.place_objects_thread = threading.Thread(target=self.place_objects)
            self.place_objects_thread.start()

        except Exception as e:
            print(f"Error during processing: {e}")

    def disable_buttons(self):
        # Disable all buttons
        self.b1.setEnabled(False)
        self.b2.setEnabled(False)
        self.b3.setEnabled(False)
        self.b4.setEnabled(False)
        self.b5.setEnabled(False)
        self.b6.setEnabled(False)

    def enable_buttons(self):
        # Enable all buttons
        self.b1.setEnabled(True)
        self.b2.setEnabled(True)
        self.b3.setEnabled(True)
        self.b4.setEnabled(True)
        self.b5.setEnabled(True)
        self.b6.setEnabled(True)

    def place_objects(self):
        object_names = [str(i) for i in range(1, 31)]
        for object_name in object_names:
            if not self.place_objects_flag:
                print("Object placement stopped.")
                break
            self.set_type_objects(object_name)
            self.set_object_properties("Intruding", object_name, "simulation_behaviour",
                                       "Simulation Behaviour/movement")
            self.set_object_properties("Intruding", object_name, "status", "Alive Status/Alive")
            self.set_object_properties("Intruding", object_name, "weapon", "Weapons/Crossbow")
            self.set_object_location(object_name)
            time.sleep(5)
            self.enable_buttons()


    def update_status_label(self, text):
        # Update the status label
        self.status_label.setText(text)

    def set_direction(self, object_name, property, new_prop_val):
        # print("Setting " + property + " for " + name)

        url = "http://"+ "localhost" +"/SmartSpaceApi/api/ObjectProperties/Defending/" + object_name + '/' + property
        request_body = '"' + new_prop_val + '"'
        headers = {"Content-Type": "application/json"}
        response_code = requests.put(url, data=request_body, headers=headers)
        print(response_code)  # response code: 200=success, 400=prop could not be set
        return response_code

    def set_type_objects(self, object_name):
        # Construct the URL
        url = f"http://localhost/SmartSpaceApi/api/TypeObjects/Intruding/{object_name}"

        # Print URL for debugging
        print("URL:", url)

        # Send the PUT request with the data
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, headers=headers)

        # Check the response status
        print(response.status_code)  # response code: 200=success, 400=prop could not be set
        print(response.text)  # Print response text for debugging
        return response

    def set_object_properties(self, object_type, object_name, property, value):
        url = "http://" + "localhost" + "/SmartSpaceApi/api/ObjectProperties/" + object_type + '/' + object_name + '/' + property
        request_body = json.dumps(value)
        # Print URL and request body for debugging
        print("URL:", url)
        print("Request Body:", request_body)

        # Send the PUT request with the data
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, data=request_body, headers=headers)

        # Check the response status
        print(response.status_code)  # response code: 200=success, 400=prop could not be set
        print(response.text)
        return response

    def set_object_location(self, object_name):
        url = "http://" + "localhost" + "/SmartSpaceApi/api/ObjectLocations/Intruding"
        data = [
            {
            "object": "Intruding/" + object_name,
            "x": 109.90,
            "y": 237.75,
            "z": 0,
            "theta": 0.57
         }
        ]
        request_body = json.dumps(data)

        # Print URL and request body for debugging
        print("URL:", url)
        print("Request Body:", request_body)

        # Delay their placement by 3 seconds
        timer = QTimer(self)
        timer.singleShot(7000, lambda: self.send_location_request(url, request_body))

        # Send the PUT request with the data
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, data=request_body, headers=headers)

        # Check the response status
        print(response.status_code)  # response code: 200=success, 400=prop could not be set
        print(response.text)
        return response

    def send_location_request(self, url, request_body):
        # Send the PUT request with the data
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, data=request_body, headers=headers)

        # Check the response status
        print(response.status_code)  # response code: 200=success, 400=prop could not be set
        print(response.text)


def window():
    app = QApplication(sys.argv)
    win = GameController()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()