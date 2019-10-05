#include <ESP8266WiFi.h>  
#include <PubSubClient.h>
#include <Wire.h>
#include "Adafruit_MCP9808.h"
 
//defines
#define SSID_REDE     "teste" 
#define SENHA_REDE    "12345678" 
#define INTERVALO_ENVIO_THINGSPEAK  30000  
 
//constantes e variáveis globais
char EnderecoAPIThingSpeak[] = "api.thingspeak.com";
String ChaveEscritaThingSpeak = "34VKCO5MTXCTUPLA";
long lastConnectionTime; 
WiFiClient client;
const char* BROKER_MQTT = "teste_pse";
int BROKER_PORT         = 1883;
 
//prototypes
void EnviaInformacoesThingspeak(String StringDados);
void FazConexaoWiFi(void);
float FazLeituraUmidade(void);
void initMQTT(); 

void EnviaInformacoesThingspeak(String StringDados){
    if (client.connect(EnderecoAPIThingSpeak, 80)) {         
        //faz a requisição HTTP ao ThingSpeak
        client.print("POST /update HTTP/1.1\n");
        client.print("Host: api.thingspeak.com\n");
        client.print("Connection: close\n");
        client.print("X-THINGSPEAKAPIKEY: "+ChaveEscritaThingSpeak+"\n");
        client.print("Content-Type: application/x-www-form-urlencoded\n");
        client.print("Content-Length: ");
        client.print(StringDados.length());
        client.print("\n\n");
        client.print(StringDados);
   
        lastConnectionTime = millis();
        Serial.println("- Informações enviadas ao ThingSpeak!");
     }   
}
 
void FazConexaoWiFi(void){
    client.stop();
    Serial.println("Conectando-se à rede WiFi...");
    Serial.println();  
    delay(1000);
    WiFi.begin(SSID_REDE, SENHA_REDE);
 
    while (WiFi.status() != WL_CONNECTED){
        delay(500);
        Serial.print(".");
    }
 
    Serial.println("");
    Serial.println("WiFi connectado com sucesso!");  
    Serial.println("IP obtido: ");
    Serial.println(WiFi.localIP());
 
    delay(1000);
}

float FazLeituraUmidade(void){
    int ValorADC;
    float UmidadePercentual;
 
     ValorADC = analogRead(0);   //978 -> 3,3V
     Serial.print("[Leitura ADC] ");
     Serial.println(ValorADC);  
      
     UmidadePercentual = 100 * ((978-(float)ValorADC) / 978);
     Serial.print("[Umidade Percentual] ");
     Serial.print(UmidadePercentual);
     Serial.println("%");
 
     return UmidadePercentual;
}

void EscreveLeitura(){
 if(mqqt.connected()&& millis() - lastConnectionTime > INTERVALO_MQTT)){
    delay(1000);
    mqtt.publish("COLOCAR CANAL DO BROKER AQUI", UmidadePercentual)
 }
}

void initMQTT() {
  mqtt.setServer(BROKER_MQTT, BROKER_PORT);
  mqtt.setCallback(mqtt_callback);
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    char c = (char)payload[i];
    message += c;
  }
  Serial.println("Tópico => " + String(topic) + " | Valor => " + String(message));
  Serial.flush();
}

void reconnectMQTT() {
  while (!mqtt.connected()) {
    Serial.println("Tentando se conectar ao Broker MQTT: " + String(BROKER_MQTT));
    if (mqtt.connect("anonymous")) {
      Serial.println("Conectado");
      mqtt.subscribe("COLOCAR CANAL DO BROKER AQUI");
    } else {
      Serial.println("Falha ao Reconectar");
      Serial.println("Tentando se reconectar em 2 segundos");
      delay(2000);
    }
  }
}

void setup(){  
    initMQTT();
    Serial.begin(9600);
    lastConnectionTime = 0; 
    FazConexaoWiFi();
    Serial.println("Sistema de Monitoramento de Umidade de Solo");
}

void loop(){
    float UmidadePercentualLida;
    int UmidadePercentualTruncada;
    char FieldUmidade[11];
    
    if (!mqtt.connected()) {
    reconnectMQTT();
    }  
    mqtt.loop();
     
    //Força desconexão ao ThingSpeak (se ainda estiver desconectado)
    if (client.connected()){
        client.stop();
        Serial.println("- Desconectado do ThingSpeak");
        Serial.println();
    }

    UmidadePercentualLida = FazLeituraUmidade();
    UmidadePercentualTruncada = (int)UmidadePercentualLida; //trunca umidade como número inteiro
     
    //verifica se está conectado no WiFi e se é o momento de enviar dados ao ThingSpeak
    if(!client.connected() && (millis() - lastConnectionTime > INTERVALO_ENVIO_THINGSPEAK)){
        sprintf(FieldUmidade,"field1=%d",UmidadePercentualTruncada);
        EnviaInformacoesThingspeak(FieldUmidade);
    }
    delay(1000);
}
