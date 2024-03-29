from utils import SSHConnector, APPUpdater, ReportCard, DiscordMessage

def main():
    try:
        # Connect to docker container with default info
        client = SSHConnector("localhost", "root", "sshpass1", 2222)
        client.connect()

        # Run the app updater
        updater = APPUpdater(client)
        updater.run()

        # Generate report card
        report = ReportCard(client)
        report.generate()

        print("\nFinished\n------------------------------------")

    except Exception as e:
        DiscordMessage(e).send()
    finally:
        # Disconnect from the server
        client.disconnect()


if __name__ == "__main__":
    main()
