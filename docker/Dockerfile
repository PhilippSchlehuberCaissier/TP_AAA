FROM debian:sid

# We have a lot of timeout issues when fetching packages from
# http://httpredir.debian.org/debian
RUN RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive \
    apt-get update
RUN RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive \
    apt-get upgrade -y
RUN RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive \
    apt-get install -y wget gnupg apt-utils

RUN wget -O /etc/apt/trusted.gpg.d/lrde.gpg https://www.lrde.epita.fr/repo/debian.gpg

RUN RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive \
    apt-get update

RUN echo 'deb http://debian.mirrors.ovh.net/debian sid main' > /etc/apt/sources.list && \
    echo 'deb [trusted=true] http://www.lrde.epita.fr/repo/debian/ unstable/' >> /etc/apt/sources.list && \
    apt-get update && \
    RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
      spot python3-spot divine-ltsmin spins spin \
      python3-pip python3-dev python3-setuptools python3-matplotlib python3-numpy python3-pandas \
      build-essential git graphviz fonts-lato \
      sudo unzip imagemagick ghostscript libbdd0c2 libspot-dev libbddx-dev \
      libbdd-dev man-db less bison \
      openjdk-11-jre-headless && \
    apt-get clean

RUN RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends npm
RUN rm -rf /var/lib/apt/lists/* && \
    set -x && \
    pip3 install --no-cache-dir jupyter ipywidgets jupyterlab && \
    jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
    rm -rf ~/.cache

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN mkdir -p ${HOME} && \
    groupadd -g ${NB_UID} -r ${NB_USER} && \
    useradd -u ${NB_UID} -r -s /bin/bash -g ${NB_USER} ${NB_USER} && \
    chown ${NB_USER}:${NB_USER} ${HOME}

COPY install.sh /tmp/install.sh
COPY custom.css ${HOME}/.jupyter/custom/custom.css
COPY custom.js ${HOME}/.jupyter/custom/custom.js

# 2017-01-19: Today's version of Jupyter takes custom.js from
# ~/.jupyter, and custom.css from ~/.ipython.

RUN ln -s /usr/share/fonts/truetype/lato/Lato-Regular.ttf ${HOME}/.jupyter/custom/Lato-Regular.ttf \
  && mkdir -p ${HOME}/.ipython \
  && ln -s ${HOME}/.jupyter/custom ${HOME}/.ipython/custom \
  && cd /tmp && ./install.sh && rm -f install.sh

RUN python3 -m pip install --no-cache-dir notebook jupyterlab
RUN pip install --no-cache-dir jupyterhub

COPY ./README* ${HOME}/README
COPY ./exercices/* ${HOME}/
COPY ./AAA_utils/__init__.py ${HOME}/AAA_utils/__init__.py
COPY ./AAA_utils/lift_demo.py ${HOME}/AAA_utils/lift_demo.py
USER root
RUN chown -R ${NB_UID} ${HOME}

WORKDIR ${HOME}
USER ${NB_USER}

USER ${NB_USER}

RUN echo "Extensions"
RUN jupyter nbextension enable --py widgetsnbextension
RUN echo "DONE!"

