#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"

void xbee_rx(void);
Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);
BufferedSerial xbee(D1, D0);

BBCar car(pin5, pin6, servo_ticker);
Thread X;
int main() {
   X.start(xbee_rx);

   char buf[256], outbuf[256];
   FILE *devin = fdopen(&xbee, "r");
   FILE *devout = fdopen(&xbee, "w");
   while (1) {
      memset(buf, 0, 256);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         buf[i] = fputc(recv, devout);
      }
   RPC::call(buf, outbuf);
   }
}


void xbee_rx(void)
{
   static int i = 0;
   static char buf[5] = {"test"};
   while(1){
         xbee.write(buf, sizeof(buf));
         ThisThread::sleep_for(100ms);
   }
   ThisThread::sleep_for(100ms);
}