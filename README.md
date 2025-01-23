# EquipTrack - Sistema de Gerenciamento de EPIs para CIPAs

## Descrição

EquipTrack é um software web desenvolvido para auxiliar as CIPAs (Comissões Internas de Prevenção de Acidentes) na gestão eficiente dos Equipamentos de Proteção Individual (EPIs) dos colaboradores. O sistema oferece um conjunto completo de funcionalidades para o controle de estoque, alocação, descarte e rastreamento de EPIs, além de facilitar a administração dos funcionários e dos membros da CIPA (cipeiros).

**O que é CIPA?**

A CIPA (Comissão Interna de Prevenção de Acidentes) é uma comissão obrigatória em empresas que visa promover a saúde e segurança no trabalho, prevenindo acidentes e doenças ocupacionais.

O EquipTrack foi desenvolvido utilizando Python Flask, HTML, CSS, Bootstrap e MySQL, com o objetivo de fornecer uma solução completa e intuitiva para a gestão de EPIs.

## Funcionalidades Principais

*   **Gestão de Funcionários (CRUD):**
    *   Criação, leitura, atualização e exclusão de registros de funcionários.
*   **Gestão de EPIs (CRUD):**
    *   Cadastro, edição, visualização e exclusão de EPIs.
*   **Gestão de Cipeiros:**
    *   Cadastro e gerenciamento dos membros da CIPA (administradores do sistema).
*   **Descarte de EPIs:**
    *   Registro e controle dos descartes de EPIs, mantendo um histórico de utilização.
*   **Controle de Estoque por Setor:**
    *   Gerenciamento do estoque de EPIs por setor da empresa, permitindo um controle preciso da disponibilidade.
*   **Alocação de EPIs:**
    *   Alocação de EPIs para funcionários específicos, registrando a data de entrega e os equipamentos utilizados.
*   **Consulta de EPIs Alocados:**
    *   Visualização dos EPIs alocados a um determinado funcionário, facilitando o controle e a reposição.
*   **Segurança:**
    *   Criptografia de senhas armazenadas no banco de dados para garantir a segurança das informações.

## Tecnologias Utilizadas

*   **Python:** Linguagem de programação utilizada no back-end.
*   **Flask:** Framework web em Python para o desenvolvimento do lado do servidor.
*   **Blueprints (Flask):** Padrão de projeto para organização modular da aplicação Flask.
*   **HTML, CSS e Bootstrap:** Linguagens de marcação e framework CSS para a construção da interface de usuário.
*   **MySQL:** Sistema de gerenciamento de banco de dados relacional para armazenar os dados do sistema.
*   **Git:** Sistema de controle de versão para o gerenciamento do código-fonte.

## Instruções de Configuração

Para configurar e executar o EquipTrack em seu ambiente local, siga as instruções abaixo:

1.  **Clone o Repositório:**

    ```bash
    git clone <https://github.com/otavioDev07/Grupo7_EquipTrack.git>
    cd EquipTrack
    ```

2.  **Crie o Ambiente Virtual (Recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate  # No Windows
    ```

3.  **Instale as Dependências:**

    ```bash
    pip install Flask
    pip install mysql-connector-python  # Necessário para conectar ao MySQL
    ```

4.  **Instale e Configure o MySQL:**

    *   Certifique-se de ter o MySQL instalado em sua máquina. Se não, siga as instruções de instalação para o seu sistema operacional.
    *   Crie um banco de dados chamado `equipTrack` (ou outro nome de sua preferência) no MySQL.
    *   Configure as credenciais de acesso ao banco de dados no arquivo de configuração do Flask (geralmente `config.py` ou similar).

5.  **Importe o Esquema do Banco de Dados:**

    *   Utilize o arquivo `database/esquema.sql` para criar as tabelas e a estrutura do banco de dados. Você pode importar este arquivo usando a linha de comando do MySQL ou uma ferramenta como o phpMyAdmin.

    ```bash
    mysql -u <seu_usuario> -p equipTrack < database/esquema.sql
    ```

6.  **Execute o Aplicativo:**

    ```bash
    python app.py
    ```

7.  **Acesse o Aplicativo no Navegador:**

    *   Abra seu navegador e acesse `http://localhost:5000` para visualizar o EquipTrack.

## Estrutura do Projeto
- `app.py`: O código principal do aplicativo Flask.
- `templates/`: Diretório contendo os modelos HTML.
- `static/`: Diretório contendo arquivos estáticos, como CSS, imagens e arquivos JavaScript.
- `database/`: Diretório contendo os arquivos referentes ao banco de dados.
- `esquema.sql`: Arquivo com o esquema do banco de dados MySQL.
- `home/`: Diretório contendo os arquivos referentes à página principal.
- `admin/`: Diretório contendo os arquivos referentes as funções de administrador (CRUD).
- `alocar/`: Diretório contendo os arquivos referentes à alocação de EPIs.
- `estoqueEPI/`: Diretório contendo os arquivos referentes ao gerenciamento de estoque de EPIs.
- `login/`: Diretório contendo os arquivos referentes à autenticação e login de usuários.
- `model/`: Diretório contendo as classes de modelo (ex: Funcionario, EPI).
- `session/`: Diretório contendo os arquivos referentes ao controle de sessão.
- `telaadm/`: Diretório contendo os arquivos referentes à tela de administração geral.

## Contribuições

Contribuições são sempre bem-vindas! Sinta-se à vontade para fazer um fork do repositório e enviar um Pull Request com suas melhorias.

## Licença

Este projeto é fornecido sob a Licença [MIT](LICENSE).

## Contato
- Rafael Ribas: Instrutor de Programação Web Front-End.
- João Paulo: Instrutor de Programação Web Back-End.

- [Otávio Neto: Back-end Developer e Tech Lead](www.linkedin.com/in/otávio-neto12)
- Pedro Schidmit: Front-end Developer
- Samantha Fernandes: Scrum Master
- [Sara Barros: Product Owner](https://www.linkedin.com/in/sararesendd/) 
