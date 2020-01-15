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
      La connexion du client est ouverte. Se déclenche après l'ouverture
       la prise de contact Websockets est terminée et nous pouvons envoyer
       et recevoir des messages.
 
       Enregistrez le client en usine(factory), afin qu'il puisse le suivre.
       Essayez de trouver un partenaire de conversation pour ce client.
       """
        self.factory.register(self)
        self.factory.findPartner(self)
 
    def connectionLost(self, reason):
        """
       Le client a perdu la connexion, déconnecté ou une erreur.
       Supprimez le client de la liste des connexions suivies.
       """
        self.factory.unregister(self)
 
    def onMessage(self, payload, isBinary):
        """
       Message envoyé par le client, communiquez ce message à son interlocuteur,
       """
        self.factory.communicate(self, payload, isBinary)
 
 
 
class ChatRouletteFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(ChatRouletteFactory, self).__init__(*args, **kwargs)
        self.clients = {}
 
    def register(self, client):
        """
      
        Ajoutez le client à la liste des connexions gérées
       """
        self.clients[client.peer] = {"object": client, "partner": None}
 
    def unregister(self, client):
        """
       Supprimez le client de la liste des connexions gérées.
       """
        self.clients.pop(client.peer)
 
    def findPartner(self, client):
        """
       Trouvez un partenaire de chat pour un client. Vérifiez s'il y a des clients suivis
       est inactif. S'il n'y a pas de client inactif, quittez tranquillement. S'il y a
       partenaire disponible l'affecter à notre client.
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
      Message du courtier du client à son partenaire..
       """
        c = self.clients[client.peer]
        if not c["partner"]:
            c["object"].sendMessage("Désolé, vous n'avez pas encore de partenaire, revenez dans une minute")
        else:
            c["partner"].sendMessage(payload)
 
 
if __name__ == "__main__":
    log.startLogging(sys.stdout)
 
    # static file server seving index.html as root
    root = File(".")
 
    factory = ChatRouletteFactory(u"ws://127.0.0.1:8080", debug=True)
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)
 
    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()