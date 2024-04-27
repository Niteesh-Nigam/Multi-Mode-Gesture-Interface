import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
from util import *
from pynput.keyboard import Controller
import pyautogui
# from TEST import loc_resize_keyboard

# Initialize the video capture and detector
cap = cv2.VideoCapture(2)  # Adjust the device index according to your setup
cap.set(3,1280)
cap.set(4, 720)
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.95, minTrackCon=0.8)

options = np.arange(2)  # Placeholder array
i = 0
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False
# print("Option1 Selected: Typing Mode")
last_time0 = 0
last_time = 0  # Timestamp to manage the delay
last_time1 = 0
attached_move = False
attached_resize = False
finalText=""
ret, img1 = cap.read()
img1 = cv2.flip(img1, 1)
frame_height, frame_width, _ = img1.shape

# Start the rectangle at the center of the frame
move_x, move_y = frame_width // 2, frame_height // 3  # Correct assignment for X and Y
w, h = 500, 300
keyboard = Controller()
# buttonList = []  # Placeholder for UI elements
hand_presence_counter = 0
hand_absence_counter = 0
debounce_threshold = 5
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=True, flipType=False)
    # ret, img = cap.read()
    if i==0:
        cv2.rectangle(img, (1100, 0), (1280, 30), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (1100, 30), (1280, 60), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (1100, 60), (1280, 90), (0, 0, 255), cv2.FILLED)
    elif i==1:
        cv2.rectangle(img, (1100, 0), (1280, 30), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (1100, 30), (1280, 60), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (1100, 60), (1280, 90), (0, 0, 255), cv2.FILLED)
    elif i==2:
        cv2.rectangle(img, (1100, 0), (1280, 30), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (1100, 30), (1280, 60), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (1100, 60), (1280, 90), (0, 255, 0), cv2.FILLED)

    cv2.putText(img, "TYPING MODE", (1100, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, "RESIZE MODE", (1100, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, "MOUSE MODE", (1100, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    if hands:
        hand_absence_counter = 0
        hand_presence_counter += 1
    else:
        hand_presence_counter = 0
        hand_absence_counter += 1

        # Determine if a stable state has been reached
    stable_hands = None
    if hand_presence_counter > debounce_threshold:
        stable_hands = hands
    elif hand_absence_counter > debounce_threshold:
        stable_hands = []

    if stable_hands:  # Check if 1 second has passed
        hand1 = stable_hands[0]
        lmList1 = hand1['lmList']
        bbox1 = hand1['bbox']
        center1 = hand1['center']
        handType1 = hand1['type']

        rect_x1 = move_x - w // 2
        rect_y1 = move_y + 10
        rect_x2 = move_x + w // 2
        rect_y2 = move_y + h + 10
        # Draw the rectangle on the frame (for visualization, can be omitted if not needed)
        # cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (255, 255, 0), cv2.FILLED)

        # keyboard_image = create_keyboard_layout(rect_x2 - rect_x1, rect_y2 - rect_y1)
        keyboard_image, buttonList, text_start_x, text_start_y, text_end_x, text_end_y, key_width = create_keyboard_layout(rect_x1, rect_x2, rect_y1, rect_y2)
        img[rect_y1:rect_y2, rect_x1:rect_x2] = keyboard_image
        cv2.circle(img, (move_x, move_y), 5, (0, 0, 255), -1)
        cv2.circle(img, ((move_x + w // 2 + 10), (move_y + 10 + h)), 5, (0, 0, 255), -1)


        current_time0 = time.time()
        if len(stable_hands) == 2 and (current_time0 - last_time0 > 1):
            hand2 = stable_hands[1]
            lmList2 = hand2['lmList']
            handType2 = hand1['type']

            length_option1_1, info_option1_1, _ = detector.findDistance(lmList1[0][0:2], lmList2[0][0:2], img)
            length_option1_2, info_option1_2, _ = detector.findDistance(lmList1[4][0:2], lmList2[4][0:2], img)
            current_time0 = time.time()
            # print(length_option1_1, length_option1_2)



            current_time = time.time()
            if length_option1_1 < 50 and length_option1_2 < 150 and (current_time - last_time > 1):
                i += 1

                last_time = current_time
                if i == 3:
                    i=0
                #     print("Option0 Selected: Typing Mode")
                #       # Reset the counter after action
                # last_time = current_time  # Update the last interaction time
    # cv2.imshow("Hand Control Interface", img)
        current_time1 = time.time()
        if i==0 and len(hands)==1 and handType1 == "Right":
            # pass
            # print("Option1 Selected: Typing Mode")
            for button in buttonList:
                x, y = button.pos[0]+move_x-w/2, button.pos[1]+move_y
                button_w, button_h = button.size
                # print("helooo2222")
                if x < lmList1[8][0] < x + button_w and y < lmList1[8][1] < y + button_h:
                    # cv2.rectangle(img, (button.pos), (button.pos[0] + button.size[0], button.pos[1] + button.size[1]), (0, 0, 175), cv2.FILLED)
                    # # print(button.pos[0]+move_x-w/2)
                    # # cv2.rectangle(img, (x,y), (x + button_w, y + button.size[1]),(0, 0, 175), cv2.FILLED)
                    # cv2.putText(img, button.text, (button.pos[0] + 22, button.pos[1] + 75), cv2.FONT_HERSHEY_PLAIN, 5,
                    #             (255, 255, 255), 5)
                    length3, _, _ = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
                    # print("heloooooooooooooooooooooo")

                    current_time1 = time.time()
                    if length3 < 25 and (current_time1 - last_time1 > 0.5):
                        keyboard.press(button.text)
                        # cv2.rectangle(img, button.pos, (button.pos[0] + button.size[0], button.pos[1] + button.size[1]),
                        #               (0, 255, 0), cv2.FILLED)
                        # cv2.putText(img, button.text, (button.pos[0] + 22, button.pos[1] + 15), cv2.FONT_HERSHEY_PLAIN,
                        #             5,
                        #             (255, 255, 255), 5)
                        # print("helo11111111111111")

                        finalText += button.text
                        last_time1 = current_time1
        # cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (int(text_start_x+ move_x-w/2 ), int(text_start_y+ move_y+w/10.2)), cv2.FONT_HERSHEY_PLAIN, key_width / 17,
                    (255, 255, 255), key_width // 15)


        if i==1 and len(hands)==1 and handType1 == "Right":
            # pass
            # print("Option2 Selected: Resize Keyboard")
            if handType1 == "Right":
                if not attached_move:
                    # Calculate distance between index fingertip (landmark 8) and thumb tip (landmark 4)
                    length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
                    # move_x, move_y = lmList1[8][0], lmList1[8][1]  # Follow the index finger
                    cv2.circle(img, (move_x, move_y), 30, (255, 0, 0), 2)
                    length1, info1, frame1 = detector.findDistance((move_x, move_y), lmList1[12][0:2], img)

                    if length < 30 and length1 < 30:  # If fingers close together, toggle attachment
                        attached_move = True
                        print("Attached_move")
                else:
                    # Check if user performs the detach gesture
                    length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
                    move_x, move_y = lmList1[12][0], lmList1[12][1]
                    if length < 30:
                        attached_move = False
                        print("Detached_move")
                        # Update position where rectangle will be dropped
                        move_x, move_y = lmList1[12][0], lmList1[12][1]
                # print(f"{info[0],info[1]}")

                length2, info2, frame2 = detector.findDistance(((move_x + w // 2 + 10), (move_y + 10 + h)),
                                                               lmList1[12][0:2], img)
                if not attached_resize:
                    length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
                    cv2.circle(img, ((move_x + w // 2 + 10), (move_y + 10 + h)), 30, (255, 0, 0), 2)
                    # length2, info2, frame2 = detector.findDistance(((move_x + w // 2+10), (move_y + 10+h)), lmList1[12][0:2], frame)
                    if length < 30 and length2 < 30:
                        # cv2.circle(frame, ((move_x + w // 2 + 10), (move_y + 10 + h)), 30, (255, 0, 0), 2)
                        attached_resize = True
                        print("Attached_resize")
                else:
                    length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
                    w = int(w + (lmList1[12][0] - (move_x + w // 2 + 10)))
                    h = int(h + (lmList1[12][1] - (move_y + 10 + h)))
                    if length < 30:
                        attached_resize = False
                        print("Detached_resize")

        if i==2 and len(hands)==1 and handType1 == "Right":
            # pass
            # print("Option3 Selected: Mouse Mode")

            border_x, border_y = int(screen_width / frame_width * 66.7 * 2), int(
                screen_height / frame_height * 66.7 * 2)
            crop_width, crop_height = frame_width - border_x, frame_height - border_y

            # Finding hands in the frame
            # hands, img = detector.findHands(frame, draw=True, flipType=False)

            # if hands:
            #     hand1 = hands[0]
            #     lmList1 = hand1['lmList']
            #     bbox1 = hand1['bbox']
            #     center1 = hand1['center']
            #     handType1 = hand1['type']

            if handType1 == "Right":
                # Calculate screen coordinates
                thumb_x, thumb_y = lmList1[8][0], lmList1[8][1]

                # Map to cropped frame coordinates
                cropped_x, cropped_y = map_to_cropped_frame(thumb_x, thumb_y, frame_width, frame_height, crop_width,
                                                            crop_height)

                # Scale these coordinates to the screen
                screen_x = cropped_x * screen_width / crop_width
                screen_y = cropped_y * screen_height / crop_height

                pyautogui.moveTo(screen_x, screen_y)

                # Check for click gesture
                length, info, _ = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
                if length < 10:
                    pyautogui.click()
                    pyautogui.sleep(1)


    cv2.imshow("Hand Control Interface", img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()