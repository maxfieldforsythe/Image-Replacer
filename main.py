import cv2
import numpy as np

def main():
    import cv2
    import sys
    import numpy as np
    # Read images
    bgr_img = cv2.imread("US_Cellular.jpg")
    overlay_img = cv2.imread("Blip-BillBoards-1.jpg")
    # create blank image the size of the overlay image
    blank = np.zeros(overlay_img.shape).astype(overlay_img.dtype)
    # points from bgr image and target overlay img
    pts1_ortho = np.array([[628, 385], [905, 371], [633, 498], [908, 480]])
    pts1 = np.array([[356, 232], [1289, 108], [359, 525], [1293, 484]])
    # Fill the blank image with white inside the bounds of the points
    cv2.fillPoly(blank, [np.array([[356, 232], [1289, 108], [1293, 484], [359, 525]])],
                 color=[255, 255, 255])
    # use the bitwise and to reverse the image so that the new billboard is surrounded by black pixels

    result = cv2.bitwise_and(overlay_img, blank)
    # Compute the homagraphy matrix
    H1, _ = cv2.findHomography(srcPoints=pts1, dstPoints=pts1_ortho)
    # Output dimensions equal to resolution of bgr_img
    output_width = 2592
    output_height = 1944
    # apply perspective warp to new billboard
    bgr_ortho = cv2.warpPerspective(result, H1, (output_width, output_height))
    # Fill the are of the billboard on the bgr_img with black pixels
    cv2.fillPoly(bgr_img, pts=[np.array([[628, 385], [905, 371], [908, 480], [633,
                                                                              498]])], color=(0, 0, 0))
    # Adding the images so that the black space is filled with pixels from the opposite images
    final = cv2.add(bgr_img, bgr_ortho)
    # Show final image and write
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", final)
    cv2.imwrite("Final.jpg", final)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
