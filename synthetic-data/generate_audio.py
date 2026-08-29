"""
Audio Evidence Generation

Generates 4 audio evidence files (WAV format):
1. Phone call between Chen and Rodriguez
2. Voicemail from Kim to Martinez
3. Meeting recording at TechVentures
4. Phone call between Morgan and Parker

Audio is synthesized locally with Windows text-to-speech. gTTS is only a
fallback when an offline voice is unavailable, so the generator works without
an internet connection.
"""

import os
import shutil
import subprocess
import sys


def _get_ffmpeg_executable() -> str:
    """Return a locally available FFmpeg binary without requiring a global install."""
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as error:
        raise RuntimeError(
            "FFmpeg is required for audio generation. Install imageio-ffmpeg or add ffmpeg to PATH."
        ) from error


def _synthesize_with_pyttsx3(text: str, output_path: str) -> bool:
    """Use Windows/offline text-to-speech as the primary synthesis path."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except Exception as error:
        print(f"    Offline TTS fallback failed ({error})")
        return False


def text_to_wav(text: str, output_path: str, lang='en', slow=False):
    """
    Convert text to a non-silent WAV audio file.

    The offline voice is deliberately preferred: evidence generation should be
    reproducible in a classroom or lab with no internet access. If Windows TTS
    is unavailable, gTTS plus ffmpeg provides a secondary path.
    """
    temp_mp3 = output_path.replace('.wav', '_temp.mp3')

    if _synthesize_with_pyttsx3(text, output_path):
        return
    if os.path.exists(output_path):
        os.remove(output_path)

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(temp_mp3)
    except Exception as error:
        print(f"    ⚠ gTTS fallback failed ({error})")
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)
        if os.path.exists(output_path):
            os.remove(output_path)
        raise RuntimeError("Both gTTS and offline TTS failed; no audio file was generated.")

    # Convert MP3 to WAV using ffmpeg
    try:
        result = subprocess.run(
            [_get_ffmpeg_executable(), '-y', '-i', temp_mp3, '-ac', '1', '-ar', '22050', output_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr[-500:])
    except Exception as error:
        raise RuntimeError(f"Audio conversion failed: {error}") from error
    finally:
        if os.path.exists(temp_mp3):
            os.remove(temp_mp3)

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
