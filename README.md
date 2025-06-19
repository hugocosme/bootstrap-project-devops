# 🔧 GitLab CI/CD Generator
Este é um Gerador Interativo de Pipeline GitLab CI/CD construído com Streamlit e persistência de dados em SQLite. Ele permite que desenvolvedores e equipes DevOps configurem rapidamente arquivos .gitlab-ci.yml complexos através de uma interface de usuário intuitiva, salvando e reutilizando as configurações dos projetos.

<img title="example" alt="Alt text" src="/images/example.jpg">

# ✨ Recursos
**Configuração de Projetos**: Defina o nome, descrição, linguagem de programação, versão, frameworks e dependências do seu projeto.
**Seleção de Tecnologias**: Suporte para Java (.NET), C# e Node.js com opções de frameworks e versões específicas.
**Integração com Banco de Dados**: Escolha o tipo de banco de dados para o seu projeto.
**Roles Ansible**: Selecione papéis comuns do Ansible para automação de infraestrutura.
**Monitoramento**: Opção para incluir Grafana e Prometheus na configuração.
**Configuração de Pipeline**: Selecione os estágios do pipeline CI/CD (Build, Test, SAST, DAST, Deploy) e o ambiente de destino.
**Visualização e Download**: Pré-visualize o .gitlab-ci.yml gerado e faça o download diretamente da aplicação.
**Persistência de Dados**: Salve as configurações dos seus projetos em um banco de dados SQLite para acesso e reutilização futuros.
**Projetos Salvos**: Visualize detalhes dos projetos salvos e o respectivo .gitlab-ci.yml.

# 🚀 Como Usar

**Pré-requisitos**
Certifique-se de ter o Python 3.x instalado em sua máquina.

Instalação:

1- Clone o repositório (se este código estiver em um repositório Git):
```git clone git@github.com:hugocosme/bootstrap-project-devops.git```

2- Entre no diretorio do projeto:
```cd bootstrap-project-devops```

3- Crie um ambiente virtual (recomendado):
```python -m venv .venv```

4- Ative seu ambiente virtual
```source venv/bin/activate```

5- Instale as dependências
```pip install streamlit sqlite3 json```

(Nota: sqlite3 e json geralmente já vêm com o Python padrão, mas streamlit precisa ser instalado.)

Execução
6- Após a instalação, execute o aplicativo Streamlit:

```
streamlit run devops_bootstrap.py
```
O aplicativo será aberto automaticamente no seu navegador padrão, geralmente em http://localhost:8501.


# 📁 Estrutura do Projeto
**devops_bootstrap.py**: O arquivo principal que contém todo o código do aplicativo Streamlit e as funções de manipulação do banco de dados.
**projects.db**: O banco de dados SQLite que será criado automaticamente na primeira execução para armazenar as configurações dos seus projetos.
# 🤝 Contribuições
Sinta-se à vontade para abrir issues ou pull requests se você tiver sugestões de melhorias, detecção de bugs ou novas funcionalidades!