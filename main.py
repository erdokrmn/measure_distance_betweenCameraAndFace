import cv2
import mediapipe as mp
import json

# A ve B değerlerini calibration.json'dan oku
try:
    with open("calibration.json", "r") as f:
        calibration = json.load(f)
        A = calibration["A"]
        B = calibration["B"]
except FileNotFoundError:
    print("❌ calibration.json dosyası bulunamadı. Lütfen önce kalibrasyon yapın.")
    exit()

# MediaPipe yapılandırması
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.7)

cap = cv2.VideoCapture(1)

MIN_DIST = 30
MAX_DIST = 80

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Kamera görüntüsü alınamadı.")
        break

    height, width, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(frame_rgb)

    status = "Yüz algılanamadı."
    face_width_px = None

    if results.detections:
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        face_width_px = bbox.width * width

        x = int(bbox.xmin * width)
        y = int(bbox.ymin * height)
        w = int(bbox.width * width)
        h = int(bbox.height * height)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        distance_cm = A / face_width_px + B
        distance_text = f"{int(distance_cm)} cm"

        if distance_cm < MIN_DIST:
            status = "Çok yakınsınız, biraz geri çekilin."
        elif distance_cm > MAX_DIST:
            status = "Alan dışındasınız, yaklaşın."
        else:
            status = "Mesafe uygun"

        color = (0, 255, 0) if status == "Mesafe uygun" else (0, 0, 255)
        cv2.putText(frame, distance_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, status, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Mesafe Uyarı Sistemi", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
