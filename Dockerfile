FROM  ubuntu:latest
RUN apt-get update && apt-get install -y curl

RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}

RUN apt-get update
RUN pip install --upgrade pip

COPY ./application /application
COPY ./data /data

WORKDIR /application
RUN pip install -r requirements.txt

CMD [ "/bin/bash" ]