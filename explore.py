from twilio.rest import Client

#DON'T CHANGE THESE
ACCOUNT_ID = "AC60d011621f93dc3a30404c45975a7189"
AUTH_TOKEN = "a575a4fbac25f8f3b682d617bb0f028a"

client = Client(
    ACCOUNT_ID, AUTH_TOKEN
)

#since the messages are objects and you can get those sent by the Twilio account as a list
#you can iterate through them
#if you really want you can also delete them lol
# for msg in client.messages.list():
#     print(msg.body)
 

msg = client.messages.create(
    to="+16478666902", #REPLACE WITH DESIRED PHONE NUMBER (it's currently maggie's)
    from_="+17622357138", #DON'T CHANGE THIS!
    body="HELLO FROM MY COMPUTER"
)   

print(f"Created a new message: {msg.sid}") 