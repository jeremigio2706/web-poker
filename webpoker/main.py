from flask import Flask, request, render_template, session
from pyChatGPT import ChatGPT
import time
import pygetwindow as gw
from selenium import webdriver

app = Flask(__name__)
app.secret_key = " 548-135-2623"
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
            prompt = "Quiero que actúes como el mejor jugador de Poker profesional y cumplas los siguientes pasos 1 - me vas a preguntar mis cartas de pre flop, te escribire las cartas, tu vas a analizar mi respuesta y me escribirás la mejor opción a tomar, en una respuesta que comience con “pre flop”, esta respuesta no puede ser mayor de 10 palabras. 2 – Después de decirme que opción tomar en el pre flop, yo voy a escribirte las cartas del flop, me escribirás la mejor opción a tomar según las cartas de mi mano y la mesa, en una respuesta que comience con “flop”, esta respuesta no puede ser mayor de 10 palabras. 3 – después de decirme que opción tomar en el flop, yo voy a escribirte las cartas del turn, me escribirás la mejor opción a tomar según las cartas de mi mano y la mesa, en una respuesta que comience con “turn”, esta respuesta no puede ser mayor de 10 palabras. 4 – después de decirme que opción tomar en el turn, yo voy a escribirte las cartas del river, me escribirás la mejor opción a tomar según las cartas de mi mano y la mesa, en una respuesta que comience con “river”, esta respuesta no puede ser mayor de 10 palabras. Cuando escriba “up” va significar que otro jugador subió la apuesta, y tu debes decirme si igualar o retirarme según mis cartas y las cartas de la mesa. Cuando escriba “xxx” comenzaremos de nuevo. Reglas que debes tomar en cuenta para entender lo que escribo: me voy a referir a el palo de trebol como T por ejemplo la carta de 2 de trebol la escribiré 2T me voy a referir a el palo de diamante como D por ejemplo la carta de 2 de diamante la escribiré 2D me voy a referir a el palo de corazones como C por ejemplo la carta de 2 de corazón la escribire 2C me voy a referir a el palo de picas como P por ejemplo la carta de 2 de picas la escribiré 2P"

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
    texto = 'xxx'
    return texto


def escribir_box():
    up_value = "UP"
    return up_value


def concatenar_flop():
    if session['nombre_imagen_1'] and session['nombre_imagen_2'] and session['nombre_imagen_3']:
        cartas_flop = session['nombre_imagen_1'] + " " + session['nombre_imagen_2'] + " " + session['nombre_imagen_3']
    else:
        cartas_flop = "No esttan todas las cartas del Flop (Espacio 1, 2 y 3)"
    return cartas_flop


def concatenar_turn():
    cartas_turn = session['nombre_imagen_4']
    return cartas_turn


def concatenar_river():
    cartas_river = session['nombre_imagen_5']
    return cartas_river


def concatenar_preflop():
    cartas_preflop = session['nombre_imagen_6'] + " " + session['nombre_imagen_7']
    return cartas_preflop


def chat_ia(prompt):
    global chat
    chrome_windows = gw.getWindowsWithTitle('Google Chrome')
    if not chrome_windows:
        chat = ChatGPT(session_token, conversation_id)
        time.sleep(5)

    else:
        chrome_window = chrome_windows[0]

    response = chat.send_message(prompt)
    time.sleep(1)
    respuesta = response['message']

    return respuesta


