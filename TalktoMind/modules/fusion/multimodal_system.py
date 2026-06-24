import os
import cv2
import sounddevice as sd
import numpy as np
import librosa
import torch
import torch.nn as nn
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from torchvision.models import efficientnet_b0
import torchvision.transforms as transforms
from PIL import Image
import threading
import queue
import time
import csv
import matplotlib.pyplot as plt

from pathlib import Path

# =====================================================================
# 1. AUDIO CLASSIFIER BACKBONE ARCHITECTURE
# =====================================================================
class SpeechEmotionModel(nn.Module):
    def __init__(self, input_dim=13, num_classes=8):
        super(SpeechEmotionModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
    def forward(self, x):
        return self.network(x)

# =====================================================================
# 2. CORE MULTIMODAL SYSTEM ENGINE (WITH SMOOTHING & LOGGING)
# =====================================================================
class MultimodalEmotionSystem:
    def __init__(self):
        self.fused_emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        
        # Thread-safe buffers
        self.current_audio_probs = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]) 
        
        # --- SMOOTHING & ANALYTICS INITIALIZATION ---
        self.smoothed_probs = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
        self.smoothing_factor = 0.15  # Lower = smoother transitions, Higher = faster reaction
        
        self.session_log = []
        self.start_time = time.time()

        self.BASE_DIR = Path(__file__).resolve().parents[2]
        self.MODELS_DIR = self.BASE_DIR / "models"
        self.DATA_DIR = self.BASE_DIR / "data"
        
        print("Initializing Smooth Multimodal Subsystems...")
        self._setup_vision()
        self._setup_audio()
        
    def _setup_vision(self):
        base_options = python.BaseOptions(
            model_asset_path=str(self.MODELS_DIR / "detector.tflite")
        )
        options = vision.FaceDetectorOptions(base_options=base_options, running_mode=vision.RunningMode.IMAGE)
        self.detector = vision.FaceDetector.create_from_options(options)
        
        self.v_model = efficientnet_b0()
        self.v_model.classifier[1] = nn.Linear(self.v_model.classifier[1].in_features, 7)
        emotion_model_path = self.MODELS_DIR / "talk2mind_emotion_model.pth"
        if emotion_model_path.exists():
            self.v_model.load_state_dict(torch.load(emotion_model_path, map_location='cpu'))
        self.v_model.eval()
        
        self.v_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def _setup_audio(self):
        self.a_model = SpeechEmotionModel(input_dim=13, num_classes=8)
        speech_model_path = self.MODELS_DIR / "talk2mind_speech_model.pth"
        if speech_model_path.exists():
            self.a_model.load_state_dict(torch.load(speech_model_path, map_location='cpu'))
        self.a_model.eval()
        
        scaler_mean_path = self.MODELS_DIR / "scaler_mean.npy"
        scaler_scale_path = self.MODELS_DIR / "scaler_scale.npy"

        self.scaler_mean = np.load(scaler_mean_path) if scaler_mean_path.exists() else None
        self.scaler_scale = np.load(scaler_scale_path) if scaler_scale_path.exists() else None

    def audio_recording_worker(self):
        sample_rate = 22050
        duration = 3.0
        while True:
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()
            audio_chunk = recording.flatten()
            
            # Simple noise gate: check if there's actual speech or just ambient silence
            rms = np.sqrt(np.mean(audio_chunk**2))
            if rms < 0.005:
                # If silent, pull audio predictions smoothly back to Neutral
                mapped_probs = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
            else:
                mfccs = librosa.feature.mfcc(y=audio_chunk, sr=sample_rate, n_mfcc=13)
                mfccs_mean = np.mean(mfccs.T, axis=0)
                
                if self.scaler_mean is not None:
                    mfccs_mean = (mfccs_mean - self.scaler_mean) / self.scaler_scale
                    
                tensor_features = torch.tensor(mfccs_mean, dtype=torch.float32).unsqueeze(0)
                with torch.no_grad():
                    outputs = self.a_model(tensor_features)
                    probs = torch.nn.functional.softmax(outputs[0], dim=0).numpy()
                
                mapped_probs = np.zeros(7)
                mapped_probs[0] = probs[4]                 # Angry
                mapped_probs[1] = probs[6]                 # Disgust
                mapped_probs[2] = probs[5]                 # Fear
                mapped_probs[3] = probs[2]                 # Happy
                mapped_probs[4] = probs[3]                 # Sad
                mapped_probs[5] = probs[7]                 # Surprise
                mapped_probs[6] = probs[0] + probs[1]      # Neutral + Calm
            
            self.current_audio_probs = mapped_probs

    def fusion_inference(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = self.detector.detect(mp_image)
        
        video_probs = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
        xmin, ymin, w, h = 0, 0, 0, 0
        face_found = False

        if detection_result.detections:
            face_found = True
            bbox = detection_result.detections[0].bounding_box
            xmin, ymin, w, h = max(0, bbox.origin_x), max(0, bbox.origin_y), bbox.width, bbox.height
            face_crop = rgb_frame[ymin:ymin+h, xmin:xmin+w]
            
            if face_crop.size > 0:
                pil_img = Image.fromarray(face_crop)
                tensor_img = self.v_transform(pil_img).unsqueeze(0)
                with torch.no_grad():
                    outputs = self.v_model(tensor_img)
                    video_probs = torch.nn.functional.softmax(outputs[0], dim=0).numpy()

        # Late Fusion Mix
        raw_fused_probs = (0.6 * video_probs) + (0.4 * self.current_audio_probs)
        
        # --- THE SIGNAL SMOOTHING FILTER ---
        # Moving Average Formula: Smoothed = (Alpha * New) + ((1 - Alpha) * Old)
        self.smoothed_probs = (self.smoothing_factor * raw_fused_probs) + ((1.0 - self.smoothing_factor) * self.smoothed_probs)
        
        max_idx = np.argmax(self.smoothed_probs)
        final_emotion = self.fused_emotions[max_idx]
        confidence = self.smoothed_probs[max_idx] * 100

        # Log metrics with timestamp for analytics
        elapsed_time = round(time.time() - self.start_time, 2)
        self.session_log.append([elapsed_time] + list(self.smoothed_probs))

        # UI Overlay Generation
        if face_found:
            cv2.rectangle(frame, (xmin, ymin), (xmin + w, ymin + h), (255, 0, 165), 2)
            label = f"Fused: {final_emotion} ({confidence:.1f}%)"
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 165), 2)
            
        cv2.putText(frame, "TALK2MIND LIVE TELEMETRY MATRIX:", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        for idx, emo in enumerate(self.fused_emotions):
            bar_w = int(self.smoothed_probs[idx] * 150)
            cv2.putText(frame, f"{emo}:", (15, 55 + idx*25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
            
            # Change telemetry bar colors based on emotion severity
            color = (0, 255, 0) if emo in ['Happy', 'Neutral'] else (0, 165, 255) if emo in ['Surprise'] else (0, 0, 255)
            cv2.rectangle(frame, (100, 43 + idx*25), (100 + bar_w, 55 + idx*25), color, -1)

        return frame

    def generate_session_report(self):
        print("\n📊 Generating Session Analytics Report...")
        if not self.session_log:
            print("No data logged.")
            return
            
        # 1. Save data points cleanly to a CSV spreadsheet
        csv_file = "emotion_session_log.csv"
        headers = ["Timestamp (s)"] + self.fused_emotions
        with open(csv_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(self.session_log)
        print(f"📁 Raw metric spreadsheet saved to '{csv_file}'")

        # 2. Build the visual line plot timeline using matplotlib
        data = np.array(self.session_log)
        timestamps = data[:, 0]
        
        plt.figure(figsize=(10, 5))
        for idx, emo in enumerate(self.fused_emotions):
            plt.plot(timestamps, data[:, idx + 1], label=emo, linewidth=2)
            
        plt.title("Talk2Mind - Multimodal Emotion Timeline Analysis", fontsize=14, fontweight='bold')
        plt.xlabel("Session Time (Seconds)", fontsize=11)
        plt.ylabel("Model Prediction Confidence", fontsize=11)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(loc="upper right")
        plt.tight_layout()
        
        # Save graph image to disk
        plt.savefig("emotion_timeline_report.png", dpi=300)
        print("📈 Session timeline chart rendered and saved as 'emotion_timeline_report.png'")
        plt.show()

# =====================================================================
# 3. STREAM CONTROL EXECUTOR
# =====================================================================
if __name__ == "__main__":
    system = MultimodalEmotionSystem()
    
    audio_thread = threading.Thread(target=system.audio_recording_worker, daemon=True)
    audio_thread.start()
    
    cap = cv2.VideoCapture(0)
    print("\n🚀 Polished Multimodal Engine Active! Press 'q' to stop and generate reports.")
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success: break
            
            annotated_frame = system.fusion_inference(frame)
            cv2.imshow("Talk2Mind - Multimodal Intelligence Engine", annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        # Trigger the analytics generation automatically upon exit
        system.generate_session_report()