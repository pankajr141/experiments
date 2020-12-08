from scipy.spatial import distance
import numpy as np
import cv2

def detect_nearest_neighbours(midpoints, num, thresh):
    person_1 = []
    person_2 = []
    distances = []
    for i in range(num):
      for j in range(num):
          if i >= j:
              continue
          distance_ = distance.euclidean(midpoints[i], midpoints[j])
          if not distance_ <= thresh:
              continue
          person_1.append(i)
          person_2.append(j)
          distances.append(distance_)
    return person_1, person_2, distances

#define a function which return the bottom center of every bbox
def mid_point(img, person, idx):
  #get the coordinates
  x1, y1, x2, y2 = person[idx]
  _ = cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 1)

  #compute bottom center of bbox
  x_mid = int((x1+x2)/2)
  y_mid = int(y2)
  mid   = (x_mid,y_mid)
  
  _ = cv2.circle(img, mid, 3, (0, 255, 0), -1)
  cv2.putText(img, str(idx), mid, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
  return mid

def change_2_red(img,person,p1,p2):
  risky = np.unique(p1+p2)
  for i in risky:
    x1,y1,x2,y2 = person[i]
    _ = cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 1)  
  return img