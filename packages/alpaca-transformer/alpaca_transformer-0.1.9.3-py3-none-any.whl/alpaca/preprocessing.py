

class Preprocess:
    def __init__(self):
        self.text = None


    def train_test_split(self, txt_path, split):
    
        # Read the text file
        with open(txt_path, 'r') as f:
            text = f.read()

        # Calculate the number of words for training and testing
        total_words = len(text.split())
        train_amount = int(total_words * split)
        test_amount = total_words - train_amount

        # Split the text into training and testing sets
        words = text.split()
        train_text = ' '.join(words[:train_amount])
        test_text = ' '.join(words[train_amount:])

        # Print the word counts
        print(f"Train Word Count: {train_amount}")
        print(f"Test Word Count: {test_amount}")

        return train_text, test_text


    def process_txt(self, txt_path, max_seq_len, new_file=None, split_tool='.'):
        text = ""
        with open(txt_path, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) > max_seq_len:
                    sentences = line.split(split_tool)
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if sentence:
                            text += sentence + '\n'
                else:
                    text += line + '\n'
        
        
        if new_file:
            with open(new_file, 'w') as f:
                f.write(text)

        
        self.text = text
        return text
    
    def remove_from_text(self, text=None, remove_strings=None):
        if not text:
            if not self.text:
                raise LookupError("No text to modify.")
            else:
                text = self.text
        
        if remove_strings:
            for thing in remove_strings:
                text = text.replace(thing, '')
        
        self.text = text
        return text

    def change_all_instances(self, text=None, og_word=None, change=None):
        if not text:
            if not self.text:
                raise LookupError("No text to modify.")
            else:
                text = self.text
        
        if og_word and change:
            text = text.replace(og_word, change)
        
        self.text = text
        return text
    
    def lowercase_text(self, text=None):
        if not text:
            if not self.text:
                raise LookupError("No text to modify.")
            else:
                text = self.text
        
        text = text.lower()
        self.text = text
        return text