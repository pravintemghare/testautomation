# AWS Application Loadbalancer

The componets here create an ALB which listens to port 80 and 443 resepectively. Traffic coming to port 80 is automatically redirected to port 443.

The ALB is configured to serve 1 application installed on a ec2 instance. 

In addition to that, this stack creates some alarming on the ec2 instance served by the ALB along with SNS topics and everything required in order to receive email automatically in case an alarm is triggered.

The Healthehck is configurable on a separate port so that we can allow ALB to call the healthcheck but it will not be publicly available.

