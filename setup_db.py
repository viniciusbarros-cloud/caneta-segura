import psycopg2

# COLOQUE A SUA URL EXTERNA DO RENDER AQUI DENTRO DAS ASPAS
DATABASE_URL = 'postgresql://db_caneta_segura_user:F6C12MHGkBcLfKC6TbrxvwNLVyyyvYqe@dpg-d6m8ognkijhs73e7ih2g-a.oregon-postgres.render.com/db_caneta_segura'

def configurar_banco_completo():
    try:
        print("⏳ Conectando à nuvem do Render...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        print("🧹 Limpando tabelas antigas (se existirem)...")
        # Remove a tabela do nosso teste anterior
        cursor.execute("DROP TABLE IF EXISTS lotes_falsos;")
        
        # Remove as tabelas atuais caso precise rodar o script de novo no futuro
        cursor.execute("DROP TABLE IF EXISTS lotes_suspeitos;")
        cursor.execute("DROP TABLE IF EXISTS medicamentos_aprovados;")

        print("🔨 Criando tabela: medicamentos_aprovados...")
        cursor.execute("""
            CREATE TABLE medicamentos_aprovados (
                id SERIAL PRIMARY KEY,
                nome_comercial VARCHAR(100),
                principio_ativo VARCHAR(100),
                registro_anvisa VARCHAR(50),
                empresa VARCHAR(100)
            );
        """)

        print("🔨 Criando tabela: lotes_suspeitos...")
        cursor.execute("""
            CREATE TABLE lotes_suspeitos (
                id SERIAL PRIMARY KEY,
                medicamento VARCHAR(100),
                lote VARCHAR(50),
                motivo_alerta TEXT,
                resolucao_anvisa TEXT
            );
        """)

        print("💊 Inserindo dados dos Medicamentos Aprovados...")
        cursor.execute("""
            INSERT INTO medicamentos_aprovados (nome_comercial, principio_ativo, registro_anvisa, empresa) VALUES
            ('OZEMPIC', 'SEMAGLUTIDA', '117660036', 'NOVO NORDISK'),
            ('RYBELSUS', 'SEMAGLUTIDA', '117660037', 'NOVO NORDISK'),
            ('WEGOVY', 'SEMAGLUTIDA', '117660039', 'NOVO NORDISK'),
            ('MOUNJARO', 'TIRZEPATIDA', '112600202', 'ELI LILLY');
        """)

        print("🚨 Inserindo dados dos Lotes Suspeitos/Falsos...")
        cursor.execute("""
            INSERT INTO lotes_suspeitos (medicamento, lote, motivo_alerta, resolucao_anvisa) VALUES
            ('Ozempic 1mg', 'LP6F832', 'Falsificação. Caneta azul escura (insulina) em vez da caneta original.', 'RE 3945/2023'),
            ('Ozempic 1mg', 'MP5C960', 'Falsificação. Embalagem em espanhol não autorizada no Brasil.', 'RE 2011/2023'),
            ('Ozempic 1mg', 'MP5A064', 'Lote irregular identificado pela fabricante.', 'Alerta Jan/2024'),
            ('Rybelsus', 'M088499', 'Falsificação. Embalagens alteradas de forma fraudulenta.', 'Alerta Jun/2025');
        """)

        # Salva as mudanças e fecha
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ SUCESSO! A sua base de dados agora é um espelho perfeito do seu sistema local!")

    except Exception as e:
        print(f"❌ Erro ao configurar o banco: {e}")

if __name__ == '__main__':
    configurar_banco_completo()