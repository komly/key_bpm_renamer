import os
import shutil
import argparse
from pathlib import Path
from essentia.standard import MonoLoader, KeyExtractor, RhythmExtractor
import eyed3  # For editing metadata of MP3 files

# Function to analyze audio and get key and BPM
def analyze_audio(file_path, bpm_limit=100):
    try:
        # Load audio file
        loader = MonoLoader(filename=str(file_path))
        audio = loader()

        # Initialize extractors
        key_extractor = KeyExtractor()
        rhythm_extractor = RhythmExtractor()

        # Extract key
        key, scale, _ = key_extractor(audio)

        # Extract rhythm
        rhythm_data = rhythm_extractor(audio)
        if len(rhythm_data) < 4:
            print(f"Unexpected rhythm extraction result for {file_path}: {rhythm_data}")
            return key + scale, None  # Return key and skip BPM

        bpm = rhythm_data[0]

        # Adjust BPM if below the lower limit
        if bpm < bpm_limit:
            bpm *= 2

        return key + scale, round(bpm)
    except Exception as e:
        print(f"Failed to analyze {file_path}: {e}")
        return None, None


# Function to embed key and BPM into MP3 metadata
def embed_metadata(file_path, key, bpm):
    if file_path.suffix.lower() == ".mp3":
        try:
            # Load MP3 file using eyed3
            audio_file = eyed3.load(file_path)

            # Set BPM (ensure it's an integer and properly encoded)
            audio_file.tag.bpm = bpm

            # Set Key as text frame
            if key:
                key_frame = eyed3.id3.frames.TextFrame(b"TKEY", key)  # 'TKEY' as ID and key as string
                audio_file.tag.frame_set[b"TKEY"] = key_frame  # Add the TKEY frame directly

            # Save the changes to the metadata
            audio_file.tag.save()
            print(f"Metadata updated for {file_path} with Key: {key} and BPM: {bpm}")
        except Exception as e:
            print(f"Failed to update metadata for {file_path}: {e}")
            
# Function to process and rename files
def process_files(input_dir, output_dir, bpm_limit=100):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    for root, _, files in os.walk(input_dir):
        # Preserve folder structure
        relative_path = Path(root).relative_to(input_dir)
        destination_folder = output_dir / relative_path
        destination_folder.mkdir(parents=True, exist_ok=True)

        for file in files:
            if not file.lower().endswith(('.mp3', '.wav', '.flac')):
                print(f"Skipping non-audio file: {file}")
                continue  # Skip non-audio files

            source_path = Path(root) / file
            print(f"Analyzing {source_path}...")

            # Detect key and BPM
            key, bpm = analyze_audio(source_path, bpm_limit)
            if key is None or bpm is None:
                print(f"Skipping {source_path} due to analysis failure.")
                continue

            # Create new filename
            name, ext = os.path.splitext(file)
            new_name = f"{name}_{key}_{bpm}bpm{ext}"
            destination_path = destination_folder / new_name

            # Copy and rename file
            try:
                shutil.copy2(source_path, destination_path)
                print(f"Renamed and copied to: {destination_path}")

                # Embed BPM and key in the metadata
                embed_metadata(destination_path, key, bpm)

            except Exception as e:
                print(f"Failed to copy {source_path} to {destination_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Detect Key and BPM of audio files, rename them, and embed the information in the metadata.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input folder containing audio files.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output folder where renamed files will be stored.")
    parser.add_argument("--bpm-limit", type=int, default=100, help="Set the lower limit for BPM adjustment. Default is 100.")
    args = parser.parse_args()
    process_files(args.input, args.output, args.bpm_limit)

if __name__ == "__main__":
    main()