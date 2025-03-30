import json
from collections import Counter
import torch
from tqdm.auto import tqdm

class Tokenizer():
    def __init__(self):
        self.vocab = None
        self.letter_pairs = []
        self.byte_pairs = []
        self.text = ''
        self.tokens = []

    def save_as_file(self, vocab_save_path='vocab.json', token_save_path='tokens.json'):
        tokenizer_data = {
            "vocab": {str(k): v for k, v in self.vocab.items()},
            "merges": ["".join(map(str, pair)) for pair in self.vocab.keys()],
            "special_tokens": {"<unk>": 0, "<pad>": 1}
        }

        with open(vocab_save_path, 'w', encoding='utf-8') as vocab_file:
            json.dump(tokenizer_data, vocab_file, indent=4)

        with open(token_save_path, 'w', encoding='utf-8') as token_file:
            json.dump(self.tokens, token_file, indent=4)

        print(f"Saved tokens at: '{token_save_path}'")
        print(f"Saved vocab at: '{vocab_save_path}'")

    def text_to_byte(self, text: str):
        last_letter = text[-1]
        text += last_letter
        self.text = text
        return text.encode('utf-8')

    def byte_to_pairs(self, byte_text, text=None):
        if not text:
            text = self.text
        byte_pairs = [(byte_text[i], byte_text[i + 1]) for i in range(len(byte_text) - 1)]
        letter_pairs = [(text[i], text[i + 1]) for i in range(len(text) - 1)]

        for pair in byte_pairs:
            self.byte_pairs.append(pair)
        for pair in letter_pairs:
            self.letter_pairs.append(pair)

        return byte_pairs

    def byte_pair_frequency(self, pair_list):
        return Counter(pair_list)

    def merge_pairs(self, byte_pairs, pair_to_merge):
        new_byte_pairs = []
        replacement = (pair_to_merge[0], pair_to_merge[1])

        for i in range(len(byte_pairs) - 1):
            if byte_pairs[i] == pair_to_merge:
                new_byte_pairs.append(replacement)
                i += 1
            else:
                new_byte_pairs.append(byte_pairs[i])

        if byte_pairs[-1] != pair_to_merge:
            new_byte_pairs.append(byte_pairs[-1])

        return new_byte_pairs

    def create_vocab(self, text, num_merges=5):
        byte_text = self.text_to_byte(text)
        byte_pairs = self.byte_to_pairs(byte_text)
        byte_frequency = self.byte_pair_frequency(byte_pairs)

        self.vocab = {pair: i + 1 for i, pair in enumerate(byte_frequency.keys())}

        for _ in tqdm(range(num_merges), desc="Vocab Creation Progress: "):
            if not byte_frequency:
                break

            most_frequent = max(byte_frequency, key=byte_frequency.get)
            new_token = (most_frequent[0] + most_frequent[1],)

            self.vocab[new_token] = max(self.vocab.values()) + 1

            byte_pairs = self.merge_pairs(byte_pairs, most_frequent)
            byte_frequency = self.byte_pair_frequency(byte_pairs)

        return self.vocab

    def load_vocab(self, vocab_path):
        with open(vocab_path, "r") as f:
            data = json.load(f)

        vocab = {eval(k): v for k, v in data["vocab"].items()}

        self.vocab = vocab
        self.merges = data.get("merges", [])
        self.special_tokens = data.get("special_tokens", {})

        return vocab

    def tokenize(self, text, vocab=None, save_as_file=False, save_file_path='tokens.txt'):
        if vocab is None and self.vocab is None:
            self.vocab = self.create_vocab(text)
        elif isinstance(vocab, str):
            self.load_vocab(vocab)

        if not isinstance(self.vocab, dict):
            raise ValueError(f"Vocabulary must be a dictionary, got {type(self.vocab)}")

        byte_text = self.text_to_byte(text)
        tokens = []

        while len(byte_text) > 0:
            longest_match = None
            longest_match_len = 0

            for length in range(2, len(byte_text) + 1):
                pair = tuple(byte_text[:length])
                if pair in self.vocab:
                    if length > longest_match_len:
                        longest_match = pair
                        longest_match_len = length

            if longest_match:
                tokens.append(self.vocab[longest_match])
                byte_text = byte_text[longest_match_len:]
            else:
                tokens.append(0)
                byte_text = byte_text[1:]

        self.tokens = tokens

        if save_as_file:
            with open(save_file_path, 'w') as f:
                f.writelines(f"{token}\n" for token in tokens)

        return tokens

    def detokenize(self, tokenized, vocab=None, include_unknown=False):
        if not vocab:
            vocab = {v: k for k, v in self.vocab.items()}
        detokenized = ''
        for token in tokenized:
            if isinstance(token, torch.Tensor):
                token = token.item()

            try:
                # Get the byte pair corresponding to the token
                pair = vocab[token]
                # Append the corresponding characters
                for char in pair:
                    detokenized += chr(char)
            except KeyError:
                if include_unknown:
                    detokenized += "<unk>"

        return detokenized



if __name__ == "__main__":

    tokenizer = Tokenizer()

    text = ' Doing work is a lot of work fooly foool! and if you dont understand that then you need to do some work fooly fool '

    tokenizer.create_vocab(text, num_merges=100)
    print(f"Vocab: {tokenizer.vocab}")

    tokenized = tokenizer.tokenize(text, vocab=tokenizer.vocab)
    print(f"tokenized: {tokenized}")

    detokenized = tokenizer.detokenize(tokenized)
    print(f"Detokenized: {detokenized}")
