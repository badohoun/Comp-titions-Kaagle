# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:32:39 2020

@author: BADOHOUN
"""


import sys
import random
 
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
 
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol
 
from autobahn.twisted.resource import WebSocketResource
 
 
class SomeServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        """
       Connection from client is opened. Fires after opening
       websockets handshake has been completed and we can send
       and receive messages.
 
       Register client in factory, so that it is able to track it.
       Try to find conversation partner for this client.
       """
        self.factory.register(self)
        self.factory.findPartner(self)
 
    def connectionLost(self, reason):
        """
       Client lost connection, either disconnected or some error.
       Remove client from list of tracked connections.
       """
        self.factory.unregister(self)
 
    def onMessage(self, payload, isBinary):
        """
       Message sent from client, communicate this message to its conversation partner,
       """
        self.factory.communicate(self, payload, isBinary)
 
 
 
class ChatRouletteFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(ChatRouletteFactory, self).__init__(*args, **kwargs)
        self.clients = {}
 
    def register(self, client):
        """
       Add client to list of managed connections.
       """
        self.clients[client.peer] = {"object": client, "partner": None}
 
    def unregister(self, client):
        """
       Remove client from list of managed connections.
       """
        self.clients.pop(client.peer)
 
    def findPartner(self, client):
        """
       Find chat partner for a client. Check if there any of tracked clients
       is idle. If there is no idle client just exit quietly. If there is
       available partner assign him/her to our client.
       """
        available_partners = [c for c in self.clients if c != client.peer and not self.clients[c]["partner"]]
        if not available_partners:
            print("no partners for {} check in a moment".format(client.peer))
        else:
            partner_key = random.choice(available_partners)
            self.clients[partner_key]["partner"] = client
            self.clients[client.peer]["partner"] = self.clients[partner_key]["object"]
 
    def communicate(self, client, payload, isBinary):
        """
       Broker message from client to its partner.
       """
        c = self.clients[client.peer]
        if not c["partner"]:
            c["object"].sendMessage("Sorry you dont have partner yet, check back in a minute")
        else:
            c["partner"].sendMessage(payload)
 







            
    #         class SomeServerProtocol(WebSocketServerProtocol):
    # def onOpen(self):
    #     """
    #    Connection from client is opened. Fires after opening
    #    websockets handshake has been completed and we can send
    #    and receive messages.
 
    #    Register client in factory, so that it is able to track it.
    #    Try to find conversation partner for this client.
    #    """
    #     self.factory.register(self)
    #     self.factory.findPartner(self)
 
    # def connectionLost(self, reason):
    #     """
    #    Client lost connection, either disconnected or some error.
    #    Remove client from list of tracked connections.
    #    """
    #     self.factory.unregister(self)
 
    # def onMessage(self, payload, isBinary):
    #     """
    #    Message sent from client, communicate this message to its conversation partner,
    #    """
    #     self.factory.communicate(self, payload, isBinary)
    # if __name__ == "__main__":
    # log.startLogging(sys.stdout)
 
    # # static file server seving index.html as root
    # root = File(".")
 
    # factory = ChatRouletteFactory(u"ws://127.0.0.1:8080")
    # factory.protocol = SomeServerProtocol
    # resource = WebSocketResource(factory)
    # # websockets resource on "/ws" path
    # root.putChild(u"ws", resource)
 
    # site = Site(root)
    # reactor.listenTCP(8080, site)
    # reactor.run()
  
    
  
#Le code ci-dessus ajoute un protocole Websockets simple qui ne fait que répondre à chaque message avec un message assez stupide: «message reçu». 


# Ce n'est pas grave, mais c'est plutôt bien car à ce stade, 


# nous  avons réellement un serveur Websockets fonctionnel. 

# Il n'y a pas encore de code websockets côté client, 

# mais vous pouvez tester votre serveur avec des clients websockets en ligne de commande ou une extension de navigateur, 


#  par exemple avec l'extension Chrome «Simple WebSocket Client». Exécutez simplement votre server.py et envoyez une requête ping à ws: // localhost: 8080 / ws à partir de l'extension Chrome.  
    
    
    
    
    
    
    
    
    
    
    
    
    # Avant de commencer le développement de websockets côté serveur, 

# nous  devons configurer quelque chose qui servira 


# le fichier index.html avec JavaScript + HTML côté client 

# pour gérer l'interaction utilisateur avec votre serveur websocket.
            
# Enregistrons -le sous server.py 

# et créons le fichier index.html dans le même répertoire. 

# Index.html peut être vide pour l'instant, nous écrirons du HTML dans un instant.

    
if __name__ == "__main__":
    log.startLogging(sys.stdout)
 
    # static file server seving index.html as root
    root = File(".")
 
    factory = ChatRouletteFactory(u"ws://127.0.0.1:8080")
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)
 
    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()
    
    



