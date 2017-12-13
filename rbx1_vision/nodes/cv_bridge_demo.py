#!/usr/bin/env python

""" cv_bridge_demo.py - Version 1.1 2013-12-20

    A ROS-to-OpenCV node that uses cv_bridge to map a ROS image topic and optionally a ROS
    depth image topic to the equivalent OpenCV image stream(s).
    
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2011 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html
      
"""

import rospy
import sys
import cv2
import Queue
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class cvBridgeDemo():
    def __init__(self):
        self.node_name = "cv_bridge_demo"
        
        rospy.init_node(self.node_name)
        
        # What we do during shutdown
        rospy.on_shutdown(self.exit_loop)

        # cv2.imshow fine
        # image = cv2.imread("1.jpg")
        # cv2.imshow('image', image)
        # cv2.waitKey(0)
        
        # Create the OpenCV display window for the RGB image
        self.cv_window_name = self.node_name
        cv2.namedWindow(self.cv_window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.cv_window_name, 25, 75)
        self.queue = Queue.Queue()
        self.loop_continue = True
        
        # And one for the depth image
        cv2.namedWindow("Depth Image", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Depth Image", 25, 350)
        
        # Create the cv_bridge object
        self.bridge = CvBridge()
        
        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        self.image_sub = rospy.Subscriber("/camera/rgb/image_color", Image, self.image_callback, queue_size=1)
        self.depth_sub = rospy.Subscriber("/camera/depth/image_view", Image, self.depth_callback, queue_size=1)
        
        rospy.loginfo("Waiting for image topics...")
        rospy.wait_for_message("/camera/rgb/image_color", Image)
        rospy.loginfo("Ready.")
        self.loop()

    def image_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError, e:
            print e
        
        # Convert the image to a numpy array since most cv2 functions
        # require numpy arrays.
        frame = np.array(frame, dtype=np.uint8)
        
        # Process the frame using the process_image() function
        display_image = self.process_image(frame)
                       
        # Display the image.
        # TODO DO update ui in main threads
        # cv2.imshow(self.node_name, display_image)
        self.queue.put((cv2.imshow, (self.node_name, display_image,), {}))

        
        # Process any keyboard commands
        # self.keystroke = cv2.waitKey(5)
        # if self.keystroke != -1:
        #     cc = chr(self.keystroke & 255).lower()
        #     if cc == 'q':
        #         # The user has press the q key, so exit
        #         rospy.signal_shutdown("User hit q key to quit.")
                
    def depth_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            # Convert the depth image using the default passthrough encoding
            depth_image = self.bridge.imgmsg_to_cv2(ros_image, "passthrough")
        except CvBridgeError, e:
            print e

        # Convert the depth image to a Numpy array since most cv2 functions require Numpy arrays.
        depth_array = np.array(depth_image, dtype=np.float32)
                
        # Normalize the depth image to fall between 0 (black) and 1 (white)
        cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
        
        # Process the depth image
        depth_display_image = self.process_depth_image(depth_array)
    
        # Display the result
        cv2.imshow("Depth Image", depth_display_image)
          
    def process_image(self, frame):
        # Convert to greyscale
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Blur the image
        grey = cv2.blur(grey, (7, 7))
        
        # Compute edges using the Canny edge filter
        edges = cv2.Canny(grey, 15.0, 30.0)
        
        return edges
    
    def process_depth_image(self, frame):
        # Just return the raw image for this demo
        return frame
    
    def exit_loop(self):
        self.loop_continue = False

    def loop(self):
        while self.loop_continue:
            func, args, argv = self.queue.get()
            func(*args, **argv)

            self.keystroke = cv2.waitKey(30)
            if self.keystroke != -1:
                cc = chr(self.keystroke & 255).lower()
                if cc == 'q':
                    # The user has press the q key, so exit
                    rospy.signal_shutdown("User hit q key to quit.")

        print "Shutting down vision node."
        cv2.destroyAllWindows()   
        sys.exit(0)
    
def main(args):       
    try:
        cvBridgeDemo()
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vision node."
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
    
