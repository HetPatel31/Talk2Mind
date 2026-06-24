import numpy as np
import torch
import torch.nn as nn
import librosa
from pathlib import Path


class SpeechEmotionModel(nn.Module):
    def __init__(self, input_dim=13, num_classes=8):
        super().__init__()

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


class SpeechPredictor:
    def __init__(self):
        root_dir = Path(__file__).resolve().parents[2]
        models_dir = root_dir / "models"

        self.scaler_mean = np.load(models_dir / "scaler_mean.npy")
        self.scaler_scale = np.load(models_dir / "scaler_scale.npy")

        self.emotions = [
            "Angry",
            "Disgust",
            "Fear",
            "Happy",
            "Sad",
            "Surprise",
            "Neutral"
        ]

        self.model = SpeechEmotionModel(input_dim=13, num_classes=8)

        self.model.load_state_dict(
            torch.load(
                models_dir / "talk2mind_speech_model.pth",
                map_location="cpu"
            )
        )

        self.model.eval()

    def predict_audio(self, audio_path):

        audio, sr = librosa.load(audio_path, sr=22050)

        mfccs = librosa.feature.mfcc(
            y=audio,
            sr=sr,
            n_mfcc=13
        )

        features = np.mean(mfccs.T, axis=0)

        features = (
            features - self.scaler_mean
        ) / self.scaler_scale

        tensor_features = torch.tensor(
            features,
            dtype=torch.float32
        ).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(tensor_features)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)

        mapped_probs = np.zeros(7)

        mapped_probs[0] = probs[4].item()
        mapped_probs[1] = probs[6].item()
        mapped_probs[2] = probs[5].item()
        mapped_probs[3] = probs[2].item()
        mapped_probs[4] = probs[3].item()
        mapped_probs[5] = probs[7].item()
        mapped_probs[6] = (probs[0] + probs[1]).item()

        emotion_idx = np.argmax(mapped_probs)

        return {
            "emotion": self.emotions[emotion_idx],
            "confidence": round(float(mapped_probs[emotion_idx] * 100), 2)
        }