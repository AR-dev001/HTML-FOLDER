
"""
L2: Voice Analysis Lab

Record → Analyze → Compare Two Recordings
Live Waveform Visualization
"""

import threading
import sys

# Dependency check
try:
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import speech_recognition as sr
    from speech_recognition import AudioData

except ImportError as e:
    print(f"Missing library: {e.name}")
    print("\nInstall commands:")
    print("pip install SpeechRecognition pyaudio numpy matplotlib")
    sys.exit(1)


stop_event = threading.Event()


def wait_for_enter():
    input()
    stop_event.set()


def record_audio(label):

    stop_event.clear()

    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        input_device_index=3,
        frames_per_buffer=1024,
    )

    frames = []

    # Waveform configuration
    window_size = 4096
    waveform = np.zeros(window_size, dtype=np.int16)

    fig, ax = plt.subplots(figsize=(12, 5))

    line, = ax.plot(
        np.arange(window_size),
        waveform,
        color="blue",
        linewidth=1
    )

    ax.set_title("LIVE VOICE WAVEFORM")
    ax.set_xlabel("Audio Samples")
    ax.set_ylabel("Amplitude")
    ax.set_xlim(0, window_size)
    ax.set_ylim(-35000, 35000)
    ax.grid(True, alpha=0.3)

    print(f"\n{label}")
    print("Speak into your microphone!")
    print("Press Enter in the terminal to stop.")

    threading.Thread(
        target=wait_for_enter,
        daemon=True
    ).start()

    def update(frame):

        nonlocal waveform

        if stop_event.is_set():
            animation.event_source.stop()
            plt.close(fig)
            return line,

        try:
            data = stream.read(
                1024,
                exception_on_overflow=False
            )

            frames.append(data)

            samples = np.frombuffer(
                data,
                dtype=np.int16
            )

            waveform = np.roll(
                waveform,
                -len(samples)
            )

            waveform[-len(samples):] = samples

            line.set_ydata(waveform)

        except Exception as e:
            print(f"Recording error: {e}")
            stop_event.set()

        return line,

    print("Recording...")

    # Live animation
    animation = FuncAnimation(
        fig,
        update,
        interval=30,
        blit=False,
        cache_frame_data=False
    )

    plt.show()

    # Stop recording if window is closed manually
    stop_event.set()

    stream.stop_stream()
    stream.close()

    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()

    print("Recording stopped.")

    return b"".join(frames), 16000, width


def analyze_audio(data, rate):

    samples = np.frombuffer(
        data,
        dtype=np.int16
    )

    if len(samples) == 0:
        return {
            "duration": 0,
            "avg_volume": 0,
            "max_volume": 0,
            "samples": samples,
        }

    return {
        "duration": len(samples) / rate,
        "avg_volume": np.mean(np.abs(samples)),
        "max_volume": np.max(np.abs(samples)),
        "samples": samples,
    }


def transcribe(data, rate, width):

    recognizer = sr.Recognizer()

    try:
        return recognizer.recognize_google(
            AudioData(data, rate, width)
        )

    except Exception:
        return "[Could not transcribe]"


def display_stats(stats, text, label):

    print("\n" + "─" * 40)
    print(label)
    print("─" * 40)

    print(f"Duration: {stats['duration']:.2f} seconds")
    print(f"Avg Amplitude: {stats['avg_volume']:.0f}")
    print(f"Max Amplitude: {stats['max_volume']:.0f}")
    print(f"Transcription: {text}")


def compare(stats1, stats2):

    print("\n" + "=" * 40)
    print("COMPARISON RESULTS")
    print("=" * 40)

    # Duration comparison
    if stats1["duration"] > stats2["duration"]:
        longer = "Recording 1"
        diff = (
            (stats1["duration"] - stats2["duration"])
            / stats2["duration"] * 100
            if stats2["duration"] else 0
        )
    else:
        longer = "Recording 2"
        diff = (
            (stats2["duration"] - stats1["duration"])
            / stats1["duration"] * 100
            if stats1["duration"] else 0
        )

    print(f"{longer} is longer by {diff:.1f}%")

    # Volume comparison
    if stats1["avg_volume"] > stats2["avg_volume"]:
        louder = "Recording 1"
        diff = (
            (stats1["avg_volume"] - stats2["avg_volume"])
            / stats2["avg_volume"] * 100
            if stats2["avg_volume"] else 0
        )
    else:
        louder = "Recording 2"
        diff = (
            (stats2["avg_volume"] - stats1["avg_volume"])
            / stats1["avg_volume"] * 100
            if stats1["avg_volume"] else 0
        )

    print(f"{louder} is louder by {diff:.1f}%")


def plot_both(stats1, stats2, rate):

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(12, 6)
    )

    # Recording 1
    t1 = np.arange(len(stats1["samples"])) / rate

    ax1.plot(
        t1,
        stats1["samples"],
        color="blue",
        linewidth=0.5
    )

    ax1.set_title(
        f"Recording 1 (Normal) | Duration: "
        f"{stats1['duration']:.2f}s | "
        f"Avg: {stats1['avg_volume']:.0f}"
    )

    ax1.set_ylabel("Amplitude")
    ax1.set_ylim(-35000, 35000)
    ax1.grid(True, alpha=0.3)

    # Recording 2
    t2 = np.arange(len(stats2["samples"])) / rate

    ax2.plot(
        t2,
        stats2["samples"],
        color="red",
        linewidth=0.5
    )

    ax2.set_title(
        f"Recording 2 (Modified) | Duration: "
        f"{stats2['duration']:.2f}s | "
        f"Avg: {stats2['avg_volume']:.0f}"
    )

    ax2.set_xlabel("Time (seconds)")
    ax2.set_ylabel("Amplitude")
    ax2.set_ylim(-35000, 35000)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def main():

    print("=" * 40)
    print("VOICE ANALYSIS LAB")
    print("=" * 40)

    print("Record twice and compare your voice!")

    # Recording 1
    audio1, rate, width = record_audio(
        "Recording 1: Speak NORMALLY"
    )

    stats1 = analyze_audio(audio1, rate)
    text1 = transcribe(audio1, rate, width)

    display_stats(
        stats1,
        text1,
        "Recording 1 Results"
    )

    # Recording 2 prompt
    input(
        "\nPress Enter, then speak LOUDER or FASTER..."
    )

    # Recording 2
    audio2, rate, width = record_audio(
        "Recording 2: CHANGE your voice!"
    )

    stats2 = analyze_audio(audio2, rate)
    text2 = transcribe(audio2, rate, width)

    display_stats(
        stats2,
        text2,
        "Recording 2 Results"
    )

    # Comparison and graphs
    compare(stats1, stats2)

    plot_both(stats1, stats2, rate)


if __name__ == "__main__":
    main()
