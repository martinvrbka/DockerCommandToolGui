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

        self.list_containers_button = QPushButton("List Containers")
        self.list_containers_button.clicked.connect(self.list_docker_containers)
        layout.addWidget(self.list_containers_button)

        self.command_button = QPushButton("Apply Command")
        self.command_button.clicked.connect(self.apply_docker_command)
        layout.addWidget(self.command_button)

        self.container_list = QListWidget()
        layout.addWidget(self.container_list)

        # Add the layout to the central widget
        central_widget.setLayout(layout)

    # rest of the code...
    def connect_to_multidocker(self):
        address = self.address_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        # Connect to the server using Fabric
        self.conn = Connection(host=address, user=username, connect_kwargs={"password": password})
        self.conn.run()

    def list_docker_containers(self):
        # Run the "docker ps" command
        result = self.conn.run("docker ps")
        # Split the output by newline and remove the first and last element
        container_list = result.stdout.split("\n")[1:-1]

        # Clear the container list widget and add the containers
        self.container_list.clear()

        for container in container_list:
            self.container_list.addItem(container)

    def apply_docker_command(self):
        command = self.select_docker_command()
        selected_container = self.container_list.currentItem().text().split()[0]
        # Run the command on the selected container
        self.conn.run(f"docker {command} {selected_container}")

    def select_docker_command(self):
        print("Select a Docker command:")
        print("1. start")
        print("2. stop")
        print("3. restart")
        print("4. logs")
        command = input()
        if command == "1":
            return "start"
        elif command == "2":
            return "stop"
        elif command == "3":
            return "restart"
        elif command == "4":
            return "logs"
        else:
            print("Invalid command. Try again.")
            self.select_docker_command()

    def closeEvent(self, event):
        self.conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DockerGUIApp()
    window.show()
    sys.exit(app.exec_())

