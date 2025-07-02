from faster_whisper import WhisperModel
import tempfile
import shutil

model_size = "small"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(file):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(file, tmp)
        tmp_path = tmp.name

    # Transcribe using faster-whisper
    segments, _ = model.transcribe(tmp_path, language="auto")

    # Join all segments into final transcription
    text = " ".join([segment.text for segment in segments])
    return text