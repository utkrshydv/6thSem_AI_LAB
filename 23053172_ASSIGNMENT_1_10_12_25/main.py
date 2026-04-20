import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import os


def main():
    input_filename = 'somefile.txt'

    if not os.path.exists(input_filename):
        print(
            f"Error: '{input_filename}' not found. Please make sure the file is in the same folder.")
        return

    print("--- Starting Assignment Processing ---")

    # PART 1
    print(f"Reading {input_filename}...")

    with open(input_filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    data = []
    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            body = lines[i]
            headline = lines[i+1]
            label = lines[i+2]
            data.append([body, headline, label])

    df = pd.DataFrame(
        data, columns=['News Body Content', 'News Body Headline', 'Label'])

    df.to_csv('1_formatted_data.csv', index=False)
    print("✅ Part I Complete: Saved '1_formatted_data.csv'")

    # PART 2

    print("Calculating word counts...")

    df_words = df.copy()

    def count_words_simple(text):
        if pd.isna(text):
            return 0
        return len(str(text).split())

    df_words['Body_Word_Count'] = df_words['News Body Content'].apply(
        count_words_simple)
    df_words['Headline_Word_Count'] = df_words['News Body Headline'].apply(
        count_words_simple)

    output_df_words = df_words[[
        'News Body Content', 'News Body Headline', 'Body_Word_Count', 'Headline_Word_Count']]
    output_df_words.to_csv('2_word_counts.csv', index=False)
    print("✅ Part II Complete: Saved '2_word_counts.csv'")

    # PART 3

    print("Calculating NLTK token counts (this might take a moment)...")

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK tokenizer data...")
        nltk.download('punkt')
        nltk.download('punkt_tab')

    df_tokens = df.copy()

    def count_tokens_nltk(text):
        if pd.isna(text):
            return 0
        return len(word_tokenize(str(text)))

    df_tokens['Body_Token_Count'] = df_tokens['News Body Content'].apply(
        count_tokens_nltk)
    df_tokens['Headline_Token_Count'] = df_tokens['News Body Headline'].apply(
        count_tokens_nltk)

    output_df_tokens = df_tokens[[
        'News Body Content', 'News Body Headline', 'Body_Token_Count', 'Headline_Token_Count']]
    output_df_tokens.to_csv('3_token_counts.csv', index=False)
    print("✅ Part III Complete: Saved '3_token_counts.csv'")

    print("\nAll tasks finished successfully.")


if __name__ == "__main__":
    main()
