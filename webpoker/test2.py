


lista_d = ['familia', 'dinero', 'desarrollo']
messages = []
question = {}

for elemento in lista_d:
    question = {}
    question['role'] = 'user'
    question['content'] = elemento
    messages.append(question.copy())
    print(messages)