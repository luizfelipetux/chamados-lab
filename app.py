import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.56.200"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "chamados_app"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "chamados"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

@app.get("/")
def index():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, titulo, solicitante, status, criado_em
                FROM chamados
                ORDER BY criado_em DESC
            """)
            chamados = cur.fetchall()
    return render_template("index.html", chamados=chamados)

@app.route("/chamados/novo", methods=["GET", "POST"])
def novo_chamado():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        solicitante = request.form.get("solicitante", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not titulo or not solicitante or not descricao:
            return render_template(
                "novo.html",
                erro="Preencha todos os campos.",
                dados=request.form
            ), 400

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO chamados (titulo, solicitante, descricao)
                    VALUES (%s, %s, %s)
                """, (titulo, solicitante, descricao))

        return redirect(url_for("index"))

    return render_template("novo.html", erro=None, dados={})

@app.get("/chamados/<int:chamado_id>")
def detalhe(chamado_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, titulo, solicitante, descricao, status,
                       criado_em, atualizado_em
                FROM chamados
                WHERE id = %s
            """, (chamado_id,))
            chamado = cur.fetchone()

    if chamado is None:
        abort(404)

    return render_template("detalhe.html", chamado=chamado)

@app.post("/chamados/<int:chamado_id>/status")
def atualizar_status(chamado_id):
    novo_status = request.form.get("status", "")
    permitidos = {"Aberto", "Em andamento", "Concluído"}

    if novo_status not in permitidos:
        abort(400)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE chamados
                SET status = %s
                WHERE id = %s
            """, (novo_status, chamado_id))

            if cur.rowcount == 0:
                abort(404)

    return redirect(url_for("detalhe", chamado_id=chamado_id))

@app.get("/health")
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 AS ok")
                result = cur.fetchone()
        return {"status": "ok", "database": result["ok"] == 1}, 200
    except Exception as exc:
        return {"status": "erro", "database": False, "detail": str(exc)}, 503

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    app.run(host=host, port=port, debug=False)
