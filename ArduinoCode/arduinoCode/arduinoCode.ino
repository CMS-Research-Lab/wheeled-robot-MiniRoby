/******************************************
  Date: 07-2025
  Authors: CMS, JSG, DLM
  Board: Arduino Nano
  Description: 
  This code controls a two-wheeled differential mobile robot using an Arduino Nano.
  It receives velocity commands from a Single Board Computer (Jetson Nano) via serial communication,
  drives two motors through a H-bridge, and calculates angular velocities of the wheels
  using quadrature encoders.
  
  Note: It is necessary to install the PinChangeInterrupt.h library before uploading the program to the Arduino board.

  Key functionalities:
  - Serial communication with SBC for receiving motor commands
  - Velocity decoding and PWM generation for each motor
  - Encoder signal processing with interrupts
  - Real-time calculation of angular velocities
*******************************************/
// Library to use multiple interrupt pins on Arduino Nano
#include "PinChangeInterrupt.h"

//-------------------- Variable Declarations -------------------------
// H-bridge pin definitions
#define IN1izq 6
#define IN2izq 7
#define pwm_i 11
#define pwm_d  10
#define IN1der 8
#define IN2der 9

int ledPin = 13;
char comando;  // Incoming serial character command
int valor = 0 ;
int signo=1;  // Sign of the velocity command
double PWM_der = 0.0;
double PWM_izq = 0.0;
int motor_der=0;
int motor_izq=0;
volatile bool  paroEmergencia = false; // Emergency stop flag
unsigned long lastTime, sampleTime = 100;
//------------------------------------------------------------------------------------------------

//------------------ Serial Communication Variables ---------------------
String velocidadRuedas = "";
String lastVelocidadRuedas = "";

//------------------ Right Motor Encoder ----------------------
const int    CAR = 2;    // Encoder A channel
const int    CBR = 3;    // Encoder B channel
volatile int tickR = 0;
volatile int antR      = 0;
volatile int actR      = 0;
double omegaR = 0; // Angular velocity of right wheel

//------------------ Left Motor Encoder -----------------------
const int    CAL = 4; // Encoder A channel.
const int    CBL = 5; // Encoder B channel
volatile int tickL = 0;
volatile int antL      = 0;
volatile int actL      = 0; 
double omegaL = 0; // Angular velocity of left wheel

//------------ Constants for velocity calculation ------------
double constValue = 3.1733; // (1000*2*pi)/R ---> R = 1980 (encoder resolution x4)

void setup()
{
  // Pin setup and serial configuration
  pinMode(ledPin,OUTPUT);
  digitalWrite(ledPin,LOW);
  pinMode(pwm_i, OUTPUT);
  pinMode(pwm_d, OUTPUT);
  pinMode(IN1izq, OUTPUT);
  pinMode(IN2izq, OUTPUT);
  pinMode(IN1der, OUTPUT);
  pinMode(IN2der, OUTPUT);
  Serial.begin(115200);
  
  // Encoder input pin setup
  pinMode(CAR, INPUT);
  pinMode(CBR, INPUT);
  pinMode(CAL, INPUT);
  pinMode(CBL, INPUT);
  
  // Attach interrupts for encoder signals
  attachInterrupt(digitalPinToInterrupt(CAR), encoderR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(CBR), encoderR, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(CAL), encoderL, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(CBL), encoderL, CHANGE);             

  lastTime = millis(); // Initialize timer
     
}
void loop() {
  
  if(millis()-lastTime >= sampleTime)
  {
    omegaR = constValue*tickR/(millis()-lastTime);
    omegaL = constValue*tickL/(millis()-lastTime);
    lastTime = millis();
    tickR = 0;
    tickL = 0;
    // Format velocity string for transmission    
    velocidadRuedas = "r,";
    velocidadRuedas += omegaR;
    velocidadRuedas += ",l,";
    velocidadRuedas += omegaL;
    velocidadRuedas += ",";
  }
  
  // Send new velocity string only if it has changed
  if (!velocidadRuedas.equals(lastVelocidadRuedas)){
    Serial.println(velocidadRuedas);
  }
  lastVelocidadRuedas=velocidadRuedas;
  
  // Emergency stop logic, Note: This option is currently not implemented 
  if (paroEmergencia == true)
  {
    digitalWrite(ledPin,HIGH);
   analogWrite(pwm_d, 0);
   analogWrite(pwm_i, 0);
  }
  else
  {
    // Receive and process serial motor commands
    if (Serial.available() > 0)
      {      
        comando = ((byte)Serial.read());
        if(isDigit(comando))//es un valor entre 0-9
        {
          valor = (valor*10)+(comando-'0');
           
        }
        else if (comando == '-')
        {
          signo=-1;
        }
        else if (comando == 'D')
        {
          // Right motor control 
          digitalWrite(ledPin,HIGH);           
          PWM_der=valor/100.0;          
          motor_der=(int)((PWM_der)*255);
                   
          if (signo>0 ){        
            digitalWrite(IN1der,LOW);
            digitalWrite(IN2der,HIGH);        
          }
          else
          {
            digitalWrite(IN1der,HIGH);
            digitalWrite(IN2der,LOW);
          }    
          analogWrite(pwm_d, motor_der);                                   
          valor=0;
          signo=1;
          PWM_der=0.0;    
        }  
        else if (comando == 'I')
        {                      
          PWM_izq=valor/100.0;
          motor_izq=(int)((PWM_izq)*255);
          if (signo>0 )
          {
            digitalWrite(IN1izq,HIGH);
            digitalWrite(IN2izq,LOW);
          }
          else
          {
            digitalWrite(IN1izq,LOW);
            digitalWrite(IN2izq,HIGH);
          }
          analogWrite(pwm_i, motor_izq);
          valor=0;
          signo=1;
          PWM_izq=0.0;
        }          
        else if (comando == '.')      
        {
          valor=valor;
        }
        else
        {
          signo=1;
        }    
      }
    }      
}


void encoderR(void)
{
    antR=actR;             
    actR=PIND & 12;  
    
    if(antR==0  && actR== 4){
       tickR=tickR+1;
    } 
    if(antR==4  && actR==12){
       tickR=tickR+1;
    } 
    if(antR==8  && actR== 0){
      tickR=tickR+1;
    }  
    if(antR==12 && actR== 8){
      tickR=tickR+1;
    }  
    
    if(antR==0 && actR==8){
      tickR=tickR-1;
    }   
    if(antR==4 && actR==0){
      tickR=tickR-1;
    }  
    if(antR==8 && actR==12){
      tickR=tickR-1;
    } 
    if(antR==12 && actR==4){
      tickR=tickR-1;
    }       

}
void encoderL(void)
{
    antL=actL;                
    actL=PIND & 48;                 
                                       
    if(antL==0  && actL==16){
      tickL=tickL+1;
    }  
    if(antL==16 && actL==48){
      tickL=tickL+1;
    }  
    if(antL==32 && actL== 0){
      tickL=tickL+1;
    }  
    if(antL==48 && actL==32){
      tickL=tickL+1;
    }  
    
    if(antL==0  && actL==32){
      tickL=tickL-1;
    }   
    if(antL==16 && actL== 0){
      tickL=tickL-1;
    }  
    if(antL==32 && actL==48){
      tickL=tickL-1;
    }  
    if(antL==48 && actL==16){
      tickL=tickL-1;
    }  
    
}
