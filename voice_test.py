import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

print("Speak something...")

with sd.RawInputStream(
    device=6,
    samplerate=16000,
    blocksize=8000,
    dtype='int16',
    channels=1
) as stream:

    while True:
        data, overflowed = stream.read(4000)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print("You said:", result.get("text", ""))