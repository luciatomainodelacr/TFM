from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('ruta_2_puntos_v1.html')
if __name__ == '__main__':
   app.run(host='0.0.0.0')
