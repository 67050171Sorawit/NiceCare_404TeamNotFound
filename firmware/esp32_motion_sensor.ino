#include <WiFi.h>
#include <PubSubClient.h>

// ---------------- WIFI ----------------
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// ---------------- MQTT ----------------
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

// ---------------- PIR SENSOR ----------------
const int pirPin = 14;   // ขา OUT ของ PIR sensor
int motionState = LOW;

void setup_wifi() {

  delay(10);

  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void reconnectMQTT() {

  while (!client.connected()) {

    Serial.print("Connecting to MQTT...");

    String clientId = "ESP32-NiceCare-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {

      Serial.println("Connected");

    } else {

      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retry in 3 sec");

      delay(3000);
    }
  }
}

void setup() {

  Serial.begin(115200);

  pinMode(pirPin, INPUT);

  setup_wifi();

  client.setServer(mqtt_server, mqtt_port);

  Serial.println("System Ready");
}

void loop() {

  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();

  int sensorValue = digitalRead(pirPin);

  // ตรวจจับการเคลื่อนไหว
  if (sensorValue == HIGH && motionState == LOW) {

    Serial.println("Motion Detected!");

    client.publish(
      "nicecare/motion",
      "MOTION DETECTED"
    );

    motionState = HIGH;
  }

  // ไม่มีการเคลื่อนไหว
  else if (sensorValue == LOW && motionState == HIGH) {

    Serial.println("No Motion");

    client.publish(
      "nicecare/motion",
      "NO MOTION"
    );

    motionState = LOW;
  }

  delay(500);
}