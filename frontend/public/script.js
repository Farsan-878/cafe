// Use local API in development, Render backend in production
const API_BASE_URL = window.location.hostname === 'localhost'
    ? '/api'
    : 'https://cafe-backend.onrender.com/api'; // Replace with your actual Render URL

const apiBase = API_BASE_URL;

const state = {
    menuItems: [],
    staffMembers: [],
};

const menuList = document.getElementById('menuList');
const inventoryList = document.getElementById('inventoryList');
const reviewList = document.getElementById('reviewList');
const serviceBoySelect = document.getElementById('serviceBoySelect');
const orderItems = document.getElementById('orderItems');
const orderRowTemplate = document.getElementById('orderRowTemplate');

const menuForm = document.getElementById('menuForm');
const staffForm = document.getElementById('staffForm');
const reviewForm = document.getElementById('reviewForm');
const orderForm = document.getElementById('orderForm');

const menuMessage = document.getElementById('menuMessage');
const staffMessage = document.getElementById('staffMessage');
const reviewMessage = document.getElementById('reviewMessage');
const orderMessage = document.getElementById('orderMessage');

// Shared helpers for showing API feedback.
function showMessage(target, text, isSuccess = false) {
    target.textContent = text;
    target.classList.toggle('success-message', isSuccess);
}

function clearMessage(target) {
    target.textContent = '';
    target.classList.remove('success-message');
}

// Wrapper around fetch so each API call gets the same JSON handling.
async function fetchJson(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {}),
        },
        ...options,
    });

    const payload = await response.json();

    if (!response.ok || payload.success === false) {
        throw new Error(payload.message || 'Something went wrong.');
    }

    return payload;
}

// Render helpers for each dashboard section.
function renderEmptyState(container, text) {
    container.innerHTML = `<div class="empty-state">${text}</div>`;
}

function renderMenu() {
    if (!state.menuItems.length) {
        renderEmptyState(menuList, 'No menu items available yet. Add one from the form below.');
        return;
    }

    menuList.innerHTML = state.menuItems
        .map(
            (item) => `
            <article class="menu-card">
                <h3>${item.name}</h3>
                <p class="price">₹${Number(item.price).toFixed(2)}</p>
                <p>Quantity: ${item.quantity}</p>
                <span class="badge ${item.available && item.quantity > 0 ? '' : 'unavailable'}">
                    ${item.available && item.quantity > 0 ? 'Available' : 'Unavailable'}
                </span>
            </article>
        `,
        )
        .join('');
}

function renderInventory(items) {
    if (!items.length) {
        renderEmptyState(inventoryList, 'Inventory is empty.');
        return;
    }

    inventoryList.innerHTML = items
        .map(
            (item) => `
            <article class="inventory-item">
                <strong>${item.name}</strong>
                <p>Stock: ${item.quantity}</p>
                <p>Status: ${item.available ? 'Available' : 'Unavailable'}</p>
            </article>
        `,
        )
        .join('');
}

function renderReviews(reviews) {
    if (!reviews.length) {
        renderEmptyState(reviewList, 'No reviews yet.');
        return;
    }

    reviewList.innerHTML = reviews
        .slice()
        .reverse()
        .map(
            (review) => `
            <article class="review-card">
                <div class="rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</div>
                <p>${review.comment}</p>
                <p><small>${review.created_at ? new Date(review.created_at).toLocaleString() : ''}</small></p>
            </article>
        `,
        )
        .join('');
}

function renderStaffDropdown() {
    serviceBoySelect.innerHTML = state.staffMembers.length
        ? state.staffMembers.map((staff) => `<option value="${staff.name}">${staff.name}</option>`).join('')
        : '<option value="">Add staff first</option>';
}

function buildOrderSelectOptions(selectElement) {
    selectElement.innerHTML = state.menuItems.length
        ? state.menuItems
              .map(
                  (item) =>
                      `<option value="${item.id}">${item.name} - ₹${Number(item.price).toFixed(2)} (${item.available && item.quantity > 0 ? 'Available' : 'Unavailable'})</option>`,
              )
              .join('')
        : '<option value="">No menu items available</option>';
}

function createOrderRow() {
    const fragment = orderRowTemplate.content.cloneNode(true);
    const row = fragment.querySelector('.order-row');
    const select = fragment.querySelector('.order-menu-select');
    const removeButton = fragment.querySelector('.remove-row-button');

    buildOrderSelectOptions(select);

    removeButton.addEventListener('click', () => {
        if (orderItems.children.length > 1) {
            row.remove();
        }
    });

    return fragment;
}

