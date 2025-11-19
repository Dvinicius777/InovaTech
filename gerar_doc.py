import os

# Lista exata dos arquivos do teu projeto InovaTech
arquivos = [
    'app.py',
    'cerebro_ia.py',
    'populate_db.py',
    'analise.c',
    'static/style.css',
    'static/script.js',
    'templates/index.html',
    'templates/aluno.html',
    'templates/professor.html'
]

nome_saida = "CODIGO_COMPLETO_PIM.txt"

def ler_arquivo(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"[ARQUIVO NÃO ENCONTRADO: {caminho}]"
    except Exception as e:
        return f"[ERRO AO LER {caminho}: {str(e)}]"

print(f"🚀 Iniciando a geração da documentação em: {nome_saida}...")

with open(nome_saida, 'w', encoding='utf-8') as saida:
    saida.write("="*60 + "\n")
    saida.write("DOCUMENTAÇÃO TÉCNICA - SISTEMA INOVATECH\n")
    saida.write("CÓDIGO FONTE COMPLETO\n")
    saida.write("="*60 + "\n\n")

    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"📄 Adicionando: {arquivo}...")
            saida.write(f"{'='*50}\n")
            saida.write(f"ARQUIVO: {arquivo}\n")
            saida.write(f"{'='*50}\n")
            
            conteudo = ler_arquivo(arquivo)
            saida.write(conteudo)
            saida.write("\n\n" + "-"*50 + "\n\n")
        else:
            print(f"⚠️ Aviso: O arquivo '{arquivo}' não foi encontrado na pasta.")

print(f"\n✅ SUCESSO! O arquivo '{nome_saida}' foi criado.")
print("👉 Podes enviar este arquivo TXT diretamente para quem vai fazer o relatório.")