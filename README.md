# ✨ GlowStore — E-commerce de Beleza

## Descrição do Problema

O mercado de beleza possui muitos produtos, marcas e lojas espalhadas por diferentes plataformas. Isso dificulta a descoberta de novos itens, a comparação entre categorias, a organização de favoritos e a experiência de compra completa em um único ambiente.

Além disso, muitos e-commerces pequenos possuem problemas como:

- interface visual pouco intuitiva;
- falta de organização por lojas e categorias;
- carrinho e checkout pouco claros ou muito poluídos;
- ausência de programa de pontos/fidelidade;
- dificuldade de manutenção no código;
- baixa separação entre regras de negócio, interface e infraestrutura.

**Proposta de solução:** a **GlowStore** é um marketplace de beleza desenvolvido em Django, inspirado em experiências de compra profissionais. O sistema centraliza lojas de maquiagem, skincare, cabelo, perfumes, corpo e unhas em uma plataforma com identidade visual sofisticada, carrinho de compras funcional, seleção de favoritos, checkout claro, formas de pagamento com estratégias de desconto, várias opções de entrega e um sistema de pontos chamado **GlowClub**.

---

## Acesso ao sistema

> **https://glowstore-np0g.onrender.com/**

**Atenção — hospedagem em plano gratuito do Render:**

O projeto está publicado em uma instância gratuita. Caso o site demore para abrir, isso pode acontecer porque o serviço ficou inativo por algum tempo e precisa “acordar” no primeiro acesso.

Também foi adotada uma estratégia específica para as imagens de produtos e lojas em produção: as imagens de exemplo foram servidas como arquivos estáticos do projeto para evitar perda de mídia no ambiente gratuito.

---

## Tecnologias utilizadas

- Python 3.12
- Django
- HTML5
- CSS3
- JavaScript
- SQLite
- Docker
- Docker Compose
- Gunicorn
- WhiteNoise
- Behave (BDD)
- Django TestCase (TDD)
- Render

---

## Arquitetura — Microsserviços

A GlowStore foi organizada com uma separação em **microsserviços lógicos internos**. Ou seja, as responsabilidades principais foram divididas em módulos independentes dentro do mesmo projeto Django.

Essa escolha permite demonstrar separação de responsabilidades, reaproveitamento de regras e baixo acoplamento, sem a complexidade de múltiplos deploys independentes.

| Serviço | Pasta | Responsabilidade |
|---|---|---|
| Serviço principal | `store/` | Interface, páginas, produtos, lojas, categorias, favoritos, pedidos e integração geral |
| Microsserviço de carrinho | `servico_carrinho/` | Cálculo de itens, subtotal e regras relacionadas ao carrinho |
| Microsserviço de pagamentos | `servico_pagamentos/` | Estratégias de pagamento e descontos |
| Microsserviço GlowClub | `servico_GlowClub/` | Pontos, recompensas, resgates e códigos de benefício |

### Serviço principal — `store/`

Responsável por:

- renderização das páginas;
- cadastro e login;
- busca de produtos;
- favoritos;
- páginas de lojas e categorias;
- carrinho;
- checkout;
- perfil do usuário;
- pedidos;
- integração com carrinho, pagamentos e GlowClub.

### Microsserviço de carrinho — `servico_carrinho/`

Responsável por:

- calcular total de cada item;
- calcular subtotal do carrinho;
- manter a regra de cálculo separada das views;
- facilitar testes e reutilização.

Arquivo principal:

```text
servico_carrinho/services.py
```

### Microsserviço de pagamentos — `servico_pagamentos/`

Responsável por:

- representar formas de pagamento;
- aplicar descontos conforme método escolhido;
- centralizar regras financeiras;
- permitir novas formas de pagamento sem alterar diretamente o checkout.

Formas de pagamento utilizadas:

- Pix — desconto;
- Cartão de crédito;
- Cartão de débito;
- Boleto;
- PayPal;
- GlowClub.

Arquivo principal:

```text
servico_pagamentos/services.py
```

### Microsserviço GlowClub — `servico_GlowClub/`

Responsável por:

