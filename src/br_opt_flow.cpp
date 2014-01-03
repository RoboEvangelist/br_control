#include <ros/ros.h>
#include "std_msgs/String.h"
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
/*
static const std::string OPENCV_WINDOW = "Image window";

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  
public:
  ImageConverter()
    : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
//    image_sub_ = it_.subscribe("/camera/image_raw", 1, 
    image_sub_ = it_.subscribe("image", 1, 
      &ImageConverter::imageCb, this);
    image_pub_ = it_.advertise("/image_converter/output_video", 1);

    cv::namedWindow(OPENCV_WINDOW);
  }

  ~ImageConverter()
  {
    cv::destroyWindow(OPENCV_WINDOW);
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

    // Draw an example circle on the video stream
    if (cv_ptr->image.rows > 60 && cv_ptr->image.cols > 60)
      cv::circle(cv_ptr->image, cv::Point(50, 50), 10, CV_RGB(255,0,0));

    // Update GUI Window
    cv::imshow(OPENCV_WINDOW, cv_ptr->image);
    cv::waitKey(3);
    
    // Output modified video stream
    image_pub_.publish(cv_ptr->toImageMsg());
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "br_opt_flow");
  ImageConverter ic;
  ros::spin();
  return 0;
}

*/


#include "std_msgs/String.h"

/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */
// void chatterCallback(const sensor_msgs::ImageConstPtr& msg)
void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
//    cv_bridge::CvImagePtr cv_ptr;
    try
    {
//      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
      std::stringstream ss;
      ss << msg->data.c_str() << " para ti!!!!!";
      std::string s = ss.str();
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }

}

int main(int argc, char **argv)
{
  std::stringstream node_stream;
  // argv[1] is the last byte of a robot's address
  node_stream << "br_opt_flow" << argv[1];
  std::string node_name = node_stream.str();
  ros::init(argc, argv, node_name);

  ros::NodeHandle n;

  std::stringstream sub_stream;
  sub_stream << "/output/image_raw/compressed" << argv[1];
  std::string sub_name = sub_stream.str();
  ros::Subscriber sub = n.subscribe(sub_name, 1000, chatterCallback);

  ros::spin();

  return 0;
}
