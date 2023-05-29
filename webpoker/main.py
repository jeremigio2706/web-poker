from flask import Flask, request, render_template, session
import time
import random
import string
import openai




openai.api_key = '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'
messages = []
messages.append({"role": "system", "content": """Quiero que actúes como el mejor jugador de Poker profesional y cumplas los siguientes pasos
    Todo comenzara cuando recibas la respuesta "comencemos" y me vas a preguntar mis cartas de pre flop en una respuesta que empezara con: “Comencemos, dime tus cartas del pre flop:”
    Tomaras todas las decisiones sobre si igualar, subir la apuesta de manera moderada o agresiva o si retirarme de la ronda siempre y me dirás la decisión según lo siguiente:
    1-	Te escribiré las cartas, tú vas a analizar mi respuesta que empezara con: “Estas son mis cartas del pre flop:” y me escribirás la mejor opción a tomar, en una respuesta que comience con “pre flop:”, esta respuesta no puede ser mayor de 10 palabras.
    2-	Después de decirme que opción tomar en el pre flop, yo voy a escribirte las cartas del flop, tú vas a analizar mi respuesta que empezara con: “Estas son las cartas del flop:” y me escribirás la mejor opción a tomar según mis cartas del pre flop y las cartas del flop, en una respuesta que comience con “flop:”, esta respuesta no puede ser mayor de 10 palabras. 
    3-	Después de decirme que opción tomar en el flop, yo voy a escribirte las cartas del turn, tú vas a analizar mi respuesta que empezara con: “Estas son las cartas del turn:” y me escribirás la mejor opción a tomar según mis cartas del pre flop y las cartas del flop y del turn, en una respuesta que comience con “turn”, esta respuesta no puede ser mayor de 10 palabras. 
    4-	Después de decirme que opción tomar en el turn, yo voy a escribirte las cartas del river, tú vas a analizar mi respuesta que empezara con: “Estas son las cartas del river:” y me escribirás la mejor opción a tomar según las cartas de mi mano y la mesa, en una respuesta que comience con “river”, esta respuesta no puede ser mayor de 10 palabras. 
    Cuando te escriba “Un Jugador subió la apuesta” va significar que otro jugador subió la apuesta, y tú debes decidir y decirme que opción tomar según mis cartas del pre flop y del flop, del turn y/o del river en una respuesta que comenzara con “Apuesta subida por otro jugador tu deberías:” y me dices que opción tomar.
    Cuando te escriba “Reiniciar el juego” comenzaremos de nuevo y me pedirás mis cartas del pre flop en una respuesta que empezara con: “Comencemos de nuevo, dime tus cartas del pre flop”.
    Reglas que debes tomar en cuenta para entender lo que escribo: me voy a referir a el palo de trébol como T por ejemplo la carta de As de trébol la escribiré AT me voy a referir a el palo de diamante como D por ejemplo la carta King de diamante la escribiré KD me voy a referir a el palo de corazones como C por ejemplo la carta Queen de corazón la escribiré QC me voy a referir a el palo de picas como P por ejemplo la carta de 2 de picas la escribiré 2P
    En todo momento me vas a  evaluar la fuerza de mi mano y me vas a decir que decisión tomar sobre el juego, si debo retirarme, subir la apuesta de manera moderada o fuerte o si retirame de la ronda.
"""})


def generar_valor_aleatorio():
    caracteres = string.ascii_letters + string.digits + '-'
    longitud = 256
    valor_aleatorio = ''.join(random.choice(caracteres) for _ in range(longitud))
    return valor_aleatorio


