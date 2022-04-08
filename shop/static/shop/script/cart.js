function handleClick(id, action) {
  cart = JSON.parse(localStorage.getItem("cart"));
  numItems = document.getElementById(`numItems-${id}`);
  
  if (action === "dec") {
      cart[id]--;
      numItems.innerText --;
      if(cart[id] <= 0){
        let card = document.getElementById(`card-${id}`)
        if(card) card.style.display='none'
        let emptyCart = document.getElementById('emptyCart')
        if(emptyCart){
          emptyCart.style.display = 'block';
          document.getElementById('notEmptyCart').style.display = 'none';
        }
      }
  } else {
    cart[id]++;
    numItems.innerText ++;
  }

  let price = document.getElementById(`price-${id}`)
  if(price){
    document.getElementById(`itemTotal-${id}`).innerText = price.innerText*cart[id]
    itemTotal = document.getElementsByClassName('itemTotal')
    sum = 0
    Array.prototype.forEach.call(itemTotal, (itemTot)=>{
      sum += parseInt(itemTot.innerText)
      console.log(sum)
    });
    document.getElementById('subTotal').innerText = sum
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  setTotal()
  updateCartRequest(id, action);
}

decBtns = document.getElementsByClassName("dec-button");
Array.prototype.forEach.call(decBtns, (dec) => {
  
  dec.addEventListener("click", () => {
    id = dec.dataset.item;
    
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