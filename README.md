# Key BPM Renamer

`key_bpm_renamer` is a Python command-line tool that automatically analyzes audio files (MP3, WAV, FLAC), extracts the musical key and beats per minute (BPM), renames the files with this information, and embeds the key and BPM into the metadata (for MP3 files).

## Features

- Extracts the musical key and BPM from audio files.
- Renames the audio files by appending the detected key and BPM.
- Embeds the key and BPM in the metadata of MP3 files (using `eyed3`).
- Supports MP3, WAV, and FLAC audio formats.
- Works with directories and preserves folder structure.

## Installation

To install `key_bpm_renamer`, you can use `pip`:

```bash
pip install key_bpm_renamer
```

## Usage

After installing the dependencies, you can use the `key_bpm_renamer` command to process your audio files.

### Command Structure

```bash
key_bpm_renamer -i <input_directory> -o <output_directory>
```

-i <input_directory>: The path to the directory containing the audio files you want to process.
-o <output_directory>: The path to the directory where the renamed audio files will be saved.

### Example

```bash
key_bpm_renamer -i ./input_audio_files -o ./output_audio_files
```

This command will:

1. Analyze all the audio files in the `input_audio_files` directory.
2. Detect the key and BPM of each file.
3. Rename the files with the format `<original_filename>_<key>_<bpm>bpm.<extension>`.
4. Save the renamed files in the `output_audio_files` directory.
5. Embed the detected key and BPM into the metadata of each audio file.

### Notes

- Supported audio formats: `.mp3`, `.wav`, `.flac`
- The key will be extracted using Essentia’s `KeyExtractor` and the BPM using `RhythmExtractor`.
- Files are copied (not moved), so the original files remain untouched.
