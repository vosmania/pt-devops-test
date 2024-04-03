import requests
import paramiko
import pandas as pd
from twilio.rest import Client
from tabulate import tabulate
import re
import datetime


class SSHConnector:
    """
    A class that represents an SSH connector.

    Attributes:
        hostname (str): The hostname or IP address of the remote server.
        username (str): The username used for authentication.
        password (str): The password used for authentication.
        port (int): The port number to connect to on the remote server.
        client (paramiko.SSHClient): The SSH client object.

    Methods:
        connect(): Connects to the remote server.
        disconnect(): Disconnects from the remote server.
        execute(command): Executes a command on the remote server and returns the output.

    """

    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        """
        Connects to the remote server.
        """
        self.client.connect(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            port=self.port,
        )

    def disconnect(self):
        """
        Disconnects from the remote server.
        """
        self.client.close()

    def execute(self, command):
        """
        Executes a command on the remote server and returns the output.

        Args:
            command (str): The command to execute on the remote server.

        Returns:
            str: The output of the command executed on the remote server.
        """
        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode()
        return output


class APPUpdater:
    """
    A class that handles updating the application.

    Attributes:
        client (object): The client object used for executing commands.
        working_dir (str): The working directory where the application is located.
        exec_string (str): The command used to execute the application.
        version_string (str): The expected version string of the application.
    """

    def __init__(self, client):
        self.client = client
        self.working_dir = "/opt/local/apps"
        self.exec_string = "java -jar sql.jar"
        self.version_string = "App version: 1.1"

    def get_version(self):
        """
        Get the current version of the application.

        Returns:
            bool: True if the current version matches the expected version, False otherwise.
        """
        result = self.client.execute(
            f"cd {self.working_dir} && {self.exec_string} -version"
        ).strip()
        version_check = result == self.version_string
        return version_check

    def update(self):
        """
        Update the application to the latest version.
        """
        print(f"\nCreating backup in {self.working_dir}/versions...")
        self.client.execute(
            f"cp {self.working_dir}/sql.jar {self.working_dir}/versions/sql@1.0.jar"
        )
        print("\nDecompressing new version...")
        self.client.execute(f"zstd -d {self.working_dir}/versions/sql.jar.zst")
        print("\nUpdating app...")
        self.client.execute(
            f"cp {self.working_dir}/versions/sql.jar {self.working_dir}/sql.jar"
        )

    def run(self):
        """
        Run the application update process.

        Raises:
            Exception: If the application update fails.
        """
        if not self.get_version():
            print("\nApp version 1.0\nResolving...\n")
            self.update()
            if self.get_version():
                print("\nSuccess! Version is now 1.1")
            else:
                raise Exception("App update failed")
        else:
            print(f"\n{self.version_string}\nNo update needed")


class ReportCard:
    """
    A class representing a report card generator.

    Attributes:
        query_str (str): The SQL query used to fetch the report card data.
        client: The client object used to execute the SQL query.

    Methods:
        __init__(self, client): Initializes a new instance of the ReportCard class.
        generate(self): Generates the report card.
        clean_output(self, data_in): Cleans the output data by removing unnecessary patterns.
    """

    query_str = """
    SELECT
        students.name,
        students.age,
        classes.name AS class_name,
        grades.grade
    FROM students
    JOIN grades ON students.id = grades.student_id
    JOIN classes ON grades.class_id = classes.id
    """

    def __init__(self, client):
        """
        Initializes a new instance of the ReportCard class.

        Args:
            client: The client object used to execute the SQL query.
        """
        self.client = client

    def generate(self):
        """
        Generates the report card.
        """
        print("\nGenerating report card...")
        data = self.client.execute(
            f"cd /opt/local/apps && java -jar sql.jar -query '{self.query_str}'"
        ).strip()
        data = self.clean_output(data)
        rows = data.split("\n")
        # split rows and create a dataframe
        data_list = [row.split(",") for row in rows]
        df = pd.DataFrame(data_list, columns=["Name", "Age", "class_name", "Grade"])
        # create Student column as in example
        df["Student"] = df["Name"] + " (" + df["Age"].astype(str) + ")"
        # pivot the classes to create a report card style table
        report_card = df.pivot(
            index="Student", columns="class_name", values="Grade"
        )
        # get the unique class names and reorder the columns to match the original order
        class_names = df["class_name"].unique()
        report_card = report_card[class_names]
        # use tabulate for a prettier table, add a couple newlines for readability
        print("\n", tabulate(report_card, headers="keys", tablefmt="grid"))

    def clean_output(self, data_in):
        """
        Cleans the output data by removing unnecessary patterns.

        Args:
            data_in (str): The input data to be cleaned.

        Returns:
            str: The cleaned output data.
        """
        patterns = [" \(name\)", " \(age\)", " \(class_name\)", " \(grade\)", ""]
        for pattern in patterns:
            data_in = re.sub(pattern, "", data_in)
        data_in = re.sub(", ", ",", data_in)
        return data_in

class NotificationSender:
    """
    Represents a unified notification sender that can send messages to Discord and SMS via Twilio.
    """

    def __init__(self, exception):
        """
        Initializes a new instance of the NotificationSender class.

        Args:
            exception (Exception): The exception that occurred.
        """
        self.exception = exception
        self.discord_webhook_url = "your_discord_webhook_url_here"
        self.twilio_account_sid = 'your_account_sid_here'
        self.twilio_auth_token = 'your_auth_token_here'
        self.twilio_phone_number = 'your_twilio_phone_number_here'
        self.to_phone_number = 'your_phone_number_here'

    def send_discord_message(self):
        """
        Sends the Discord message to the webhook URL.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if hasattr(self.exception, 'strerror'):
            message = f"Error occurred at {timestamp}: {self.exception.strerror}"
        else:
            message = f"Error occurred at {timestamp}: {str(self.exception)}"
        data = {"content": message}
        response = requests.post(self.discord_webhook_url, json=data)
        if response.status_code == 204:
            print("Discord message sent successfully.")
        else:
            print("Failed to send Discord message, check webhook URL.")

    def send_sms_via_twilio(self):
        """
        Sends an SMS via Twilio.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if hasattr(self.exception, 'strerror'):
            message_body = f"Error occurred at {timestamp}: {self.exception.strerror}"
        else:
            message_body = f"Error occurred at {timestamp}: {str(self.exception)}"
        client = Client(self.twilio_account_sid, self.twilio_auth_token)
        message = client.messages.create(
            body=message_body,
            from_=self.twilio_phone_number,
            to=self.to_phone_number
        )
        print(f"SMS ID: {message.sid} was sent to {self.to_phone_number}")

    def send_notifications(self):
        """
        Sends notifications to both Discord and via SMS.
        """
        self.send_discord_message()
        # uncomment the next line if you want to send an SMS via Twilio (credentials required)
        # self.send_sms_via_twilio()
