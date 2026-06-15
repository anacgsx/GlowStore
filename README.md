# GlowStore — E-commerce de Beleza com Arquitetura, Design Patterns, TDD, BDD, Docker e Deploy

## 1. Descrição do problema escolhido

O mercado de beleza possui muitos produtos espalhados em sites diferentes, dificultando a descoberta de marcas, a comparação de opções, a organização de favoritos e a experiência de compra. A proposta da **GlowStore** é centralizar lojas de maquiagem, skincare, cabelo, perfume, corpo e unhas em um marketplace visualmente sofisticado, com experiência inspirada em e-commerces profissionais como a Sephora.

A aplicação permite navegar por lojas e categorias, buscar produtos, favoritar lojas/produtos, adicionar itens ao carrinho, finalizar pedido, escolher pagamento/entrega e acumular pontos no programa **GlowClub**.

---

## 2. Proposta da solução

A GlowStore é um e-commerce desenvolvido em **Django**, com foco em:

- experiência de compra quase completa;
- organização de lojas e categorias;
- carrinho de compras;
- checkout com pagamento e entrega;
- favoritos;
- perfil do usuário;
- sistema de pontos GlowClub;
- padrões de projeto aplicados de verdade;
- testes unitários com TDD;
- cenários BDD;
- Docker/Docker Compose;
- configuração para deploy no Render.

---

## 3. Tecnologias utilizadas

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite
- Docker
- Docker Compose
- Gunicorn
- WhiteNoise
- Render

---

## 4. Estrutura do projeto

```text
GlowStore/
│
├── glowstore/                  ← Configurações principais do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/                      ← Serviço principal da aplicação
│   ├── models.py               ← Entidades do domínio
│   ├── views.py                ← Casos de uso chamados pela interface
│   ├── forms.py                ← Formulários
│   ├── patterns.py             ← Design Patterns integrados ao fluxo real
│   ├── tests.py                ← Testes unitários/TDD
│   ├── templates/store/        ← Páginas HTML
│   └── static/store/           ← CSS e JavaScript
│
├── servico_pagamentos/         ← Microsserviço lógico de pagamentos
│   └── services.py
│
├── servico_carrinho/           ← Microsserviço lógico de carrinho
│   └── services.py
│
├── servico_GlowClub/           ← Microsserviço lógico de pontos e recompensas
│   └── services.py
│
├── features/                   ← Cenários BDD em Gherkin
│   └── glowstore.feature
│
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── Procfile
├── requirements.txt
└── README.md
```

---

## 5. Divisão da solução em microsserviços

Para manter o projeto simples, acadêmico e funcional, a GlowStore utiliza uma divisão em **microsserviços lógicos internos**. Isso significa que as responsabilidades foram separadas em módulos independentes, mas executadas dentro do mesmo deploy Django para evitar complexidade desnecessária.

### 5.1 Serviço principal — `store/`

Responsável por:

- renderizar páginas;
- controlar fluxo de navegação;
- gerenciar lojas, categorias, produtos e pedidos;
- integrar os serviços internos.

### 5.2 Microsserviço de carrinho — `servico_carrinho/`

Responsável por:

- calcular total de item;
- calcular subtotal do carrinho;
- manter a regra de cálculo fora das views.

Arquivo principal:

```text
servico_carrinho/services.py
```

### 5.3 Microsserviço de pagamentos — `servico_pagamentos/`

Responsável por:

- criar estratégias de pagamento;
- aplicar descontos por método de pagamento;
- centralizar as formas de pagamento.

Formas implementadas:

- Pix — 5% de desconto;
- Cartão de crédito — sem desconto;
- Cartão de débito — 2% de desconto;
- Boleto — 3% de desconto;
- PayPal — sem desconto;
- GlowClub — 10% de desconto.

Arquivo principal:

```text
servico_pagamentos/services.py
```

### 5.4 Microsserviço GlowClub — `servico_GlowClub/`

Responsável por:

- criar conta de pontos;
- adicionar pontos após compra;
- calcular 1 ponto a cada R$1 gasto;
- resgatar recompensas;
- gerar códigos de desconto.

Arquivo principal:

```text
servico_GlowClub/services.py
```

---

## 6. Organização com Arquitetura Limpa

A solução foi organizada tentando respeitar os princípios da **Arquitetura Limpa**, separando responsabilidades em camadas.

### Camada de domínio

Arquivo:

```text
store/models.py
```

Contém as entidades principais:

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

### Camada de aplicação / casos de uso

Arquivos:

```text
store/patterns.py
servico_carrinho/services.py
servico_pagamentos/services.py
servico_GlowClub/services.py
```

Contém as regras de negócio:

- carrinho;
- descontos;
- frete;
- checkout;
- montagem do pedido;
- atualização de estoque;
- pontos GlowClub.

### Camada de interface

