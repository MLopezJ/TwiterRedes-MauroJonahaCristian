import tweepy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
fromaddr = 'maurocristianjohannaenredes@gmail.com'
toaddrs = 'lopezjimenezmauro05@gmail.com'
msg = 'Correo enviado utilizano Python + smtplib en www.pythondiario.com'
subject = "Prueba"


username = 'maurocristianjohannaenredes@gmail.com'
password = 'nosganamosun100!'
"""

#enviar correo
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

def prettyText(listaTweets):
    text = ""
    num = 1
    for t in listaTweets:
        text += str(num) +" "+ t.get("nombre") +"("+t.get("nombreDeUsuario")+")"+":"+ t.get("texto")+"\n"
        num+=1
    return(text)



# Autentificacion
consumer_key = '4OctRbQqpNjYJWzCWlHkI0VNQ' #CONSUMER_KEY_AQUI
consumer_secret = 'WTOqwdZsMLoqvEe7ORXGEIqRVMeluZeTdwpTLhXYPnwSgxL05H' #CONSUMER_KEY_AQUI

access_token = '838988510-WVyOJsl4cP76jUCGxQxWeSljWtsRi48UrUeIC11p'
access_token_secret = 'cgmEGwo2sbde4LSR9kj3swrpUAxR4TNJg4aNKMdr9y7LW'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Buscar tweets
hashtag = '#intentadoSalvarElSemestreConRojo'
public_tweets = api.search(q=hashtag,count=1000)

contadorDeTweets = 0
listaTweetsAEnviarPorCorreoCadaDiez = []


for tweet in public_tweets:

    if contadorDeTweets % 10 == 0 and contadorDeTweets != 0:
        #enviar correo
        print("enviar correo")
        tweetTexto = prettyText(listaTweetsAEnviarPorCorreoCadaDiez)
        print("\n"+  tweetTexto + "\n")

        envCorreo(tweetTexto)
        print(listaTweetsAEnviarPorCorreoCadaDiez)
        print(len(listaTweetsAEnviarPorCorreoCadaDiez))
        print("----")
        listaTweetsAEnviarPorCorreoCadaDiez = []

    #insertar en base de datos
    #print (contadorDeTweets, tweet.user._json["name"], tweet.user._json["screen_name"],tweet.text,tweet.created_at, tweet._json["id_str"] )
    listaTweetsAEnviarPorCorreoCadaDiez.append({
        "nombre":tweet.user._json["name"], "nombreDeUsuario":tweet.user._json["screen_name"],
        "texto":tweet.text,"fechaCreacion":tweet.created_at,"idTweet": tweet._json["id_str"]
    })
    contadorDeTweets +=1


if len(listaTweetsAEnviarPorCorreoCadaDiez) != 0:
    print("quedaron estos", len(listaTweetsAEnviarPorCorreoCadaDiez))
    print(listaTweetsAEnviarPorCorreoCadaDiez)
    tweetTexto=prettyText(listaTweetsAEnviarPorCorreoCadaDiez)
    envCorreo(tweetTexto)
print("Empieza monitoreo en tiempo real")
exec(open("./streamingTweet.py").read())