const STORAGE_KEY = "kantinku-cart-v1";
const DISCOUNT_THRESHOLD = 50000;
const DISCOUNT_RATE = 0.1;

let cart = loadCart();
let promoActive = false;

const elements = {
  form: document.querySelector("#product-form"),
  name: document.querySelector("#product-name"),
  price: document.querySelector("#unit-price"),
  quantity: document.querySelector("#quantity"),
  formSuccess: document.querySelector("#form-success"),
  cartBody: document.querySelector("#cart-body"),
  emptyCart: document.querySelector("#empty-cart"),
  cartCount: document.querySelector("#cart-count"),
  resetButton: document.querySelector("#reset-transaction"),
  subtotal: document.querySelector("#subtotal-display"),
  discount: document.querySelector("#discount-display"),
  discountNote: document.querySelector("#discount-note"),
  total: document.querySelector("#total-display"),
  promoCode: document.querySelector("#promo-code"),
  applyPromo: document.querySelector("#apply-promo"),
  promoMessage: document.querySelector("#promo-message"),
  payment: document.querySelector("#payment"),
  paymentResult: document.querySelector("#payment-result")
};

const rupiah = (amount) => new Intl.NumberFormat("id-ID", {
  style: "currency", currency: "IDR", maximumFractionDigits: 0
}).format(amount);

function loadCart() {
  try {
    const savedCart = localStorage.getItem(STORAGE_KEY);
    const parsedCart = savedCart ? JSON.parse(savedCart) : [];
    return Array.isArray(parsedCart) ? parsedCart : [];
  } catch (error) {
    console.warn("Keranjang tidak dapat dimuat dari localStorage.", error);
    return [];
  }
}

function saveCart() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
  } catch (error) {
    console.warn("Keranjang tidak dapat disimpan ke localStorage.", error);
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#039;", '"': "&quot;"
  }[character]));
}

function validateProduct() {
  const values = {
    name: elements.name.value.trim(),
    price: Number(elements.price.value),
    quantity: Number(elements.quantity.value)
  };
  const errors = {};

  if (values.name.length < 3) errors.name = "Nama barang wajib diisi minimal 3 karakter.";
  if (!Number.isFinite(values.price) || values.price < 500) errors.price = "Harga wajib berupa angka minimal Rp 500.";
  if (!Number.isInteger(values.quantity) || values.quantity < 1) errors.quantity = "Qty wajib berupa angka bulat minimal 1.";

  ["name", "price", "quantity"].forEach((field) => {
    const input = elements[field];
    const errorElement = document.querySelector(`#${input.id}-error`);
    input.classList.toggle("input-invalid", Boolean(errors[field]));
    input.setAttribute("aria-invalid", String(Boolean(errors[field])));
    errorElement.textContent = errors[field] || "";
  });

  return Object.keys(errors).length === 0 ? values : null;
}

function renderCart() {
  elements.cartBody.innerHTML = cart.map((item, index) => {
    const subtotal = item.price * item.quantity;
    return `<tr>
      <td>${index + 1}</td>
      <td><span class="item-name">${escapeHtml(item.name)}</span><span class="item-subtle">Produk kantin</span></td>
      <td>${rupiah(item.price)}</td>
      <td>${item.quantity}</td>
      <td><strong>${rupiah(subtotal)}</strong></td>
      <td><button class="delete-button" type="button" data-id="${escapeHtml(item.id)}" aria-label="Hapus ${escapeHtml(item.name)}">Hapus</button></td>
    </tr>`;
  }).join("");
  elements.emptyCart.hidden = cart.length > 0;
  elements.cartCount.textContent = cart.length;
  updateSummary();
}

function calculateSummary() {
  const subtotal = cart.reduce((total, item) => total + item.price * item.quantity, 0);
  const eligibleByTotal = subtotal >= DISCOUNT_THRESHOLD;
  const hasDiscount = eligibleByTotal || promoActive;
  const discount = hasDiscount ? Math.round(subtotal * DISCOUNT_RATE) : 0;
  return { subtotal, discount, total: subtotal - discount, eligibleByTotal, hasDiscount };
}

