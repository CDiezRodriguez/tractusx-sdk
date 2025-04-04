#################################################################################
# Eclipse Tractus-X - Software Development KIT
#
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

# Build stage
FROM alpine:3.19 AS builder

# --- Python Compilation Setup ---
ARG PYTHON_VERSION=3.12.9
ENV PYHON_PATH=/opt/python${PYTHON_VERSION}
ENV PATH="${PYHON_PATH}/bin:${PATH}"

WORKDIR /tmp

RUN apk add --no-cache \
    build-base \
    bzip2-dev \
    gdbm-dev \
    libffi-dev \
    ncurses-dev \
    openssl-dev \
    readline-dev \
    tk-dev \
    zlib-dev

RUN mkdir -p ${PYHON_PATH}

ADD https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz python.tar.xz
RUN tar -xJf python.tar.xz \
    && rm python.tar.xz

RUN cd Python-${PYTHON_VERSION} \
    && ./configure --prefix=${PYHON_PATH} --with-ensurepip=install \
    && make -j $(nproc) \
    && make install \
    && cd /tmp \
    && rm -rf Python-${PYTHON_VERSION}
    
RUN python3 -m ensurepip --upgrade \
  && pip3 install --no-cache --upgrade pip setuptools wheel virtualenv

RUN python -V && pip -V
# --- End Python Compilation Setup --

WORKDIR /build

# Copy source code and build configuration
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install build tool and build the wheel
RUN python3 -m pip install --no-cache-dir build \
    && python3 -m build --wheel

# Production stage
FROM alpine:3.19 AS production

# --- Python Compilation Setup ---
ARG PYTHON_VERSION=3.12.9
ENV PYTHON_PATH=/opt/python${PYTHON_VERSION}
ENV PATH="${PYTHON_PATH}/bin:${PATH}"

WORKDIR /tmp

RUN apk add --no-cache curl  

COPY --from=builder /opt/python${PYTHON_VERSION} ${PYTHON_PATH}

RUN ln -s ${PYTHON_PATH}/bin/python3 /usr/bin/python3 \
    && ln -s ${PYTHON_PATH}/bin/pip3 /usr/bin/pip3
# --- End Python Compilation Setup --

# Set environment variables for runtime
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only the built wheel
COPY --from=builder /build/dist/*.whl ./

# Install the package wheel
RUN python3 -m pip install --no-cache-dir ./*.whl && rm -f ./*.whl \
# Create required directories
    && mkdir -p ./logs ./data \
# Create a non-root user
    && addgroup -S appgroup && adduser -S -G appgroup appuser \
    && chown -R appuser:appgroup /app ./logs ./data

# Set the user for running the application
USER appuser

# Expose the port
EXPOSE 8000

# Define the health check command to verify if the application is responsive
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000/api/check/health"]

# Run the industry module from the installed package
CMD ["python3", "-m", "tractusx_sdk.dataspace.main", "--host", "0.0.0.0", "--port", "8000"]
