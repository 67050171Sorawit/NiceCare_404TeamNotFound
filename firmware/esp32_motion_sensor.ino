#include <WiFi.h>
#include <PubSubClient.h>

// ================= WIFI =================
const char* ssid = "A06Sorawit";
const char* password = "m02062548";

// ================= MQTT =================
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

// ================= PIN =================
const int pirPin = 14;
const int ledPin = 26;
const int buzzerPin = 25;

// ================= STATE =================
bool alertActive = false;
int lastPirState = LOW;

unsigned long ledOnTime = 0;
const unsigned long ledDuration = 10000;

// ================= WIFI =================
void setup_wifi() {

  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

// ================= MQTT RECONNECT =================
void reconnectMQTT() {

  while (!client.connected()) {

    Serial.print("Connecting to MQTT...");

    String clientId = "ESP32-NiceCare-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {

      Serial.println("MQTT Connected");

      // 🔥 สำคัญ: subscribe topic
      client.subscribe("nicecare/fall");

    } else {

      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retry in 3 sec");

      delay(3000);
    }
  }
}

// ================= CALLBACK =================
void callback(char* topic, byte* payload, unsigned int length) {

  String msg = "";

  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  Serial.println("MQTT MSG: " + msg);

  if (msg == "FALL") {

    Serial.println("FALL DETECTED!");

    digitalWrite(ledPin, HIGH);
    digitalWrite(buzzerPin, HIGH);
    delay(2000);
    digitalWrite(buzzerPin, LOW);
    digitalWrite(ledPin, LOW);
  }
}

// ================= SETUP =================
void setup() {

  Serial.begin(115200);

  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  digitalWrite(ledPin, LOW);
  digitalWrite(buzzerPin, LOW);

  setup_wifi();

  client.setServer(mqtt_server, mqtt_port);

  // 🔥 สำคัญมาก
  client.setCallback(callback);

  Serial.println("NiceCare System Ready");
}

// ================= LOOP =================
void loop() {

  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  int pirState = digitalRead(pirPin);

  if (pirState == HIGH && lastPirState == LOW && !alertActive) {

    Serial.println("ELDERLY GOT UP");

    client.publish("nicecare/motion", "ELDERLY GOT UP");

    digitalWrite(ledPin, HIGH);
    digitalWrite(buzzerPin, HIGH);
    delay(100);
    digitalWrite(buzzerPin, LOW);

    ledOnTime = millis();
    alertActive = true;
  }

  if (alertActive && millis() - ledOnTime >= ledDuration) {

    digitalWrite(ledPin, LOW);
    alertActive = false;
  }

  lastPirState = pirState;

  delay(100);
}
