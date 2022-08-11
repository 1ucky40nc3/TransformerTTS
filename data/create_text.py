import glob
import random
import argparse

import pandas as pd

from tqdm import tqdm

from miditok import REMI
from miditok import MidiFile


def main(args):
    tokenizer = REMI()
    
    print("Loading songs...")
    paths = glob.glob(f"{args.path}/.midi")
    songs = []
    for path in tqdm(paths):
        midi = MidiFile(path)
        tokens = tokenizer.midi_to_tokens(midi)
        songs.append(tokens)

    print("Extracting snippets...")
    metadata = {
        "filename": [],
        "tokens": [],
        "origin": []
    }
    max_songs = len(songs) - 1
    for i in tqdm(args.num_seq):
        song_idx = random.randint(0, max_songs)
        song_tokens = songs[song_idx][0]
        start_token_idx = random.randint(
            0, len(song_tokens) - 1 - args.min_tokens)
        num_seq_tokens = random.randint(
            args.min_tokens, args.max_tokens)
        end_token_idx = min(
            len(song_tokens), start_token_idx + num_seq_tokens)

        seq = song_tokens[start_token_idx:end_token_idx]

        metadata["filename"].append(f"{str(i)}.wav")
        metadata["tokens"].append(seq)
        metadata["origin"].append(paths[i])

    df = pd.DataFrame(metadata)
    df.to_csv(args.out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="./data", help="Path of the directory containing MIDI files.")
    parser.add_argument("--min_tokens", type=int, default=32, help="Minimum number of tokens for each extracted snippet of the tokenized MIDI file.")
    parser.add_argument("--max_tokens", type=int, default=64, help="Maximum number of tokens for each extracted snippet of the tokenized MIDI file.")
    parser.add_argument("--num_seq", type=int, default=10_000, help="Number of token sequences to extract.")
    parser.add_argument("--out_file", type=str, default="metadata.csv", help="Path and filename of the output csv file.")


    args = parser.parse_args()
    main(args)

