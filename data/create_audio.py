import os
import argparse
import subprocesss

import pandas as pd

from tqdm import tqdm

from miditok import REMI
from miditok import MidiFile
from miditok import get_midi_programs


def main(args):
    tokenizer = REMI()

    os.makedirs(args.midi_dir, exist_ok=True)
    os.makedirs(args.wav_dir, exist_ok=True)

    df = pd.read_csv(args.csv_file)
    for f, t, o in tqdm(zip(df["filename"], df["tokens"], df["origin"])):
        # Create the midi file.
        original = MidiFile(o)
        midi = tokenizer.tokens_to_midi(
            t, get_midi_programs(original))
        filename = f.split("/")[-1]
        midi_path = f"{args.midi_dir}/{filename}.midi"
        midi.dump(midi_path)

        # Create the wav file
        wav_path = f"{args.wav_dir}/{f}"
        subprocesss.run(
            f"fluidsynth {args.sound_font} {midi_path} -F {wav_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file", type=str, default="metadata.csv", help="Path and filename of a metadata csv file.")
    parser.add_argument("--midi_dir", type=str, default="data/midi", help="Path of the directory to store synthesized midi files.")
    parser.add_argument("--wav_dir", type=str, default="data/wav", help="Path of the directory to store synthesized wav files.")
    parser.add_argument("--sound_font", type=str, default="/usr/share/sounds/sf2/FluidR3_GM.sf2", help="Sound font to synthesize wavs from midi files. See fluidsynth documentation for further details!")

    args = parser.parse_args()
    main(args)