- criar conta de pontos do usuário;
- calcular pontos com base no valor do pedido;
- aplicar a regra **1 ponto a cada R$1 gasto**;
- permitir resgate de recompensas;
- gerar códigos GlowClub;
- registrar transações de pontos.

Arquivo principal:

```text
servico_GlowClub/services.py
```

---

## Arquitetura Limpa

A organização do projeto segue a ideia da **Arquitetura Limpa**, separando responsabilidades em camadas para deixar o sistema mais legível, testável e fácil de manter.

```text
GlowStore/
│
├── glowstore/                  ← Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/                      ← Serviço principal
│   ├── models.py               ← Entidades do domínio
│   ├── views.py                ← Interface entre usuário e casos de uso
│   ├── forms.py                ← Formulários
│   ├── patterns.py             ← Design Patterns e regras de fluxo
│   ├── tests.py                ← Testes unitários/TDD
│   ├── templates/store/        ← Templates HTML
│   └── static/store/           ← CSS, JavaScript e imagens da interface
│
├── servico_carrinho/           ← Regras de carrinho
│   └── services.py
│
├── servico_pagamentos/         ← Regras de pagamento
│   └── services.py
│
├── servico_GlowClub/           ← Regras de pontos e recompensas
│   └── services.py
│
├── features/                   ← Cenários BDD
│   ├── glowstore.feature
│   ├── environment.py
│   └── steps/
│       └── glowstore_steps.py
│
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── Procfile
├── requirements.txt
├── build.sh
└── README.md
```

### Camada de domínio

Arquivo:

```text
store/models.py
```

Contém as principais entidades do sistema:

- `Category`
- `BeautyStore`
- `Product`
- `FavoriteProduct`
- `FavoriteStore`
- `Order`
- `OrderItem`
- `GlowClubAccount`
- `GlowReward`
- `GlowClubRedemption`
- `GlowClubTransaction`

Essa camada representa os dados essenciais da aplicação.

### Camada de aplicação / casos de uso

Arquivos:

```text
store/patterns.py
servico_carrinho/services.py
servico_pagamentos/services.py
servico_GlowClub/services.py
```

Contém as regras de negócio:

- cálculo de carrinho;
- cálculo de subtotal;
- pagamento;
- desconto;
- frete;
- criação do pedido;
- atualização de estoque;
- pontos GlowClub;
- resgate de recompensas.

### Camada de interface

Arquivos:

```text
store/views.py
store/templates/store/
store/static/store/
```

Responsável por:

- receber requisições;
- renderizar páginas;
- acionar comandos;
- exibir dados ao usuário;
- controlar interações de UI/UX.

### Camada de infraestrutura

Arquivos:

```text
Dockerfile
docker-compose.yml
render.yaml
Procfile
requirements.txt
build.sh
```

Responsável por:

- ambiente de execução;
- dependências;
- Docker;
- deploy;
- configuração de produção;
- coleta de arquivos estáticos.

---

## Padrões de Projeto Utilizados

O projeto utiliza 7 padrões de projeto, todos aplicados no funcionamento real da GlowStore.

### Singleton — Carrinho de compras

Arquivo:

```text
store/patterns.py
```

Classe principal:

```python
class CartSession:
```

O padrão **Singleton** foi usado para garantir uma instância controlada do carrinho por sessão/request.

Responsável por:

- adicionar produto;
- remover produto;
- limpar carrinho;
- contar itens;
- listar itens;
- calcular subtotal.

Benefícios:

- centraliza a lógica do carrinho;
- evita duplicidade de estado;
- reduz repetição de código nas views;
- facilita manutenção.

---

### Factory — Criação de estratégias

Arquivos:

```text
servico_pagamentos/services.py
store/patterns.py
```

Exemplos:

```python
class PaymentStrategyFactory:
```

e/ou fábrica de entrega no fluxo do checkout.

O padrão **Factory** foi aplicado para criar objetos de pagamento e entrega de acordo com a escolha do usuário.

Benefícios:

- elimina condicionais grandes;
- facilita adicionar novos métodos;
- melhora a organização;
- atende ao princípio Open/Closed do SOLID.

