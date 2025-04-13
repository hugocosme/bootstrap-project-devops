import streamlit as st
import yaml
import datetime
import os

def save_yaml(data, filename="devops_config.yaml"):
    """Salva os dados do formulário em um arquivo YAML."""
    with open(filename, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)
    return filename

def validate_form_data(data):
    """Valida se todos os campos obrigatórios foram preenchidos."""
    # Verificando informações do projeto
    if not data.get('project', {}).get('name'):
        return False, "Nome do projeto obrigatório"
    
    # Verificando tecnologias
    tech = data.get('technology', {})
    if not tech.get('language'):
        return False, "Selecione uma linguagem de programação"
    if not tech.get('frameworks'):
        return False, "Selecione pelo menos um framework"
    if not tech.get('project_type'):
        return False, "Selecione pelo menos um tipo de projeto"
    if not tech.get('databases'):
        return False, "Selecione pelo menos um banco de dados"
    
    # Verificando dependências
    deps = data.get('dependencies', {})
    if not deps.get('manager'):
        return False, "Selecione um gerenciador de dependências"
    if not deps.get('infrastructure'):
        return False, "Selecione pelo menos uma ferramenta de infraestrutura"
    if not deps.get('monitoring'):
        return False, "Selecione pelo menos uma ferramenta de monitoramento"
    
    # Verificando pipeline
    pipe = data.get('pipeline', {})
    if not pipe.get('stages'):
        return False, "Selecione pelo menos um estágio da pipeline"
    if not pipe.get('testing'):
        return False, "Selecione pelo menos um framework de teste"
    if not pipe.get('code_quality'):
        return False, "Selecione pelo menos uma ferramenta de qualidade de código"
    if not pipe.get('security'):
        return False, "Selecione pelo menos uma ferramenta de análise de segurança"
    
    return True, "Todos os campos foram preenchidos corretamente"

