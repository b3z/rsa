# Client Sicht
Der Client sendet eine Nachricht an den Server nach dem Handshake.
Diese ist verschlüsselt und wird mittels des shared Secrets nach dem Diffie Hellmann Key Exchange vom Server entschlüsselt.

![](img/2022-09-18-15-37-24.png)

# Server Sicht 

Das sind hier bei verschiedene Maschinen im selben Netzwerk

![](img/2022-09-18-15-42-45.png)
# Ablauf eines Handshakes und das Senden und einer verschlüsselten Nachricht

Client Hello

![](img/2022-09-18-15-34-28.png)

Server Hello

![](img/2022-09-18-15-34-49.png)

Austausch des client Public Keys

![](img/2022-09-18-15-35-31.png)

Austausch Zwischenergebnisse

![](img/2022-09-18-15-35-45.png)

![](img/2022-09-18-15-35-58.png)

Senden einer verschlüsselten Nachricht

![](img/2022-09-18-15-36-24.png)
