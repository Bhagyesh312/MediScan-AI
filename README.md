# MediScan AI - Disease Predictor

A machine learning-powered web application that predicts potential diseases based on symptoms you select.

🔗 **Live Demo:** [https://mediscan-ai-yqdy.onrender.com](https://mediscan-ai-yqdy.onrender.com)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![ML](https://img.shields.io/badge/ML-scikit--learn-orange.svg)

## Features

- **130+ Symptoms** - Comprehensive symptom selection
- **40+ Diseases** - Wide range of disease predictions
- **Machine Learning** - Random Forest classifier for accurate predictions
- **Modern UI** - Clean, responsive, and user-friendly interface
- **Real-time Search** - Quickly find symptoms with search functionality

## Screenshots

The application features a bright, modern interface with:
- Searchable symptom grid
- Selected symptoms displayed as tags
- Detailed prediction results with recommendations

## How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bhagyesh312/MediScan-AI.git
   cd MediScan-AI
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   
   Navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure

```
MediScan-AI/
├── app.py                 # Flask application
├── final_pipeline.pkl     # ML model + label encoder + symptoms
├── requirements.txt       # Python dependencies
├── static/
│   ├── script.js          # Frontend JavaScript
│   └── style.css          # Styling
└── templates/
    └── index.html         # Main HTML template
```

## Tech Stack

- **Backend**: Flask (Python)
- **ML Model**: Random Forest Classifier (scikit-learn)
- **Frontend**: HTML, CSS, JavaScript
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Poppins)

## Disclaimer

This AI-powered tool is for **educational purposes only**. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult a healthcare professional for medical concerns.

## License

MIT License - Feel free to use and modify for your own projects.
