# Shipay Back-End Engineer Challenge

Desafio técnico para a posição de Back-End Engineer.

## Questões

- [x] Questão 1 — Validação de cadastro
- [x] Questão 2 — Relatório de lançamentos
- [x] Questão 3 — Event Scheduler e testes de performance
- [x] Questão 4 — Análise de anti-patterns
- [x] Questão 5 — API de criação de usuários
- [x] Questão 6 — Code Review do bot
- [x] Questão 7 — Design Patterns

## Documentação

As respostas e materiais complementares estão organizados dentro de cada questão:

- [Questão 1](question_1/)
- [Questão 2](question_2/)
- [Questão 3](question_3/)
- [Questão 4](question_4/)
- [Questão 5](question_5/)
- [Questão 6](question_6/)
- [Questão 7](question_7/)

## Tecnologias e conceitos

Durante o desafio foram utilizados ou abordados conceitos como:

- Python
- FastAPI
- Pydantic
- SQLite
- Redis
- RQ
- Kafka
- Amazon SQS
- Testes automatizados com Pytest
- Testes de performance com Locust
- Design Patterns
- Arquitetura orientada a serviços e eventos
- Resiliência, retry, timeout e circuit breaker

## Testes

Os testes automatizados das questões que possuem implementação podem ser executados a partir de seus respectivos diretórios.

Para a Questão 5:

```bash
cd question_5
pytest -v
```


Para verificar a qualidade e formatação do código:

```bash
ruff check app tests
ruff format --check app tests
```

## Observações
As soluções foram desenvolvidas considerando os requisitos apresentados em cada questão, buscando equilíbrio entre simplicidade, manutenibilidade, testabilidade e boas práticas de engenharia de software.

As questões de análise e arquitetura não possuem implementação quando o enunciado solicita apenas a descrição ou revisão das soluções propostas.