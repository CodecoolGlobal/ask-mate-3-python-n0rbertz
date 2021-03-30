import csv




def get_data_from_file(data_file):
    data=[]
    with open(data_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def write_questions(data_file, new_questions):
    with open(data_file, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for question in new_questions:
            csv_writer.writerow(question)

def add_question(data_file, question):
    with open(data_file, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(question)

def write_answers(data_file, new_answers):
    with open(data_file, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for answer in new_answers:
            csv_writer.writerow(answer)