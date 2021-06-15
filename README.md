# Final
1. Download the files in the "Second_test" dir. 
2. Make sure your XBee is connected, and use "mbed add http://gitlab.larc-nthu.net/ee2405_2021/bbcar" to get the libarary.
3. Connect the OpenMV to your host, and save the "Final_2.py" as "main.py" into the OpenMV, then connect it back to the mbed.
4. Note that you need to use D10 and D9 for the tx and rx of the OpeMV.(D1, D0 is used by XBee).
5. Compile the program.
6. Exercute "sudo python3 XBee_host.py /dev/ttyUSB0" to get the task that the car is doing from the XBee.
7. The car would start moving if there are lines in the lower front of the car, and it would send "Go along with the line" from the XBee.
8. If there is no lines detected, it would start rotate clockwise, trying to find AprilTags, and it would send "Find an AprilTag" from the XBee.
9. Then if it finds a AprilTag, it would moving towards to the AprilTag, and it would send "Go to the AprilTag" from the XBee.
10. You can use "reset" button to back to redo the tasks form the beginning.
11. Demo : 
    pt.1: https://www.youtube.com/watch?v=K6U-sBiof1M
    pt.2: https://www.youtube.com/watch?v=-KGvd8muTuk