# Maintenant que nous avons le squelette de base du projet websockets, 



# nous pouvons commencer à ajouter des fonctionnalités réelles. 




# La première chose que nous devons faire est d'enregistrer et de désinscrire les clients commençant des conversations avec notre serveur. 



# Pour ce faire, nous devrons ajouter une usine à notre protocole. 



# Dans Twisted, des protocoles sont créés par connexion et vous permettent de définir des écouteurs d'événements pour votre application. 



# Dans le cas des sockets Web, cela signifie que votre protocole peut définir des gestionnaires d'événements pour les scénarios courants: message envoyé, connexion établie, connexion perdue, etc. 


# Les usines(factory) fabriquent en revanche des protocoles. 


# Ils sont communs à plusieurs protocoles, 


# ils définissent comment les protocoles doivent interagir les uns avec les autres.

# Dans le cas de notre roullette de chat, tout cela signifie qu'en plus d'écrire le protocole, 


# nous avons juste besoin d'écrire l'usine(factory) qui définira comment les clients websocket interagiront entre eux. 


# Bien sûr, nous devons également définir des protocoles pour spécifier comment allons-nous gérer les événements Websockets typiques.

# Commençons par le protocole. 


# Notre classe de base ressemblera à ceci, 

# pas de vrai code pour l'instant juste une docstring 

# et une structure de base de notre objet.





# La mise en œuvre de notre protocole ressemblerait à ceci:





# class SomeServerProtocol(WebSocketServerProtocol):
#     def onOpen(self):
#         self.factory.register(self)
#         self.factory.findPartner(self)

#     def connectionLost(self, reason):
#         self.factory.unregister(self)

#     def onMessage(self, payload, isBinary):
#         self.factory.communicate(self, payload, isBinary)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# Maintenant que nous avons notre protocole, 

# nous devons définir des fonctionnalités communes par protocole 

# et ajouter un moyen de gérer les interactions entre les protocoles. 


# Notre usine de protocole de base pourrait ressembler à ceci.


# class ChatRouletteFactory(WebSocketServerFactory):
#     def register(self, client):
#         """
#         Add client to list of managed connections.
#         """
#         pass

#     def unregister(self, client):
#         """
#         Remove client from list of managed connections.
#         """
#         pass

#     def findPartner(self, client):
#         """
#         Find chat partner for a client. Check if there any of tracked clients
#         is idle. If there is no idle client just exit quietly. If there is
#         available partner assign him/her to our client.
#         """
#         pass

#     def communicate(self, client, payload, isBinary):
#         """
#         Broker message from client to its partner.
#         """
#         pass
    
    
    
# et la mise en œuvre de cela pourrait ressembler à ceci:

# class ChatRouletteFactory(WebSocketServerFactory):
#     def __init__(self, *args, **kwargs):
#         super(ChatRouletteFactory, self).__init__(*args, **kwargs)
#         self.clients = {}

#     def register(self, client):
#         self.clients[client.peer] = {"object": client, "partner": None}

#     def unregister(self, client):
#         self.clients.pop(client.peer)

#     def findPartner(self, client):
#         available_partners = [c for c in self.clients if c != client.peer 
#                               and not self.clients[c]["partner"]]
#         if not available_partners:
#             print("no partners for {} check in a moment".format(client.peer))
#         else:
#             partner_key = random.choice(available_partners)
#             self.clients[partner_key]["partner"] = client
#             self.clients[client.peer]["partner"] = self.clients[partner_key]["object"]

#     def communicate(self, client, payload, isBinary):
#         c = self.clients[client.peer]
#         if not c["partner"]:
#             c["object"].sendMessage("Sorry you dont have partner yet, check back in a minute")
#         else:
#             c["partner"].sendMessage(payload)
    
    
   # Maintenant que nous avons tout défini, 
   
   # il vous suffit de le lier ensemble, 
   
   # de créer des instances d'objets et de démarrer votre programme:
   
   
   # if __name__ == "__main__":
   #  log.startLogging(sys.stdout)

   #  # static file server seving index.html as root
   #  root = File(".")

   #  factory = ChatRouletteFactory(u"ws://127.0.0.1:8080", debug=True)
   #  factory.protocol = SomeServerProtocol
   #  resource = WebSocketResource(factory)
   #  # websockets resource on "/ws" path
   #  root.putChild(u"ws", resource)

   #  site = Site(root)
   #  reactor.listenTCP(8080, site)
   #  reactor.run()
   
   
   
# Avec le code ci-dessus, on doit pouvoir  parler via notre serveur de chat. 

# Ouvrons simplement quelques onglets du navigateur 

# et commencons par écrire dans chaque zone de saisie. 


# Il y a probablement beaucoup de choses qui pourraient être améliorées, 


# mais je voulais juste créer une démo très basique qui pourrait faire démarrer le projet


