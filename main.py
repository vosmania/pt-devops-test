import time
from utils import SSHConnector, APPUpdater, ReportCard

def main():
    # Connect to docker container with default info
    client = SSHConnector('localhost', 'root', 'sshpass1', 2222)
    client.connect()

    # Run the app updater
    start_time = time.time()
    updater = APPUpdater(client)
    updater.run()
    update_time = time.time() - start_time
    print(f"Update time: {update_time:.2f} seconds")

    # Generate report card
    start_time = time.time()
    report = ReportCard(client)
    report.generate()
    report_time = time.time() - start_time
    print(f"Report generation time: {report_time:.2f} seconds")

    # Disconnect from the server
    client.disconnect()

    total_time = update_time + report_time
    print(f"Total execution time: {total_time:.2f} seconds")

if __name__ == '__main__':
    main()