//Recommend using 47.5k resistors for wider range in ADC values.
//Potentially require a calibration function for setting upper and lower adc values instead of using constants every time.

const int WINDOW_SIZE = 5;
int filterSum[5] = {0};
int adc = 0;
int idx[5] = {0};

const int  INDEX = 0;
const int MIDDLE = 1;
const int   RING = 2;
const int  PINKY = 3;
const int  THUMB = 4;

int READINGS[5][5] = {0};

int angle[5] = {0};
int Roll = 0;
int Pitch = 0;
int Yaw = 0;

const int FLEX_PIN[5] = {A3, A2, A1, A0, A6};
const int UPPER_ADC[5] = {615, 640, 690, 635, 650};
const int LOWER_ADC[5] = {575, 560, 620, 570, 570};

void setup() {
    Serial.begin(9600);
    pinMode(FLEX_PIN[INDEX], INPUT);
    pinMode(FLEX_PIN[MIDDLE], INPUT);
    pinMode(FLEX_PIN[RING], INPUT);
    pinMode(FLEX_PIN[PINKY], INPUT);
    pinMode(FLEX_PIN[THUMB], INPUT);
}

void loop() {
    //Read 5 fingers bend angles
    //int finger = THUMB;
    //angle[finger] = readFlexSensor(finger);
    for (int finger = 0; finger < 5; finger++) {
        angle[finger] = readFlexSensor(finger);
    }
    
    //IMU RPY: to complete

    //Send 8 angles serially
    Serial.println((String)angle[0] + "/" + angle[1] + "/" + angle[2] + "/" + angle[3] + "/" + angle[4] + "/" +  Roll + "/" + Pitch + "/" + Yaw);

    delay(10);
}

int readFlexSensor(int finger) {
    filterSum[finger] = filterSum[finger] - READINGS[finger][idx[finger]];
    adc = analogRead(FLEX_PIN[finger]);
    READINGS[finger][idx[finger]] = adc;
    filterSum[finger] = filterSum[finger] + adc;
    idx[finger] = (idx[finger] + 1) % WINDOW_SIZE;
    int average = filterSum[finger] / WINDOW_SIZE;
    int angle = map(average, LOWER_ADC[finger], UPPER_ADC[finger], 90, 0);
    //int adc = analogRead(FLEX_PIN[finger]);
    //int angle = map(adc, LOWER_ADC[finger], UPPER_ADC[finger], 90, 0);
    if (angle > 90) {
        angle = 90;
    }
    else if (angle < 0) {
        angle = 0;
    }
    //Serial.println((String)adc + " - " + angle);
    return angle;
}
