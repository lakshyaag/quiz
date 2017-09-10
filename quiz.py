import html
import random



import requests

category = {}
questions = []


def get_categories():
    url = "https://opentdb.com/api_category.php"
    categories = (requests.get(url)).json()

    for category_obj in categories['trivia_categories']:
        category[category_obj['name']] = category_obj['id']

def inp_category():
    get_categories()
    cat_choice = input("Press 0 for general questions or any other key for categories: ")
    if cat_choice is not "0":
        print("Choose from the following: ")
        n = 1
        for key in category:
            print("{}. {}".format(n, key))
            n += 1

        return str(int(input("=> ")) + 8)
    else:
        return '0'

def get_questions():

    cat = (inp_category())
    url = "https://opentdb.com/api.php?amount=10&category={}&type=multiple".format(cat)

    print('-'*75)
    if(cat is not '0'):
        for key, val in category.items():
            if val == int(cat):
                cat = str(key)
                break

        print("Your category is: {}".format(cat))

    else:
        print("Your category is: General")

    questions_bundle = requests.get(url).json()

    for question in questions_bundle['results']:
        incorrects = []
        for inc in question['incorrect_answers']:
            incorrects.append(html.unescape(inc))

        questions.append(
            {
                "question": html.unescape(question['question']),
                "correct": html.unescape(question['correct_answer']),
                "incorrect": incorrects

            }
        )

def answer(user, q):
    if (user == questions[q]['correct']):
        return True
    return False

def print_questions(q):
    q = questions[q]

    answers = []
    answers.append(q['correct'])
    answers = answers + (q['incorrect'])
    random.shuffle(answers)

    question = q['question']

    print("{}".format(question))
    print("A. {}\tB. {}\nC. {}\tD. {}".format(*answers))

    return answers

def game():
    score = 0
    for i in range(10):
        print(i+1, end='. ')
        answers = print_questions(i)
        answer_user = input("=> ").upper()

        if(answer_user == 'A'):
            answer_user = answers[0]
        if (answer_user == 'B'):
            answer_user = answers[1]
        if (answer_user == 'C'):
            answer_user = answers[2]
        if (answer_user == 'D'):
            answer_user = answers[3]

        if(answer(answer_user, i)) is True:
            print("Correct!")
            score += 1

        else:
            print("Incorrect!")
            print("Correct answer is: {}".format(questions[i]['correct']))

        print('-'*75)

    print("Your score is: {}/10".format(score))
    print("Thank you for playing")

get_questions()

print('-'*100)
game()
