int level = A0;
char printBuffer[128];
char id_barrel = 'A';
int RED = 2;
int GREEN = 3;
int BLUE = 4;
int BUTTON = 7;
long t = 0;
long debounce_delay = 200;

int value = 0; // get adc value
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
      digitalWrite(GREEN, HIGH);
      digitalWrite(RED, LOW);
      digitalWrite(BLUE, LOW);
      break;
    case 3:
      //digitalWrite(GREEN, LOW);
      digitalWrite(RED, HIGH);
      //digitalWrite(BLUE, HIGH);
      setColor(0, 50, 0);
      break;
    case 4:
      digitalWrite(GREEN, LOW);
      digitalWrite(RED, HIGH);
      digitalWrite(BLUE, LOW);
      delay(1);
      break;
  }


  iState = iFutureState;
  //sprintf(printBuffer,"ADC%d level is %d \n",level, value);
  //sprintf(printState,"State is %d \n", iState);
  //Serial.print(printBuffer);
  //Serial.print(printState);

}


int computeFutureState(int iState, int buttonValue, int value) {

  if (iState == 0 && buttonValue == LOW)iFutureState = 0;
  else if (iState == 0 && buttonValue == HIGH && (millis() - t) > debounce_delay) {
    iFutureState = 1;
    //Serial.print(id_barrel);
    t = millis();
  }
  else if (iState == 1 && value > 210)iFutureState = 2;
  else if (iState == 1 && value < 210 && value > 100)iFutureState = 3;
  else if (iState == 1 && value < 100)iFutureState = 4;
  else if (iState == 2 && value < 210 && value > 100)iFutureState = 3;
  else if (iState == 3 && value < 100)iFutureState = 4;
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
