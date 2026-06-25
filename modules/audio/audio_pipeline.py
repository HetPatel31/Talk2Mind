import sounddevice as sd
import numpy as np
import librosa
import time

class AudioFeatureExtractor:
    def __init__(self, sample_rate=22050, duration=3):
        self.sample_rate = sample_rate
        self.duration = duration # Process audio in 3-second rolling chunks
        
    def record_chunk(self):
        """Records a 3-second audio clip from your microphone."""
        print("\n🎤 Recording audio chunk...")
        # Record audio data as float32 mono channel
        recording = sd.rec(
            int(self.duration * self.sample_rate), 
            samplerate=self.sample_rate, 
            channels=1, 
            dtype='float32'
        )
        sd.wait() # Wait until the recording is finished
        return recording.flatten()

    def extract_features(self, audio_data):
        """Extracts the exact acoustic features requested by the Talk2Mind blueprint."""
        # 1. Extract MFCCs (Mel-Frequency Cepstral Coefficients)
        mfccs = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=13)
        mfccs_mean = np.mean(mfccs.T, axis=0)
        
        # 2. Extract Pitch (Chroma STFT can represent pitch classes)
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=self.sample_rate)
        pitch_mean = np.mean(chroma.T, axis=0)
        
        # 3. Extract Energy (Root Mean Square - RMS)
        rms = librosa.feature.rms(y=audio_data)
        energy_mean = np.mean(rms.T, axis=0)
        
        # 4. Extract Tempo
        onset_env = librosa.onset.onset_strength(y=audio_data, sr=self.sample_rate)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=self.sample_rate)
        
        return {
            "mfccs": mfccs_mean,
            "pitch_profile": pitch_mean,
            "energy": energy_mean[0],
            "tempo": float(tempo[0]) if isinstance(tempo, (list, np.ndarray)) else float(tempo)
        }

if __name__ == "__main__":
    extractor = AudioFeatureExtractor()
    print("Talk2Mind Audio Pipeline Initialized. Press Ctrl+C in terminal to stop.")
    
    try:
        while True:
            # 1. Record live microphone data
            audio_chunk = extractor.record_chunk()
            
            # 2. Parse features
            features = extractor.extract_features(audio_chunk)
            
            # 3. Display live audio profile metrics
            print("📊 Extracted Acoustic Features:")
            print(f"   -> Tempo (BPM): {features['tempo']:.1f}")
            print(f"   -> Average Energy: {features['energy']:.4f}")
            print(f"   -> MFCCs Shape: {features['mfccs'].shape}")
            print(f"   -> Pitch Vector Sample: {features['pitch_profile'][:3]}")
            
            time.sleep(0.5) # Short pause before capturing the next chunk
            
    except KeyboardInterrupt:
        print("\nAudio pipeline stopped safely.")