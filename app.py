from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración del correo (usa los datos de tu proveedor SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'alexisrg620@gmail.com'
app.config['MAIL_PASSWORD'] = 'knnn jawr cmyh azwd'  # Usa una contraseña de aplicación segura
app.config['MAIL_DEFAULT_SENDER'] = 'alexisrg620@gmail.com'

mail = Mail(app)

# Factores de emisión por tipo de transporte (kg CO₂ por km)
FACTORES_EMISION = {
    "Auto": 0.21,
    "Moto": 0.12,
    "Camión": 0.05,
    "Bicicleta": 0.0,
    "Caminar": 0.0,
    "Jet": 3.15
}

# Lista para almacenar últimas consultas
ultimas_consultas = []

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    nivel = None
    transporte = None
    kilometros = 0

    if request.method == 'POST':
        transporte = request.form.get('transporte')
        try:
            kilometros = float(request.form.get('kilometros', 0))
        except ValueError:
            kilometros = 0

        if transporte in FACTORES_EMISION and kilometros >= 0:
            factor_emision = FACTORES_EMISION[transporte]
            huella_carbono = kilometros * factor_emision
            resultado = round(huella_carbono, 2)

            # Determinar nivel
            if resultado <= 5:
                nivel = 'excelente'
            elif resultado <= 15:
                nivel = 'bueno'
            elif resultado <= 25:
                nivel = 'regular'
            elif resultado <= 35:
                nivel = 'malo'
            else:
                nivel = 'muy-malo'

            # Guardar la consulta
            consulta = {
                'transporte': transporte,
                'kilometros': kilometros,
                'resultado': resultado,
                'nivel': nivel
            }
            ultimas_consultas.insert(0, consulta)
            ultimas_consultas[:] = ultimas_consultas[:5]  # Limita a 5

    return render_template(
        'index.html',
        resultado=resultado,
        nivel=nivel,
        transporte=transporte,
        kilometros=kilometros,
        ultimas_consultas=ultimas_consultas
    )

@app.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    email_destino = request.form.get('correo')

    if not email_destino:
        return "Correo no proporcionado", 400

    if not ultimas_consultas:
        return "No hay consultas para enviar", 400

    cuerpo = "Últimas 5 consultas de huella de carbono:\n\n"
    for consulta in ultimas_consultas:
        cuerpo += (
            f"- Transporte: {consulta['transporte']}\n"
            f"  Kilómetros: {consulta['kilometros']} km\n"
            f"  CO₂ generado: {consulta['resultado']} kg\n"
            f"  Nivel: {consulta['nivel'].replace('-', ' ').capitalize()}\n\n"
        )

    try:
        msg = Message(
            subject="Resumen de huella de carbono",
            recipients=[email_destino],
            body=cuerpo
        )
        mail.send(msg)
        return "Correo enviado correctamente"
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
