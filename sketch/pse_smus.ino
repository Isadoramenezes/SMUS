#include <ESP8266WiFi.h>  
#include <Wire.h>
 
//defines
#define SSID_REDE     "teste" 
#define SENHA_REDE    "12345678" 
#define INTERVALO_ENVIO_THINGSPEAK  30000  
 
//constantes e vari�veis globais
char EnderecoAPIThingSpeak[] = "api.thingspeak.com";
String ChaveEscritaThingSpeak = "34VKCO5MTXCTUPLA";
long lastConnectionTime; 
WiFiClient client;
 
//prototypes
void EnviaInformacoesThingspeak(String StringDados);
void FazConexaoWiFi(void);
float FazLeituraUmidade(void);
 
/*
 * Implementa��es
 */
 
//Fun��o: envia informa��es ao ThingSpeak
//Par�metros: String com a  informa��o a ser enviada
//Retorno: nenhum
void EnviaInformacoesThingspeak(String StringDados)
{
    if (client.connect(EnderecoAPIThingSpeak, 80))
    {         
        //faz a requisi��o HTTP ao ThingSpeak
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
        Serial.println("- Informa��es enviadas ao ThingSpeak!");
     }   
}
 
void FazConexaoWiFi(void){
    client.stop();
    Serial.println("Conectando-se � rede WiFi...");
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

float FazLeituraUmidade(void)
{
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
void setup(){  
    Serial.begin(9600);
    lastConnectionTime = 0; 
    FazConexaoWiFi();
    Serial.println("Planta IoT com ESP8266 NodeMCU");
}
 
//loop principal
void loop(){
    float UmidadePercentualLida;
    int UmidadePercentualTruncada;
    char FieldUmidade[11];
     
    //For�a desconex�o ao ThingSpeak (se ainda estiver desconectado)
    if (client.connected()){
        client.stop();
        Serial.println("- Desconectado do ThingSpeak");
        Serial.println();
    }
 
    UmidadePercentualLida = FazLeituraUmidade();
    UmidadePercentualTruncada = (int)UmidadePercentualLida; //trunca umidade como n�mero inteiro
     
    //verifica se est� conectado no WiFi e se � o momento de enviar dados ao ThingSpeak
    if(!client.connected() && 
      (millis() - lastConnectionTime > INTERVALO_ENVIO_THINGSPEAK)){
        sprintf(FieldUmidade,"field1=%d",UmidadePercentualTruncada);
        EnviaInformacoesThingspeak(FieldUmidade);
    }
 
     delay(1000);
}