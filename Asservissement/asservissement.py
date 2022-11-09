import numpy as np
import cv2
import math

img1 = cv2.imread('Asservissement/Image1.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('Asservissement/Image2.png', cv2.IMREAD_GRAYSCALE)

akaze = cv2.AKAZE_create()
kp1, des1 = akaze.detectAndCompute(img1, None)
kp2, des2 = akaze.detectAndCompute(img2, None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

good_matches = []
for m, n in matches:
    if m.distance < 0.75*n.distance:
        good_matches.append([m])

output = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imwrite('Asservissement/output.png', output)

# Select good matched keypoints
ref_matched_kpts = np.float32([kp1[m[0].queryIdx].pt for m in good_matches])
sensed_matched_kpts = np.float32([kp2[m[0].trainIdx].pt for m in good_matches])

# Compute homography
H, status = cv2.findHomography(sensed_matched_kpts, ref_matched_kpts, cv2.RANSAC,5.0)
#print(H)
theta=math.degrees(math.asin(H[1][0]))

print(H[0][2]) # Deplacement en x (beaucoup de chance que ce soit en pixel (à vérifier))
print(H[1][2]) # Deplacement en y (beaucoup de chance que ce soit en pixel (à vérifier))
print(theta) # Rotation

# Warp image
warped_image = cv2.warpPerspective(img2, H, (img2.shape[1], img2.shape[0]))
            
cv2.imwrite('Asservissement/warped.jpg', warped_image)