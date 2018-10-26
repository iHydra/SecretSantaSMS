import yaml, re, random, sys, getopt, os
from twilio.rest import Client

account_sid = 'ABC12345'  # Twilio Account ID
auth_token = 'abc54321'  # Twilio Auth Token
twilio_number = '+12345678900'  # Twilio Registered Phone Number
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')

#  Modify Line 114 to customize SMS message. Otherwise, a predefined will be sent.

client = Client(account_sid, auth_token)

class Person:
    def __init__(self, name, sms, invalid_matches):
        self.name = name
        self.sms = sms
        self.invalid_matches = invalid_matches

    def __str__(self):
        return "%s <%s>" % (self.name, self.sms)


class Pair:
    def __init__(self, giver, receiver):
        self.giver = giver
        self.receiver = receiver

    def __str__(self):
        return "%s ---> %s" % (self.giver.name, self.receiver.name)


def parse_yaml(yaml_path=CONFIG_PATH):
    return yaml.load(open(yaml_path))


def choose_receiver(giver, receivers):
    choice = random.choice(receivers)
    if choice.name in giver.invalid_matches or giver.name == choice.name:
        if len(receivers) is 1:
            raise Exception('Only one receiver left, try again')
        return choose_receiver(giver, receivers)
    else:
        return choice


def create_pairs(g, r):
    givers = g[:]
    receivers = r[:]
    pairs = []
    for giver in givers:
        try:
            receiver = choose_receiver(giver, receivers)
            receivers.remove(receiver)
            pairs.append(Pair(giver, receiver))
        except:
            return create_pairs(g, r)
    return pairs


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "shc", ["send"])
        except getopt.error as msg:
            raise Usage(msg)

        send = False
        for option, value in opts:
            if option in ("-s", "--send"):
                send = True

        config = parse_yaml()

        participants = config['PARTICIPANTS']
        dont_pair = config['DONT-PAIR']
        dont_repeat = config['DONT-REPEAT']
        if len(participants) < 2:
            raise Exception('Not enough participants specified.')

        givers = []
        for person in participants:
            name, sms = re.match(r'([^<]*)<([^>]*)>', person).groups()
            name = name.strip()
            invalid_matches = []
            for pair in dont_pair:
                names = [n.strip() for n in pair.split(',')]
                if name in names:
                    for member in names:
                        if name != member:
                            invalid_matches.append(member)
            for pair in dont_repeat:
                pairs = [n.strip() for n in pair.split(',')]
                if pairs[0] == name:
                    invalid_matches.append(pairs[1])

            print(name, invalid_matches)
            person = Person(name, sms, invalid_matches)
            givers.append(person)

        receivers = givers[:]
        pairs = create_pairs(givers, receivers)
        if not send:
            print("Test Pairings:\n%s" % "\n".join([str(p) for p in pairs]))
        for pair in pairs:
            to = pair.giver.sms
            if send:
                message = client.messages.create(body='\U0001F384 \U00002728Secret Santa 2018\U00002728 \U0001F384\n\n'
                + pair.giver.name + ", your pick for this year is...\n\n" + pair.receiver.name +
                "\n\nMinimum Spending: $75.00\nMaximum Spending: $100.00", from_=twilio_number, to=to)
                print("Sent to %s at %s" % (pair.giver.name, to))

    except Usage as err:
        print(sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg))
        return 2


if __name__ == "__main__":
    sys.exit(main())
