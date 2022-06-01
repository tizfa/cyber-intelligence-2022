# cyber-intelligence-2022
Soluzione dockerizzata per NiFi e Elasticsearch. Il progetto sarà utilizzato nell'ambito del corso 2022 di "Cyber Intelligence" del master in CyberSecurity dell'Università di Pisa

## Istruzioni per utilizzare la soluzione dockerizzata

1. Scaricate e installate Docker Desktop da https://www.docker.com/products/docker-desktop/#
2. Scaricare la soluzione dockerizzata da  https://github.com/tizfa/cyber-intelligence-2022 all’interno di una cartella locale utilizzando uno dei metodi possibili (ad esempio pacchetto zip oppure tramite il comando git clone). Ad esempio tramite git potete scaricare il progetto con il seguente comando  
`git clone https://github.com/tizfa/cyber-intelligence-2022.git` Se non avete installato git sulla vostra macchina potete eseguire le istruzioni disponibili su https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.
3. Posizionatevi con una shell all’interno della cartella contenente i file del progetto
4. Eseguite il comando  
`docker-compose up`  
per runnare la soluzione docker
5. La prima volta che invocherete il comando docker-compose verrano scaricate e opportunamente create le varie immagini Docker (una per ES, una per Kibana e una per Nifi) che compongono la soluzione, l’operazione potrebbe richiedere un po’ di tempo quindi armatevi di pazienza…  
Dopo che le immagini delle varie macchine saranno pronte, saranno istanziate e pronte per l’uso. In particolare, 
      - potrete accedere a Nifi collegandovi all’indirizzo [https://localhost:8443/nifi/](https://localhost:8443/nifi/) . Per l'accesso vi sarà richiesto username e password, inserite come username *user* e password *cyberintelligence*.
      - potrete accedere a Kibana all’indirizzo [http://localhost:5601/app/home#/](http://localhost:5601/app/home#/)
      
      **N.B.: il comando `docker-compose up` rimane in esecuzione a tempo indefinito perchè serve a lanciare in foreground i software elasticsearch, kibana e nifi. Se volete terminare l'esecuzione dei software dovete farlo in modo esplicito terminando da shell il comando docker-compose con un CTRL-c.**


La soluzione dockerizzata viene eseguita all'interno di una rete privata composta da 3 macchine:
- es-container: nome della VM contenente l'istanza di Elasticsearch
- kb-container: nome della VM contenente l'istanza di Kibana
- nifi-container: nome della VM contenente l'istanza di Nifi.

Da ciascuna di queste macchine si può comunicare con le altre riferendosi con il nome macchina riportato sopra, ad esempio nel processore PutElasticsearchHttp di Nifi posso connettermi al web service esposto da `elasticsearch` utilizzando l'url http://es-container:9200.
