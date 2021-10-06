

int Pres_R = A5; //right pressure sensor
int Pres_L = A4; //left pressure sensor
int Light_R = A1; //right light sensor
int Light_L = A2; //left light sensor
int val_LR = 0;
int val_LL = 0;
int speakerPin = 9;


int length = 51;     // 노래의 총 길이 설정
char notes[] = "eeeeeeegcde fffffeeeeddedgeeeeeeegcde fffffeeeggfdc";   // 음계 설정
int beats[] = { 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 4,

                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,

                1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 4,

                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4
              };

int tempo = 200;                   // 캐럴이 연주되는 속도

void playTone(int tone, int duration) {
  for (long i = 0; i < duration * 1000L; i += tone * 2) {
    if (analogRead(Pres_R) > 80 && analogRead(Pres_L) > 80 && (val_LR) > 55 && (val_LL) > 55) {
      loop();
    }
    else if (((analogRead(Pres_R)) < 80 || (val_LR) < 55) && ((analogRead(Pres_L)) < 80 || (val_LL) < 55)) {
      loop();
    }

    digitalWrite(speakerPin, HIGH);
    delayMicroseconds(tone);
    digitalWrite(speakerPin, LOW);
    delayMicroseconds(tone);
  }
}

void playNote(char note, int duration) {
  char names[] = { 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'C' };        //음계 함수 설정
  int tones[] = { 1915, 1700, 1519, 1432, 1275, 1136, 1014, 956 };          // 음계 톤 설정
  for (int i = 0; i < 8; i++) {
    if (names[i] == note) {
      playTone(tones[i], duration);
    }
  }
}

void setup() {
  pinMode(Pres_R, OUTPUT);
  pinMode(Pres_L, OUTPUT);
  pinMode(Light_R, OUTPUT);
  pinMode(Light_L, OUTPUT);
  pinMode(speakerPin, OUTPUT);

  Serial.begin(9600);
}


void loop() {
//Pressure) non-touch=:140 & touch:10  
  Serial.print("Pressure----------Right: ");
  Serial.println(analogRead(Pres_R));
  Serial.print("Pressure----------Left: ");
  Serial.println(analogRead(Pres_L));
  Serial.println();

//Light) non-touch=:90 & touch:0
  val_LR = map(analogRead(Light_R), 0, 30, 0, 100); 
  val_LL = map(analogRead(Light_L), 0, 30, 0, 100);

  Serial.print("Light-------------Right: ");
  Serial.println(val_LR);
  Serial.print("Light-------------Left: ");
  Serial.println(val_LL);
  Serial.println();

  if (analogRead(Pres_R) > 80 && analogRead(Pres_L) > 80 && (val_LR) > 55 && (val_LL) > 55) {
    delay(500);
    loop();
  }
  else if (((analogRead(Pres_R)) > 80 && (val_LR) > 55) || ((analogRead(Pres_L)) > 80 && (val_LL) > 55)) {
    for (int i = 0; i < length; i++) {
      if (notes[i] == ' ') {
        delay(beats[i] * tempo); // rest
      }
      else {
        playNote(notes[i], beats[i] * tempo);
      }
      delay(tempo / 10);
    }
    delay(500);
  }



  delay(500);
}
