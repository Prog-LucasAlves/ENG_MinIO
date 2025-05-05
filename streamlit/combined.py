import subprocess
import threading

from flask import Flask, redirect

app = Flask(__name__)


# Roda o Streamlit como subprocesso
def run_streamlit():
    subprocess.run(
        [
            "streamlit",
            "run",
            "combined.py",
            "--server.port=8501",
            "--server.headless=true",
            "--server.enableCORS=false",
        ]
    )


@app.route("/")
def index():
    return """
    <h1>Projeto Integrado</h1>
    <ul>
        <li><a href="/hello">API Flask</a></li>
        <li><a href="http://localhost:8501" target="_blank">Abrir Streamlit</a></li>
    </ul>
    """


@app.route("/hello")
def hello():
    return "Olá do Flask!"


# Conteúdo da interface Streamlit
def streamlit_app():
    import streamlit as st

    st.title("App Streamlit")
    st.write("Este é o app Streamlit rodando junto com o Flask!")


# Roda Flask
def run_flask():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    # Executa Streamlit em thread separada
    t = threading.Thread(target=run_streamlit)
    t.start()

    # Inicia Flask
    run_flask()
