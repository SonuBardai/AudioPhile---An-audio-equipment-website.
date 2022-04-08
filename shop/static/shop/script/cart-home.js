btns = document.getElementsByClassName("cart-button");


document.querySelector("body").onload = function () {
  Array.prototype.forEach.call(btns, (btn) => {
    item_id = btn.dataset.item;
    if (cart[item_id]) {
      btn.style.display = "none";
      document.getElementById(`dec-${item_id}`).style.display = "block";
      document.getElementById(`inc-${item_id}`).style.display = "block";
      let numItems = document.getElementById(`numItems-${item_id}`);
      numItems.innerText = cart[item_id];
      numItems.style.display = "block";
    }
  });
};

Array.prototype.forEach.call(btns, (btn) => {
  btn.addEventListener("click", () => {
    let item_id = btn.dataset.item;
    btn.style.display = "none";
    document.getElementById(`dec-${item_id}`).style.display = "block";
    document.getElementById(`inc-${item_id}`).style.display = "block";

    if (cart[item_id]) {
      cart[item_id] += 1;
    } else {
      cart[item_id] = 1;
    }
    localStorage.setItem("cart", JSON.stringify(cart));

    let numItems = document.getElementById(`numItems-${item_id}`);
    numItems.innerText = cart[item_id];
    numItems.style.display = "block";
    
    setTotal()
    
    updateCartRequest(item_id, 'inc')
  });
});

dec_btns = document.getElementsByClassName("dec-button");
Array.prototype.forEach.call(dec_btns, (btn) => {
  btn.addEventListener("click", () => {
    item_id = btn.dataset.item;
    cart[item_id]--;
    if (cart[item_id] <= 0) {
      cart[item_id] = 0;
      document.getElementById(`cart-${item_id}`).style.display = "block";
      document.getElementById(`dec-${item_id}`).style.display = "none";
      document.getElementById(`inc-${item_id}`).style.display = "none";
      let numItems = document.getElementById(`numItems-${item_id}`);
      numItems.style.display = "none";
    }
    localStorage.setItem("cart", JSON.stringify(cart));
    let numItems = document.getElementById(`numItems-${item_id}`);
    numItems.innerText = cart[item_id];

    setTotal()
    
    updateCartRequest(item_id, 'dec')
  });
});

inc_btns = document.getElementsByClassName("inc-button");
Array.prototype.forEach.call(inc_btns, (btn) => {
  btn.addEventListener("click", () => {
    item_id = btn.dataset.item;
    cart[item_id]++;
    localStorage.setItem("cart", JSON.stringify(cart));
    let numItems = document.getElementById(`numItems-${item_id}`);
    numItems.innerText = cart[item_id];
    
    setTotal()
    
    updateCartRequest(item_id, 'inc')
  });
});