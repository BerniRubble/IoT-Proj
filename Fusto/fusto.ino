
int level = A0;
char printBuffer[128];
//char printState[128];
char id_barrel[6]="A001\n";
int RED=2;
int GREEN=3;
int BLUE=4;
int BUTTON=7;

int value = 0; // get adc value
int iFutureState;
int buttonValue;

int iState;

//int computeFutureState(int iState, int buttonValue, int value);

void setup()
{
  Serial.begin(9600);
  pinMode(level,INPUT);
  pinMode(RED,OUTPUT);
  pinMode(GREEN,OUTPUT);
  pinMode(BLUE,OUTPUT);
  pinMode(BUTTON,INPUT);
  Serial.print(id_barrel);
  iState=0;
  
}

void loop()
{
    value = analogRead(level); // get adc value
    
    buttonValue=digitalRead(BUTTON);
   
    iFutureState=computeFutureState(iState,buttonValue,value);
    
    switch(iFutureState)
    {
      case 0:
        digitalWrite(GREEN,LOW);
        digitalWrite(RED,LOW);
        digitalWrite(BLUE,LOW);
        break;
      case 1:
      //Qui ci andrà l'invio dell'ID
        
        digitalWrite(GREEN,LOW);
        digitalWrite(RED,LOW);
        digitalWrite(BLUE,LOW);
        break;
      case 2:
        digitalWrite(GREEN,HIGH);
        digitalWrite(RED,LOW);
        digitalWrite(BLUE,LOW);
        break;
      case 3:
        digitalWrite(GREEN,LOW);
        digitalWrite(RED,LOW);
        digitalWrite(BLUE,HIGH);
        break;
      case 4:
        digitalWrite(GREEN,LOW);
        digitalWrite(RED,HIGH);
        digitalWrite(BLUE,LOW);
        break;
    }
    
    
    iState=iFutureState;
    //sprintf(printBuffer,"ADC%d level is %d \n",level, value);
    //sprintf(printState,"State is %d \n", iState);
    //Serial.print(printBuffer);
    //Serial.print(printState);
    
}


int computeFutureState(int iState, int buttonValue, int value){

    /*
    if(iState==0&&buttonValue==LOW)iFutureState=0;
    else if(iState==0&&value>280&&buttonValue==HIGH)iFutureState=1;
    else if(iState==0&&value<280&&value>150&&buttonValue==HIGH)iFutureState=2;
    else if(iState==0&&value<150&&buttonValue==HIGH)iFutureState=3;
    else if(iState==1&&buttonValue==HIGH)iFutureState==1;
    else if(iState==1&&value>280&&buttonValue==LOW)iFutureState=1;
    else if(iState==1&&value<280&&value>150&&buttonValue==LOW)iFutureState=2;
    else if(iState==2&&buttonValue==HIGH)iFutureState=2;
    else if(iState==2&&value<280&&value>150&&buttonValue==LOW)iFutureState=2;
    else if(iState==2&&value<150&&buttonValue==LOW)iFutureState=3;
    else if(iState==3&&value<150&&buttonValue==LOW)iFutureState=3;
    else if(iState==3&&value<150&&buttonValue==HIGH)iFutureState=0;
    */

    if(iState==0&&buttonValue==LOW)iFutureState=0;
    else if(iState==0&&buttonValue==HIGH)iFutureState=1;
    else if(iState==1&&value>280)iFutureState=2;
    else if(iState==1&&value<280&&value>100)iFutureState=3;
    else if(iState==1&&value<150)iFutureState=4;    //else if(iState==1&&buttonValue==HIGH)iFutureState==1;
    else if(iState==2&&value>280)iFutureState=2;
    else if(iState==2&&value<280&&value>150)iFutureState=3;   // else if(iState==2&&buttonValue==HIGH)iFutureState=2;
    else if(iState==3&&value<280&&value>150)iFutureState=3;
    else if(iState==3&&value<150)iFutureState=4;
    else if(iState==4&&buttonValue==HIGH)iFutureState=0;

    return iFutureState;
}
