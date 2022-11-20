#include <ESP8266WiFi.h>
#include <WebSocketClient.h>

boolean handshakeFailed=0;
String data= "";
char path[] = "/";   //identifier of this device
const char* ssid     = "wifi ssid";
const char* password = "wifi password";
char* host = "ws://127.0.0.1:5000";  //ip address of  node.js server (localhost port 5000)
const int espport= 3000;
  
WebSocketClient webSocketClient;
unsigned long previousMillis = 0;
unsigned long currentMillis;
unsigned long interval=300; //interval for sending data to the websocket server in ms

// Use WiFiClient class to create TCP connections
WiFiClient client;
void setup() {
  Serial.begin(115200);
  pinMode(readPin, INPUT);     // Initialize the LED_BUILTIN pin as an output
  delay(10);
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("[INFO] : Connecting to WiFi Network ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("[INFO]: WiFi connected");  
  Serial.println("[INFO] : IP address: ");
  Serial.println(WiFi.localIP());
  delay(1000);
  
wsconnect();
//  wifi_set_sleep_type(LIGHT_SLEEP_T);
}

void loop() {
  if (client.connected()) {
    currentMillis=millis(); 
    webSocketClient.getData(data);    
    if (data.length() > 0) {
      Serial.println(data);
      //************* send log data to server in certain interval************************************
      if (abs(currentMillis - previousMillis) >= interval) {
        previousMillis = currentMillis;
        // TODO : Replace this with proper method to read sensor values. This is generating dummy data to test functionality.        
        data= (String) analogRead(A0); 

        //Send data to server
        Serial.println("[INFO]: Sending data to server...")
        Serial.println(data)
        webSocketClient.sendData(data);
      }
    } else {
      Serial.println("[WARNING]: No data to send")
    }
    delay(5);
    }
  }


//=========================== Function Definitions ===========================
void wsconnect(){
  // Connect to the websocket server
  if (client.connect(host, espport)) {
    Serial.println("[INFO] Connected to node.js server");
  } else {
    Serial.println("[ERROR] Connection to node.js server failed");
    delay(1000);  
   
   if(handshakeFailed){
    handshakeFailed=0;
    ESP.restart();
    }
    handshakeFailed=1;
  }
  // Handshake with the server
  webSocketClient.path = path;
  webSocketClient.host = host;
  if (webSocketClient.handshake(client)) {
    Serial.println("[INFO] Handshake successful");
  } else {
    Serial.println("[ERROR] Handshake failed.");
    delay(4000);  
   
   if(handshakeFailed){
    handshakeFailed=0;
    ESP.restart();
    }
    handshakeFailed=1;
  }
}