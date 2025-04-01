FROM python:3.10-slim AS builder

RUN mkdir /install
WORKDIR /app
COPY mtg_card_puller/ /app/mtg_card_puller
COPY pyproject.toml LICENSE README.md /app

RUN python -m pip install . --prefix=/install

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /install /usr/local

ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/"

CMD ["mtg_card_puller"]