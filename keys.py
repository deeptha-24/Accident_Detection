from twilio.rest import Client
account_sid =  'ACf7b85428cff4b8d53fb51ea70c2f2df5'
auth_token = 'c4bd446ad6657f6025bb7ed26ca407ec'
client = Client(account_sid, auth_token)


message = client.messages.create(
            body = "hi",
            from_ = "+15074458887", 
            to = "+919739561820"
        )
print(message.sid)