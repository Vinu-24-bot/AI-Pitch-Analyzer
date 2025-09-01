Pitch Analyzer AI


training video link https://drive.google.com/drive/folders/1DSrE9m1ojWzcula0lYHF_gaG55aI2VRR?usp=sharing

Project Description

Pitch Analyzer AI is an automated tool to assess and score video pitches (startup, sales, product intros, etc). By uploading a video or pasting a YouTube link, users receive instant machine-learning-based feedback on their speaking pace, filler words, structure adherence, and overall delivery—along with the full transcript. The goal: quick, actionable analysis to help you perfect your pitch.

Features
Upload video (.mp4) or analyze YouTube pitch via link

Automatic audio extraction and robust speech-to-text transcription (Google Speech Recognition)

ML-powered scoring on 5 key dimensions:

Pacing

Filler Words Frequency

Fumbling/Awkwardness

Pitch Structure Coverage (problem, solution, ask, etc.)

Total Score

Detailed feedback and highlight of improvement points

Batch dataset auto-labeling via CLI tool—for bulk scoring

Python Flask web interface and simple local deployment

Installation Instructions
Clone the repository:

bash
git clone https://github.com/yourname/pitch-analyzer-ai.git
cd pitch-analyzer-ai
Create a virtual environment (recommended) and activate:

bash
python -m venv venv
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
How to Run It
Start the Web Application
(Optional) Train the model:
If you wish to retrain the ML model, use your labeled data in multi_labels.csv and:

bash
python train_model.py
(A default-trained model file pitch_model.pkl is expected.)

Launch the server:

bash
python app.py
The app will be accessible at http://localhost:5000.

Example Usage
Web Mode:

Go to the website (http://localhost:5000).

Enter your startup name and date.

Upload a .mp4 video file or paste a public YouTube link.

Click 'Analyze'.

See your:

Core pitch scores (pacing, filler words, etc)

Full transcript

Model’s overall confidence

Batch Labeling:

To auto-label all videos in a folder (training_videos/):

bash
python auto_label_videos.py
This will process each video, score it, and output results in multi_labels.csv, ready for ML use.

Sample Output:

text
Startup: Example AI
Pitch Duration: 61.2 seconds

Scores:
  - Pacing: 9.0 / 10
  - Filler Words: 8.5 / 10
  - Fumbling: 10.0 / 10
  - Structure: 7.5 / 10
  - Total: 8.8 / 10

Confidence: High 😎
For developers and contributors, see the source files for modular logic in:

app.py (web backend)

ml_features.py (feature extraction)

speech_analysis.py (ML scoring)

auto_label_videos.py (batch labeling)

MIT License. Contributions welcome!