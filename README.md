# websocket Python pour un démonstrateur en temps réel 

Il s'agit d'un référentiel pour nous aider à exécuter notre premier websocket python (coté serveur et client)

Il existe deux versions du protocole websocket :

1.  Version standard comme le http

2. Version sécurisée / crypté comme le https  


la notation d'une url websocket se fait de manière proche à celle d'une connexion http et utilise les memes ports par défaut (80,443)


Dans le premier cas la notation est ws://url-site[:port] et pour la version securisée wss://url_site[:port]
Impossible d'ouvrir une websocket standard sur un site en https 

Deux canaux d'ouverts en meme temps 

* Un pour les envois 
* L'autre pour la réception 

Nous pouvons recevoir aussi bien du binaire que du texte dans les messages


1. Initilaisez une websocket 
2. Exécuter une action à l'ouverture (on open)
3. Exécuter une action en cas d'erreurs (on_error)
4. Exécuter une action en cas de réception des données (on_message)
5. Fermeture connexion (on_close)






