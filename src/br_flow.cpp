#include "ros/ros.h"
#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <cmath>
 
using namespace cv;
using namespace std; 
 
int main(int argc, char** argv)
{
	// Load two images and allocate other structures
	Mat imgA = imread("images/1.png", CV_LOAD_IMAGE_GRAYSCALE);
	Mat imgB = imread("images/3.png", CV_LOAD_IMAGE_GRAYSCALE);
	
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
