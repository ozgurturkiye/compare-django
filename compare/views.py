from django.shortcuts import render

import os


def home(request):
    return render(request, 'compare/home.html')


def show(request):
    return render(request, 'compare/show.html')


def result(request):

    with open("compare/original.txt") as f:
        total_word_count = len(f.readlines())


    def write_user_input_to_file():

        user_input = request.POST['user_input']
        user_input_splitted = user_input.split()

        # Write words line by line to original_file
        with open("compare/original.txt", "w") as f:
            for word in user_input_splitted:
                f.write(word + "\n")


    def write_diff_to_file():
        os.system('git diff compare/original.txt > compare/diff_result.txt')


    def show_result():
        missing_words = []  # These words are in the original text but didn't write -
        misspelled_words = []  # These words aren't in the original text but have written +
        mistake_count = 0  # Just missing_words will be added
        correct_words = []

        # Open git diff results
        with open("compare/diff_result.txt") as f:
            result_list = f.readlines()

        for line in result_list:
            if line[0] == "-" and (line[1] != "-"):
                mistake_count += 1
                missing_words.append(line[1:-1])

            if line[0] == "+" and (line[1] != "+"):
                # These words didn't count as mistake
                misspelled_words.append(line[1:-1])

            if line[0] == " ":
                # Correct word
                correct_words.append(line[1:-1])

        correct_word_count = total_word_count - mistake_count

        all_result = {"total_word_count": total_word_count,
                    "mistake_count": mistake_count,
                    "correct_word_count": correct_word_count,
                    "missing_words" : missing_words,
                    "misspelled_words" : misspelled_words,
                    "correct_words": correct_words,
        }

        os.system('git checkout compare/original.txt')

        return all_result
    
    write_user_input_to_file()
    write_diff_to_file()
    all_result = show_result()

    return render(request, 'compare/result.html', {'all_result': all_result})




