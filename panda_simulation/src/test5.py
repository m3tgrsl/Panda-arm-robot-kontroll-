#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point

class Kamera():
    def __init__(self):
        # ROS node ve CV Bridge nesnesi oluşturulur
        rospy.init_node("kamera_dugumus")
        self.bridge = CvBridge()
        # Görüntü yayınını abone ol
        rospy.Subscriber("/r200/camera/color/image_raw", Image, self.kamera_callback)
        # Merkez koordinatlarını yayınlamak için bir yayıncı oluştur
        self.merkez_pub = rospy.Publisher("/nesne/merkezs", Point, queue_size=1)
        rospy.spin()
        
    def kamera_callback(self, mesaj):
        # Görüntüyü OpenCV formatına çevir
        img = self.bridge.imgmsg_to_cv2(mesaj, "mono8")
        # Görüntüyü ikili (binary) formata çevir
        ret, esiklenmis = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        # İkili görüntüdeki sınırları bul
        sinirlar, hiyerarsi = cv2.findContours(esiklenmis, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # En büyük sınırı seç (varsa)
        if len(sinirlar) > 0:
            cnt = sinirlar[0]
            # Sınırın merkezini bul
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # Merkez koordinatlarını ROS mesajı olarak yayınla
            merkez_mesaji = Point()
            merkez_mesaji.x = cx
            merkez_mesaji.y = cy
            #print(merkez_mesaji)
            self.merkez_pub.publish(merkez_mesaji)
            

Kamera()


