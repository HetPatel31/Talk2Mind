

# 🧠 Talk2Mind

AI-Powered Multimodal Mental Well-Being Assessment System

## 📌 Overview

Talk2Mind is a multimodal AI application that combines:

- 📝 Questionnaire-Based Mental Health Assessment
- 😊 Facial Emotion Recognition
- 🎤 Voice Emotion Analysis
- 🧠 Multimodal Fusion Analysis
- 📄 PDF Report Generation

The system provides a comprehensive mental wellness assessment by integrating psychological questionnaires, computer vision, and speech emotion recognition.

---

## ✨ Features

### 📝 Assessment Module

- PHQ-9 Depression Assessment
- GAD-7 Anxiety Assessment
- Lifestyle Evaluation
- Wellness Score Generation

### 😊 Face Emotion Analysis

- MediaPipe Face Detection
- Deep Learning Emotion Classification
- Emotion Confidence Score
- Real-Time Image Analysis

### 🎤 Voice Emotion Analysis

- Audio Recording through Streamlit
- MFCC Feature Extraction
- Speech Emotion Recognition Model
- Confidence Score Generation

### 🧠 Fusion Analysis

Combines:

- Questionnaire Results
- Face Emotion Results
- Voice Emotion Results

To generate a final mental wellness assessment.

### 📄 PDF Report

Generate and download a complete wellness report including:

- Assessment Results
- Face Emotion Results
- Voice Emotion Results
- Recommendations

---

## 🏗️ Project Structure

```text
TalktoMind/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
├── modules/
│   ├── face/
│   ├── audio/
│   ├── fusion/
│   └── questionnaire/
│
├── pages/
│   ├── Assessment
│   ├── Results
│   ├── About
│   ├── Face Analysis
│   ├── Voice Analysis
│   └── Fusion Analysis
│
├── reports/
├── utils/
└── notebooks/
```

---

## ⚙️ Technologies Used

- Python
- Streamlit
- PyTorch
- MediaPipe
- OpenCV
- Librosa
- NumPy
- Scikit-Learn
- ReportLab

---

## 🚀 Installation

### Clone Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_LINK>
cd TalktoMind
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## 📊 Workflow

```text
Questionnaire Assessment
           +
Face Emotion Analysis
           +
Voice Emotion Analysis
           ↓
Multimodal Fusion Engine
           ↓
Mental Wellness Assessment
           ↓
PDF Report Generation
```

---

## 📷 Screenshots

Add screenshots of:

- Home Page
- Assessment Page
- Face Analysis
- Voice Analysis
- Fusion Dashboard
- PDF Report

---

## 🔮 Future Enhancements

- Historical Assessment Tracking
- Cloud Database Integration
- Advanced Emotion Models
- Personalized Wellness Recommendations
- Mobile Application Support

---

## 👨‍💻 Developer

Het Patel

Computer Science Engineering Student

AI/ML Internship Project

---

## 📄 License

This project is developed for educational and research purposes.