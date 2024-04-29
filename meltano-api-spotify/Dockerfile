ARG MELTANO_IMAGE=meltano/meltano:v3.1-python3.10
FROM $MELTANO_IMAGE

# Crie um usuário não-root, crie a pasta /project e defina a propriedade
RUN useradd -m meltano_user && \
    mkdir -p /project && \
    chown -R meltano_user:meltano_user /project

# Alterne para o usuário não-root
USER meltano_user

WORKDIR /project

# Instale o bash
USER root
RUN apt-get update

RUN apt-get install -y bash

RUN apt-get clean

RUN rm -rf /var/lib/apt/lists/*
USER meltano_user

# Instale quaisquer requisitos adicionais
# COPY --chown=meltano_user:meltano_user requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Copie o diretório do projeto Meltano com a propriedade apropriada
COPY --chown=meltano_user:meltano_user . .
RUN meltano install

# Permitir alterações nos arquivos do projeto containerizados
ENV MELTANO_PROJECT_READONLY 0

ENTRYPOINT ["meltano"]
