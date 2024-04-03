# PT-Devops-Task docs

## About

The first part of the technical test solution is implemented using **Python** and **SQL**, demonstrating the ability to interact with Docker containers and manage SQL databases. The program is structured around the main script, **main.py**, and a utility script, **utils.py**.

The main.py script serves as the entry point of the program. It establishes an **SSH connection to a Docker container running locally on port 2222** using the SSHConnector class from utils.py. Once connected, it **checks the version of an application (sql.jar)** using the APPUpdater class, updating it to a working version **if necessary**. It then makes a single SQL query and **uses the result to generate and print a 'report card'** using the ReportCard class. **In case of any exceptions, it sends a message via Discord and SMS using the NotificationSender class.**

The utils.py script contains all necessary classes (SSHConnector, APPUpdater, ReportCard, NotificationSender) for the program to function.

The program's **dependencies are listed in the requirements.txt** file and include **paramiko**, **pandas**, and **tabulate**. These can be installed using pip.

The second part of the technical test involves **log analysis using Bash commands**. This part of the test is is focused on parsing and analyzing server logs compressed with Zstandard (.gz files).

The program's source code and documentation are available on **[GitHub](https://github.com/vosmania/pt-devops-test)**. For more information, please contact me on **[LinkedIn](https://www.linkedin.com/in/oskarvosman/)**.
