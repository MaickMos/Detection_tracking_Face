#include <Servo.h>
//Creamos una variable servo para poder usar las funciones con ella.
Servo miservo;
char letra;
String codigo;
int angulo;
int x;

void setup()
{
  Serial.begin(9600); // Velocidad en baudios y configuraciçon de inicio.
  //Definimos el pin al que ira conectado el servo.
  miservo.attach(6); //Como salida, el pin 6 con uso de PWM.
  //Movemos el servo al centro
  miservo.write(90);  // Coloca el servo en su posición central.
}
void loop() {
  while(Serial.available() > 0) // Espera entrada de datos de 0 a 180.
  {
    letra = Serial.read(); // Los datos leidos se almacena en la variable valor.
    codigo.concat(letra);
    delay(10);
  }
  if (codigo.length() > 0) {
    Serial.println("Has escrito el codigo:" + codigo);
     
    Serial.println(codigo.toInt());        
    miservo.write(codigo.toInt()); // Envía los comando finales de 0 a 180 al servo.
    delay(20);
    codigo=""; 
  } 
}