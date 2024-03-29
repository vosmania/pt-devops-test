import paramiko
import pandas as pd
from tabulate import tabulate
import re

class SSHConnector:
    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.client.connect(hostname=self.hostname, username=self.username, password=self.password, port=self.port)
        except Exception as e:
            raise e

    def disconnect(self):
        self.client.close()

    def execute(self, command):
        try:
            print(f"\n>> {command}")
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode()
        except Exception as e:
            print("\nFailed")
            raise e
        print("\nOK")
        return output

class APPUpdater:
    def __init__(self, client):
        self.client = client
        self.working_dir = '/opt/local/apps'
        self.exec_string = 'java -jar sql.jar'
        self.version_string = 'App version: 1.1'

    def get_version(self):
        
        try:
            result = self.client.execute(f'cd {self.working_dir} && {self.exec_string} -version').strip()
            version_check = result == self.version_string
            return version_check
        except Exception as e:
            raise e

    def update(self):
        try:
            print(f"\nCreating backup in {self.working_dir}/versions...")
            self.client.execute(f'cp {self.working_dir}/sql.jar {self.working_dir}/versions/sql@1.0.jar')
            print("\nDecompressing new version...")
            self.client.execute(f'zstd -d {self.working_dir}/versions/sql.jar.zst')
            print("\nUpdating app...")
            self.client.execute(f'cp {self.working_dir}/versions/sql.jar {self.working_dir}/sql.jar')
        except Exception as e:
            raise e

    def run(self):
        if self.get_version():
            print("\nVersion is 1.1\n")
        else:
            print("\nAttempting app update")
            self.update()
            if self.get_version():
                print("\nSuccess! Version is now 1.1")
            else:
                raise Exception("App update failed")


class ReportCard:
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
        self.client = client

    def generate(self):
        data = self.client.execute(f"cd /opt/local/apps && java -jar sql.jar -query '{self.query_str}'").strip()
        data = self.clean_output(data)
        rows = data.split('\n')
        # split rows and create a dataframe
        data_list = [row.split(',') for row in rows]
        df = pd.DataFrame(data_list, columns=['Name', 'Age', 'class_name', 'Grade'])
        # create Student column as in example
        df['Student'] = df['Name'] + ' (' + df['Age'].astype(str) + ')'
        # pivot the classes to create a report card style table
        report_card = df.pivot(index='Student', columns='class_name', values='Grade')
        # get the unique class names and reorder the columns to match the original order
        class_names = df['class_name'].unique()
        report_card = report_card[class_names]
        # use tabulate for a prettier table, add a couple newlines for readability
        print("\n\n",tabulate(report_card, headers='keys', tablefmt='grid'))

    def clean_output(self, data_in):
        patterns = [' \(name\)', ' \(age\)', ' \(class_name\)', ' \(grade\)', '']
        for pattern in patterns:
            data_in = re.sub(pattern, '', data_in)
        data_in = re.sub(', ', ',', data_in)
        return data_in