function updateSummary() {
  const summary = calculateSummary();
  elements.subtotal.textContent = rupiah(summary.subtotal);
  elements.discount.textContent = `− ${rupiah(summary.discount)}`;
  elements.total.textContent = rupiah(summary.total);
  elements.discountNote.textContent = summary.eligibleByTotal ? "(10% otomatis)" : promoActive ? "(HEMAT10)" : "(min. Rp 50.000)";
  updatePayment(summary.total);
}

function updatePayment(total) {
  const payment = Number(elements.payment.value);
  elements.paymentResult.className = "payment-result neutral";
  if (!elements.payment.value) {
    elements.paymentResult.innerHTML = `<span class="result-label">Status pembayaran</span><strong>Masukkan nominal uang bayar</strong>`;
  } else if (total === 0) {
    elements.paymentResult.innerHTML = `<span class="result-label">Status pembayaran</span><strong>Tambahkan barang terlebih dahulu</strong>`;
  } else if (!Number.isFinite(payment) || payment < total) {
    const shortage = total - (Number.isFinite(payment) ? payment : 0);
    elements.paymentResult.className = "payment-result warning";
    elements.paymentResult.innerHTML = `<span class="result-label">Uang belum mencukupi</span><strong>Kurang ${rupiah(shortage)}</strong>`;
  } else {
    elements.paymentResult.className = "payment-result success";
    elements.paymentResult.innerHTML = `<span class="result-label">Kembalian</span><strong>${rupiah(payment - total)}</strong>`;
  }
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  const product = validateProduct();
  if (!product) {
    elements.formSuccess.textContent = "Periksa kembali data barang yang ditandai.";
    return;
  }

  cart.push({ id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()), ...product });
  saveCart();
  renderCart();
  elements.form.reset();
  [elements.name, elements.price, elements.quantity].forEach((input) => {
    input.classList.remove("input-invalid");
    input.removeAttribute("aria-invalid");
  });
  document.querySelectorAll(".field-error").forEach((error) => { error.textContent = ""; });
  elements.formSuccess.textContent = `${product.name} berhasil ditambahkan ke keranjang.`;
  elements.name.focus();
});

elements.cartBody.addEventListener("click", (event) => {
  const button = event.target.closest("[data-id]");
  if (!button) return;
  cart = cart.filter((item) => item.id !== button.dataset.id);
  saveCart();
  renderCart();
});

elements.payment.addEventListener("input", () => updatePayment(calculateSummary().total));

elements.applyPromo.addEventListener("click", () => {
  const code = elements.promoCode.value.trim().toUpperCase();
  if (code === "HEMAT10") {
    promoActive = true;
    elements.promoMessage.textContent = "Kode HEMAT10 aktif — diskon 10% diterapkan.";
    elements.promoMessage.className = "helper-text success";
  } else {
    promoActive = false;
    elements.promoMessage.textContent = code ? "Kode promo tidak dikenali." : "Masukkan kode promo terlebih dahulu.";
    elements.promoMessage.className = "helper-text error";
  }
  updateSummary();
});

elements.resetButton.addEventListener("click", () => {
  if (cart.length > 0 && !window.confirm("Kosongkan seluruh keranjang dan mulai transaksi baru?")) return;
  cart = [];
  promoActive = false;
  elements.promoCode.value = "";
  elements.payment.value = "";
  elements.form.reset();
  elements.formSuccess.textContent = "";
  elements.promoMessage.textContent = "Gunakan HEMAT10 untuk mengaktifkan diskon.";
  elements.promoMessage.className = "helper-text";
  try { localStorage.removeItem(STORAGE_KEY); } catch (error) { console.warn("LocalStorage tidak dapat dibersihkan.", error); }
  renderCart();
});

renderCart();
