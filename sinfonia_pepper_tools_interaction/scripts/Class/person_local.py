#!/usr/bin/env python
# license removed for brevity

"""
//======================================================================//
//  This software is free: you can redistribute it and/or modify        //
//  it under the terms of the GNU General Public License Version 3,     //
//  as published by the Free Software Foundation.                       //
//  This software is distributed in the hope that it will be useful,    //
//  but WITHOUT ANY WARRANTY; without even the implied warranty of      //
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE..  See the      //
//  GNU General Public License for more details.                        //
//  You should have received a copy of the GNU General Public License   //
//  Version 3 in the file COPYING that came with this distribution.     //
//  If not, see <http://www.gnu.org/licenses/>                          //
//======================================================================//
//                                                                      //
//      Copyright (c) 2019 SinfonIA Pepper RoboCup Team                 //
//      Sinfonia - Colombia                                             //
//      https://sinfoniateam.github.io/sinfonia/index.html              //
//                                                                      //
//======================================================================//
"""
import cv2
import os
import sys
import face_recognition


class PersonLocal:

    def __init__(self):
        pass

    def detectPerson(self, frame):
        self.frame = frame
        # cap = cv2.VideoCapture(0)
        # ret, img = cap.read()
        rgb_frame = frame[:, :, ::-1]
        frame_size = frame.shape[0]*frame.shape[1]
        face_locations = face_recognition.face_locations(rgb_frame)
        peoples = list()
        print("Face detected ",len(face_locations))

        for face_location in face_locations:
            width = face_location[1]-face_location[3]
            height = face_location[2]-face_location[0]
            dictionary_of_features = {'faceId': None, 'faceRectangle': {'width': int(width), 'top': int(
                face_location[0]), 'height': int(height), 'left': int(face_location[3])}, 'faceAttributes': None}
            peoples.append(dictionary_of_features)
        peoples.sort(key=sortDictionary, reverse=True)

        return peoples


class Less_Blurred:
    def __init__(self, nImages):
        self.nImages = nImages
        self.fm = qe.PriorityQueue(100)
        self.frames = []

    def sort_less_blurred(self, images):
        self.fm = qe.PriorityQueue(100)
        self.frames = []
        if type(images) == dict:
            for imgID in images:
                self.fm.put(
                    (1/cv2.Laplacian(images[imgID], cv2.CV_64F).var(), imgID))
            for i in range(self.nImages):
                dat = self.fm.get()
                nIma = dat[1]
                self.frames.append(images[nIma])
        else:
            print('review images type')

def sortDictionary(val):
    return val['faceRectangle']['width']