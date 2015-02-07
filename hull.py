"""
# Canny edge detection
edges = cv2.Canny(small_hand,100,200)
edges_copy = np.copy(edges)
edges_copy = cv2.cvtColor(edges_copy, cv2.COLOR_GRAY2BGR)

contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)


cv2.drawContours(edges_copy, contours, -1, (0,255,0),3)

#cv2.imshow('Hand with Edges',edges_copy)

cnt = contours[-1]
hull = cv2.convexHull(cnt)
print hull

"""
