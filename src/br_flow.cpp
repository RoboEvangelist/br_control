#include "ros/ros.h"
#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <cmath>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
 
/*
using namespace cv;
using namespace std; 
 
int main(int argc, char** argv)
{
	// Load two images and allocate other structures
	Mat imgA = imread("im1.jpg", CV_LOAD_IMAGE_GRAYSCALE);
	Mat imgB = imread("im2.jpg", CV_LOAD_IMAGE_GRAYSCALE);
	
	Size img_sz = imgA.size();
	Mat imgC(img_sz,1);
 
	int win_size = 15;
	int maxCorners = 20; 
    double qualityLevel = 0.05; 
    double minDistance = 5.0; 
    int blockSize = 3; 
    double k = 0.04; 
    std::vector<cv::Point2f> cornersA; 
    cornersA.reserve(maxCorners); 
	std::vector<cv::Point2f> cornersB; 
    cornersB.reserve(maxCorners);
	
 
	goodFeaturesToTrack( imgA,cornersA,maxCorners,qualityLevel,minDistance,cv::Mat());
	goodFeaturesToTrack( imgB,cornersB,maxCorners,qualityLevel,minDistance,cv::Mat());
 
	cornerSubPix( imgA, cornersA, Size( win_size, win_size ), Size( -1, -1 ), 
				  TermCriteria( CV_TERMCRIT_ITER | CV_TERMCRIT_EPS, 20, 0.03 ) );
	
	cornerSubPix( imgB, cornersB, Size( win_size, win_size ), Size( -1, -1 ), 
				  TermCriteria( CV_TERMCRIT_ITER | CV_TERMCRIT_EPS, 20, 0.03 ) );
 
	// Call Lucas Kanade algorithm
 
	CvSize pyr_sz = Size( img_sz.width+8, img_sz.height/3 );
 
	std::vector<uchar> features_found; 
    features_found.reserve(maxCorners);
	std::vector<float> feature_errors; 
	feature_errors.reserve(maxCorners);
    
	calcOpticalFlowPyrLK( imgA, imgB, cornersA, cornersB, features_found, feature_errors ,
		Size( win_size, win_size ), 5,
		 cvTermCriteria( CV_TERMCRIT_ITER | CV_TERMCRIT_EPS, 20, 0.3 ), 0 );
 
	// Make an image of the results
 
	for( int i=0; i < features_found.size(); i++ ){
			cout<<"Error is "<<feature_errors[i]<<endl;
			//continue;
	
		cout<<"Got it"<<endl;
		Point p0( ceil( cornersA[i].x ), ceil( cornersA[i].y ) );
		Point p1( ceil( cornersB[i].x ), ceil( cornersB[i].y ) );
		line( imgC, p0, p1, CV_RGB(255,255,255), 2 );
	}
 
	namedWindow( "ImageA", 0 );
	namedWindow( "ImageB", 0 );
	namedWindow( "LKpyr_OpticalFlow", 0 );
 
	imshow( "ImageA", imgA );
	imshow( "ImageB", imgB );
	imshow( "LKpyr_OpticalFlow", imgC );
 
	cvWaitKey(0);
	
	return 0;
}
*/


using namespace cv;
using namespace std;

#define MAX_COUNT 500
char rawWindow[] = "Raw Video";
char opticalFlowWindow[] = "Optical Flow Window";
char imageFileName[32];
long imageIndex = 0;
char keyPressed;

int main() {
 VideoCapture cap(0);

  Mat frame, grayFrames, rgbFrames, prevGrayFrame;
 Mat opticalFlow = Mat(cap.get(CV_CAP_PROP_FRAME_HEIGHT),
   cap.get(CV_CAP_PROP_FRAME_HEIGHT), CV_32FC3);

  vector<Point2f> points1;
 vector<Point2f> points2;

  Point2f diff;

  vector<uchar> status;
 vector<float> err;

  RNG rng(12345);
 Scalar color = Scalar(rng.uniform(0, 255), rng.uniform(0, 255),
   rng.uniform(0, 255));
 bool needToInit = true;

  int i, k;
 TermCriteria termcrit(CV_TERMCRIT_ITER | CV_TERMCRIT_EPS, 20, 0.03);
 Size subPixWinSize(10, 10), winSize(31, 31);
 namedWindow(rawWindow, CV_WINDOW_AUTOSIZE);
 double angle;

  while (1) {
  cap >> frame;
  frame.copyTo(rgbFrames);
  cvtColor(rgbFrames, grayFrames, CV_BGR2GRAY);

   if (needToInit) {
   goodFeaturesToTrack(grayFrames, points1, MAX_COUNT, 0.01, 5, Mat(),
     3, 0, 0.04);
   needToInit = false;
  } else if (!points2.empty()) {
   cout << "\n\n\nCalculating  calcOpticalFlowPyrLK\n\n\n\n\n";
   calcOpticalFlowPyrLK(prevGrayFrame, grayFrames, points2, points1,
     status, err, winSize, 3, termcrit, 0, 0.001);

    for (i = k = 0; i < points2.size(); i++) {
    cout << "Optical Flow Difference... X is "
      << int(points1[i].x - points2[i].x) << "\t Y is "
      << int(points1[i].y - points2[i].y) << "\t\t" << i
      << "\n";

     if ((points1[i].x - points2[i].x) > 0) {
     line(rgbFrames, points1[i], points2[i], Scalar(0, 0, 255),
       1, 1, 0);

      circle(rgbFrames, points1[i], 2, Scalar(255, 0, 0), 1, 1,
       0);

      line(opticalFlow, points1[i], points2[i], Scalar(0, 0, 255),
       1, 1, 0);
     circle(opticalFlow, points1[i], 1, Scalar(255, 0, 0), 1, 1,
       0);
    } else {
     line(rgbFrames, points1[i], points2[i], Scalar(0, 255, 0),
       1, 1, 0);

      circle(rgbFrames, points1[i], 2, Scalar(255, 0, 0), 1, 1,
       0);

      line(opticalFlow, points1[i], points2[i], Scalar(0, 255, 0),
       1, 1, 0);
     circle(opticalFlow, points1[i], 1, Scalar(255, 0, 0), 1, 1,
       0);
    }
    points1[k++] = points1[i];

    }

    goodFeaturesToTrack(grayFrames, points1, MAX_COUNT, 0.01, 10, Mat(),
     3, 0, 0.04);

   }

   imshow(rawWindow, rgbFrames);
  imshow(opticalFlowWindow, opticalFlow);

   std::swap(points2, points1);
  points1.clear();
  grayFrames.copyTo(prevGrayFrame);

   keyPressed = waitKey(10);
  if (keyPressed == 27) {
   break;
  } else if (keyPressed == 'r') {
   opticalFlow = Mat(cap.get(CV_CAP_PROP_FRAME_HEIGHT),
     cap.get(CV_CAP_PROP_FRAME_HEIGHT), CV_32FC3);
  }

  }
}
