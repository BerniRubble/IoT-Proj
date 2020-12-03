//Valori min e max degli intervalli
#define MIN 150
#define MAX 210

char id_barrel = 'A';

//Pin
int level = A0;
int RED = 2;
int GREEN = 3;
int BLUE = 4;
int BUTTON = 7;

//Var globali codice
long t = 0;
long debounce_delay = 200;
long print_state_delay=5000;
long t2=0;

int value = 0; // valore sensore

//Variabili di stato 
int iFutureState;
int buttonValue;

int iState;

int computeFutureState(int iState, int buttonValue, int value);
void setup()
{
  Serial.begin(9600);
  pinMode(level, INPUT);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(BUTTON, INPUT);
  iState = 0;
}

void loop()
{
  value = analogRead(level); // get adc value

  buttonValue = digitalRead(BUTTON);

  iFutureState = computeFutureState(iState, buttonValue, value);

  switch (iFutureState)
  {
    case 0:
      digitalWrite(GREEN, LOW);
      digitalWrite(RED, LOW);
      digitalWrite(BLUE, LOW);
      break;
    case 1:
      Serial.print(id_barrel);
      digitalWrite(GREEN, LOW);
      digitalWrite(RED, LOW);
      digitalWrite(BLUE, LOW);
      break;
    case 2:
      if((millis()-t2)>print_state_delay)
      {
        Serial.print('2');
        t2=millis();
      }
      
      digitalWrite(GREEN, HIGH);
      digitalWrite(RED, LOW);
      digitalWrite(BLUE, LOW);
      break;
    case 3:
      //digitalWrite(GREEN, LOW);
      //Serial.print('3');
      if((millis()-t2)>print_state_delay)
      {
        Serial.print('3');
        t2=millis();
      }
      digitalWrite(RED, HIGH);
      //digitalWrite(BLUE, HIGH);
      setColor(0, 50, 0);
      break;
    case 4:
      //Serial.print('4');
      if((millis()-t2)>print_state_delay)
      {
        Serial.print('4');
        t2=millis();
      }
      digitalWrite(GREEN, LOW);
      digitalWrite(RED, HIGH);
      digitalWrite(BLUE, LOW);
      
      break;
  }


  iState = iFutureState;
  

}



int computeFutureState(int iState, int buttonValue, int value) {

  if (iState == 0 && buttonValue == LOW)iFutureState = 0;
  else if (iState == 0 && buttonValue == HIGH && (millis() - t) > debounce_delay) {
    iFutureState = 1;
    //Serial.print(id_barrel);
    t = millis();
  }
  else if (iState == 1 && value > MAX)iFutureState = 2;
  else if (iState == 1 && value < MAX && value > MIN)iFutureState = 3;
  else if (iState == 1 && value < MIN)iFutureState = 4;
  else if (iState == 2 && value < MAX && value > MIN)iFutureState = 3;
  else if (iState == 3 && value < MIN)iFutureState = 4;
  else if (iState == 4 && buttonValue == HIGH && (millis() - t) > debounce_delay) {
    iFutureState = 0;
    t = millis();
  }

  return iFutureState;
}

void setColor(int red, int green, int blue)
{
#ifdef COMMON_ANODE
  red = 255 - red;
  green = 255 - green;
  blue = 255 - blue;
#endif
  analogWrite(GREEN, green);
}
