# IHERO API

API REST feita com FastAPI para solucionar problemas de alocacoes dos herois de 3050.

## Instalação

Após o download do repositório do projeto, existem duas formas de inicializá-lo. Siga um dos guias a seguir para iniciar o servidor do projeto.

### Container do docker

To do

### Localmente

Para executar o projeto localmente é necessário ter uma versão do python 3 instalado. (recomendas-se alguma versão do python 3.9)

*Com o python instalado recomenda-se a criar uma virtualenv para instalação das dependências do projeto. Você pode seguir os passos da própria [documentação do python](https://docs.python.org/pt-br/3/library/venv.html "Documentacao Python") para criar e ativar o seu próprio ambiente virtual*

Com o seu ambiente python configurado, rode o seguinte comando dentro do diretório do projeto para a instalação das dependências.

```sh
pip install -r _requirements.txt
```

Após a execução desse comando podemos configurar a conexão com o banco de dados.

```
DATABASE_URL="postgresql://[user]:[password]@[endereco]:[port]/[NomeDataBase]"
```

*Substitua o que se encontra entre [ ] de acordo com a configuração do seu banco de dados postgres local*

Obs.: Caso não haja nenhum banco de dados instalado no seu ambiente você pode rodar o projeto sem configurar o endereço da database. Com isso será utilizado o banco de dados sqlite para permanência dos dados.

Com o banco de dados configurado deve-se rodar as migrações do projeto. (Isso irá criar as tabelas necessárias para a execução do projeto no banco de dados)
Basta rodar o seguinte comando para executar as migrações :

```sh
alembic upgrade head
```

Agora o projeto está pronto para a execução, rode o seguinte comando para levantar o servidor do projeto

```sh
uvicorn main:app 
```

Ao rodar esse comando espere até o terminal mostrar uma linha com um link. Esse link e o endereço do projeto, para ver quais os serviços estão disponíveis no projeto basta acessar ```[link]/docs/``` que uma lista com a descrição deles será mostrada.

## Endpoints

O projeto disponibiliza 12 endpoints. Toda a documentação deles pode ser encontrada acessando o servidor do projeto no endpoint ```/docs/```

## Estrutura relacional

Analisando as regras disponibilizadas para a construcao do projeto foi modelado duas tabelas para persistencia dos dados
Tabela ```Hero``` - As colunas eram:
1. name
2. rank
3. lat
4. long
5. available

O 5 atributo nao e o unico atributo utilizado para dizer se um heroi esta disponivel para atender uma ocorrencia.
Como eu entendi esse projeto como um "uber" de herois, queria que o heroi pudesse mudar o proprio estado de disponibilidade

Tabela ```Occurrence``` - As colunas eram:
1. monster_name
2. rank
3. lat
4. long
5. create
6. start
7. finish

Essas tabelas estavam ligadas por um relacionamento N:N com uma tabela auxiliar chamada ```Attendance```

A tabela occurrence possui 3 dados do tipo ```datetime```, utilizados para as seguintes finalidades
1. create - Salva a data e hora de quando a Occurrence foi criada, utilizada para dar prioridade na hora de alocar herois
2. start - Salva quando um heroi comeca a atender a ocorrencia
3. finish - Salva quando o heroi termina de atender a ocorrencia. Entre o periodo de tempo dos atributos ```start``` e ```finish``` o heroi nao esta disponivel para atender outra ocorrencia 

Alem disso ao iniciar o projeto duas threads sao criadas.

Uma delas e para a leitura do socket disponibilizado na descricao do teste. Ao receber um evento do tipo ```occurrence``` uma Occurrence com os dados disponibilizados pelo socket eh criada e salva no banco de dados conectado.

A outra thread eh utilizada para alocacao dos herois. Para cada ocorrencia eh feito uma pesquisa no banco de dados que retorna os herois disponiveis para solucionar o problema. Com essa lista de herois eh feito um ```sort``` para que os primeiros da lista sejam sempre os mais proximos da ocorrencia. Com a lista ja ordenada comecamos a percorre-la, para cada heroi eh verificado se sua forca mais a dos herois anteriores eh suficiente para combater a ocorrencia, caso sua forca sozinha seja suficiente para combater a ocorrencia o heroi eh alocado, em outro caso, se a forca dele mais a de herois anteriores da lista seja suficiente, os herois ja percorridos sao alocados para a missao.

A criação das tabelas é feita com migrations criadas automaticamentes pela biblioteca [Alembic](https://alembic.sqlalchemy.org/en/latest/ "Documentacao Alembic"), junto com o [SQLAlchemy](https://www.sqlalchemy.org/ "Documentacao SQLAlchemy"), a partir dos modelos escritos no projeto no módulo ```users```