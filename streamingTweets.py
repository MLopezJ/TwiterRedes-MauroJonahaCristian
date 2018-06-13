from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

correo = MIMEMultipart()
correo['from'] = "maurocristianjohannaenredes@gmail.com"
correo['To'] = "lopezjimenezmauro05@gmail.com"
correo['Subject'] = 'Tweet Redes'
password = "nosganamosun100!"

def envCorreo(bodyParametro):
    body = bodyParametro
    correo.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(correo['from'], password)
    server.sendmail(correo['from'], correo['To'], correo.as_string())
    server.quit()

contadorDeTweetsStreaming = 0
listaTweetsAEnviarPorCorreoCadaDiezStreaming = []

#consumer key, consumer secret, access token, access secret.
ckey="4OctRbQqpNjYJWzCWlHkI0VNQ"
csecret="WTOqwdZsMLoqvEe7ORXGEIqRVMeluZeTdwpTLhXYPnwSgxL05H"
atoken="838988510-WVyOJsl4cP76jUCGxQxWeSljWtsRi48UrUeIC11p"
asecret="cgmEGwo2sbde4LSR9kj3swrpUAxR4TNJg4aNKMdr9y7LW"

def prettyText(listaTweets):
    text = ""
    num = 1
    for t in listaTweets:
        text += str(num) +" "+ t.get("nombre") +"("+t.get("nombreDeUsuario")+")"+":"+ t.get("texto")+"\n"
        num+=1
    return(text)

hashtag = '#intentadoSalvarElSemestreConRojo'
print(hashtag)
listaTweetsAEnviarPorCorreoCadaDiezStreaming = []

class listener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        listaTweetsAEnviarPorCorreoCadaDiezStreaming.append({
            "nombre": data.get("user").get("name"), "nombreDeUsuario": data.get("user").get("screen_name"),
            "texto": data.get("text"), "fechaCreacion": data.get("created_at"), "idTweet": data.get("id_str")
        })
        print(len(listaTweetsAEnviarPorCorreoCadaDiezStreaming))
        if len(listaTweetsAEnviarPorCorreoCadaDiezStreaming) == 2:
            envCorreo(str(listaTweetsAEnviarPorCorreoCadaDiezStreaming))
            print(listaTweetsAEnviarPorCorreoCadaDiezStreaming)
            listaTweetsAEnviarPorCorreoCadaDiezStreaming.clear()
        return(True)

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=[hashtag])