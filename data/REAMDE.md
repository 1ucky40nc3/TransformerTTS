# Piano dataset
The first dataset shall be constructed to enable TransformerTTS to learn to play the piano. To make things easier at first we will employ MIDI songs as a source for aligned data. In this case the selection of MIDI songs arises from [REMI](https://github.com/YatingMusic/remi) and is tokenized via [MidiTok](https://github.com/Natooz/MidiTok). Both works are interconnected. The songs are synthesized via [FluidSynth](https://github.com/FluidSynth/fluidsynth) to aggregate wav data.

A colab notebook will be provide which demonstrates the following steps.

## Download the data
The [download_remi.sh](data/download_remi.sh) script  is provided to download the MIDI dataset published by REMI.

## Create the text data
In this case tokenized snippets of MIDI songs shall be used as data to train TransformersTTS. To create theese snippets a [create_text.sh](data/create_text.sh) script is provided. This script implements the tokenization of MIDI songs via MidiTok as it is described by REMI. Resulting is a list of tokens per song. For each song we than randomly sample a number of sequences of a given length. Theese are than treated as the text for which audio shall be synthesized.
The results will be saved in a `.csv` file in order to mimic the LJSpeech format.

## Create the audio data
After creating the text data we will synthesize corresponding audio data by using the reverse process of the MidiTok tokenization. This is implemented in the [create_audio.sh](data/create_audio.sh) script. We will first use the previously generated token sequences with a hint of the original MIDI source to generate each MIDI samples. Next we synthesize wav data using FluidSynth. The resulting files will also be noted in the `.csv` file. This is again to integrate with the LJSpeech format used in TransformerTTS.