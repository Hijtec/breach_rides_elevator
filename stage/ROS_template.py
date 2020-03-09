#!/usr/bin/python

# Imports
import rospy
import roslib

# Messages
from std_msgs.msg import Float32, Float64

#############
#Input: Determine node input
#Output: Determine node output
#############

# Create node class
class ClassName:
	def __init__(self):
        #Initialize node
		rospy.init_node('node_name')

		#Subscribers
		self.local_message_name_sub = rospy.Subscriber('message_name_sub', Float64, self.message_name_callback)

		#Publishers
		self.local_message_name_pub = rospy.Publisher('message_name_pub', Float32, queue_size = 10)

		#Parameters - set
		self.param = rospy.get_param('~parameter_name', 0.18)
		self.rate = rospy.get_param('~rate',50)

        #Parameters - inherited
		self.param_inherited = rospy.get_param('~inherited_param','/message')

		#Initialization - values
		self.value_that_needs_to_be_set = 0;
		self.time_prev_update = rospy.Time.now(); #Refresh time

    #Message reader
	def message_name_callback(self, msg):
		self.message_name = msg.data #Reads data from message


	#Class functions
    def fcn(self, par1, par2):
        #Generic class function
        #Input
        par = self.par1;
        #Output
        return(par)

    def fcn_update(self, par1, par2):
        #Function that updates a class parameter in update
        #Input
        par = self.par1;
        #Output
        return(par)

    def fcn_timed(self, par1, par2):
        #Generic class function with timing
        #Input
        par = self.par1;
        #Timing
        time = rospy.Time.now();
        d_time = (time - self.time_prev_update).to_sec()
        self.time_prev_update = time;
        #Output
        return(par)

    def fcn_pub(self, par1, par2):
        #Input
        par = self.par1;
        #Pub_construct
        out = par;
        #Output
        self.local_message_name_pub.publish(out)
        return(par)

    def update(self):
        #Calls the updates for every spin, passes the parameters
		self.par = self.fcn_update();   #updater
		self.fcn(self.par)              #par passer
		self.fcn_pub(self.par)          #pub par passer

    def spin(self):
        #Node instance
		rospy.loginfo("Start node_name")#logger handle
		rate = rospy.Rate(self.rate)    #declares frequency of node
		rospy.on_shutdown(self.shutdown)#shutdown function on node shutdown
        #Loop
		while not rospy.is_shutdown():
			self.update();              #update state
			rate.sleep()                #sleep based on frequency
		rospy.spin()

    def shutdown(self):
        #Shutdown handler
		rospy.loginfo("Stop diffdrive_odom") #logger handle
		rospy.sleep(1)

def main():
	class_name = ClassName();       #class assign
	class_name.spin()               #start spin loop

if __name__ == '__main__':
    main();