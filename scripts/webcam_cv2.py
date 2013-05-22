import cv2
import numpy as np

def draw_flow(im, flow, step=16):
    #Plot optical flow
    #im is a frame of the video
    #flow is a two channel image drawn of flow vectors

    h,w=im.shape[:2]
    y,x=np.mgrid[step/2:h:step,step/2:w:step].reshape(2,-1)
    fx,fy=flow[y,x].T

    lines=np.vstack([x,y,x+fx,y+fy]).T.reshape(-1,2,2)
    lines=np.int32(lines)

    vis=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    for (x1,y1),(x2,y2) in lines:
	    cv2.line(vis,(x1,y1),(x2,y2),(0,255,0),1)
	    cv2.circle(vis,(x1,y1),1,(0,255,0),1)
    return vis

c=cv2.VideoCapture(0)
ret,im = c.read()
prev_gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

while (1):
	ret,im=c.read()
	gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

	flow=cv2.calcOpticalFlowFarneback(prev_gray,gray,0.5,1,1,15,3,5,1)
    	cv2.imshow('optical flow',draw_flow(im,flow))
    	if cv2.waitKey(1)==27:
		break

cv2.destroyAllWindows()