---

### Strategy — Pagamentos e entregas

Arquivos:

```text
servico_pagamentos/services.py
store/patterns.py
```

O padrão **Strategy** foi aplicado para permitir diferentes comportamentos de pagamento e entrega sem alterar diretamente a lógica do checkout.

Exemplos de estratégias de pagamento:

- Pix;
- cartão de crédito;
- cartão de débito;
- boleto;
- PayPal;
- GlowClub.

Exemplos de estratégias de entrega:

- entrega padrão;
- entrega expressa;
- retirada.

Cada estratégia possui sua própria regra de cálculo.

Benefícios:

- cada regra fica isolada;
- melhora a testabilidade;
- permite trocar comportamento em tempo de execução;
- facilita expansão futura.

---

### Builder — Construção de pedido

Arquivo:

```text
store/patterns.py
```

Classe principal:

```python
class OrderBuilder:
```

O padrão **Builder** foi aplicado para montar um pedido passo a passo.

Fluxo:

```python
OrderBuilder()
    .with_customer(...)
    .with_cart(...)
    .with_payment(...)
    .with_shipping(...)
    .build()
```

Responsável por organizar:

- cliente;
- endereço;
- carrinho;
- pagamento;
- entrega;
- desconto;
- total.

Benefícios:

- evita construtor gigante;
- melhora legibilidade;
- reduz risco de criar pedido incompleto;
- deixa o checkout mais organizado.

---

### Observer — Eventos após finalização do pedido

Arquivo:

```text
store/patterns.py
```

O padrão **Observer** foi aplicado para executar ações automáticas após a criação/finalização de um pedido.

Observadores utilizados:

- `DashboardObserver` — atualiza status do pedido;
- `StockObserver` — reduz estoque dos produtos;
- `GlowClubObserver` — adiciona pontos no programa GlowClub.

Benefícios:

- desacopla efeitos colaterais;
- permite adicionar novos eventos sem mexer no checkout;
- automatiza processos após compra;
- melhora escalabilidade da regra.

---

### Facade — Checkout

Arquivo:

```text
store/patterns.py
```

Classe principal:

```python
class CheckoutFacade:
```

O padrão **Facade** foi usado para centralizar a complexidade do checkout atrás de uma interface simples.

Responsável por:

- obter carrinho;
- calcular subtotal;
- aplicar desconto;
- calcular frete;
- aplicar resgate GlowClub;
- montar pedido com Builder;
- criar `Order`;
- criar `OrderItem`;
- notificar observers;
- limpar carrinho.

Benefícios:

- deixa as views mais limpas;
- reduz acoplamento;
- centraliza o fluxo de compra;
- facilita manutenção.

---

### Command — Ações do usuário

Arquivo:

```text
store/patterns.py
```

Comandos implementados:

- `AddToCartCommand`
- `ToggleFavoriteProductCommand`
- `ToggleFavoriteStoreCommand`

O padrão **Command** foi aplicado para encapsular ações do usuário em objetos próprios.

Responsável por:

- adicionar item ao carrinho;
- favoritar/desfavoritar produto;
- favoritar/desfavoritar loja.

Benefícios:

- separa ação da view;
- facilita reaproveitamento;
- melhora organização;
- torna o fluxo mais testável.

---

## Princípios SOLID aplicados

| Princípio | Aplicação na GlowStore |
|---|---|
| **S — Single Responsibility** | Cada classe possui uma responsabilidade clara. `CartSession` cuida do carrinho, `GlowClubService` cuida dos pontos, `CheckoutFacade` cuida do checkout. |
| **O — Open/Closed** | Novas formas de pagamento podem ser adicionadas criando novas estratégias e registrando na Factory, sem reescrever o checkout. |
| **L — Liskov Substitution** | As classes de pagamento substituem a abstração `PaymentStrategy` sem quebrar o fluxo. |
| **I — Interface Segregation** | As abstrações são pequenas e específicas: `Command`, `OrderObserver`, `PaymentStrategy`, `ShippingStrategy`. |
| **D — Dependency Inversion** | O checkout trabalha com fábricas e abstrações, não diretamente com implementações fixas. |

