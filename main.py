import cv2

# Load the trained classifier for car number plates detection
plate_cascade = cv2.CascadeClassifier('numberplatemodel.xml')

# Start capturing the video stream from the default camera
cap = cv2.VideoCapture(0)

# Process the video stream frame-by-frame
while True:
    # Read the next frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale for easier processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect car number plates in the frame using the classifier
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles around the detected number plates and display the plate number
    for (x, y, w, h) in plates:
        plate = frame[y:y+h, x:x+w]
        plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        _, plate_thresh = cv2.threshold(plate_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        plate_text = pytesseract.image_to_string(plate_thresh, config='--psm 7')
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(frame, plate_text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
