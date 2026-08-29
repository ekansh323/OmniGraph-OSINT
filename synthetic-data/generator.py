#!/usr/bin/env python3
"""
OmniGraph OSINT - Synthetic Data Generator

Main orchestrator that runs all generators in sequence and validates output.
"""

import sys
from scenarios import load_scenarios
from generate_documents import generate_all_documents
from generate_images import generate_all_images
from generate_audio import generate_all_audio
from generate_transactions import generate_all_transactions
from generate_extractions import generate_all_extractions
from validate_data import main as validate


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def main():
    print("=" * 60)
    print("OmniGraph OSINT - Synthetic Data Generator")
    print("=" * 60)

    # Load scenarios
    print("\n[1/6] Loading scenario definitions...")
    scenarios = load_scenarios()
    print(f"  ✓ Loaded {len(scenarios)} scenarios")

    # Generate PDFs
    print("\n[2/6] Generating PDF evidence files...")
    try:
        pdf_files = generate_all_documents(scenarios)
        print(f"  ✓ Generated {len(pdf_files)} PDF files")
    except Exception as e:
        print(f"  ✗ PDF generation failed: {e}")
        return 1

    # Generate images
    print("\n[3/6] Generating image evidence files...")
    try:
        image_files = generate_all_images(scenarios)
        print(f"  ✓ Generated {len(image_files)} image files")
    except Exception as e:
        print(f"  ✗ Image generation failed: {e}")
        return 1

    # Generate audio
    print("\n[4/6] Generating audio evidence files...")
    try:
        audio_files = generate_all_audio(scenarios)
        print(f"  ✓ Generated {len(audio_files)} audio files")
    except Exception as e:
        print(f"  ✗ Audio generation failed: {e}")
        return 1

    # Generate CSV
    print("\n[5/6] Generating CSV evidence files...")
    try:
        csv_files = generate_all_transactions(scenarios)
        print(f"  ✓ Generated {len(csv_files)} CSV files")
    except Exception as e:
        print(f"  ✗ CSV generation failed: {e}")
        return 1

    # Generate extraction JSONs
    print("\n[6/6] Generating prepared extraction JSONs...")
    try:
        json_files = generate_all_extractions(scenarios)
        print(f"  ✓ Generated {len(json_files)} extraction JSON files")
    except Exception as e:
        print(f"  ✗ Extraction JSON generation failed: {e}")
        return 1

    # Validate
    print("\n" + "=" * 60)
    print("Running validation...")
    print("=" * 60)
    result = validate()

    if result == 0:
        print("\n" + "=" * 60)
        print("✅ Data generation complete!")
        print("=" * 60)
        print(f"Evidence files: synthetic-data/evidence/")
        print(f"Extraction JSONs: synthetic-data/prepared-extractions/")
    else:
        print("\n" + "=" * 60)
        print("⚠ Data generation completed with validation warnings")
        print("=" * 60)

    return result


if __name__ == "__main__":
    sys.exit(main())
