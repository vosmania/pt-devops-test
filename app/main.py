from utils import SSHConnector, APPUpdater, ReportCard, NotificationSender

def main():
    try:
        # Connect to docker container with default info
        # Storing credentials like this is something I would normally never do.
        client = SSHConnector("localhost", "root", "sshpass1", 2222)
        client.connect()

        # Run the app updater
        updater = APPUpdater(client)
        updater.run()

        # Generate report card
        report = ReportCard(client)
        report.generate()

        print("\nFinished\n------------------------------------")
    # in case of any exception, catch it and send it over Discord and SMS via Twilio
    except Exception as e:
        print(f"\nError: {e}")
        notifier = NotificationSender(e)
        notifier.send_notifications()
    finally:
        # Disconnect from the server
        client.disconnect()


if __name__ == "__main__":
    main()
