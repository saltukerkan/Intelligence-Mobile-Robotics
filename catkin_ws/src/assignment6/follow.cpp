#include <ros/ros.h>
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include <string>

using namespace std;

ros::Publisher p;
geometry_msgs::Twist t = geometry_msgs::Twist();
int keepDist = 1000;

void ballLocationCallback(std_msgs::String msg){
  int c1 = msg.data.find(",");
  int row = atoi(msg.data.substr(0,c1).c_str());
  int c2 = msg.data.substr(c1+1).find(",");
  int col = atoi(msg.data.substr(c1+1, c2).c_str());
  int c3 = msg.data.substr(c2+1).find(",");
  int imgR = atoi(msg.data.substr(c2+1, c3).c_str()) / 2;
  int imgC = atoi(msg.data.substr(c3+1).c_str()) / 2;

  cout << "Hey" << endl;

  if (row != imgR){
    // yukari-asagi bak
  }
  if (col != imgC){
    cout << "Sag-sol" << endl;
    t.angular.z = (imgC - col) / imgC;
  }
  else{
    t.angular.z = 0;
  }

  p.publish(t);
}

void ballDepthCallback(std_msgs::String msg){
  int dist = atoi(msg.data.c_str());
  if (dist != keepDist){
    cout << "kirmiziii" << endl;
    t.linear.x = (dist - keepDist) / keepDist;
  }
  else{
    t.linear.x = 0;
  }
  cout << "Hey2" << endl;

  p.publish(t);
}

int main(int argc, char** argv){
  ros::init(argc, argv, "follower");
  ros::NodeHandle n;
  ros::Subscriber subs = n.subscribe("/ball/location", 10, &ballLocationCallback);
  ros::Subscriber subs2 = n.subscribe("/ball/depth", 10, &ballDepthCallback);
  p = n.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 10);
  ros::spin();
}

