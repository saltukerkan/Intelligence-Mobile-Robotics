#include <ros/ros.h>
#include <std_msgs::String>
#include <string>

ros::Publisher p;
geometry_msgs::Twist t = Twist();
int keepDist = 1000;

void ballLocationCallback(std_msgs::String msg){
  int c1 = msg.data.find(",");
  int row = msg.data.substr(0,c1);
  int c2 = msg.data.substr(c1+1).find(",");
  int col = msg.data.substr(c1+1, c2);
  int c3 = msg.data.substr(c2+1).find(",");
  int imgR = std::stoi(msg.data.substr(c2+1, c3)) / 2;
  int imgC = std::stoi(msg.data.substr(c3+1)) / 2;

  if (row != imgR){
    // yukari-asagi bak
  }
  if (col != imgC){
    t.angular.z = (imgC - col) / imgC;
  }
  else{
    t.angular.z = 0;
  }

  p.publish(t);
}

void ballDepthCallback(std_msgs::String msg){
  int dist = std::stoi(msg.data);
  if (dist != keepDist){
    t.linear.x = (dist - keepDist) / keepDist;
  }
  else{
    t.linear.x = 0;
  }

  p.publish(t);
}

int main(int argc, char** argv){
  ros::init(argc, argv, "follower")
  ros::NodeHandle n;
  ros::Subscriber subs = n.subscribe("/ball/location", 10, &ballLocationCallback);
  p = n.advertise("/mobile_base/commands/velocity");
  ros::spin();
}
