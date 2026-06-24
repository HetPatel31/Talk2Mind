import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import torch
import torch.nn as nn
from torchvision.models import efficientnet_b0
import torchvision.transforms as transforms
from PIL import Image
import os
from pathlib import Path

class VisualEmotionClassifier:
    def __init__(self):
        # 1. MediaPipe Tasks API Setup
        BASE_DIR = Path(__file__).resolve().parents[2]
        MODELS_DIR = BASE_DIR / "models"

        self.model_path = MODELS_DIR / "detector.tflite"
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Detector model not found: {self.model_path}"
            )

        base_options = python.BaseOptions(model_asset_path=str(self.model_path))
        options = vision.FaceDetectorOptions(base_options=base_options, running_mode=vision.RunningMode.IMAGE)
        self.detector = vision.FaceDetector.create_from_options(options)
        
        # 2. PyTorch Custom Emotion Model Setup (Matching FER2013 configurations)
        self.emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        
        # Initialize the raw structural architecture skeleton
        self.model = efficientnet_b0()
        num_features = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(num_features, len(self.emotions))
        
        # Load your custom high-accuracy weights file downloaded from Colab
        weights_path = MODELS_DIR / "talk2mind_emotion_model.pth"
        if weights_path.exists():
            print(f"Loading custom high-accuracy emotion weights from '{weights_path}'...")
            # map_location='cpu' optimizes the model matrices natively for Mac CPUs (M1/M2/M3 chips)
            self.model.load_state_dict(torch.load(weights_path, map_location='cpu'))
            print("Weights loaded successfully!")
        else:
            print(f"Warning: Emotion model not found: {weights_path}")
            
        self.model.eval() # Freeze layers for live validation processing
        
        # 3. Pre-processing Transformation Pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict_image(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        detection_result = self.detector.detect(mp_image)

        if detection_result.detections:
            for detection in detection_result.detections:
                bbox = detection.bounding_box
                xmin, ymin, w, h = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
                xmin, ymin = max(0, xmin), max(0, ymin)

                face_crop = rgb_frame[ymin:ymin+h, xmin:xmin+w]

                if face_crop.size > 0:
                    pil_img = Image.fromarray(face_crop)
                    tensor_img = self.transform(pil_img).unsqueeze(0)

                    with torch.no_grad():
                        outputs = self.model(tensor_img)
                        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                        max_idx = torch.argmax(probabilities).item()
                        predicted_emotion = self.emotions[max_idx]
                        confidence = probabilities[max_idx].item() * 100

                    annotated = frame.copy()

                    cv2.rectangle(
                        annotated,
                        (xmin, ymin),
                        (xmin + w, ymin + h),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        annotated,
                        f"{predicted_emotion} ({confidence:.1f}%)",
                        (xmin, ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

                    return {
                        "emotion": predicted_emotion,
                        "confidence": round(confidence, 2),
                        "frame": annotated
                    }

        return {
            "emotion": "No Face Detected",
            "confidence": 0.0,
            "frame": frame
        }

    def process_frame(self, frame):
        # Convert OpenCV native BGR matrices to standard RGB space
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Run local tracking inference
        detection_result = self.detector.detect(mp_image)
        
        if detection_result.detections:
            for detection in detection_result.detections:
                bbox = detection.bounding_box
                xmin, ymin, w, h = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
                xmin, ymin = max(0, xmin), max(0, ymin)
                
                # Crop out the tracked face area
                face_crop = rgb_frame[ymin:ymin+h, xmin:xmin+w]
                
                if face_crop.size > 0:
                    # Map cropped matrix to standard PIL format and process into numerical PyTorch Tensors
                    pil_img = Image.fromarray(face_crop)
                    tensor_img = self.transform(pil_img).unsqueeze(0) # Pad explicit batch dimension
                    
                    # Prevent gradient tree calculation to keep operations lightweight
                    with torch.no_grad():
                        outputs = self.model(tensor_img)
                        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                        max_idx = torch.argmax(probabilities).item()
                        predicted_emotion = self.emotions[max_idx]
                        confidence = probabilities[max_idx].item() * 100
                    
                    # Draw a crisp bounding box and text overlay label over the active window
                    label = f"{predicted_emotion} ({confidence:.1f}%)"
                    cv2.rectangle(frame, (xmin, ymin), (xmin + w, ymin + h), (0, 255, 0), 2)
                    cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    return frame
                    
        return frame

if __name__ == "__main__":
    classifier = VisualEmotionClassifier()
    cap = cv2.VideoCapture(0) # Open local camera stream

    print("Press 'q' inside the video window to stop.")
    while cap.isOpened():
        success, frame = cap.read()
        if not success: 
            break
            
        annotated_frame = classifier.process_frame(frame)
        cv2.imshow('Talk2Mind - Custom Emotion Intelligence', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()