
#!/usr/bin/env python3
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import cv2
from pyzbar.pyzbar import decode


def scan_barcode():

    # cap = cv2.VideoCapture(0)

    # while True:
    #     if not cap.isOpened():
    #         print("cannot open camera ")
    #     success , img = cap.read()
    #     cv2.imshow('Result',img)
    #     cv2.waitKey(1)
    #     code=decode(img)
    #     print(len(code))
    #     if len(code) > 0:
    #         message = code[0].data.decode('utf-8')
    #         print(message)
    #         break

    img = cv2.imread("/home/warlord/Desktop/ros_ws/src/Robotics_ws/src/atom/script/Barcodes/barcode1.jpg")
    cv2.imshow('Result',img)
    cv2.waitKey(3000) 
    code=decode(img)
    message = code[0].data.decode('utf-8')
    print(message , "is the message.....reaching rack")


    return message

def movebase_client(x,y):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.z = 0
    goal.target_pose.pose.orientation.w = 1

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':

    racks_coordinates = {"Classics":(-5,1),
                         "Comic & Novels":(-10,1),
                         "Detective/Mystery":(-5,4) ,
                         "Fantasy":(-10,4),
                         "Historical Fiction":(-5,7),
                         "Horror":(-10,7),
                         "Romance":(-5,10),
                         "Literary Fiction":(-10,10)
                         }

    try:
        message = scan_barcode()
        coordinate = racks_coordinates[message]
        # print(coordinate)
        if message in racks_coordinates:
            # print("Reaching coordinate" , coordinate[0],",",coordinate[1])
            rospy.init_node('movebase_client_py')
            result = movebase_client(coordinate[0],coordinate[1])
            if result:
                rospy.loginfo("Goal execution done!")
        else:
            print("Try again")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

         