"""
Audio Evidence Generation

Generates 4 audio evidence files (WAV format):
1. Phone call between Chen and Rodriguez
2. Voicemail from Kim to Martinez
3. Meeting recording at TechVentures
4. Phone call between Morgan and Parker

Audio is synthesized with gTTS (MP3) then converted to WAV using ffmpeg.
Uses gTTS for realistic speech synthesis (requires internet).
"""

import os
import subprocess
import sys


def text_to_wav(text: str, output_path: str, lang='en', slow=False):
    """
    Convert text to WAV audio file using gTTS + ffmpeg.
    Falls back to a silent WAV placeholder if synthesis fails.
    """
    temp_mp3 = output_path.replace('.wav', '_temp.mp3')

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(temp_mp3)
    except Exception as e:
        print(f"    ⚠ TTS synthesis failed ({e}), generating silent placeholder")
        _write_silent_wav(output_path, duration_seconds=5)
        return

    # Convert MP3 to WAV using ffmpeg
    try:
        result = subprocess.run(
            ['ffmpeg', '-y', '-i', temp_mp3, '-ac', '1', '-ar', '22050', output_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr[-500:])
    except Exception as e:
        print(f"    ⚠ ffmpeg conversion failed ({e}), writing silent placeholder")
        _write_silent_wav(output_path, duration_seconds=5)
    finally:
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)


def _write_silent_wav(output_path: str, duration_seconds: int = 5):
    """Write a silent WAV file (stdlib only) as a fallback placeholder."""
    import wave
    import struct
    sample_rate = 22050
    with wave.open(output_path, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        # Very quiet tone modulated by a low amplitude sine (below speech, inaudible-ish)
        # Keep it effectively silent (0 amplitude) to stay < 5MB
        frames = b'\x00\x00' * (sample_rate * duration_seconds)
        wav.writeframes(frames)


def generate_phone_call_chen_rodriguez(output_dir: str, scenario):
    """Generate phone call between Chen and Rodriguez discussing fund movement"""
    filename = os.path.join(output_dir, "phone_call_chen_rodriguez_20260315.wav")

    text = (
        "Marcus Chen speaking. Sarah, we need to move the eight hundred fifty "
        "thousand dollars through the CryptoHoldings account before end of quarter. "
        "The offshore arrangement is finalized. David Kim has everything ready. "
        "Please coordinate with Jennifer White on the accounting. Keep this confidential."
    )

    text_to_wav(text, filename)
    print(f"  ✓ Generated: {filename}")


def generate_voicemail_kim_martinez(output_dir: str, scenario):
    """Generate voicemail from Kim to attorney Martinez"""
    filename = os.path.join(output_dir, "voicemail_kim_to_martinez_20260420.wav")

    text = (
        "Hey Robert, it's David Kim. The OffshoreConsult paperwork came through. "
        "Everything looks good on the Delaware registration. "
        "Call me back when you get a chance. Thanks."
    )

    text_to_wav(text, filename)
    print(f"  ✓ Generated: {filename}")


def generate_meeting_recording(output_dir: str, scenario):
    """Generate snippet of TechVentures meeting"""
    filename = os.path.join(output_dir, "meeting_recording_techventures_20260522.wav")

    text = (
        "Okay everyone, let's review the Q2 numbers. "
        "The three hundred thousand from CryptoHoldings is showing as consulting revenue, which is correct. "
        "Sarah, can you confirm the offshore payments are properly categorized? "
        "Good. Jennifer, make sure the auditors see the standard expense documentation. "
        "The structure is working as planned."
    )

    text_to_wav(text, filename, slow=True)
    print(f"  ✓ Generated: {filename}")


def generate_phone_call_morgan_parker(output_dir: str, scenario):
    """Generate phone call between Dr. Morgan and James Parker"""
    filename = os.path.join(output_dir, "phone_call_morgan_parker_20260610.wav")

    text = (
        "James, this is Doctor Morgan. Make sure those PharmaCorp invoices match what we bill HealthInsure. "
        "We don't want any discrepancies showing up in the audit. "
        "The consulting fees need to look legitimate. Keep the amounts consistent."
    )

    text_to_wav(text, filename)
    print(f"  ✓ Generated: {filename}")


def generate_all_audio(scenarios: dict):
    """Generate all audio evidence files"""
    output_dir = "evidence/audio"
    os.makedirs(output_dir, exist_ok=True)

    scenario_1 = scenarios['scenario_1']
    scenario_2 = scenarios['scenario_2']

    print("Generating audio evidence files...")
    print("  (Synthesizing speech - this may take a moment...)")

    generate_phone_call_chen_rodriguez(output_dir, scenario_1)
    generate_voicemail_kim_martinez(output_dir, scenario_1)
    generate_meeting_recording(output_dir, scenario_1)
    generate_phone_call_morgan_parker(output_dir, scenario_2)

    return [
        "phone_call_chen_rodriguez_20260315.wav",
        "voicemail_kim_to_martinez_20260420.wav",
        "meeting_recording_techventures_20260522.wav",
        "phone_call_morgan_parker_20260610.wav"
    ]


if __name__ == "__main__":
    from scenarios import load_scenarios
    scenarios = load_scenarios()
    generate_all_audio(scenarios)
