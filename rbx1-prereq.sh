#!/binsh

# Install the prerequisites for the ROS By Example code, Volume 1

sudo apt-get install ros-kinetic-turtlebot-bringup \
ros-kinetic-turtlebot-create ros-kinetic-openni-* \
ros-kinetic-openni2-* ros-kinetic-freenect-* ros-kinetic-usb-cam \
ros-kinetic-laser-* \
ros-kinetic-slam-gmapping \
ros-kinetic-joystick-drivers python-rosinstall \
ros-kinetic-orocos-kdl ros-kinetic-python-orocos-kdl \
python-setuptools ros-kinetic-dynamixel-motor-* \
python-opencv ros-kinetic-vision-opencv \
ros-kinetic-depthimage-to-laserscan \
ros-kinetic-turtlebot-teleop ros-kinetic-move-base \
ros-kinetic-map-server ros-kinetic-fake-localization \
ros-kinetic-amcl git
# use git clone source code then catkin_make
# ros-kinetic-arbotix-* \

# audio see you later
# ros-kinetic-audio-common ros-kinetic-pocketsphinx gstreamer0.10-pocketsphinx \

# TX2 don't need these
# libopencv-dev
# ros-kinetic-hokuyo-node
# subversion mercurial
