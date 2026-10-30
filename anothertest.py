
import pyaudio
import numpy as np

p = pyaudio.PyAudio()

DEVICE_ID = 3

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    input_device_index=DEVICE_ID,
    frames_per_buffer=1024
)

print("Speak into your microphone for 5 seconds!")

for i in range(50):
    data = stream.read(1024, exception_on_overflow=False)
    samples = np.frombuffer(data, dtype=np.int16)

    print(
        "Average:", round(np.mean(np.abs(samples))),
        "| Maximum:", np.max(np.abs(samples))
    )

stream.stop_stream()
stream.close()
p.terminate()
