# utilsCheckout

### repo synchronize
```bash
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/QuartoDaBagunca/utilsCheckout.git
    git push -f -u origin main
```

#### PASSO 1 - SETAR CREDENCIAIS
- Exporte as credenciais da AWS no bash profile ou usando os comandos abaixo:

###### Exportando 
```bash
export AWS_ACCESS_KEY_ID='<<id_de_sua_secret>>'
export AWS_SECRET_ACCESS_KEY='<<chave_de_sua_secret>>'
```

> Recomendo setar as credenciais no bash pois usando o comando acima será necessário faze-lo sempre um novo terminal for iniciado

#### PASSO 2 - CRIANDO IMAGEM DOCKER
- cria a imagem docker com base no docker que está na raiz do projeto
```bash
docker build -t sparkenv .
```

#### PASSO 3 - CRIANDO E USANDO O CONTAINER
- Segue abaixo comando pra criação do container efêmeros (excluído logo que se termine a utilização dele) passando pra dentro dele as credenciais AWS
*O comando, além de criar o container, atrela o terminal permitindo a interação com o mesmo pelo console, dessa forma, testar a execução da aplicação*

###### Executando o container
```bash
docker run -it \
        --env AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
        --env AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
        -v $(pwd)/main.py:/opt/spark/python/main.py \
        --rm sparkenv /bin/bash
```
> Na execução do container temos uma linha que mapeia o arquivo main.py como volume dentro do container, isso quer dizer que qualquer alteração feita no arquivo será refletida e poderá ser testada com a execução dentro do container como se estivessemos executando na maquina local. Essa linha `$(pwd)/main.py:/opt/spark/python/main.py` pode ser replicada pra qualquer outro script que se deseje testar dentro do container
