#!/usr/bin/python

import psutil
import rospy
import time
from jetson_performance_reporter.msg import PerformanceReport
from jtop import jtop


class PerformancePublisherHandler:
	def __init__(self):
		rospy.loginfo('Setting up node.')
		rospy.init_node('jetson_performance_report')
		self.jetson = jtop()
		self.report = PerformanceReport()
		self.publisher = rospy.Publisher('/jetson_performance_report', PerformanceReport, queue_size=1)
		rospy.loginfo('Node setup correctly!')

	def publish_report(self):
		self.report.cpu_usage = psutil.cpu_percent()
		self.report.gpu_usage = self.jetson.gpu['val']
		self.report.mem_usage = psutil.virtual_memory().percent
		self.report.mem_total = psutil.virtual_memory().total
		self.publisher.publish(self.report)

	def run(self):
		# set thee control rate
		rate = rospy.Rate(2)
		while not rospy.is_shutdown():
			self.publish_report()
			rate.sleep()


if __name__ == '__main__':
	handler = PerformancePublisherHandler()
	handler.run()
