import csv

DATA_HEADER = ['id','submission_time','view_number','vote_number','title','message','image']
QUESTIONS = 'sample_data/question.csv'
ANSWERS = 'sample_data/answer.csv'

def collect_qestions():
    with open(QUESTIONS, 'r') as questions:
        result = []
        questions_dict = csv.DictReader(questions, fieldnames=DATA_HEADER)
        for question in questions_dict:
            result.append(question)
        return result


def collect_answers():
    pass
