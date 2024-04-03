## Dependencies

- python >=3.9.2
- twilio
- requests
- paramiko
- pandas
- tabulate

### Installing dependencies

    pip install -r requirements.txt

## Running the program from project root

    python3 main.py

## Expected output

| Student | Biology | Mathematics | Arts | Chemistry | Programming | Geography | Physics | Astronomy | History | Robotics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Abbigail Barrera (24) | 4 | 5 | 4 | 4 | 2 | 2 | 2 | 3 | 4 | 2 |
| Abigayle Hogan (23) | 2 | 4 | 5 | 2 | 2 | 2 | 2 | 2 | 3 | 3 |
| Adrian Abbott (25) | 4 | 2 | 3 | 4 | 3 | 4 | 5 | 2 | 5 | 5 |
| Aidyn Gilbert (30) | 3 | 5 | 4 | 4 | 4 | 4 | 3 | 2 | 4 | 3 |
| Alayna Hardy (31) | 3 | 5 | 5 | 4 | 2 | 2 | 2 | 2 | 2 | 3 |
| Aldo Leach (28) | 5 | 5 | 5 | 2 | 3 | 3 | 3 | 2 | 4 | 5 |
| Alijah Whitney (31) | 5 | 2 | 2 | 5 | 4 | 2 | 3 | 3 | 5 | 5 |
| Alondra Duran (23) | 2 | 2 | 2 | 5 | 3 | 4 | 5 | 4 | 5 | 3 |

## Error handling

Should the program run into any exceptions it will send out timestamped error messages via Discord and SMS (Twilio). Since I am using a Twilio trial to demonstrate this implementation, it means that messages can only be sent to my own phone number, however that also means that I can safely leave the API credentials in the code without any risk to myself.

### Discord Message

![Discord Message](img/discord.png)

### Twilio Message

![Twilio SMS](img/twilio.png)
