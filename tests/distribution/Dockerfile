ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}

RUN mkdir -p /code

COPY ./ /code/

WORKDIR /code

# install testing dependencies
RUN pip3 install \
    parameterized

RUN pip3 install /code/

RUN make test-unit
