with open("raw_original_text.txt") as f:
    raw_text = f.read()

    # Split raw_text
    splitted_text = raw_text.split()
    total_word_count = len(splitted_text)


# Write words line by line to original.txt
with open("original.txt", "w") as file:
    for word in splitted_text:
        file.write(word + "\n")
