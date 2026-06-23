const stripeData = document.getElementById("stripe-data");
const publicKey = stripeData.dataset.publicKey;
const clientSecret = stripeData.dataset.clientSecret;
const successUrl = stripeData.dataset.successUrl;
const csrfToken = stripeData.dataset.csrfToken;

const stripe = Stripe(publicKey);
const elements = stripe.elements({ locale: "en-GB" });
const card = elements.create("card", {
  hidePostalCode: true,
});
card.mount("#card-element");

card.on("change", function (event) {
  const display = document.getElementById("card-errors");
  display.textContent = event.error ? event.error.message : "";
});

const form = document.getElementById("payment-form");
form.addEventListener("submit", async function (e) {
  e.preventDefault();
  document.getElementById("submit-btn").disabled = true;

  const response = await fetch("", {
    method: "POST",
    headers: { "X-CSRFToken": csrfToken },
  });
  const data = await response.json();

  const result = await stripe.confirmCardPayment(data.client_secret, {
    payment_method: { card: card },
  });

  if (result.error) {
    document.getElementById("card-errors").textContent = result.error.message;
    document.getElementById("submit-btn").disabled = false;
  } else {
    window.location.href =
      successUrl + "?payment_intent=" + result.paymentIntent.id;
  }
});