Arquivos:

```text
store/views.py
store/templates/store/
store/static/store/
```

Contém:

- páginas;
- formulários;
- rotas;
- interações com JavaScript;
- interface responsiva.

### Camada de infraestrutura

Arquivos:

```text
Dockerfile
docker-compose.yml
render.yaml
requirements.txt
```

Contém:

- execução local;
- ambiente em container;
- dependências;
- configuração para deploy.

---

## 7. Aplicação de Clean Code

O projeto aplica Clean Code por meio de:

- nomes descritivos para classes e métodos;
- funções pequenas e com responsabilidade clara;
- separação de regras em serviços;
- uso de classes específicas para pagamentos, entrega, carrinho e GlowClub;
- remoção de lógica complexa das views;
- templates organizados por página;
- CSS centralizado e responsivo;
- JavaScript separado em arquivo próprio.

Exemplo:

```python
class GlowClubService:
    @classmethod
    def points_for_order(cls, amount: Decimal) -> int:
        return max(int(amount), 0)
```

O método possui nome claro e uma única responsabilidade: calcular pontos a partir do valor do pedido.

---

## 8. Aplicação dos princípios SOLID

### S — Single Responsibility Principle

Cada classe possui uma responsabilidade principal.

Exemplos:

- `CartSession` gerencia carrinho;
- `GlowClubService` gerencia pontos;
- `PaymentStrategyFactory` cria estratégias de pagamento;
- `CheckoutFacade` centraliza o checkout.

### O — Open/Closed Principle

O sistema está aberto para extensão e fechado para alteração direta.

Exemplo: para adicionar uma nova forma de pagamento, basta criar uma nova classe e registrá-la na Factory.

```python
class DebitCardPayment(PaymentStrategy):
    code = "debit"
    label = "Cartão de débito"
```

### L — Liskov Substitution Principle

As classes filhas de `PaymentStrategy` podem substituir a classe base sem quebrar o sistema.

Exemplos:

- `PixPayment`
- `CreditCardPayment`
- `GlowClubPayment`

Todas implementam:

```python
apply_discount()
```

### I — Interface Segregation Principle

As abstrações são pequenas e específicas.

Exemplos:

```python
class PaymentStrategy(ABC)
class ShippingStrategy(ABC)
class Command(ABC)
class OrderObserver(ABC)
```

Cada interface exige apenas o necessário.

### D — Dependency Inversion Principle

O checkout depende de abstrações, e não de implementações fixas.

Exemplo:

```python
payment = PaymentStrategyFactory.create(payment_method)
shipping_strategy = ShippingStrategyFactory.create(shipping_method)
```

---

## 9. Design Patterns aplicados

O projeto utiliza mais de 4 padrões de projeto, todos integrados ao funcionamento real do sistema.

### 9.1 Singleton — `CartSession`

Arquivo:

```text
store/patterns.py
```

Usado para garantir uma única instância do carrinho por request/sessão.

Benefícios:

- centraliza o carrinho;
- evita duplicação de lógica;
- facilita contagem, subtotal e itens.

### 9.2 Factory — `PaymentStrategyFactory` e `ShippingStrategyFactory`

Arquivos:

```text
servico_pagamentos/services.py
store/patterns.py
```

Usado para criar dinamicamente formas de pagamento e entrega.

Benefícios:

- evita `if/else` gigante;
- facilita adicionar novas opções;
- melhora manutenção.

### 9.3 Strategy — pagamentos e entregas

Arquivos:

```text
servico_pagamentos/services.py
store/patterns.py
```

Cada pagamento e entrega possui uma regra própria.

Exemplos:

- `PixPayment`
- `DebitCardPayment`
- `BankSlipPayment`
- `StandardShipping`
- `ExpressShipping`
- `PickupShipping`

Benefícios:

- regras isoladas;
- fácil expansão;
- baixo acoplamento.

### 9.4 Builder — `OrderBuilder`

Arquivo:

```text
store/patterns.py
```

Usado para montar o pedido passo a passo.

Fluxo:

```python
OrderBuilder()
    .with_customer(...)
    .with_cart(...)
    .with_payment(...)
    .with_shipping(...)
    .build()
```

Benefícios:

- melhora legibilidade;
- evita construtor gigante;
- reduz erro na criação de pedidos.

### 9.5 Observer — atualização após pedido

Arquivo:

```text
store/patterns.py
```

Quando o pedido é finalizado, observadores são notificados.

Observadores implementados:

- `DashboardObserver` — muda status para pago;
- `StockObserver` — reduz estoque;
- `GlowClubObserver` — adiciona pontos ao usuário.

Benefícios:

- ações automáticas desacopladas;
- fácil adicionar novos eventos;
- melhora organização.

### 9.6 Facade — `CheckoutFacade`

Arquivo:

```text
store/patterns.py
```