### Exemplos práticos

#### Single Responsibility

```python
class GlowClubService:
    @classmethod
    def points_for_order(cls, amount):
        return max(int(amount), 0)
```

A classe possui uma responsabilidade clara: lidar com regras do programa de pontos.

#### Open/Closed

Para adicionar uma nova forma de pagamento, basta criar uma nova classe e registrar na Factory.

```python
class DebitCardPayment(PaymentStrategy):
    code = "debit"
    label = "Cartão de débito"
```

#### Dependency Inversion

```python
payment = PaymentStrategyFactory.create(payment_method)
shipping_strategy = ShippingStrategyFactory.create(shipping_method)
```

A lógica do checkout depende da abstração/fábrica, e não de uma classe concreta fixa.

---

## Evidências de Clean Code

O projeto apresenta práticas de Clean Code em várias partes:

- nomes descritivos para classes, funções e métodos;
- separação entre interface e regra de negócio;
- uso de serviços para regras específicas;
- funções com responsabilidades menores;
- templates organizados por página;
- CSS centralizado;
- JavaScript separado para interações;
- evitar duplicação de regras de pagamento, frete e pontos;
- uso de `get_or_create` para evitar duplicações no banco;
- comentários usados apenas quando ajudam a entender decisões específicas.

### Exemplos

```python
def points_for_order(cls, amount):
    return max(int(amount), 0)
```

O nome deixa claro o objetivo do método.

```python
def apply_discount(self, subtotal):
    return subtotal * Decimal("0.05")
```

A regra de desconto fica dentro da estratégia correta, e não misturada na view.

```python
def finish_order(self, full_name, address, payment_method, shipping_method):
```

O método da Facade deixa claro que representa a finalização de um pedido.

---

## TDD — Testes unitários

Os testes unitários foram criados para validar regras importantes antes da entrega e garantir que alterações não quebrem o comportamento principal do sistema.

Arquivo:

```text
store/tests.py
```

### Regras testadas

| Teste | Objetivo |
|---|---|
| Desconto via Pix | Garante aplicação correta do desconto |
| Pagamento inválido | Garante fallback seguro para cartão |
| Frete padrão | Garante frete grátis acima do valor mínimo |
| Frete expresso | Garante valor fixo da entrega expressa |
| Builder de pedido | Garante cálculo correto do total |
| Pontos GlowClub | Garante 1 ponto a cada R$1 gasto |
| Resgate GlowClub | Garante geração de código e redução de saldo |

### Rodar os testes

```bash
python manage.py test
```

### Resultado esperado

```text
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.......
Ran 7 tests
OK
Destroying test database for alias 'default'...
```

### Por que isso representa TDD?

Os testes validam regras de negócio isoladas, como desconto, frete, montagem do pedido e pontos. Isso permite evoluir o código com mais segurança e seguir o ciclo:

```text
Red → Green → Refactor
```

Ou seja:

1. escrever/planejar o comportamento esperado;
2. implementar a menor solução possível;
3. refatorar mantendo os testes passando.

---

## BDD — Cenários de comportamento

Os cenários BDD foram escritos em português usando **Behave**, aproximando os testes da linguagem de negócio e do comportamento esperado pelo usuário.

Arquivos:

```text
features/glowstore.feature
features/steps/glowstore_steps.py
features/environment.py
```

### Cenários implementados

| Cenário | Comportamento validado |
|---|---|
| Cliente adiciona produto ao carrinho | Produto aparece no carrinho e subtotal é calculado |
| Cliente escolhe forma de pagamento | Pix aplica desconto e total é atualizado |
| Cliente acumula pontos no GlowClub | Pedido pago gera pontos no perfil |
| Cliente resgata recompensa GlowClub | Código é gerado e pontos são descontados |

### Exemplo de cenário

```gherkin
Feature: Experiência de compra GlowStore
  Como cliente de beleza
  Quero comprar produtos, acumular pontos e resgatar benefícios
  Para ter uma experiência parecida com um e-commerce profissional

  Scenario: Cliente acumula pontos no GlowClub
    Given que o cliente finalizou um pedido pago
    When o pedido é confirmado
    Then o sistema deve adicionar 1 ponto a cada R$1 gasto
    And os pontos devem aparecer no perfil do cliente
```

