#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <math.h>
#include "std_msgs/String.h"
#include <string>

static const std::string OPENCV_WINDOW = "Image window";

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  image_transport::Subscriber depth;
  ros::Publisher depth_pub;
  ros::Publisher pixel_pub;
  int row;
  int col;

public:
  ImageConverter()
    : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    image_sub_ = it_.subscribe("/usb_cam/image_raw", 10,
      &ImageConverter::imageCb, this);
    // image_pub_ = it_.advertise("/image_converter/output_video", 10);
    pixel_pub = nh_.advertise<std_msgs::String>("/ball/location", 10);
    depth_pub = nh_.advertise<std_msgs::String>("/ball/depth", 10);
    depth = it_.subscribe("/camera/depth/image_raw", 10, &ImageConverter::ballDist , this);
    row = 0;
    col = 0;

    cv::namedWindow(OPENCV_WINDOW);
  }

  ~ImageConverter()
  {
    cv::destroyWindow(OPENCV_WINDOW);
  }

  void ballDist(const sensor_msgs::ImageConstPtr& msg){
    cv_bridge::CvImageConstPtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvShare(msg);
      double max = 0.0;

      cv::minMaxLoc(cv_ptr->image, 0, &max, 0, 0);
      cv::Mat normalized;
      cv_ptr->image.convertTo(normalized, CV_32F, 1.0/max, 0)  ;

      cv::imshow("foo", normalized);
      cv::waitKey(1);

    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }
    int dist = cv_ptr->image.at<float>(row,col);
    std::stringstream ss;
    ss << dist;
    std_msgs::String m;
    m.data = ss.str();
    depth_pub.publish(m);
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }


    int dis_min = 1000000;
    for (int i=0; i < cv_ptr->image.rows; i++) {
        for (int j=0; j < cv_ptr->image.cols; j++) {
            int b = cv_ptr->image.at<cv::Vec3b>(i, j).val[0];
            int g = cv_ptr->image.at<cv::Vec3b>(i, j).val[1];
            int r = cv_ptr->image.at<cv::Vec3b>(i, j).val[2];
            // int dis = pow((r-255)*(r-255) + g*g + b*b, 0.5);
            int dis = (r-255)*(r-255) + g*g + b*b;
            // ROS_INFO("b: %d", b);
            // ROS_INFO("g: %d", g);
            // ROS_INFO("r: %d", r);
            // ROS_INFO("%d", dis);
            if (dis < dis_min) {
                dis_min = dis;
                row = i;
                col = j;
            }
        }
    }

    // ROS_INFO("value: %d", cv_ptr->image.at<cv::Vec3b>(0,0).val[0]);
    // ROS_INFO("value: %d", cv_ptr->image.at<cv::Vec3b>(0,0).val[1]);
    // ROS_INFO("value: %d", cv_ptr->image.at<cv::Vec3b>(0,0).val[2]);
    // ROS_INFO("height: %d", msg->height);
    // ROS_INFO("width: %d", msg->width);
    // ROS_INFO_STREAM("encoding: " << msg->encoding);


    // ROS_INFO("r: %d", row);
    // ROS_INFO("c: %d", col);


    //
    // cv::circle(cv_ptr->image, cv::Point(col, row), 10, CV_RGB(255,0,0));
    //
    // // Update GUI Window
    // cv::imshow(OPENCV_WINDOW, cv_ptr->image);
    // cv::waitKey(3);
    //
    // // Output modified video stream
    // image_pub_.publish(cv_ptr->toImageMsg());
    //
    //

    std_msgs::String pixels;
    std::stringstream r;
    r << row;
    std::stringstream rs;
    rs << cv_ptr->image.rows;
    std::stringstream c;
    c << col;
    std::stringstream cs;
    cs << cv_ptr->image.cols;
    pixels.data = r.str() + "," + c.str() + "," + rs.str() + "," + cs.str();
    pixel_pub.publish(pixels);
  }
};

int main(int argc, char** argv)
{
  // ros::init(argc, argv, "image_converter");
  ros::init(argc, argv, "ball");
  ImageConverter ic;
  ros::spin();
  return 0;
}
