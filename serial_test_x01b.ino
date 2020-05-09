byte incomingByte; // for incoming serial data
int dec;

void setup() {
  Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    dec = (int)incomingByte;

    // say what you got:
    //Serial.println(dec);
    analogWrite(9,dec);
  }
}