### Rodar os cenários

```bash
behave
```

ou:

```bash
python -m behave
```

### Resultado obtido

```text
USING RUNNER: behave.runner:Runner
1 feature passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
16 steps passed, 0 failed, 0 skipped
```

### Por que isso representa BDD?

O BDD descreve o comportamento do sistema a partir do ponto de vista do usuário. Em vez de focar apenas em métodos internos, os cenários validam fluxos como comprar, acumular pontos e resgatar recompensas.

---

## Docker

O projeto utiliza Docker para padronizar o ambiente de execução e evitar problemas de dependências entre diferentes máquinas.

### Dockerfile

O `Dockerfile` define:

- imagem base Python;
- instalação de dependências;
- cópia do projeto;
- execução com Gunicorn.

### docker-compose.yml

O `docker-compose.yml` permite subir o sistema localmente com um único comando.

### Rodar com Docker Compose

```bash
docker compose up --build
```

### Acessar

```text
http://127.0.0.1:8000/
```

### Rodar comandos dentro do container

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_glowstore
docker compose exec web python manage.py test
docker compose exec web python -m behave
```

---

## Como rodar localmente sem Docker

### 1. Clonar o repositório

```bash
git clone https://github.com/anacgsx/GlowStore
cd GlowStore
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar ambiente virtual

Windows:

```bash
.\venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Rodar migrações

```bash
python manage.py migrate
```

### 6. Popular banco com dados iniciais

```bash
python manage.py seed_glowstore
```

### 7. Criar superusuário

```bash
python manage.py createsuperuser
```

### 8. Rodar servidor

```bash
python manage.py runserver
```

### 9. Acessar

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

---

## Banco de dados

O projeto utiliza SQLite para desenvolvimento, mantendo a execução simples.

Em um ambiente profissional, o recomendado seria utilizar PostgreSQL em produção, principalmente por questões de persistência, escalabilidade e confiabilidade.

### Resetar banco local

```bash
python manage.py flush
```

### Rodar seed novamente

```bash
python manage.py seed_glowstore
```

### Observação sobre imagens

Localmente, imagens cadastradas pelo admin podem ficar em:

```text
media/
```

Para o Render, as imagens de exemplo foram movidas/servidas como arquivos estáticos, evitando problemas de persistência em plano gratuito.

Estrutura usada para produção:

```text
store/static/media/products/
store/static/media/stores/logos/
```

---

## Deploy no Render

O deploy foi configurado para a plataforma **Render**.

Arquivos relacionados:

```text
render.yaml
Procfile
build.sh
requirements.txt
```

### Link publicado

```text
https://glowstore-np0g.onrender.com/
```

### Como funciona o deploy

O Render lê as configurações do projeto e executa os comandos necessários para preparar a aplicação.

Fluxo configurado:

```text
Push no GitHub
→ Render detecta alteração
→ instala dependências
→ executa collectstatic
→ executa migrations
→ executa seed inicial
→ inicia aplicação com Gunicorn
```

### Observação sobre plano gratuito

Como o plano gratuito pode ter limitações de shell, persistência de mídia e tempo de inicialização, o projeto foi ajustado para:

- popular o banco automaticamente no deploy;
- servir imagens de produtos/lojas como arquivos estáticos;
- evitar dependência de uploads manuais no servidor.

---

## Estrutura do Projeto

```text
GlowStore/
│
├── glowstore/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── store/
│   ├── management/
│   │   └── commands/
│   │       └── seed_glowstore.py
│   ├── migrations/
│   ├── static/
│   │   ├── media/
│   │   │   ├── products/
│   │   │   └── stores/
│   │   │       └── logos/
│   │   └── store/
│   │       ├── css/
│   │       ├── js/
│   │       └── images/
│   ├── templates/
│   │   └── store/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── patterns.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── servico_carrinho/
│   ├── __init__.py
│   └── services.py
│
├── servico_pagamentos/
│   ├── __init__.py
│   └── services.py
│
├── servico_GlowClub/
│   ├── __init__.py
│   └── services.py
│
├── features/
│   ├── glowstore.feature
│   ├── environment.py
│   └── steps/
│       └── glowstore_steps.py
│
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── Procfile
├── build.sh
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Justificativa Técnica

