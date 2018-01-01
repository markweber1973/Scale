#include <wiringPi.h>
#define ADDO 5
#define ADSK 4

// rain sensor on gpio 7

unsigned long readcount(void)
{
  unsigned long Count;
  unsigned char i;

  wiringPiSetup () ;
  pinMode (ADSK, OUTPUT) ;
  pinMode (ADDO, OUTPUT) ;
 
  digitalWrite (ADDO, HIGH); // ADDO=1;
  digitalWrite (ADSK, LOW); // ADSK=0;
  
  Count=0;

  pinMode (ADDO, INPUT) ;  
  delayMicroseconds(1); 
  while (digitalRead(ADDO));//while(ADDO);
  for (i=0;i<24;i++)
  {
    digitalWrite(ADSK, HIGH);//ADSK=1;
    delayMicroseconds(1);
    Count=Count<<1;
    digitalWrite(ADSK, LOW); // ADSK=0;
    delayMicroseconds(1);   
    if(digitalRead(ADDO)) Count++;
    delayMicroseconds(1);   
  }
  digitalWrite(ADSK, HIGH);//ADSK=1;
  delayMicroseconds(1); 

  Count=Count^0x800000;
  digitalWrite(ADSK, LOW);//ADSK=0;
  delayMicroseconds(1);
  return(Count);
} 


