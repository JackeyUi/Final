#include"mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"
#include <stdio.h>
#include <string.h>

int der1 = 0;
int der2 = 0;
int der3 = 0;

Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);
BufferedSerial pc(USBTX,USBRX); //tx,rx
BufferedSerial xbee(D1, D0);
BufferedSerial uart(D10,D9); //tx,rx
Thread t1, t2, t3;
char recv[1];
//char r[1] = 'r';
//char s[1] = 's';
BBCar car(pin5, pin6, servo_ticker);

void steer1() {
    printf("start 1\n");
    char buf[23] = {"Go along with the line"};
    xbee.write(buf, sizeof(buf));
    while(der1) {
    if (recv[0] == 'G') {
                car.goStraight(100);
                ThisThread::sleep_for(300ms);
            }
    if (recv[0] == 'S') {
                car.stop();
                ThisThread::sleep_for(300ms);
            }
    }
}
void steer2() {
    bool line = 1;
    printf("T2 is working?\n");
    while(1) {
        printf("22");
        if(recv[0] == 'S') {
            printf("stop now\n");
            ThisThread::sleep_for(2000ms);
            printf("still stop?\n");
            if(recv[0] == 'S') {
                printf("Yes\n");
                break;
            }
        }
    }
    der1 = 0;
    der2 = 1;
    printf("start 2\n");
    char buf[23] = {"Find an AprilTag     "};
    xbee.write(buf, sizeof(buf));
    while(der2) {
        car.turn(20, -0.3);
    }
}
void steer3() {
    bool rotate = 1;
    while(rotate) {
        printf("33");
        if(recv[0] =='g' || recv[0] == 'r' || recv[0] == 'l' || recv[0] == 's') break;
    }
    der2 = 0;
    car.stop();
    der3 = 1;
    printf("start 3\n");
    char buf[23] = {"Go to the AprilTag   "};
    xbee.write(buf, sizeof(buf));
    while(der3) {
        if (recv[0] == 'r') {
            car.turn(80, -0.2);
            ThisThread::sleep_for(50ms);
            car.stop();
        }
        else if (recv[0] == 'l') {
            car.turn(80, 0.2);
            ThisThread::sleep_for(50ms);
            car.stop();
            
        }
        else if (recv[0] == 'g') {
            car.goStraight(100);
            ThisThread::sleep_for(50ms);
            car.stop();
        }
        else {
            car.stop();
            ThisThread::sleep_for(50ms);
        }
    }
    
}

int main(){
    der1 = 1; 
    t1.start(steer1);
    t2.start(steer2);
    t3.start(steer3);
    car.goStraight(100);
                ThisThread::sleep_for(300ms);
    car.stop();
                ThisThread::sleep_for(300ms);
   uart.set_baud(9600);
   while(1){
      if(uart.readable()){
            
            uart.read(recv, sizeof(recv));
            pc.write(recv, sizeof(recv));
            
        }
   }
}

