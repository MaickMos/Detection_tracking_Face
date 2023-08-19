#include <Servo.h> 
 
Servo brazo1;  //creamos un objeto servo 
Servo brazo2;
Servo base;
float angx=90, angy=90;
char orientacion='p',eje=' ';

void setup()
{ 
  brazo1.attach(2);
  base.attach(4);
  Serial.begin(9600);
  base.write(90);
  brazo1.write(60);  
} 
 
void loop() 
{
  if (Serial.available()>0){
    char buffer[2];
    Serial.readBytesUntil('\n', buffer, 2);
    orientacion=buffer[0];
    eje=buffer[1];
    Serial.println("orientacion");
    Serial.println(orientacion);
    Serial.println("eje");
    Serial.println(eje);}
    
    switch(orientacion)
    {
      case 'd':
      if(eje=='x')
        {angx=angx+0.5;
        base.write(angx);}
      
      if(eje=='y')
        {angy=angy+0.5;
        brazo1.write(angy);}
      break;
      case 'i':
      if(eje=='x')
        {angx=angx-0.5;
        base.write(angx);}
      
      if(eje=='y')
        {angy=angy-0.5;
        brazo1.write(angy);}
      break;
      case 'p':
      if(eje=='x')
        {angx=angx;
        base.write(angx);}
      
      if(eje=='y')
        {angy=angy;
        brazo1.write(angy);}    
      break; 
    
    case 'h':
      angy=40;
      angx=90;
      brazo1.write(angy); 
      base.write(angx);
      
    break;   
    }

    delay(100);
    
}
