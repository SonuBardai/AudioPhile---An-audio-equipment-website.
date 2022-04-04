function handleClick(id, action) {
  cart = JSON.parse(localStorage.getItem("cart"));
  numItems = document.getElementById(`numItems-${id}`);
  console.log(numItems);
  
  if (action === "dec") {
      cart[id]--;
      numItems.innerText --;
      if(!cart[id]){
        switchButtons()
        let card = document.getElementById(`card-${id}`)
        if(card) card.style.display='none'
      }
  } else {
    cart[id]++;
    numItems.innerText ++;
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  setTotal()
  updateCartRequest(id, action);
}

decBtns = document.getElementsByClassName("dec-button");
Array.prototype.forEach.call(decBtns, (dec) => {
  
  dec.addEventListener("click", () => {
    id = dec.dataset.item;
    console.log(id);
    
    handleClick(id, "dec");
  });
});

incBtns = document.getElementsByClassName("inc-button");
Array.prototype.forEach.call(incBtns, (inc) => {
  
  inc.addEventListener("click", () => {
    id = inc.dataset.item;
    handleClick(id, "inc");
  });
});