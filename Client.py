# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 12:27:27 2020

@author: admin1
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 00:18:58 2020
@author: BADOHOUN
"""


#!/usr/bin/python


#Méthodes de l'objet WebSocket

#- send (msg) : envoie un message textuel au serveur. Pour envoyer des données structurées au serveur, on les encodera au préalable en JSON par exemple.

#- close : ferme la connexion au serveur.


# WebSocket Protocol est un standard ouvert pour le développement d'applications en temps réel. 

#Il fournit une connexion persistante entre un client et un serveur 

#que les deux parties peuvent utiliser pour commencer à envoyer des données à tout moment avec ou sans connexion. 


#Lorsque vous pouvez vous connecter au tunnel, vous n'avez pas besoin d'inspecter n'importe quel élément, il vous suffit d'inspecter ce qu'il faut envoyer au tunnel, et vous pourrez récupérer vos données en continu.

from websocket import create_connection

# on crée un objet websocket en lui passant en paramètre l'adresse ip de serveur 
# ouvrant ainsi la communication avec le serveur 
# l'adresse d'un serveur est composée d'un préfixe ws:// 
# ou wss:// s'il est sécurisé par un certificat SSL
ws = create_connection("ws://localhost:8080/")
print ("Sending 'Hello, World'...")

# la comande ws.send(message) permet d'envoyer n'importe quel message au serveur

# On peut envoyer n'importe quel type de données 


# Une chaine de caractère avec un séparateur de données quelconque(| :-,),
# un JSON (pour cela on pourra utiliser le package JSON pour python),
# des données binaires ((une image par exemple))
ws.send("Hello, World")
print ("Sent")
print ("Receiving...")
result =  ws.recv()
print ("Received '%s'" % result)
ws.close()