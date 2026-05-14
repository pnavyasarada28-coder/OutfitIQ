import sys

with open('d:/outfit_iq/outfit_iq/static/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix getImageUrl
content = content.replace(
'''function getImageUrl(path) {
    if (!path) return '';
    return path.startsWith('http') ? path : `${API_BASE_URL}${path}`;
}''',
'''function getImageUrl(path) {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    if (path.startsWith('/')) return `${API_BASE_URL}${path}`;
    if (path.startsWith('media/')) return `${API_BASE_URL}/${path}`;
    return `${API_BASE_URL}/media/${path}`;
}'''
)

# Fix pagination and fetchProducts
content = content.replace(
'''let currentProductsUrl = "http://127.0.0.1:8000/api/products/";

async function fetchProducts(url = currentProductsUrl) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        
        displayProducts(data.results);
        displayPagination(data.previous, data.next, data.count);
    } catch(error) {
        console.log(error);
    }
}

/* PAGINATION DISPLAY */
function displayPagination(prevUrl, nextUrl, totalCount) {
    const paginationContainer = document.getElementById("paginationContainer");
    if (!paginationContainer) return;
    
    paginationContainer.innerHTML = `
        <button class="pagination-btn" ${!prevUrl ? 'disabled' : ''} onclick="fetchProducts('${prevUrl}')">← Previous</button>
        <span class="pagination-info">Total Products: ${totalCount || 0}</span>
        <button class="pagination-btn" ${!nextUrl ? 'disabled' : ''} onclick="fetchProducts('${nextUrl}')">Next →</button>
    `;
}''',
'''let currentProductsUrl = "http://127.0.0.1:8000/api/products/";
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
    
    const pageSize = 5;
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
}'''
)

# Fix Markdown cleanup
content = content.replace(
'''                // Simple markdown link parser for bot responses
                let botResponse = data.response.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" style="color: #ff3f6c; text-decoration: underline;">$1</a>');
                
                // Allow line breaks
                botResponse = botResponse.replace(/\\n/g, '<br>');''',
'''                // Simple markdown link parser for bot responses
                let botResponse = data.response.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" style="color: #ff3f6c; text-decoration: underline;">$1</a>');
                
                // Strip bold/italic markdown
                botResponse = botResponse.replace(/\\*\\*(.*?)\\*\\*/g, '$1');
                botResponse = botResponse.replace(/\\*/g, '');
                
                // Allow line breaks
                botResponse = botResponse.replace(/\\n/g, '<br>');'''
)

with open('d:/outfit_iq/outfit_iq/static/js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
