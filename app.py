import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import io
import base64

app = Flask(__name__)

def modified_sir(y, t, beta, gamma, alpha):
    S, I, R, H = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I - alpha * I
    dRdt = gamma * I
    dHdt = alpha * I
    return [dSdt, dIdt, dRdt, dHdt]

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_url = None

    if request.method == 'POST':
        # Ambil input user
        beta = float(request.form['beta'])
        gamma = float(request.form['gamma'])
        alpha = float(request.form['alpha'])
        S0 = float(request.form['S0'])
        I0 = float(request.form['I0'])
        duration = int(request.form['duration'])

        R0 = 0.0
        H0 = 0.0
        y0 = [S0, I0, R0, H0]

        t = np.linspace(0, duration, 300)

        result = odeint(modified_sir, y0, t, args=(beta, gamma, alpha))
        S, I, R, H = result.T

        # Plot
        plt.figure(figsize=(8,5))
        plt.plot(t, S, label='S', linewidth=2)
        plt.plot(t, I, label='I', linewidth=2)
        plt.plot(t, R, label='R', linewidth=2)
        plt.plot(t, H, label='H', linewidth=2)
        plt.xlabel("Waktu")
        plt.ylabel("Proporsi Populasi")
        plt.title("Simulasi Penyebaran Hoaks (SIR Termodifikasi)")
        plt.grid(True)
        plt.legend()

        # Simpan ke base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        graph_url = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

    return render_template("index.html", graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)
