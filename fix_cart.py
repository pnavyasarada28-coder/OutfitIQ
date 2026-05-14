import sys

with open('d:/outfit_iq/outfit_iq/templates/cart.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """            // Fetch all products
            try {
                const response = await fetch("http://127.0.0.1:8000/api/products/");
                const data = await response.json();
                const allProducts = data.results;

                for (let i = 0; i < cartIds.length; i++) {
                    const id = cartIds[i];
                    const product = allProducts.find(p => p.id === id);
                    if (product) {
                        total += parseFloat(product.price);
                        itemsHtml += `
                            <div class="cart-item">
                                <img src="${getImageUrl(product.image)}" alt="${product.title}">
                                <div class="cart-item-info">
                                    <div class="cart-item-title">${product.title}</div>
                                    <div class="cart-item-price">₹${product.price}</div>
                                </div>
                                <button class="remove-btn" onclick="removeFromCart(${i})">Remove</button>
                            </div>
                        `;
                    }
                }
                
                cartItemsContainer.innerHTML = itemsHtml;
                cartTotalEl.innerText = `Total: ₹${total}`;
                cartTotalEl.style.display = 'block';
                checkoutBtn.style.display = 'block';
            } catch(e) {
                cartItemsContainer.innerHTML = 'Error loading cart.';
            }"""

new_logic = """            // Fetch products individually
            try {
                for (let i = 0; i < cartIds.length; i++) {
                    const id = cartIds[i];
                    const response = await fetch(`http://127.0.0.1:8000/api/products/${id}/`);
                    if (response.ok) {
                        const product = await response.json();
                        total += parseFloat(product.price);
                        itemsHtml += `
                            <div class="cart-item">
                                <img src="${getImageUrl(product.image)}" alt="${product.title}">
                                <div class="cart-item-info">
                                    <div class="cart-item-title">${product.title}</div>
                                    <div class="cart-item-price">₹${product.price}</div>
                                </div>
                                <button class="remove-btn" onclick="removeFromCart(${i})">Remove</button>
                            </div>
                        `;
                    }
                }
                
                cartItemsContainer.innerHTML = itemsHtml;
                cartTotalEl.innerText = `Total: ₹${total}`;
                cartTotalEl.style.display = 'block';
                checkoutBtn.style.display = 'block';
            } catch(e) {
                cartItemsContainer.innerHTML = 'Error loading cart.';
            }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    
    # Also update ?v=7 to ?v=8 to force browser cache flush
    content = content.replace('?v=7', '?v=8')

    with open('d:/outfit_iq/outfit_iq/templates/cart.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Success')
else:
    print('Failed to find old logic')
