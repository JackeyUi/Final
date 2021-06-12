import pyb ,sensor, image, time, math
enable_lens_corr = True
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()


uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

# The AprilTags library outputs the pose information for tags. This is the x/y/z translation and
# x/y/z rotation. The x/y/z rotation is in radians and can be converted to degrees. As for
# translation the units are dimensionless and you must apply a conversion function.

# f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
# divided by the x sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# f_y is the y focal length of the camera. It should be equal to the lens focal length in mm
# divided by the y sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# c_x is the image x center position in pixels.
# c_y is the image y center position in pixels.

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

def degrees(radians):
   return (180 * radians) / math.pi
lineD = 0
i = 0
while(True):
   clock.tick()
   FindAT = 0
   img = sensor.snapshot()
   if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...
   for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
      FindAT = 1
      img.draw_rectangle(tag.rect(), color = (255, 0, 0))
      img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
      print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
            degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
      # Translation units are unknown. Rotation units are in degrees.
      #if (print_args[4] > 300) : degree = print_args[4] - 360
      #else : degree = print_args[4]
      degree = print_args[0]
      #print(degree)
      if (print_args[2] < -2.8) :
         i = 1
         if (degree > 1.2) : uart.write("l".encode())
         elif (degree < -1.2) : uart.write("r".encode())
         else : uart.write("g".encode())
   if FindAT == 0 :
      for l in img.find_line_segments(merge_distance = 5, max_theta_diff = 20 ):
         img.draw_line(l.line(), color = (255, 0, 0))
         #print(l)
         if ((l.y1() < 12 or l.y2() < 12) and (l.x1() > 55 and l.x1() < 105)): lineD = 20
      #print("%d " % lineD)
   if lineD > 0 :
      uart.write("G".encode())
   elif lineD == 0 and FindAT == 0 :
      uart.write("S".encode())
   if i == 0 and FindAT == 1:
      uart.write("s".encode())
   i = 0
   lineD = 0
      #print_args = (0)
      # print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
   #print(clock.fps())
