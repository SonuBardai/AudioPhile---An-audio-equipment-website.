btn.addEventListener("click", () => {
  numItems.style.display = "block";
  dec.style.display = "block";
  inc.style.display = "block";
  btn.style.display = "none";

  item = 1;
  numItems.innerText = item;
  cart[id] = item;
  localStorage.setItem('cart', JSON.stringify(cart));

  totalItems++;
  document.getElementById("totalItems").innerText = `(${totalItems})`;
  updateCartRequest(item_id, "inc")
});

inc.addEventListener("click", () => {
  item++;
  numItems.innerText = item;
  cart[id] = item;
  localStorage.setItem('cart', JSON.stringify(cart));

  totalItems++;
  document.getElementById("totalItems").innerText = `(${totalItems})`;
  updateCartRequest(item_id, "inc")
});

dec.addEventListener("click", () => {
  item--;
  if (item) {
    numItems.innerText = item;
  } else {
    btn.style.display = "block";
    dec.style.display = "none";
    inc.style.display = "none";
    numItems.style.display = "none";
  }
  cart[id] = item;
  localStorage.setItem('cart', JSON.stringify(cart));

  totalItems--;
  document.getElementById("totalItems").innerText = `(${totalItems})`;  
  updateCartRequest(item_id, "dec")
});