def main():
    st.set_page_config(page_title="DevOps Bootstrap", layout="wide")

    st.title("🚀 DevOps Bootstrap Generator")
    st.write("Configure seu projeto e gere automaticamente um arquivo YAML de configuração para GitLab CI/CD")

    # Inicializando o estado da sessão para armazenar os valores do formulário
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    if 'validation_error' not in st.session_state:
        st.session_state.validation_error = ""
    
    if 'yaml_content' not in st.session_state:
        st.session_state.yaml_content = ""
        
    if 'gitlab_ci_content' not in st.session_state:
        st.session_state.gitlab_ci_content = ""

    # Criando abas para organizar o formulário
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Informações do Projeto", "Tecnologias", "Dependências", "Pipeline", "Resultado"])

    with tab1:
        st.header("Informações do Projeto")
        
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Nome do Projeto", placeholder="meu-projeto-incrivel")
            project_description = st.text_area("Descrição", placeholder="Descreva seu projeto brevemente...")
        
        with col2:
            owner = st.text_input("Responsável", placeholder="Seu nome")
            team = st.text_input("Time", placeholder="Nome do time")
        
        environment = st.selectbox("Ambiente Inicial", 
                                  ["Desenvolvimento", "Homologação", "Produção"], 
                                  index=0)

    with tab2:
        st.header("Tecnologias")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Linguagem")
            language = st.selectbox("Linguagem de Programação", 
                                   ["", "Python", "JavaScript", "TypeScript", "Java", "Go", "C#", "Ruby", "PHP"],
                                   index=0)
            
            # Variáveis para armazenar versões específicas da linguagem
            python_version = None
            node_version = None
            java_version = None
            
            # Opções condicionais baseadas na linguagem
            framework = []
            if language == "Python":
                python_version = st.selectbox("Versão do Python", ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"])
                framework = st.multiselect("Frameworks", 
                                         ["Django", "FastAPI", "Flask", "Streamlit", "Pandas", "NumPy", "TensorFlow", "PyTorch"])
            
            elif language in ["JavaScript", "TypeScript"]:
                node_version = st.selectbox("Versão do Node.js", ["14", "16", "18", "20"])
                framework = st.multiselect("Frameworks", 
                                         ["React", "Angular", "Vue", "Next.js", "Express", "NestJS", "Electron"])
            
            elif language == "Java":
                java_version = st.selectbox("Versão do Java", ["8", "11", "17", "21"])
                framework = st.multiselect("Frameworks", 
                                         ["Spring Boot", "Quarkus", "Micronaut", "Jakarta EE"])
            
            elif language:  # Se uma linguagem foi selecionada, mas não é uma das com opções específicas
                framework = st.multiselect("Frameworks", ["Especifique os frameworks relevantes"])
        
        with col2:
            st.subheader("Backend/Frontend")
            project_type = st.multiselect("Tipo de Projeto", 
                                        ["Backend", "Frontend", "Full Stack", "Mobile", "Desktop", "CLI"])
            
            st.subheader("Banco de Dados")
            databases = st.multiselect("Bancos de Dados", 
                                      ["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Oracle", "SQL Server", "DynamoDB"])

    with tab3:
        st.header("Dependências")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gerenciamento de Dependências")
            dependency_manager = ""
            if language == "Python":
                dependency_manager = st.selectbox("Gerenciador de Dependências", 
                                               ["", "pip", "Poetry", "Pipenv", "Conda"],
                                               index=0)
            elif language in ["JavaScript", "TypeScript"]:
                dependency_manager = st.selectbox("Gerenciador de Dependências", 
                                               ["", "npm", "yarn", "pnpm"],
                                               index=0)
            elif language == "Java":
                dependency_manager = st.selectbox("Gerenciador de Dependências", 
                                               ["", "Maven", "Gradle"],
                                               index=0)
            elif language:  # Se uma linguagem foi selecionada
                dependency_manager = st.text_input("Gerenciador de Dependências")
        
        with col2:
            st.subheader("Infraestrutura")
            infra_tools = st.multiselect("Ferramentas de Infraestrutura", 
                                       ["Docker", "Kubernetes", "Terraform", "Ansible", "AWS", "GCP", "Azure"])
            
            st.subheader("Monitoramento")
            monitoring_tools = st.multiselect("Ferramentas de Monitoramento", 
                                            ["Prometheus", "Grafana", "ELK Stack", "Datadog", "New Relic", "Netdata"])

    with tab4:
        st.header("Configuração da Pipeline")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Etapas da Pipeline")
            pipeline_stages = st.multiselect("Estágios", 
                                          ["build", "test", "lint", "security-scan", "deploy-dev", "deploy-staging", "deploy-prod"])
            
            test_frameworks = st.multiselect("Frameworks de Teste", 
                                          ["pytest", "Jest", "JUnit", "Mocha", "Cypress", "Selenium", "Postman"])
        
        with col2:
            st.subheader("Qualidade de Código")
            code_quality = st.multiselect("Ferramentas de Qualidade", 
                                        ["SonarQube", "ESLint", "Pylint", "Black", "Prettier", "Checkstyle"])
            
            security_scan = st.multiselect("Análise de Segurança", 
                                         ["OWASP Dependency Check", "Snyk", "Trivy", "Fortify", "Aqua Security"])

        # Botão para gerar o arquivo YAML
        if st.button("Validar e Gerar Configuração", type="primary"):
            # Construindo a estrutura de dados para o YAML
            config_data = {
                "project": {
                    "name": project_name,
                    "description": project_description,
                    "owner": owner,
                    "team": team,
                    "environment": environment.lower(),
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "technology": {
                    "language": language,
                    "frameworks": framework,
                    "project_type": project_type,
                    "databases": databases
                },
                "dependencies": {
                    "manager": dependency_manager,
                    "infrastructure": infra_tools,
                    "monitoring": monitoring_tools
                },
                "pipeline": {
                    "stages": pipeline_stages,
                    "testing": test_frameworks,
                    "code_quality": code_quality,
                    "security": security_scan
                }
            }
            
            # Adicionando configurações específicas da linguagem
            if language == "Python" and python_version:
                config_data["technology"]["python_version"] = python_version
            elif language in ["JavaScript", "TypeScript"] and node_version:
                config_data["technology"]["node_version"] = node_version
            elif language == "Java" and java_version:
                config_data["technology"]["java_version"] = java_version
            
            # Validar os dados do formulário
            is_valid, validation_message = validate_form_data(config_data)
            
            if is_valid:
                # Gerar o conteúdo YAML
                st.session_state.yaml_content = yaml.dump(config_data, default_flow_style=False, sort_keys=False)
                st.session_state.form_submitted = True
                st.session_state.validation_error = ""
                
                # Gerar também um arquivo .gitlab-ci.yml básico se Docker estiver selecionado
                if "Docker" in infra_tools:
                    gitlab_ci = {
                        "stages": pipeline_stages,
                        "variables": {
                            "PROJECT_NAME": project_name
                        },
                        "build": {
                            "stage": "build",
                            "image": "docker:latest",
                            "services": ["docker:dind"],
                            "script": [
                                "docker build -t $PROJECT_NAME:$CI_COMMIT_SHORT_SHA ."
                            ]
                        }
                    }
                    
                    # Adicionar jobs baseados nas etapas selecionadas
                    if "test" in pipeline_stages:
                        if language == "Python":
                            gitlab_ci["test"] = {
                                "stage": "test",
                                "image": f"python:{python_version}",
                                "script": ["pip install -r requirements.txt", "pytest"]
                            }
                        elif language in ["JavaScript", "TypeScript"]:
                            gitlab_ci["test"] = {
                                "stage": "test",
                                "image": f"node:{node_version}",
                                "script": ["npm install", "npm test"]
                            }
                    
                    if "lint" in pipeline_stages:
                        gitlab_ci["lint"] = {
                            "stage": "lint",
                            "script": ["echo 'Running linters...'"]
                        }
                    
                    if "deploy-dev" in pipeline_stages:
                        gitlab_ci["deploy-dev"] = {
                            "stage": "deploy-dev",
                            "script": ["echo 'Deploying to development...'"],
                            "environment": {"name": "development"}
                        }
                    
                    st.session_state.gitlab_ci_content = yaml.dump(gitlab_ci, default_flow_style=False, sort_keys=False)
                
                # Alertar usuário para ir para a aba de resultado
                st.success("Configuração validada com sucesso! Acesse a aba 'Resultado' para visualizar e baixar os arquivos.")
                
            else:
                st.session_state.validation_error = validation_message
                st.error(f"Erro de validação: {validation_message}")
                st.session_state.form_submitted = False

    with tab5:
        st.header("Resultado")
        
        if st.session_state.validation_error:
            st.error(f"Erro de validação: {st.session_state.validation_error}")
            st.warning("Por favor, corrija os erros nas abas anteriores antes de gerar o arquivo YAML.")
            
        elif st.session_state.form_submitted:
            st.success("Todos os campos foram preenchidos corretamente!")
            
            # Exibir o conteúdo do YAML
            st.subheader("Conteúdo do arquivo YAML:")
            st.code(st.session_state.yaml_content, language="yaml")
            
            # Adicionar opção para download
            st.download_button(
                label="Baixar arquivo YAML",
                data=st.session_state.yaml_content,
                file_name="devops_config.yaml",
                mime="text/yaml"
            )
            
            # Exibir o arquivo gitlab-ci.yml se disponível
            if st.session_state.gitlab_ci_content:
                st.subheader("Arquivo .gitlab-ci.yml básico gerado:")
                st.code(st.session_state.gitlab_ci_content, language="yaml")
                
                st.download_button(
                    label="Baixar arquivo .gitlab-ci.yml",
                    data=st.session_state.gitlab_ci_content,
                    file_name=".gitlab-ci.yml",
                    mime="text/yaml"
                )
        else:
            st.info("Preencha todos os campos obrigatórios nas abas anteriores e clique em 'Validar e Gerar Configuração' para ver o resultado aqui.")

if __name__ == "__main__":
    main()