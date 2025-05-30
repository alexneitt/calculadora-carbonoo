from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
