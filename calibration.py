import cv2
import mediapipe as mp
import numpy as np
import json
from sklearn.linear_model import LinearRegression

# MediaPipe başlat
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.7)

cap = cv2.VideoCapture(1)

# Kalibrasyon adımları (sabit)
MESAFE_ADIMLARI = [30, 50, 70]  # cm
pixel_widths = []
true_distances = []
adim_index = 0  # hangi mesafedeyiz

print("Kalibrasyon başladı. Ekrandaki yönergeleri takip edin.")
print("[ESC] ile çıkabilirsiniz.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Kamera hatası.")
        break

    height, width, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(frame_rgb)

    mesaj = "Yüz algılanamadı"
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
        cv2.putText(frame, f"{int(face_width_px)} px", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        if adim_index < len(MESAFE_ADIMLARI):
            hedef = MESAFE_ADIMLARI[adim_index]
            mesaj = f"{hedef} cm mesafede oturun ve [SPACE] tuşuna basın."
        else:
            mesaj = "✅ Kalibrasyon tamamlandı. [ESC] ile çıkabilirsiniz."

    # Mesajı ekrana yaz
    cv2.putText(frame, mesaj, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 0) if "tamamlandı" in mesaj else (0, 0, 255), 2)

    cv2.imshow("Kalibrasyon", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    elif key == 32 and face_width_px and adim_index < len(MESAFE_ADIMLARI):  # SPACE
        hedef_mesafe = MESAFE_ADIMLARI[adim_index]
        pixel_widths.append(face_width_px)
        true_distances.append(hedef_mesafe)
        print(f"✅ {hedef_mesafe} cm → {face_width_px:.2f} px")
        adim_index += 1

cap.release()
cv2.destroyAllWindows()

# Regresyon modeli
if len(pixel_widths) >= 2:
    X = np.array(pixel_widths).reshape(-1, 1)
    y = np.array(true_distances)

    model = LinearRegression()
    model.fit(1 / X, y)

    A = model.coef_[0]
    B = model.intercept_

    print(f"\n🎯 Regresyon tamamlandı:")
    print(f"distance_cm = {A:.2f} / face_width + {B:.2f}")
    with open("calibration.json", "w") as f:
        json.dump({"A": A, "B": B}, f)

    print("\n✅ A ve B değerleri calibration.json dosyasına kaydedildi.")
else:
    print("Yeterli veri alınmadı, regresyon uygulanamadı.")

