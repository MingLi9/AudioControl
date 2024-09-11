// Analog pins only
int potentiometerPins[5] = {0, 1, 2, 3, 4};

int potValues[5] = {0, 0, 0, 0, 0};

bool updated = false;

void readAndWritePotValue(int index)
{
  int tempValue = map(analogRead(potentiometerPins[index]), 0, 1023, 0, 100);
  if (tempValue < potValues[index] - 1 || tempValue > potValues[index] + 1)
  {
    potValues[index] = tempValue;
    updated = true;
  }
}

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  for (int index = 0; index <= 4; index++)
  {
    readAndWritePotValue(index);
  }
  if(updated){
    String volumeString = String(potValues[0]) + "|" + String(potValues[1]) + "|" + String(potValues[2]) + "|" + String(potValues[3]) + "|" + String(potValues[4]);
    Serial.println(volumeString);
    updated = false;
  }
  delay(500);
}