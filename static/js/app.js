const API_BASE_URL = "http://127.0.0.1:8000";

function getImageUrl(path) {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    if (path.startsWith('/')) return `${API_BASE_URL}${path}`;
    if (path.startsWith('media/')) return `${API_BASE_URL}/${path}`;
    return `${API_BASE_URL}/media/${path}`;
}

const productsContainer =
document.getElementById(
    "productsContainer"
);

/* FETCH PRODUCTS */

let currentProductsUrl = "http://127.0.0.1:8000/api/products/";
let currentPage = 1;

async function fetchProducts(url = currentProductsUrl, page = 1) {
    try {
        let fetchUrl = url;
        if (!url.includes('page=')) {
            fetchUrl = url.includes('?') ? `${url}&page=${page}` : `${url}?page=${page}`;
        } else {
            fetchUrl = url.replace(/page=\d+/, `page=${page}`);
        }
        const response = await fetch(fetchUrl);
        const data = await response.json();
        
        currentPage = data.page || page;
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            heroSection.style.display = currentPage > 1 ? 'none' : 'block';
        }
        displayProducts(data.results);
        displayPagination(data.count, currentPage, url.replace(/page=\d+&?/, '').replace(/\?$/, ''));
    } catch(error) {
        console.log(error);
    }
}

/* PAGINATION DISPLAY */
function displayPagination(totalCount, currentPage, baseUrl) {
    const paginationContainer = document.getElementById("paginationContainer");
    if (!paginationContainer) return;
    
    const pageSize = 8;
    const totalPages = Math.ceil(totalCount / pageSize);
    
    if (totalCount === 0 || totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }
    
    const prevDisabled = currentPage <= 1 ? 'disabled' : '';
    const nextDisabled = currentPage >= totalPages ? 'disabled' : '';
    
    paginationContainer.innerHTML = `
        <button class="pagination-btn" ${prevDisabled} onclick="fetchProducts('${baseUrl}', ${currentPage - 1})">← Previous</button>
        <span class="pagination-info">Page ${currentPage} of ${totalPages}</span>
        <button class="pagination-btn" ${nextDisabled} onclick="fetchProducts('${baseUrl}', ${currentPage + 1})">Next →</button>
    `;
}

/* DISPLAY PRODUCTS */

function displayProducts(products) {

    if(!productsContainer) {

        return;
    }

    productsContainer.innerHTML = "";

    products.forEach(product => {

        const productCard = `

        <div class="product-card">

            <img src="${getImageUrl(product.image)}" />

            <div class="product-info">

                <a href="/product/${product.id}/">

                    <div class="product-title">

                        ${product.title}

                    </div>

                </a>

                <div class="product-price">

                    ₹${product.price}

                </div>

                <button
                    class="add-cart-btn"
                    onclick="addToCart(${product.id})"
                >

                    Add To Bag

                </button>

            </div>

        </div>
        `;

        productsContainer.innerHTML +=
        productCard;
    });
}

/* ADD TO CART */

async function addToCart(productId) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert('Please login to add items to your bag');
        window.location.href = '/login/';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/cart/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ product_id: productId })
        });

        if (response.ok) {
            alert('Product added to bag!');
        } else if (response.status === 401) {
            alert('Session expired. Please login again.');
            localStorage.removeItem('access_token');
            window.location.href = '/login/';
        } else {
            const data = await response.json();
            alert(data.error || 'Failed to add product to bag.');
        }
    } catch(err) {
        console.error('Error adding to bag:', err);
        alert('Network error. Could not add product.');
    }
}

/* SEARCH */

const searchBtn =
document.getElementById(
    "searchBtn"
);

if(searchBtn) {

    searchBtn.addEventListener(

        "click",

        async () => {
            const searchValue = document.getElementById("searchInput").value;
            fetchProducts(`http://127.0.0.1:8000/api/products/?search=${searchValue}`);
        }
    );
}

/* CHATBOT */

const chatbotIcon =
document.getElementById(
    "chatbotIcon"
);

const chatbotContainer =
document.getElementById(
    "chatbotContainer"
);

if(chatbotIcon) {

    chatbotIcon.addEventListener(

        "click",

        () => {

            if(

                chatbotContainer.style.display
                === "block"

            ) {

                chatbotContainer.style.display =
                "none";
            }

            else {

                chatbotContainer.style.display =
                "block";
            }
        }
    );
}

const closeChatBtn = document.getElementById("closeChatBtn");

if(closeChatBtn) {
    closeChatBtn.addEventListener("click", () => {
        chatbotContainer.style.display = "none";
    });
}

const sendBtn =
document.getElementById(
    "sendBtn"
);

const chatInput =
document.getElementById(
    "chatInput"
);

const chatMessages =
document.getElementById(
    "chatMessages"
);

if(sendBtn) {

    sendBtn.addEventListener(

        "click",

        async () => {

            const userMessage =
            chatInput.value;

            if(!userMessage.trim()) {

                return;
            }

            appendMessage(
                userMessage,
                "user-message"
            );

            chatInput.value = "";

            try {

                const response = await fetch(

                    "http://127.0.0.1:8000/api/chatbot/",

                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                            "application/json"
                        },

                        body: JSON.stringify({

                            query: userMessage
                        })
                    }
                );

                const data =
                await response.json();

                // Simple markdown link parser for bot responses
                let botResponse = data.response.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" style="color: #ff3f6c; text-decoration: underline;">$1</a>');
                
                // Strip bold/italic markdown
                botResponse = botResponse.replace(/\*\*(.*?)\*\*/g, '$1');
                botResponse = botResponse.replace(/\*/g, '');
                
                // Allow line breaks
                botResponse = botResponse.replace(/\n/g, '<br>');

                appendMessage(

                    botResponse,

                    "bot-message"
                );
            }

            catch(error) {

                appendMessage(

                    "Fashion Assistant unavailable",

                    "bot-message"
                );
            }
        }
    );
}

/* APPEND MESSAGE */

function appendMessage(
    message,
    className
) {

    const messageDiv =
    document.createElement("div");

    messageDiv.classList.add(

        "chat-message",
        className
    );

    messageDiv.innerHTML =
    message;

    chatMessages.appendChild(
        messageDiv
    );
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* AUTH STATE & NAVBAR */

function updateNavbarAuth() {
    const username = localStorage.getItem('username');
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;

    // Check if we are on the login page (don't overwrite login page navbar or just keep it simple)
    if (window.location.pathname === '/login/') return;

    if (username) {
        navLinks.innerHTML = `
            <a href="/cart/"><button style="padding: 10px 20px; border: none; border-radius: 8px; background: #ff3f6c; color: white; cursor: pointer; margin-right: 10px;">Bag</button></a>
            <span style="font-weight: bold; margin-right: 15px; color: #333;">Welcome, ${username}</span>
            <button onclick="logout()" style="padding: 10px 20px; border: 1px solid #ff3f6c; border-radius: 8px; background: white; color: #ff3f6c; cursor: pointer;">Logout</button>
        `;
    } else {
        navLinks.innerHTML = `
            <a href="/cart/"><button style="padding: 10px 20px; border: none; border-radius: 8px; background: #ff3f6c; color: white; cursor: pointer; margin-right: 10px;">Bag</button></a>
            <a href="/login/"><button style="padding: 10px 20px; border: none; border-radius: 8px; background: #ff3f6c; color: white; cursor: pointer;">Login</button></a>
        `;
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    updateNavbarAuth();
    if(window.location.pathname !== '/') {
        window.location.href = '/';
    }
}

/* INITIAL LOAD */

updateNavbarAuth();
fetchProducts();