function ensureOrderRow() {
    if (!orderItems.children.length) {
        orderItems.appendChild(createOrderRow());
    }
}

// Data loaders keep the dashboard in sync after each action.
async function loadMenu() {
    const response = await fetchJson(`${apiBase}/menu`);
    state.menuItems = response.data;
    renderMenu();
    buildOrderSelectOptionsForAllRows();
    return response.data;
}

async function loadInventory() {
    const response = await fetchJson(`${apiBase}/inventory`);
    renderInventory(response.data);
}

async function loadStaff() {
    const response = await fetchJson(`${apiBase}/staff`);
    state.staffMembers = response.data;
    renderStaffDropdown();
}

async function loadReviews() {
    const response = await fetchJson(`${apiBase}/reviews`);
    renderReviews(response.data);
}

function buildOrderSelectOptionsForAllRows() {
    const selects = orderItems.querySelectorAll('.order-menu-select');
    selects.forEach((select) => buildOrderSelectOptions(select));
}

async function refreshDashboard() {
    await Promise.all([loadMenu(), loadInventory(), loadStaff(), loadReviews()]);
    ensureOrderRow();
}

// Form handlers for menu, staff, reviews, and orders.
menuForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearMessage(menuMessage);

    const formData = new FormData(menuForm);
    const payload = {
        name: formData.get('name'),
        price: formData.get('price'),
        quantity: formData.get('quantity'),
        available: formData.get('available') === 'on',
    };

    try {
        await fetchJson(`${apiBase}/menu`, {
            method: 'POST',
            body: JSON.stringify(payload),
        });
        menuForm.reset();
        menuForm.querySelector('[name="quantity"]').value = 10;
        menuForm.querySelector('[name="available"]').checked = true;
        showMessage(menuMessage, 'Menu item added successfully.', true);
        await refreshDashboard();
    } catch (error) {
        showMessage(menuMessage, error.message);
    }
});

staffForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearMessage(staffMessage);

    const formData = new FormData(staffForm);

    try {
        await fetchJson(`${apiBase}/staff`, {
            method: 'POST',
            body: JSON.stringify({ name: formData.get('name') }),
        });
        staffForm.reset();
        showMessage(staffMessage, 'Staff member added successfully.', true);
        await loadStaff();
    } catch (error) {
        showMessage(staffMessage, error.message);
    }
});

reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearMessage(reviewMessage);

    const formData = new FormData(reviewForm);

    try {
        await fetchJson(`${apiBase}/reviews`, {
            method: 'POST',
            body: JSON.stringify({
                rating: formData.get('rating'),
                comment: formData.get('comment'),
            }),
        });
        reviewForm.reset();
        reviewForm.querySelector('[name="rating"]').value = '5';
        showMessage(reviewMessage, 'Review added successfully.', true);
        await loadReviews();
    } catch (error) {
        showMessage(reviewMessage, error.message);
    }
});

orderForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearMessage(orderMessage);

    const serviceBoyName = serviceBoySelect.value;
    const rows = Array.from(orderItems.querySelectorAll('.order-row'));
    const items = rows.map((row) => ({
        menu_item_id: Number(row.querySelector('.order-menu-select').value),
        quantity: Number(row.querySelector('.order-quantity-input').value),
    }));

    try {
        const response = await fetchJson(`${apiBase}/orders`, {
            method: 'POST',
            body: JSON.stringify({ service_boy_name: serviceBoyName, items }),
        });

        const order = response.data;
        showMessage(
            orderMessage,
            `Order #${order.id} placed successfully. Total: ₹${Number(order.total_price).toFixed(2)}. Assigned to ${order.service_boy_name}.`,
            true,
        );
        orderForm.reset();
        ensureOrderRow();
        await refreshDashboard();
    } catch (error) {
        showMessage(orderMessage, error.message);
    }
});

orderItems.addEventListener('click', (event) => {
    if (event.target.classList.contains('remove-row-button')) {
        if (orderItems.children.length > 1) {
            event.target.closest('.order-row').remove();
        }
    }
});

document.getElementById('addOrderRowBtn').addEventListener('click', () => {
    orderItems.appendChild(createOrderRow());
});

document.getElementById('refreshMenuBtn').addEventListener('click', async () => {
    await loadMenu();
    await loadInventory();
});

document.getElementById('refreshReviewsBtn').addEventListener('click', loadReviews);

// Initial dashboard load.
async function boot() {
    ensureOrderRow();
    await refreshDashboard();
}

boot().catch((error) => {
    console.error(error);
    showMessage(orderMessage, 'Unable to load dashboard data.');
});
