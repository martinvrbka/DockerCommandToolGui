from fabric import Connection
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QWidget
import sys

class DockerGUIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docker GUI")

        # Create a central widget and set it
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter server address")
        layout.addWidget(self.address_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        layout.addWidget(self.password_input)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_multidocker)
        layout.addWidget(self.connect_button)

        self.container_input = QLineEdit()
        self.container_input.setPlaceholderText("Enter container number")
        self.container_input.setEnabled(False)  # disable input field until connection is established
        layout.addWidget(self.container_input)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_container)
        self.start_button.setEnabled(False)  # disable button until container number is entered
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_container)
        self.stop_button.setEnabled(False)  # disable button until container number is entered
        layout.addWidget(self.stop_button)

        self.restart_button = QPushButton("Restart")
        self.restart_button.clicked.connect(self.restart_container)
        self.restart_button.setEnabled(False)  # disable button until container number is entered
        layout.addWidget(self.restart_button)

        self.logs_button = QPushButton("Logs")
        self.logs_button.clicked.connect(self.logs_container)
        self.logs_button.setEnabled(False)  # disable button until container number is entered
        layout.addWidget(self.logs_button)

        self.container_list = QListWidget()
        layout.addWidget(self.container_list)

        # Add the layout to the central widget
        central_widget.setLayout(layout)

    def connect_to_multidocker(self):
        address = self.address_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        # Connect to the server using Fabric
        self.conn = Connection(host=address, user=username, connect_kwargs={"password": password})
        self.conn.run("")

# Run the "docker ps" command to list available containers
        result = self.conn.run("docker ps")
        # Split the output by newline and remove the first and last element
        container_list = result.stdout.split("\n")[1:-1]

        # Clear the container list widget and add the containers
        self.container_list.clear()

        for container in container_list:
            self.container_list.addItem(container)

        self.container_input.setEnabled(True)  # enable container input field
        self.container_input.textChanged.connect(self.enable_container_buttons)

    def enable_container_buttons(self):
        # check if container number is entered in the input field
        if self.container_input.text().strip() != "":
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.restart_button.setEnabled(True)
            self.logs_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.restart_button.setEnabled(False)
            self.logs_button.setEnabled(False)

    def start_container(self):
        container = self.container_input.text()
        self.conn.run(f"docker start {container}")

    def stop_container(self):
        container = self.container_input.text()
        self.conn.run(f"docker stop {container}")

    def restart_container(self):
        container = self.container_input.text()
        self.conn.run(f"docker restart {container}")

    def logs_container(self):
        container = self.container_input.text()
        self.conn.run(f"docker logs {container}")

    def closeEvent(self, event):
        self.conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DockerGUIApp()
    window.show()
    sys.exit(app.exec_())

