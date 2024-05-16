import cv2
import numpy as np

url = "http://192.168.1.17:5000"
vid = cv2.VideoCapture(url)


# DISTANCE FUNCTION FOR LINE MERGING
def distance(line1, line2):
    line1x1, line1x2, line1y1, line1y2 = line1[0]
    line2x1, line2x2, line2y1, line2y2 = line2[0]

    distx1 = abs(line1x1 - line2x1)
    distx2 = abs(line1x2 - line2x2)
    disty1 = abs(line1y1 - line2y1)
    disty2 = abs(line1y2 - line2y2)

    totaldist = int((distx1 + distx2 + disty1 + disty2)/4)

    print(totaldist)
    return (totaldist)



def road_overlay_stream():

    global vid

    while (True):
        ret, frame = vid.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (5, 5))
        canny = cv2.Canny(blur, 100, 200)

        lines = cv2.HoughLinesP(canny, rho=1, theta=np.pi / 180, threshold=30, minLineLength=5, maxLineGap=300)

        if lines is not None:  # if no lines detected

            slopes = []
            valid_lines = []
            midlinex1s = []
            midliney1s = []
            midlinex2s = []
            midliney2s = []

            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 8)
                slope1 = (y2 - y1) / ((x2 - x1) + 1)  # +1 prevents denominator from being 0
                slope1_degrees = np.rad2deg(np.arctan(slope1))
                if slope1_degrees > 30 and slope1_degrees < 80:
                    valid_lines.append(line)
                if slope1_degrees < -30 and slope1_degrees > -80:
                    valid_lines.append(line)
                slopes.append(slope1)

            for line in valid_lines:
                x1_1, y1_1, x2_1, y2_1 = line[0]
                #cv2.line(frame, (x1_1, y1_1), (x2_1, y2_1), (255, 255, 0), 8)
                midlinex1s.append(x1_1)
                midliney1s.append(y1_1)
                midlinex2s.append(x2_1)
                midliney2s.append(y2_1)

                for line2 in valid_lines:
                    dist = distance(line, line2)



            try:
                midlinex1 = int(sum(midlinex1s) / len(midlinex1s))
                midliney1 = int(sum(midliney1s) / len(midliney1s))
                midlinex2 = int(sum(midlinex2s) / len(midlinex2s))
                midliney2 = int(sum(midliney2s) / len(midliney2s))
                cv2.line(frame, (midlinex1, midliney1), (midlinex2, midliney2), (0, 0, 255), 5)
            except:
                print("Divide by 0")




        resized = cv2.resize(frame, (400, 280))

        yield ret, resized
    vid.release()

def road_stream():

    global vid

    while True:

        ret, frame = vid.read()

        if not ret:
            break

        resized = cv2.resize(frame, (400, 280))

        yield ret, resized
    vid.release()