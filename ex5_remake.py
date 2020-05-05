# -*- coding: utf-8 -*-
import cv2
import numpy as np
import csv
import json

import math
CV_WAITKEY_CURSORKEY_RIGHT  = 2555904; #右カーソルID
CV_WAITKEY_CURSORKEY_LEFT   = 2424832; #左カーソルID

with open('csvmigite.csv') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
             
with open('csvkata.csv') as p:
        reader = csv.reader(p)
        k = [row for row in reader]
with open('csvkoshi.csv') as s:
        reader = csv.reader(s)
        m = [row for row in reader]
        
        
def save_video( frame_W, frame_H, cap ):

    cap.set( cv2.CAP_PROP_POS_FRAMES, 0 )

    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out    = cv2.VideoWriter( 'video_out.mp4' , fourcc, 20.0, (frame_W, frame_H) )
    #fourcc = -1
    #out = cv2.VideoWriter( 'video.avi' , fourcc, 20.0, (frame.shape[1], frame.shape[0])
    flag=0
    rightmaxflag=0
    count=0
    maxlong=0
    switch=0
    switchingflag=0
    switchingflagcount=0
    minnable=100
    while( True ) : 
        ret, frame = cap.read()
        if ret == False :
            break
        
        count += 1
        radian = math.atan2( float(k[count][1])-float(l[count][1]),float(k[count][0])-float(l[count][0]))
        deg=math.degrees(radian)

        #スイッチ設定
        if switchingflag==1:
            switchingflagcount+=1
            if switchingflagcount==5:
                switchingflagcount=0
                switchingflag=0
        
        
        mk=(3.0*float(k[count][1]) + 1.0*float(m[count][1]))/4

        d=math.sqrt((float(k[count][0])-float(l[count][0]))**2+(float(k[count][1])-float(l[count][1]))**2)
        if abs(float(l[count][1])-mk)<3.0:
            if switchingflag==0:
                if switch==0:
                    switch=1
                    switchingflag=1
                else : #switch==1
                    
                    switch=0
                    switchingflag=1
        elif abs(abs(float(k[count][0])-float(l[count][0]))-abs(mk-float(k[count][1])))<1.0:
            if switchingflag==0:
                if switch==1:
                    switch=2
                    switchingflag=1
                elif switch==2:
                    switch=1
                    switchingflag=1
        
        
        #各スイッチ内の処理
        if switch==0:
            if -100<deg and deg <-80:
                flag=1
            else :
                flag=2

        elif switch==1: #switch==1 
            if d<mk-float(k[count][1]):
                flag=1
            else :
                flag=2

        else :    #switch==2    
            if -20<=deg and deg<=20:
                flag=1
            else :
                flag=2
        
        
        if flag==0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'now testing...',(200,550), font, 4,(0,255,0),2,cv2.LINE_AA)
        
        elif flag==1 :
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'OK',(200,550), font, 4,(0,0,255),2,cv2.LINE_AA)
        elif flag==2:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'NO',(200,550), font, 4,(255,0,0),2,cv2.LINE_AA) 

        ##フォント系
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'frame:  '+str(count),(10,70), font, 1.2,(127,127,127),2,cv2.LINE_AA)
        cv2.putText(frame,'switch '+str(switch),(10,200), font, 1.2,(0,255,0),2,cv2.LINE_AA)
        if switch==0 :
            cv2.putText(frame,'virtical move ',(10,300), font, 1.2,(0,255,0),2,cv2.LINE_AA)
            cv2.putText(frame,'-100<=degree<=-80',(10,350), font, 1.2,(0,255,0),2,cv2.LINE_AA)
           
        elif switch==1 :
            cv2.putText(frame,'around kata ',(10,300), font, 1.2,(0,255,0),2,cv2.LINE_AA)
            cv2.putText(frame,' distance < '+str(int(mk-float(k[count][1]))),(10,350), font, 1.2,(0,255,0),2,cv2.LINE_AA)
        else :#switch==2
            cv2.putText(frame,'side move',(10,300), font, 1.2,(0,255,0),2,cv2.LINE_AA)
            cv2.putText(frame,' -20<=degree<=20',(10,350), font, 1.2,(0,255,0),2,cv2.LINE_AA)
            
        cv2.putText(frame,'kata:  x'+str(int(float(k[count][0])))+'  y'+str(int(float(k[count][1]))),(10,600), font, 1.2,(0,255,0),2,cv2.LINE_AA)
       # font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'migite:x'+str(int(float(l[count][0])))+'  y'+str(int(float(l[count][1]))),(10,650), font, 1.2,(0,255,0),2,cv2.LINE_AA)
        cv2.putText(frame,'kosi:  x'+str(int(float(m[count][0])))+'  y'+str(int(float(m[count][1]))),(10,700), font, 1.2,(0,255,0),2,cv2.LINE_AA)
       
        if minnable>(abs(abs(float(k[count][0])-float(l[count][0]))-abs(mk-float(k[count][1])))):
            minnable=(abs(abs(float(k[count][0])-float(l[count][0]))-abs(mk-float(k[count][1]))))
       # cv2.putText(frame,'yoko:'+ str(int(minnable)),(10,300), font, 1.2,(0,255,0),2,cv2.LINE_AA)
        #cv2.putText(frame,'mk='+str(int(mk)),(10,350), font, 1.2,(0,0,255),2,cv2.LINE_AA)
       
          #flag color
        if flag==1:
            cv2.putText(frame,'flag '+str(flag),(10,550), font, 1.2,(0,0,255),2,cv2.LINE_AA)
        else :
            cv2.putText(frame,'flag '+str(flag),(10,550), font, 1.2,(255,0,0),2,cv2.LINE_AA)
        
        
        #円
        
        
        cv2.circle(frame,(int(float(k[count][0])),int(float(k[count][1]))), 5, (0,0,255), -1)
        cv2.circle(frame,(int(float(l[count][0])),int(float(l[count][1]))), 5, (0,0,255), -1)
        cv2.circle(frame,(int(float(m[count][0])),int(float(m[count][1]))), 5, (0,0,255), -1)
           #判定域
        if switch ==1:
            if flag==1 :
                cv2.circle(frame,(int(float(k[count][0])),int(float(k[count][1]))),int(mk-float(k[count][1])) , (0,0,255), 2)
            else  : #flag==2
                cv2.circle(frame,(int(float(k[count][0])),int(float(k[count][1]))), int(mk-float(k[count][1])), (255,0,0), 2)
                
                
           #楕円
        if switch==0 or switch==2:
            if flag==1 :
                cv2.ellipse(frame,(int(float(k[count][0])),int(float(k[count][1]))),(50,50),270,deg-90,-90,(0,0,255),thickness=-1)
                cv2.putText(frame,'degree '+str(int(deg)),(10,400), font, 1.2,(0,0,255),2,cv2.LINE_AA)
                cv2.putText(frame,'distance '+str(int(d)),(10,450), font, 1.2,(0,152,243),2,cv2.LINE_AA)
            else : #flag==2
                cv2.ellipse(frame,(int(float(k[count][0])),int(float(k[count][1]))),(50,50),270,deg-90,-90,(255,0,0),thickness=-1)
                cv2.putText(frame,'degree '+str(int(deg)),(10,400), font, 1.2,(255,0,0),2,cv2.LINE_AA)
                cv2.putText(frame,'distance '+str(int(d)),(10,450), font, 1.2,(0,152,243),2,cv2.LINE_AA)
        else : #switch==1
            cv2.ellipse(frame,(int(float(k[count][0])),int(float(k[count][1]))),(50,50),270,deg-90,-90,(0,152,243),thickness=-1)
            cv2.putText(frame,'degree '+str(int(deg)),(10,400), font, 1.2,(0,152,243),2,cv2.LINE_AA)
            if flag==1:
                cv2.putText(frame,'distance '+str(int(d)),(10,450), font, 1.2,(0,0,255),2,cv2.LINE_AA)
            else :
                cv2.putText(frame,'distance '+str(int(d)),(10,450), font, 1.2,(255,0,0),2,cv2.LINE_AA)
        
        #線line
        cv2.line(frame,(int(float(k[count][0])),int(float(k[count][1]))),(int(float(l[count][0])),int(float(l[count][1]))),(0,255,0),2)
        cv2.line(frame,(int(float(k[count][0])),int(float(k[count][1]))),(int(float(m[count][0])),int(float(m[count][1]))),(0,255,0),2)
        cv2.line(frame,(400,int(mk)),(800,int(mk)),(0,255,0),2)
        cv2.line(frame,(400,int(float(k[count][1]))),(800,int(float(k[count][1]))),(0,255,0),2)
       
        
        out.write( frame )
    out.release()



if __name__ == '__main__':
   
   
    # read video
    cap   = cv2.VideoCapture( "video/RU.MOV"  )
    ret, frame = cap.read()

    frame_num  = int( cap.get(cv2.CAP_PROP_FRAME_COUNT) )
    frame_H    = frame.shape[0]
    frame_W    = frame.shape[1]
    frame_half = cv2.resize(frame, (frame_W // 2, frame_H // 2) )
    cv2.imshow( "video vis", frame_half)
    frame_I    = 0

    while (True) : 
        key = cv2.waitKey( 0 ) 
        
        if(   key == ord('q') ) :
            exit()
        elif( key == CV_WAITKEY_CURSORKEY_RIGHT ) :
            frame_I = min(frame_I+1, frame_num-1)
        elif( key == CV_WAITKEY_CURSORKEY_LEFT  ) :
            frame_I = max(frame_I-1, 0)
        
        elif( key == ord('s') ) : 
            save_video( frame_W, frame_H, cap )

        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_I)
        ret, frame = cap.read()
        frame_half = cv2.resize(frame, (frame_W // 2, frame_H // 2))
        cv2.imshow("video vis", frame_half)

        print("current frame i = ", frame_I)