Centraliza o fluxo complexo do checkout.

Responsável por:

- calcular subtotal;
- aplicar desconto;
- calcular frete;
- aplicar cupom GlowClub;
- criar pedido;
- criar itens;
- notificar observers;
- limpar carrinho.

Benefícios:

- view mais limpa;
- regra de negócio centralizada;
- manutenção mais simples.

### 9.7 Command — ações do usuário

Arquivo:

```text
store/patterns.py
```

Comandos implementados:

- `AddToCartCommand`
- `ToggleFavoriteProductCommand`
- `ToggleFavoriteStoreCommand`

Benefícios:

- ações encapsuladas;
- maior reutilização;
- facilita testes.

---

## 10. TDD — Testes unitários

Arquivo:

```text
store/tests.py
```

Testes implementados:

- desconto do Pix;
- fallback de pagamento inválido para cartão;
- frete padrão grátis acima de R$180;
- frete expresso com valor fixo;
- cálculo do total pelo Builder;
- geração de pontos GlowClub;
- resgate de recompensa GlowClub.

Rodar testes:

```bash
python manage.py test
```

Resultado esperado:

```text
Ran 7 tests
OK
```

---

## 11. BDD — Cenários de comportamento

Arquivo:

```text
features/glowstore.feature
```

Cenários escritos:

- cliente adiciona produto ao carrinho;
- cliente escolhe forma de pagamento no checkout;
- cliente acumula pontos no GlowClub;
- cliente resgata recompensa GlowClub.

Exemplo:

```gherkin
Scenario: Cliente acumula pontos no GlowClub
  Given que o cliente finalizou um pedido pago
  When o pedido é confirmado
  Then o sistema deve adicionar 1 ponto a cada R$1 gasto
  And os pontos devem aparecer no perfil do cliente
```

---

## 12. Docker e Docker Compose

### Dockerfile

O `Dockerfile` cria uma imagem com:

- Python 3.12;
- dependências do projeto;
- coleta de arquivos estáticos;
- execução com Gunicorn.

### docker-compose.yml

Executa o projeto localmente em container.

Rodar com Docker Compose:

```bash
docker compose up --build
```

Acessar:

```text
http://127.0.0.1:8000/
```

---

## 13. Como rodar localmente sem Docker

Clonar o repositório:

```bash
git clone URL_DO_REPOSITORIO
cd GlowStore
```

Criar ambiente virtual:

```bash
python -m venv venv
```

Ativar no Windows:

```bash
.\venv\Scripts\activate
```

Ativar no Linux/Mac:

```bash
source venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Rodar migrações:

```bash
python manage.py migrate
```

Popular o banco:

```bash
python manage.py seed_glowstore
```

Criar admin:

```bash
python manage.py createsuperuser
```

Rodar servidor:

```bash
python manage.py runserver
```

Acessar:

```text
http://127.0.0.1:8000/
```

---

## 14. Deploy no Render


### Link do sistema 

```text
.
```

---

## 15. Observação sobre imagens em produção

Para simplificar a entrega acadêmica, os arquivos de mídia de exemplo foram mantidos no próprio projeto e servidos pela configuração `SERVE_MEDIA=True`.

Em um e-commerce real, o ideal seria usar:

- Cloudinary;
- AWS S3;
- Supabase Storage;
- outro storage externo.

---

## 16. Justificativa técnica das escolhas

A GlowStore foi mantida em Django porque o framework permite entregar rapidamente um sistema completo com autenticação, rotas, templates, banco de dados, admin e segurança básica.

A divisão em microsserviços lógicos foi escolhida para demonstrar separação de responsabilidades sem transformar o projeto em uma arquitetura gigante e difícil. Assim, carrinho, pagamentos e sistema de pontos possuem módulos próprios, mas continuam integrados ao serviço principal.

Os Design Patterns foram aplicados no fluxo real do sistema, principalmente no carrinho, checkout, pagamento, entrega, pedido, favoritos e pontos. Isso mostra que os padrões não foram apenas citados: eles resolvem problemas concretos da aplicação.

Docker e Render foram adicionados para garantir execução padronizada e publicação em nuvem.

---

## 17. Fluxo principal do sistema

```text
Usuário navega → busca produto → favorita/adiciona ao carrinho → checkout
→ estratégia de pagamento → estratégia de entrega → Builder monta pedido
→ Facade finaliza → Observer atualiza status/estoque/pontos → perfil exibe pedido e pontos GlowClub
```

---

## 18. Conclusão

A GlowStore demonstra uma solução de software moderna, organizada e funcional para um marketplace de beleza. O projeto aplica conceitos de arquitetura, Clean Code, SOLID, Design Patterns, TDD, BDD, microsserviços, Docker e deploy, mantendo simplicidade suficiente para ser apresentado e profissionalismo suficiente para simular um e-commerce real.
