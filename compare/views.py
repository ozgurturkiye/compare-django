from django.shortcuts import render

import os


def home(request):
    return render(request, 'compare/home.html')


def show(request):
    return render(request, 'compare/show.html')


def result(request):

    def make_original_text_to_lined():
        # Open and read raw_original.txt file
        yollar = os.getcwd() # Current path that program runs

        with open("compare/raw_original_text.txt") as file:
            raw_text = file.read()

        # Split raw_text
        splitted_text = raw_text.split()
        total_word_count = len(splitted_text)

        # Write words line by line to original.txt
        with open("compare/original.txt", "w") as file:
            for word in splitted_text:
                file.write(word + "\n")

        os.chdir('compare')                
        os.system('git add original.txt')
        os.system('git commit -m "initial commit"')
        os.chdir('..')                


        return total_word_count

    def make_user_text_to_lined():

        # take user_input file
        with open("compare/user_input.txt", "r") as file:
            user_text = file.read()

        # splitting user text to write file
        user_text_splitted = user_text.split()

        # Write words line by line to original_file
        with open("compare/original.txt", "w") as file:
            for word in user_text_splitted:
                file.write(word + "\n")

    def write_diff_result(total_word_count):
        bash_cmd = 'echo ' + str(total_word_count) + ' >> diff_result.txt'

        os.chdir('compare')                
        os.system('git diff original.txt > diff_result.txt')
        os.system(bash_cmd) # Write to last line original total length
        os.chdir('..')                


    def show_result():
        # Open git diff results
        with open("compare/diff_result.txt") as file:
            result_list = file.readlines()

        total_word_count = int(result_list[-1])  # original text word_count result
        missing_words = []  # These words are in the original text but didn't write -
        misspelled_words = []  # These words aren't in the original text but have written +
        mistake_count = 0  # Just missing_words will be added

        for line in result_list:
            if line[0] == "-" and (line[1] != "-"):
                mistake_count += 1
                missing_words.append(line[1:-1])

            if line[0] == "+" and (line[1] != "+"):
                # These words didn't count as mistake
                misspelled_words.append(line[1:-1])

        correct_word_count = total_word_count - mistake_count

        all_result = {"total_word_count": total_word_count,
                    "mistake_count": mistake_count,
                    "correct_word_count": correct_word_count,
                    "missing_words" : missing_words,
                    "misspelled_words" : misspelled_words,
        }

        os.chdir('compare')                
        # os.system('git checkout .')
        os.system('git add .')
        os.system('git commit -m "last commit"')
        os.chdir('..')                

        return all_result


    total_word_count = make_original_text_to_lined()
    make_user_text_to_lined()
    write_diff_result(total_word_count)
    all_result = show_result()
    all_result['user_post_on_form'] = request.POST['user_input']


    return render(request, 'compare/result.html', {'all_result': all_result})