if __name__ == '__main__':
    conversation_id = ''
    session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..7RPg9022FEL5mbvg.0vEkcHQfmrHHkFpbyfbe39E7C8Ju7txCQxptByZhy7IP0wz-htozCWe1CIlY0sjd3qzxWDcx5nVtNNBQ3QnTrloAFo-5tjLmITPYFRH4-vAs0Ri0YbEQ04Zq4Bf080ZSOcn9T3qrr9sPI7vsOwB7utGotZxa99nByHcYScZ-msO33L2JXzsGaW3rPTsAlZIb7GSTVHxOnrkt1g6X7TABHn7V8bZowJziQxdwK01edq76ltUbiOuv5LDVhA7vOu-ECthYwRp9iRotHKpZmPtmfmdzydTUX1BBbrZaU-lcalTo2OAlUaqEQ__z2QvAg6E7JgP9HebIrwQIs2gsyAoBhYPvUN-jg6kS7iOJk0YeZD0nXYc-9WQczMTbfvQepu8d74Lu5R5CM6s0o5jTliZjSc7sES5bXgA2YeE8-zoZCjHVoWcx-MguHudJmaJ7tXFx_VT1uhyGiT3ZhSiHvTHvfGeGmzWCh-8rU3zspim_HRO5JcIuqpWMP9MXkAkGJfixPLzyhK6evXHLFOD31SfQD4N_tHUjYLXIXH87GOI5ofGN7EXkwRFOSsfFshNkTXECbeyyhRgnSfuqx8Z-9BXX8G-eAO8yn7m1VYDrC-j2GkB4TTbE8EiOea1oVflrhHFarqodjyYQHt_56VtEoOjsjHIkBnJ9UIVhGJ1XcRBcVcSYxw3IRsHWPo69XJZy7SOgQIfpXxra-85E8dAxCeYMZIBctzksVF33tjhhZ5kXEwhxBvu4bmHUMDAnzJfd1_PH4Bckf6bHkcoiIyKHIyIMaKhciVn3SdnNowbDMtJ7uIucQNz6V94dwlYE06Xkttqo9-9n-f_CtL3rY2FHTSk20ey2o4yJUBoxhqaVBuqBnOCTsQexbpXB62wFxX0SyK7SZzsiEymqHwdXkyyDmU4omlWswnFsOXCEDlIgyto3vQzPo3xfEGnWvlkVKRCdHJklwDRWNfzxS9hAaFq36_jna5ze42MrKVbjKOMWvplr0_elD2iFTjdvyP60BgaJ49Z0cKVX9Cq6ArxYPS14SKsUpVWBrlFxbd4bDA12FrWl4G9BSicl14fyaYLCC6MOyfDMdhuogTsQ2JYcSBuGkMMu7AHsaunHoU5a0RZiP8m_LTiy5RFESfVLvPx1lwbHCpRpOvx9so8Nov9lW0_P2g6Tj8BC2BWy_XrIRfLuZMr_z_W2LvZsrXS3X77FjxF1sNe2cmlPh7A6mdMl7Ld4M9KU2JsvQFN31yuPKJy4-seNu4tWE7_YxT-qQyXuHSGiQYJKAE1bHvkBqHffVk7PgYoXAuXmK6TDSKDrFLh77njOw7oVX6e7qDjLeA7dg95JJ4bY0orWVeZ8ALspI7F-HWnhBKIl9jFn6_thW1hXA7scuwYS-bxuBPfk0PRrKAHuXAHW9jjUPrY7viyh6s9BuCu7xH1nzqHFeAAlTPmPmW4UfoWDl5GGII6aZd-ZBW47hkh5N0KxxvgLQvy5-D-H9EEH0EO77OozMQbQl6eUorOUZhkehUzGMIZeEEpzs91sDJL-wfX00QwRubsE8Wy_aDWZlh_uBGyQMYZiOLcX0AHTZw82UOErXD_wv12zehQCOJ22s8Bert6Ybw-iyhKMP2sPrCB7bN4syNKBz6oFkjf9daBTKdUk_crQBlRqYiBfDKDVy6aOE3Y8tNDvwBQ_0vKGxGhdKmQYyLzVNUl5HeNpY0gDF3cd-_ZmV3vGN7s9UL0VK08DJjGt2q3xVseTz71-VrpItk28a4PXoNs6Vd4lAo1WFA68HA__HsWCUX1WsFgl6by6swDWhB8lxuEL_jMKfWaP1gRu-PMQEUiNdkZyowsBBPTECp426ZTQU12ODYkzGSYKqVUTjve6CIQV5WNEo5PqJ9ayS08j92X039K5qFFsjA2RMNlCxuxe7svX3qs7cCmfnL82QTbWr1O_aDxrHyO95kA4lm6UnaZuvqnInVMnuIXTeBK3fFvSQuMNoBiH8KinvLov4H3XKmh6jEUA9gxPaRyrAlLdD30pNp92UTjuXPledxk-nf-zEvTIy4Byf7oNwf0KJMzLjiEfqV2J4KxZzKq6P-ALm_LQFUBg3y2QRR7m7raEeq_7NhyQEIglG2EfP-q2Dx4wn8y5qzDECuxGjFxXoMoymqdKUQEb2vc1ka7Zybu5nnFLPsq3V0EkHodmwdfYcgt4-mRo2hcY-PH72uTeK8oO8hjjwRqIwhNSgNLqnvUFP5vOjZ1nNYJKp_j1CfX3jP2Tb1DDqF1-EoIUPRABLy9ELTfjmBBX6YT25tVpIaNmRGT9eouf49eZcFizqqTBR368ZmhUEgR2_b6MaF4ilvZWCVBXkNjj_GFhm06EUaBDo3WFUZDkVNcMx1dsJVQbUIJMzhaJUySsbtkSxITGxfJRR3UQE3Ra9mcpxHi44ZYz2LziFyPXXOyc2Mg2r5DKFUfMSnPyZw-PryShp8kcLgluHuRQQ0pHJHy_w3seY6T9J-QfCxot9dJiGc69wELe6dGSUj6jSKsgej3Hm90vyCId0g_EslLZTSyPDIJ9iugZTmQw13Hkgi-FdrNUOwtP2YHj4gOuGrjYqPZsEj1xGVpEMt0v3VDb-JXoY9Vi-BYDx4IU77K7QNSVL0GqWAUOZj_Pm8f200aOeB7j5y8_4ZNbdbMRiha7DT6wD8zophYAtpRyfAQJEAj8Zz9iS4JpE6aIyBDyhobkq-fjaNkEsQgHInHhHN1-9juI9A3njE2cLllAh2WyeMZCjl-cv7eHVgvz1JeDgLSrhsveUOuKy5yigC1K8kHaPFF6d3GJq031M5AWK8iUcoISqNk09llRZmkGA-z-QMjAjOnYTO7F.7kvTjn7sLQF-v9sUf-wj_g'
    prompt = "Quiero que actúes como el mejor jugador de Poker profesional y cumplas los siguientes pasos 1 - me vas a preguntar mis cartas de pre flop, te escribire las cartas, tu vas a analizar mi respuesta y me escribirás la mejor opción a tomar, en una respuesta que comience con “pre flop”, esta respuesta no puede ser mayor de 10 palabras y seguidamente. 2 – Después de decirme que opción tomar en el pre flop, yo voy a escribirte las cartas del flop, me escribirás la mejor opción a tomar según las cartas de mi mano y la mesa, en una respuesta que comience con “flop”, esta respuesta no puede ser mayor de 10 palabras. 3 – después de decirme que opción tomar en el flop, yo voy a escribirte las cartas del turn, me escribirás la mejor opción a tomar según las cartas de mi mano y la mesa, en una respuesta que comience con “turn”, esta respuesta no puede ser mayor de 10 palabras. 4 – después de decirme que opción tomar en el turn, yo voy a escribirte las cartas del river, me escribirás la mejor opción a tomar según las cartas de mi mano y la mesa, en una respuesta que comience con “river”, esta respuesta no puede ser mayor de 10 palabras. Cuando escriba “up” va significar que otro jugador subió la apuesta, y tu debes decirme si igualar o retirarme según mis cartas y las cartas de la mesa. Cuando escriba “xxx” comenzaremos de nuevo. Reglas que debes tomar en cuenta para entender lo que escribo: me voy a referir a el palo de trebol como T por ejemplo la carta de 2 de trebol la escribiré 2T me voy a referir a el palo de diamante como D por ejemplo la carta de 2 de diamante la escribiré 2D me voy a referir a el palo de corazones como C por ejemplo la carta de 2 de corazón la escribire 2C me voy a referir a el palo de picas como P por ejemplo la carta de 2 de picas la escribiré 2P"
    app.run(debug=True, port=5000)
