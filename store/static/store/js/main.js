document.addEventListener('DOMContentLoaded', () => {
  const navToggle = document.querySelector('.nav-toggle');
  const navMenu = document.querySelector('.nav-menu');
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = navMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
      navToggle.textContent = isOpen ? '×' : '☰';
    });
  }

  const slides = Array.from(document.querySelectorAll('.hero-slide'));
  const dots = Array.from(document.querySelectorAll('.hero-dots span'));
  if (slides.length > 1) {
    let current = 0;
    setInterval(() => {
      slides[current].classList.remove('active');
      if (dots[current]) dots[current].classList.remove('active');
      current = (current + 1) % slides.length;
      slides[current].classList.add('active');
      if (dots[current]) dots[current].classList.add('active');
    }, 4500);
  }

  document.querySelectorAll('.heart').forEach((heart) => {
    heart.addEventListener('click', () => {
      heart.classList.add('active');
    });
  });

  const configElement = document.getElementById('checkout-config');
  const checkoutForm = document.getElementById('checkout-form');
  if (configElement && checkoutForm) {
    const config = JSON.parse(configElement.textContent);
    const money = (value) => `R$ ${Number(value).toFixed(2).replace('.', ',')}`;
    const subtotal = Number(config.subtotal || 0);

    const paymentDiscount = (method) => {
      switch (method) {
        case 'pix': return subtotal * 0.05;
        case 'debit': return subtotal * 0.02;
        case 'boleto': return subtotal * 0.03;
        case 'club': return subtotal * 0.10;
        default: return 0;
      }
    };

    const shippingTotal = (method) => {
      switch (method) {
        case 'express': return 29.90;
        case 'pickup': return 0;
        case 'scheduled': return 24.90;
        default: return subtotal >= Number(config.standard_free_from || 180) ? 0 : 18.90;
      }
    };

    const updateCheckout = () => {
      const paymentMethod = checkoutForm.querySelector('[name="payment_method"]')?.value || 'credit';
      const shippingMethod = checkoutForm.querySelector('[name="shipping_method"]')?.value || 'standard';
      const payment = paymentDiscount(paymentMethod);
      const shipping = shippingTotal(shippingMethod);
      const rewardField = checkoutForm.querySelector('[name="reward_code"]');
      const reward = rewardField && rewardField.value.trim() ? 0 : 0;
      const total = Math.max(subtotal + shipping - payment - reward, 0);

      document.getElementById('checkout-subtotal').textContent = money(subtotal);
      document.getElementById('checkout-shipping').textContent = money(shipping);
      document.getElementById('checkout-payment-discount').textContent = `- ${money(payment)}`;
      document.getElementById('checkout-reward-discount').textContent = `- ${money(reward)}`;
      document.getElementById('checkout-total').textContent = money(total);
      document.getElementById('checkout-points').textContent = String(Math.floor(total));
    };

    checkoutForm.querySelectorAll('select, input[name="reward_code"]').forEach((field) => {
      field.addEventListener('change', updateCheckout);
      field.addEventListener('input', updateCheckout);
    });
    updateCheckout();
  }
});