### Por que Django?

Django foi escolhido por fornecer uma base completa para aplicações web com autenticação, ORM, rotas, templates, migrations, painel administrativo e segurança básica. Isso permitiu desenvolver uma aplicação funcional e organizada sem depender de muitas bibliotecas externas.

### Por que microsserviços lógicos?

Para manter o projeto simples e funcional, a GlowStore utiliza uma divisão lógica por responsabilidade:

- carrinho;
- pagamentos;
- GlowClub.

Essa divisão mostra separação de domínios sem criar múltiplos servidores, múltiplos bancos e múltiplos deploys, o que deixaria o projeto desnecessariamente complexo para o contexto acadêmico.

### Por que Arquitetura Limpa?

A Arquitetura Limpa foi usada para separar domínio, aplicação, interface e infraestrutura. Assim, regras de negócio como pagamento, frete, carrinho e pontos não ficam presas diretamente às views ou templates.

### Por que Design Patterns?

Os padrões foram usados para resolver problemas reais do sistema:

- carrinho com Singleton;
- pagamento e entrega com Strategy;
- criação de estratégias com Factory;
- criação de pedidos com Builder;
- ações pós-pedido com Observer;
- checkout com Facade;
- ações de usuário com Command.

Isso deixa o código mais extensível e mais fácil de evoluir.

### Por que TDD?

Os testes unitários garantem que regras críticas, como desconto, frete, pontos e total do pedido, funcionem corretamente mesmo após alterações no código.

### Por que BDD?

Os cenários BDD documentam o comportamento esperado da aplicação em linguagem próxima do usuário, facilitando a validação dos fluxos principais de compra e fidelidade.

### Por que Docker?

Docker foi usado para padronizar o ambiente de execução, reduzindo problemas de configuração e permitindo que o projeto rode de maneira semelhante em diferentes máquinas.

### Por que Render?

Render foi escolhido por permitir deploy via GitHub, HTTPS automático e configuração simples para aplicações Django, sendo adequado para publicação acadêmica.

### Por que imagens estáticas em produção?

No Render gratuito, depender de uploads manuais em `media/` pode causar problemas de persistência. Por isso, as imagens de produtos e lojas usadas na apresentação foram mantidas dentro de `static/`, garantindo que sejam coletadas no deploy e exibidas corretamente.

---

## Fluxo principal do sistema

```text
Usuário acessa a home
→ navega por lojas/categorias
→ pesquisa produtos
→ favorita produto ou loja
→ adiciona produto ao carrinho
→ escolhe pagamento e entrega
→ checkout calcula total
→ pedido é criado
→ observers atualizam status, estoque e pontos
→ usuário acompanha pedido e GlowClub no perfil
```

---

## Funcionalidades implementadas na versão 2.0

- Página inicial com carrossel
- Menu responsivo mobile
- Busca funcional
- Páginas separadas de lojas e categorias
- Checkout com atualização de valores
- Múltiplas formas de pagamento
- Formas de entrega
- Perfil do usuário
- Logout funcional no perfil
- GlowClub com pontos e recompensas
- Design responsivo e sofisticado
- Testes TDD
- Cenários BDD
- Docker
- Deploy no Render

---

## Conclusão

A GlowStore demonstra uma solução completa para um marketplace de beleza, unindo experiência visual, regras de negócio, arquitetura organizada e práticas modernas de desenvolvimento.

O projeto aplica:

- Clean Code;
- SOLID;
- Design Patterns;
- Arquitetura Limpa;
- Microsserviços lógicos;
- TDD;
- BDD;
- Docker;
- Deploy em nuvem.

Com isso, a aplicação atende aos requisitos e apresenta uma estrutura profissional, simples de executar, documentada e preparada para evolução futura.

---
