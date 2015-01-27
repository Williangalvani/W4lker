// Controlling a servo position using a potentiometer (variable resistor) 
// by Michal Rinott <http://people.interaction-ivrea.it/m.rinott> 

#include <Servo.h>
#define n_servos 12
#define COMMAND_WRITE 'a'
#define COMMAND_READ_PIN 'b'
#define COMMAND_READ_IMU 'c'

Servo servo[12];  // create servo object to control a servo
int servos_pos[] = {1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500};

char header[] = ">$";

typedef enum {STANDBY, GETTING_HEADER, WAITING_COMMAND, WAITING_TARGET, WAITING_SERVO_POS } states;
void setup() 
{
imu_setup();
  for(int i=0;i<n_servos;i++)
  {
    servo[i].attach(i);
    servo[i].writeMicroseconds(servos_pos[i]);
  }
  Serial.begin(115200);
}


void respond_with_pins_state()
{
    Serial.println("responding with states");
}

void write_to_servo(int nservo, int value)
{
    servo[nservo].writeMicroseconds(value);
}


void loop()
{
    //imu_loop();
    handleSerial();
}

void handleSerial()
{
  static int current_state = STANDBY;
  static int target = 0;
  while(Serial.available())
  {
     char newData = Serial.read();
     switch(current_state)
     {
        case STANDBY:
            Serial.println("Standy...");
            if(newData==header[0])
            {
                current_state = GETTING_HEADER;
            }
        break;
        case GETTING_HEADER:

            Serial.println("receiving header");
            if(newData==header[1])
            {
                current_state = WAITING_COMMAND;
            }else
            {
                current_state = STANDBY;
            }
        break;

        case WAITING_COMMAND:

            Serial.print("Waiting for command...");
            Serial.println(newData);
            switch(newData)
            {
            case COMMAND_WRITE:
                Serial.println("got servo request");
                current_state = WAITING_TARGET;
            break;

            case COMMAND_READ_IMU:
                Serial.println("got imu request");
                respond_with_imu();
                current_state = STANDBY;
            break;

            case COMMAND_READ_PIN:
                respond_with_pins_state();
                current_state = STANDBY;
            break;
            }
        break;

        case WAITING_TARGET:
            if(newData< n_servos)
            {
                target = newData;
                current_state = WAITING_SERVO_POS;
            }else
            {
                current_state = STANDBY;
            }
        break;

        case WAITING_SERVO_POS:
            while(!Serial.available());
            unsigned char low = newData;
            unsigned char high = Serial.read();
            unsigned int newPosition = (high  << 8)+low;
            write_to_servo(target, newPosition);

            current_state = STANDBY;
            Serial.print("Writing pos ");
            Serial.print(newPosition);
            Serial.print(" to servo ");
            Serial.println(target);
        break;

     }
  }
} 
