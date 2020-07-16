 # Getting started

## WebApp

All'interno della cartella *team12Hackathon_webapp* modificare il Dockerfile valorizzando le variabili d'ambiente:

    # insert here your api tim url
    ENV API_URL_TIM=""
    
    # insert here your api token
    ENV API_TOKEN_TIM=""

per la configurazione delle API di TIM.
Dopodiche`, lanciare l'applicaitvo il docker-compose:

    docker-compose -f docker-compose.yml up -d --build

Recarsi alla pagina **http://127.0.0.1:7766**

Credenziali di accesso webapp admin **admin / A89TmbUycYKZheP63JY** (anche per django-admin http://127.0.0.1:7766/admin)

## Dispatcher e SocketIO server

All'interno delle cartelle *team12Hackathon-dispatcher* e *team12Hackathon-socket-io* lanciare lo script per la build del docker:

    ./build-docker.sh
per lanciare il servizio:

    run-image.sh
    
## RabbitMQ

All'interno della cartella *team12Hackathon-services* lanciare il comando:

    docker-compose up -d
##  Mockup IoT Device

Scaricare ed estrarre cURL all'interno della cartella *team12Hackathon-mockup-iot*. Previa installazione della toolchain di compilazione di g++, lanciare il comando:

    g++ -o SmartBin_emulator SmartBin_emulator.cpp
per ottenere l'eseguibile.
