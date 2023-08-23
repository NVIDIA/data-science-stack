# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

ARG DOCKER_REPO=nvcr.io/nvidia/cuda
ARG CUDA_VERSION=12.1.0
ARG OS_FLAVOR=devel-ubuntu22.04
FROM ${DOCKER_REPO}:${CUDA_VERSION}-${OS_FLAVOR}

ENV PYTHONDONTWRITEBYTECODE=true
ENV PATH=${PATH}:/conda/bin

# Installing base software

ARG TINI_VERSION=v0.18.0

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y --fix-missing \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      apt-utils \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
      curl \
      font-manager \
      graphviz \
      git \
      gcc \
      g++ \
      npm \
      screen \
      tzdata \
      zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* \
    && curl https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini -L -o /usr/bin/tini \
    && chmod +x /usr/bin/tini

# Create Base environment

ARG STACK_VERSION=2.12.0-dev
ARG CONDA_VERSION=23.3.1-0
ARG NOTEBOOKS_VERSION=23.02

ENV CONDA_ROOT=/conda
ENV NOTEBOOKS_DIR=/notebooks

RUN curl https://repo.anaconda.com/miniconda/Miniconda3-py310_${CONDA_VERSION}-Linux-x86_64.sh -o miniconda.sh \
    && bash /miniconda.sh -b -p ${CONDA_ROOT} \
    && rm -f /miniconda.sh \
    && echo "conda ${CONDA_VERSION}" >> /conda/conda-meta/pinned \
    && ${CONDA_ROOT}/bin/conda init bash \
    && echo "#!/bin/bash\n\
      source /conda/bin/activate data-science-stack-${STACK_VERSION}\n\
      jupyter-lab --allow-root --ip=0.0.0.0 --no-browser --NotebookApp.token='' --notebook-dir=${NOTEBOOKS_DIR}" > /run-jupyter \
    && chmod 755 /run-jupyter \
    && mkdir -p ${NOTEBOOKS_DIR} \
    && cd ${NOTEBOOKS_DIR} \
    && git clone --single-branch --depth 1 --branch branch-${NOTEBOOKS_VERSION} \
      https://github.com/rapidsai/notebooks.git \
    && cd notebooks \
    && git submodule update --init --remote \
    && rm -rf .git \
    && rm -rf `find repos/ -maxdepth 2 -mindepth 2 | grep -v notebooks`

# Create Conda environment

COPY environment-pinned.yaml /

RUN ${CONDA_ROOT}/bin/conda env create -n data-science-stack-${STACK_VERSION} \
       -f /environment-pinned.yaml \
    && echo "conda activate data-science-stack-${STACK_VERSION}" >> ${HOME}/.bashrc \
    && bash -c 'source ${CONDA_ROOT}/bin/activate data-science-stack-${STACK_VERSION} ; \
      jupyter labextension install -y --clean \
        @jupyter-widgets/jupyterlab-manager \
        jupyter-threejs \
        dask-labextension' \
    && ${CONDA_ROOT}/bin/conda clean -afy \
    && find ${CONDA_ROOT} -follow -type f -name '*.pyc' -delete \
    && find ${CONDA_ROOT} -follow -type f -name '*.js.map' -delete

COPY data-science-stack.Dockerfile README.md /

# Jupyter notebook
EXPOSE 8888
# Dask Scheduler & Bokeh ports
EXPOSE 8787
EXPOSE 8786

WORKDIR ${NOTEBOOKS_DIR}
SHELL ["/bin/bash", "-c"]
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD ["/run-jupyter" ]