app = Flask(__name__)
app.secret_key = generar_valor_aleatorio()
global prompt, chat


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'nombre_imagen_1' not in session:
        session['nombre_imagen_1'] = None

    if 'nombre_imagen_2' not in session:
        session['nombre_imagen_2'] = None

    if 'nombre_imagen_3' not in session:
        session['nombre_imagen_3'] = None

    if 'nombre_imagen_4' not in session:
        session['nombre_imagen_4'] = None

    if 'nombre_imagen_5' not in session:
        session['nombre_imagen_5'] = None

    if 'nombre_imagen_6' not in session:
        session['nombre_imagen_6'] = None

    if 'nombre_imagen_7' not in session:
        session['nombre_imagen_7'] = None

    if request.method == 'POST':

        nombre_imagen_1 = session['nombre_imagen_1']
        nombre_imagen_2 = session['nombre_imagen_2']
        nombre_imagen_3 = session['nombre_imagen_3']
        nombre_imagen_4 = session['nombre_imagen_4']
        nombre_imagen_5 = session['nombre_imagen_5']
        nombre_imagen_6 = session['nombre_imagen_6']
        nombre_imagen_7 = session['nombre_imagen_7']

        if 'start' in request.form:
            prompt = 'comencemos'
            return render_template('index.html', nombre_imagen_1=nombre_imagen_1, nombre_imagen_2=nombre_imagen_2,
                                   nombre_imagen_3=nombre_imagen_3, nombre_imagen_4=nombre_imagen_4,
                                   nombre_imagen_5=nombre_imagen_5, nombre_imagen_6=nombre_imagen_6,
                                   nombre_imagen_7=nombre_imagen_7, respuesta=chat_ia(prompt))

        if 'up_value' in request.form:
            prompt = escribir_box()
            return render_template('index.html', nombre_imagen_1=nombre_imagen_1, nombre_imagen_2=nombre_imagen_2,
                                   nombre_imagen_3=nombre_imagen_3, nombre_imagen_4=nombre_imagen_4,
                                   nombre_imagen_5=nombre_imagen_5, nombre_imagen_6=nombre_imagen_6,
                                   nombre_imagen_7=nombre_imagen_7, respuesta=chat_ia(prompt))

        if 'reinicio' in request.form:
            prompt = reinicio()
            nombre_imagen_1 = session['nombre_imagen_1']
            nombre_imagen_2 = session['nombre_imagen_2']
            nombre_imagen_3 = session['nombre_imagen_3']
            nombre_imagen_4 = session['nombre_imagen_4']
            nombre_imagen_5 = session['nombre_imagen_5']
            nombre_imagen_6 = session['nombre_imagen_6']
            nombre_imagen_7 = session['nombre_imagen_7']
            return render_template('index.html', nombre_imagen_1=nombre_imagen_1, nombre_imagen_2=nombre_imagen_2,
                                   nombre_imagen_3=nombre_imagen_3, nombre_imagen_4=nombre_imagen_4,
                                   nombre_imagen_5=nombre_imagen_5, nombre_imagen_6=nombre_imagen_6,
                                   nombre_imagen_7=nombre_imagen_7, respuesta=chat_ia(prompt))

        if request.form.get('nombre_imagen_1') is not None:
            nombre_imagen_1 = request.form.get('nombre_imagen_1')
            session['nombre_imagen_1'] = nombre_imagen_1
            prompt = "Ingrese la segunda carta del flop"

        if session['nombre_imagen_1']:
            if request.form.get('nombre_imagen_2') is not None:
                nombre_imagen_2 = request.form.get('nombre_imagen_2')
                session['nombre_imagen_2'] = nombre_imagen_2
                prompt = "Ingrese la tercera carta del flop"

        if session['nombre_imagen_2']:
            if request.form.get('nombre_imagen_3') is not None:
                nombre_imagen_3 = request.form.get('nombre_imagen_3')
                session['nombre_imagen_3'] = nombre_imagen_3
                prompt = concatenar_flop()

                return render_template('index.html', nombre_imagen_1=nombre_imagen_1, nombre_imagen_2=nombre_imagen_2,
                                       nombre_imagen_3=nombre_imagen_3, nombre_imagen_4=nombre_imagen_4,
                                       nombre_imagen_5=nombre_imagen_5, nombre_imagen_6=nombre_imagen_6,
                                       nombre_imagen_7=nombre_imagen_7, respuesta=chat_ia(prompt))

        if request.form.get('nombre_imagen_4') is not None:
            nombre_imagen_4 = request.form.get('nombre_imagen_4')
            session['nombre_imagen_4'] = nombre_imagen_4
            prompt = concatenar_turn()

            return render_template('index.html', nombre_imagen_1=nombre_imagen_1, nombre_imagen_2=nombre_imagen_2,
                                   nombre_imagen_3=nombre_imagen_3, nombre_imagen_4=nombre_imagen_4,
                                   nombre_imagen_5=nombre_imagen_5, nombre_imagen_6=nombre_imagen_6,
                                   nombre_imagen_7=nombre_imagen_7, respuesta=chat_ia(prompt))

        if request.form.get('nombre_imagen_5') is not None:
            nombre_imagen_5 = request.form.get('nombre_imagen_5')
            session['nombre_imagen_5'] = nombre_imagen_5
            prompt = concatenar_river()

            return render_template('index.html', nombre_imagen_1=nombre_imagen_1, nombre_imagen_2=nombre_imagen_2,
                                   nombre_imagen_3=nombre_imagen_3, nombre_imagen_4=nombre_imagen_4,
                                   nombre_imagen_5=nombre_imagen_5, nombre_imagen_6=nombre_imagen_6,
                                   nombre_imagen_7=nombre_imagen_7, respuesta=chat_ia(prompt))

        if request.form.get('nombre_imagen_6') is not None:
            nombre_imagen_6 = request.form.get('nombre_imagen_6')
            session['nombre_imagen_6'] = nombre_imagen_6
            prompt = "Ingrese la otra carta del preflop"

        if session['nombre_imagen_6']:
            if request.form.get('nombre_imagen_7') is not None:
                nombre_imagen_7 = request.form.get('nombre_imagen_7')
                session['nombre_imagen_7'] = nombre_imagen_7
                prompt = concatenar_preflop()

                return render_template('index.html', nombre_imagen_1=nombre_imagen_1, nombre_imagen_2=nombre_imagen_2,
                                       nombre_imagen_3=nombre_imagen_3, nombre_imagen_4=nombre_imagen_4,
                                       nombre_imagen_5=nombre_imagen_5, nombre_imagen_6=nombre_imagen_6,
                                       nombre_imagen_7=nombre_imagen_7, respuesta=chat_ia(prompt))



    else:
        nombre_imagen_1 = session['nombre_imagen_1']
        nombre_imagen_2 = session['nombre_imagen_2']
        nombre_imagen_3 = session['nombre_imagen_3']
        nombre_imagen_4 = session['nombre_imagen_4']
        nombre_imagen_5 = session['nombre_imagen_5']
        nombre_imagen_6 = session['nombre_imagen_6']
        nombre_imagen_7 = session['nombre_imagen_7']
        prompt = 'Clic en Comenzar'

    return render_template('index.html', nombre_imagen_1=nombre_imagen_1, nombre_imagen_2=nombre_imagen_2,
                           nombre_imagen_3=nombre_imagen_3, nombre_imagen_4=nombre_imagen_4,
                           nombre_imagen_5=nombre_imagen_5, nombre_imagen_6=nombre_imagen_6,
                           nombre_imagen_7=nombre_imagen_7, respuesta=prompt)


