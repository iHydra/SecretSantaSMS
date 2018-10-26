# Secret Santa SMS
Using Twilio API, send each Santa their Santee's name directly to their phone. Supports no-match 1-way and 2-way.

https://www.twilio.com/

### No Match 1-Way
  ['Chris', 'Johnny']
  
  Chris, the Santa, will not be given Johnny as their Santee. However, Johnny as a Santa can get Chris as a Santee. The purpose of this is to not get a repeat of a previous year(s) match.
  
### No Match 2-Way
  ['Jordan', 'Johnny']
  
  Jordan and Johnny are brothers, will not be given each other at all.

# Configuration

SMS Python QuickStart https://www.twilio.com/docs/sms/quickstart/python

Register on Twilio, add funds to the wallet. Purchase a phone number, create Programmable SMS project. Account SID and Auth Token are required for this to function along with the phone number.

Update `config.yml` with participants, 1-way and 2-way blocks. Edit `santa.py` with the new new `Account SID` and `auth_token` and `twilio_number`. Line `114` has the SMS message, feel free to customize as you find fit.

Put random name in `config.yml` >> `DONT-REPEAT` and `DONT-PAIR` if you do not want to have any blocks. i.e. `  - NoName`

### Credits

This code was derived from https://github.com/underbluewaters/secret-santa and modified to work with SMS (Twilio) and added the functionality of 1-way block. 
