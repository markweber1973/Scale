#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define ADDO  3
#define ADSK  2
int number = 0;
int state = 0;

void setup() 
{
  pinMode(ADDO, INPUT);
  pinMode(ADSK, OUTPUT);    
  pinMode(13, OUTPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.println("Ready!");
}

void loop() {
delay(100);
}

// callback for received data
void receiveData(int byteCount)
{
  while(Wire.available()) 
  {
    number = Wire.read();
    Serial.print("data received: ");
    Serial.println(number);

    if (number == 1)
    {
      if (state == 0)
      {
        digitalWrite(13, HIGH); // set the LED on
        state = 1;
      }
      else
      {
        digitalWrite(13, LOW); // set the LED off
        state = 0;
      }
    }
  }
}

// callback for sending data
void sendData()
{
  long readCount = ReadCount();
  byte data[4];
  data[0] = readCount;
  data[1] = readCount >> 8;
  data[2] = readCount >> 16;
  data[3] = readCount >> 24;  
  Wire.write(data, 4);
}


unsigned long ReadCount(void)
{
 unsigned long Count;
 unsigned char i;
 digitalWrite(ADDO, HIGH);
 digitalWrite(ADSK, LOW);

 Count=0;
 while (digitalRead(ADDO));
 for (i=0;i<24;i++)
 {
   digitalWrite(ADSK, HIGH);
   Count=Count<<1;
   digitalWrite(ADSK, LOW);   

   if (digitalRead(ADDO)) Count++;
 }
 digitalWrite(ADSK, HIGH); 
 Count=Count^0x800000;
 digitalWrite(ADSK, LOW); 

 return(Count);
} 