def reinicio():
    session['nombre_imagen_1'] = None
    session['nombre_imagen_2'] = None
    session['nombre_imagen_3'] = None
    session['nombre_imagen_4'] = None
    session['nombre_imagen_5'] = None
    session['nombre_imagen_6'] = None
    session['nombre_imagen_7'] = None
    del messages[1:]
    texto = 'Reiniciar el juego'
    return texto


def escribir_box():
    up_value = "Un Jugador subió la apuesta"
    return up_value


def concatenar_flop():
    if session['nombre_imagen_1'] and session['nombre_imagen_2'] and session['nombre_imagen_3']:
        cartas_flop = 'Estas son las cartas del flop:' + " " + session['nombre_imagen_1'] + " " + session['nombre_imagen_2'] + " " + session['nombre_imagen_3']
    else:
        cartas_flop = "No estan todas las cartas del Flop (Espacio 1, 2 y 3)"
    return cartas_flop


def concatenar_turn():
    cartas_turn = 'Estas son las cartas del turn:' + " " + session['nombre_imagen_4']
    return cartas_turn


def concatenar_river():
    cartas_river = 'Estas son las cartas del river:' + " " + session['nombre_imagen_5']
    return cartas_river


def concatenar_preflop():
    if session['nombre_imagen_6'] and session['nombre_imagen_7']:
        cartas_preflop = 'Estas son mis cartas del pre flop:' + " " + session['nombre_imagen_6'] + " " + session['nombre_imagen_7']
    else:
        cartas_preflop = "no estan todas las cartas del preflop"
    return cartas_preflop


def chat_ia(prompt):
    question = {}
    response_ia = {}
    question['role'] = 'user'
    question['content'] = prompt
    messages.append(question)

    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        try:
            answer = response['choices'][0]['message']['content']
            response_ia['role'] = 'assistant'
            response_ia['content'] = answer
            messages.append(response_ia)
            print(messages)
        except:
            answer = 'Hemos tenido un error al recibir la respuesta de openai'
    except Exception as e:
        answer = f'Hay un error {e}, para soporte contactar con https://t.me/jetrader_cu'

    return answer


if __name__ == '__main__':
    app.run(debug=True)
