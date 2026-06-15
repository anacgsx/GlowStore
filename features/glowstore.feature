Feature: Experiência de compra GlowStore
  Como cliente de beleza
  Quero comprar produtos, acumular pontos e resgatar benefícios
  Para ter uma experiência parecida com um e-commerce profissional

  Scenario: Cliente adiciona produto ao carrinho
    Given que existe um produto disponível na GlowStore
    When o cliente clica em adicionar ao carrinho
    Then o produto deve aparecer no carrinho
    And o subtotal deve ser calculado corretamente

  Scenario: Cliente escolhe forma de pagamento no checkout
    Given que o carrinho possui produtos
    When o cliente escolhe Pix
    Then o checkout deve aplicar desconto de 5 por cento
    And o total deve ser atualizado na tela

  Scenario: Cliente acumula pontos no GlowClub
    Given que o cliente finalizou um pedido pago
    When o pedido é confirmado
    Then o sistema deve adicionar 1 ponto a cada R$1 gasto
    And os pontos devem aparecer no perfil do cliente

  Scenario: Cliente resgata recompensa GlowClub
    Given que o cliente possui pontos suficientes
    When ele resgata uma recompensa
    Then o sistema deve gerar um código GlowClub
    And os pontos usados devem ser removidos do saldo