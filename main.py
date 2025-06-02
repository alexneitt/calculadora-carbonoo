from waitress import serve
from app import app  # Aquí importas tu objeto Flask que está en app.py

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
