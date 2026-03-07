from flask import Flask, render_template, request, jsonify, send_from_directory
import psycopg2
import os

app = Flask(__name__)

# COLOQUE A SUA URL EXTERNA DO RENDER AQUI DENTRO DAS ASPAS
DATABASE_URL = 'postgresql://db_caneta_segura_user:F6C12MHGkBcLfKC6TbrxvwNLVyyyvYqe@dpg-d6m8ognkijhs73e7ih2g-a.oregon-postgres.render.com/db_caneta_segura'

def get_db_connection():
    # Agora conectamos ao PostgreSQL na nuvem em vez do SQL Server
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory(os.getcwd(), 'sw.js')

@app.route('/api/verificar', methods=['GET'])
def verificar():
    medicamento = request.args.get('medicamento')
    lote = request.args.get('lote')

    if not medicamento or not lote:
        return jsonify({'erro': 'Medicamento e lote são obrigatórios'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # O ILIKE ignora maiúsculas/minúsculas.
        # Adicionamos o '%' ao medicamento para que se o telemóvel enviar "Ozempic", 
        # ele encontre "Ozempic 1mg" no banco de dados.
        query = """
            SELECT motivo_alerta, resolucao_anvisa 
            FROM lotes_suspeitos 
            WHERE medicamento ILIKE %s AND lote = %s
        """
        
        cursor.execute(query, (f"{medicamento}%", lote))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:
            return jsonify({
                'status': 'PERIGO',
                'mensagem': f'ALERTA: Lote {lote} suspeito!',
                'motivo': resultado[0],
                'resolucao': resultado[1]
            })
        else:
            return jsonify({
                'status': 'SEGURO',
                'mensagem': f'Lote {lote} não consta na lista de falsificações.',
                'motivo': 'Lote não reportado pela ANVISA até o momento.',
                'resolucao': 'Verifique sempre a integridade da embalagem.'
            })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    # No Render, a porta padrão costuma ser definida por uma variável de ambiente,
    # mas para testes locais mantemos a 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)