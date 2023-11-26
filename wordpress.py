import os
print(os.environ['PATH'])

import shutil
import subprocess
import mysql.connector

def criar_ambiente_wordpress():
    nome_projeto = input("Digite o nome do projeto: ")
    caminho_htdocs = 'C:/xampp/htdocs'
    caminho_projeto = os.path.join(caminho_htdocs, nome_projeto)

    os.makedirs(caminho_projeto, exist_ok=True)

    conteudo_composer = """
    {
      "require": {
        "johnpbloch/wordpress": "*"
      }
    }
    """

    with open(os.path.join(caminho_projeto, 'composer.json'), 'w') as file:
        file.write(conteudo_composer)

    # Atualizar a configuração do Composer para permitir o plugin
    subprocess.run("composer config allow-plugins.johnpbloch/wordpress-core-installer true", cwd=caminho_projeto, shell=True)

    # Executar o Composer com a opção --no-interaction
    subprocess.run("composer install -n", cwd=caminho_projeto, shell=True)

    # Mover os arquivos da pasta 'wordpress' para a pasta raiz do projeto
    caminho_wordpress = os.path.join(caminho_projeto, 'wordpress')
    for item in os.listdir(caminho_wordpress):
        s = os.path.join(caminho_wordpress, item)
        d = os.path.join(caminho_projeto, item)
        if os.path.isdir(s):
            shutil.move(s, d)
        else:
            shutil.copy2(s, d)

    # Perguntar sobre clonar um repositório Git
    clonar_git = input("Deseja clonar um repositório Git na pasta themes? (s/n): ").lower()
    url_repositorio = ""
    if clonar_git == 's':
        url_repositorio = input("Digite o URL do repositório Git: ")

    # Caminho para a pasta 'themes'
    caminho_themes = os.path.join(caminho_projeto, 'wp-content', 'themes')

    # Verificar se a pasta 'themes' existe e removê-la
    if os.path.exists(caminho_themes):
        for item in os.listdir(caminho_themes):
            item_path = os.path.join(caminho_themes, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

    # Clonar repositório Git, se necessário
    if url_repositorio:
        subprocess.run(["git", "clone", url_repositorio], cwd=caminho_themes)

    # Limpar: Deletar pasta 'wordpress' e outros arquivos/diretórios desnecessários
    shutil.rmtree(caminho_wordpress)
    # Adicione aqui comandos para deletar outras pastas e arquivos, se necessário

    # Caminho para wp-config-sample.php
    wp_config_sample = os.path.join(caminho_projeto, 'wp-config-sample.php')
    wp_config = os.path.join(caminho_projeto, 'wp-config.php')

    # Ler o conteúdo de wp-config-sample.php e substituir as credenciais do banco de dados
    with open(wp_config_sample, 'r') as file:
        content = file.read()
        content = content.replace('database_name_here', nome_projeto)
        content = content.replace('username_here', 'root')
        content = content.replace('password_here', '')

    # Escrever as alterações no novo arquivo wp-config.php
    with open(wp_config, 'w') as file:
        file.write(content)

    # Remover arquivos e pastas do Composer
    os.remove(os.path.join(caminho_projeto, 'composer.json'))
    os.remove(os.path.join(caminho_projeto, 'composer.lock'))
    shutil.rmtree(os.path.join(caminho_projeto, 'vendor'))

    # criar banco de dados
    # conexao = mysql.connector.connect(
    #     host='localhost',
    #     user='root',
    #     password=''
    # )
    # cursor = conexao.cursor()
    # cursor.execute(f"CREATE DATABASE `{nome_projeto}`")
    # cursor.close()
    # conexao.close()

criar_ambiente_wordpress()
