#include <ESP8266WiFi.h>  
#include <Wire.h>
#include <PubSubClient.h>

//defines
#define SSID_REDE     "teste" 
#define SENHA_REDE    "12345678" 
#define INTERVALO_ENVIO_THINGSPEAK  30000  

const char* BROKER_MQTT = "m16.cloudmqtt.com";
int BROKER_PORT         = 17996;
const char* mqttUser = "povafjjv";              //user
const char* mqttPassword = "2yxCAb-waqJv";      //password
const char* mqttTopicSub ="teste_smus";            //tópico que sera assinado

//constantes e variáveis globais
char EnderecoAPIThingSpeak[] = "api.thingspeak.com";
String ChaveEscritaThingSpeak = "34VKCO5MTXCTUPLA";
long lastConnectionTime; 
WiFiClient client;

//prototypes
void EnviaInformacoesThingspeak(String StringDados);
void FazConexaoWiFi(void);
float FazLeituraUmidade(void);

void initMQTT();
PubSubClient mqtt(client);
/*
 * Implementações
 */
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
    if (mqtt.connect("ESP8266Client", mqttUser, mqttPassword)) {
      Serial.println("Conectado");
      mqtt.subscribe("teste_smus");

    } else {
      Serial.println("Falha ao Reconectar");
      Serial.println("Tentando se reconectar em 2 segundos");
      delay(2000);
    }
  }
}
//Função: envia informações ao ThingSpeak
//Parâmetros: String com a  informação a ser enviada
//Retorno: nenhum
void EnviaInformacoesThingspeak(String StringDados){
    if (client.connect(EnderecoAPIThingSpeak, 80)){         
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

     char umidade[4];
     dtostrf(ValorADC, 2, 2, umidade);
     mqtt.publish("teste_smus", umidade);
 
     return UmidadePercentual;
}
void setup(){  
    Serial.begin(9600);
    lastConnectionTime = 0; 
    FazConexaoWiFi();
    Serial.println("Monitoramento de Umidade de Solo");
    initMQTT();
}

//loop principal
void loop(){
    
    float UmidadePercentualLida;
    int UmidadePercentualTruncada;
    char FieldUmidade[11];

    //Força desconexão ao ThingSpeak (se ainda estiver desconectado)
    if (client.connected()){
        client.stop();
        Serial.println("- Desconectado do ThingSpeak");
        Serial.println();
    }

    UmidadePercentualLida = FazLeituraUmidade();
    UmidadePercentualTruncada = (float)UmidadePercentualLida; //trunca umidade como número inteiro

    //verifica se está conectado no WiFi e se é o momento de enviar dados ao ThingSpeak
    if(!client.connected() && 
      (millis() - lastConnectionTime > INTERVALO_ENVIO_THINGSPEAK)){
        sprintf(FieldUmidade,"field1=%d",UmidadePercentualTruncada);
        EnviaInformacoesThingspeak(FieldUmidade);
    }

     delay(1000);
    if (!mqtt.connected()) {
      reconnectMQTT();
    }
    mqtt.loop();
}
