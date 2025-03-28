import cv2

cap = cv2.VideoCapture(0)
# Get frame width and height from camera
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Use MJPG codec and AVI container — very stable on Mac
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter("test_input.avi", fourcc, 20.0, (frame_width, frame_height))

print("Recording for 20 seconds... Press 'q' to quit early.")
frame_count = 0
while cap.isOpened() and frame_count < 400:
    ret, frame = cap.read()
    if ret:
        # Confirm frame shape matches output resolution
        frame = cv2.resize(frame, (frame_width, frame_height))
        out.write(frame)
        cv2.imshow("Recording - Press q to stop", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        frame_count += 1
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
