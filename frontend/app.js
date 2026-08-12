const API_URL = "http://127.0.0.1:8000";

/* =========================
   GLOBAL VARIABLES
========================= */

let token = localStorage.getItem("token");
let currentRole = localStorage.getItem("role") || "";
let currentName = localStorage.getItem("userName") || "";

let allProducts = [];
let allCategories = [];
let allSuppliers = [];
let allPurchases = [];
let allSales = [];


/* =========================
   AUTH HEADERS
========================= */

function getHeaders() {
    return {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };
}


/* =========================
   ROLE PERMISSIONS
========================= */

const ROLE_PERMS = {
    "products": {
        create: ["Admin"],
        update: ["Admin", "Inventory Manager"],
        delete: ["Admin"]
    },
    "categories": {
        create: ["Admin"],
        update: ["Admin", "Inventory Manager"],
        delete: ["Admin"]
    },
    "suppliers": {
        create: ["Admin", "Inventory Manager"],
        update: ["Admin", "Inventory Manager"],
        delete: ["Admin"]
    },
    "purchases": {
        create: ["Admin", "Inventory Manager"],
        update: ["Admin", "Inventory Manager"],
        delete: ["Admin"]
    },
    "sales": {
        create: ["Admin", "Sales Executive"],
        update: ["Admin", "Sales Executive"],
        delete: ["Admin"]
    }
};

function canDo(action, module) {
    const perms = ROLE_PERMS[module];
    if (!perms || !perms[action]) return false;
    return perms[action].includes(currentRole);
}


/* =========================
   MODAL HELPERS
========================= */

let modalState = {
    module: null,
    id: null,
    submitHandler: null
};

function openModal(title) {
    document.getElementById("modal-title").textContent = title;
    document.getElementById("modal-body").innerHTML = "";
    document.getElementById("modal-error").textContent = "";
    document.getElementById("modal").classList.remove("hidden");
}

function closeModal() {
    document.getElementById("modal").classList.add("hidden");
    modalState = {
        module: null,
        id: null,
        submitHandler: null
    };
}

function showModalError(message) {
    document.getElementById("modal-error").textContent = message;
}

function fieldHTML({
    label,
    name,
    type = "text",
    value = "",
    required = false,
    placeholder = "",
    options = null,
    min = null,
    max = null,
    step = null
}) {
    let input = "";

    if (options) {

        input = `
            <select
                id="${name}"
                name="${name}"
                ${required ? "required" : ""}
            >
                ${options.map(option => `
                    <option
                        value="${option.value}"
                        ${String(option.value) === String(value) ? "selected" : ""}
                    >
                        ${option.label}
                    </option>
                `).join("")}
            </select>
        `;

    } else if (type === "textarea") {

        input = `
            <textarea
                id="${name}"
                name="${name}"
                placeholder="${placeholder}"
                ${required ? "required" : ""}
            >${value}</textarea>
        `;

    } else {

        input = `
            <input
                type="${type}"
                id="${name}"
                name="${name}"
                value="${value}"
                placeholder="${placeholder}"
                ${min !== null ? `min="${min}"` : ""}
                ${max !== null ? `max="${max}"` : ""}
                ${step !== null ? `step="${step}"` : ""}
                ${required ? "required" : ""}
            >
        `;

    }

    return `
        <div class="form-group">
            <label for="${name}">${label}</label>
            ${input}
        </div>
    `;
}

function collectField(name) {
    const element = document.getElementById(name);
    if (!element) return null;
    return element.value;
}

document
    .getElementById("modal-form")
    .addEventListener("submit", async function (event) {

        event.preventDefault();

        if (!modalState.submitHandler) {
            return;
        }

        await modalState.submitHandler();

    });


/* =========================
   LOGIN
========================= */

document
    .getElementById("login-form")
    .addEventListener("submit", async function (event) {

        event.preventDefault();

        const email =
            document.getElementById("email").value.trim();

        const password =
            document.getElementById("password").value;

        const selectedRole =
            document.getElementById("role").value;

        const message =
            document.getElementById("login-message");

        message.textContent = "";


        if (!selectedRole) {
            message.textContent = "Please select a role.";
            return;
        }


        try {

            const response = await fetch(
                `${API_URL}/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                message.textContent =
                    data.detail || "Login failed.";

                return;
            }


            /* Store JWT */

            token = data.access_token;

            localStorage.setItem(
                "token",
                token
            );


            /*
             * IMPORTANT
             *
             * Your JWT contains:
             * sub
             * email
             * role
             *
             * Decode role from JWT instead of
             * blindly trusting dropdown.
             */

            const payload =
                decodeJWT(token);


            if (payload && payload.role) {

                currentRole = payload.role;

            } else {

                currentRole = selectedRole;

            }


            if (payload && payload.name) {

                currentName = payload.name;

            }


            localStorage.setItem(
                "role",
                currentRole
            );

            localStorage.setItem(
                "userName",
                currentName
            );


            console.log(
                "Logged in role:",
                currentRole
            );


            showApplication();


        } catch (error) {

            console.error(
                "Login error:",
                error
            );

            message.textContent =
                "Cannot connect to FastAPI server.";

        }

    });


/* =========================
   DECODE JWT
========================= */

function decodeJWT(token) {

    try {

        const parts = token.split(".");

        if (parts.length !== 3) {
            return null;
        }

        const payload =
            parts[1]
                .replace(/-/g, "+")
                .replace(/_/g, "/");

        const decoded =
            atob(payload);

        return JSON.parse(decoded);

    } catch (error) {

        console.error(
            "JWT decode error:",
            error
        );

        return null;
    }
}


/* =========================
   SHOW APPLICATION
========================= */

function showApplication() {

    document
        .getElementById("login-page")
        .classList.add("hidden");


    document
        .getElementById("app")
        .classList.remove("hidden");


    document
        .getElementById("user-role")
        .textContent =
            currentRole;


    const userNameEl =
        document.getElementById(
            "user-name"
        );

    if (userNameEl) {

        userNameEl.textContent =
            currentName
                ? `Welcome, ${currentName}`
                : "Welcome";
    }


    applyRolePermissions();

    loadDashboard();
}


/* =========================
   ROLE PERMISSIONS
========================= */

function applyRolePermissions() {

    const purchaseButton =
        document.querySelector(
            "button[onclick=\"showSection('purchases-section')\"]"
        );


    const salesButton =
        document.querySelector(
            "button[onclick=\"showSection('sales-section')\"]"
        );


    const supplierButton =
        document.querySelector(
            "button[onclick=\"showSection('suppliers-section')\"]"
        );


    /*
     * SALES EXECUTIVE
     */

    if (currentRole === "Sales Executive") {

        /*
         * Cannot access purchases or suppliers
         */

        if (purchaseButton) {
            purchaseButton.style.display = "none";
        }

        if (supplierButton) {
            supplierButton.style.display = "none";
        }

    }


    /*
     * INVENTORY MANAGER
     */

    if (currentRole === "Inventory Manager") {

        /*
         * Cannot access sales
         */

        if (salesButton) {
            salesButton.style.display = "none";
        }

    }


    /*
     * ADMIN
     */

    if (currentRole === "Admin") {

        /*
         * Admin sees everything
         */

        if (purchaseButton) {
            purchaseButton.style.display = "";
        }

        if (salesButton) {
            salesButton.style.display = "";
        }

        if (supplierButton) {
            supplierButton.style.display = "";
        }

    }


    /*
     * ADD / EDIT / DELETE BUTTONS
     */

    const addButtons = {
        products: "add-product-btn",
        categories: "add-category-btn",
        suppliers: "add-supplier-btn",
        purchases: "add-purchase-btn",
        sales: "add-sale-btn"
    };

    Object.keys(addButtons).forEach(module => {

        const button =
            document.getElementById(
                addButtons[module]
            );

        if (!button) {
            return;
        }

        button.style.display =
            canDo("create", module)
                ? ""
                : "none";

    });
}


/* =========================
   NAVIGATION
========================= */

function showSection(sectionId) {

    document
        .querySelectorAll(".section")
        .forEach(section => {

            section.classList.add("hidden");

        });


    const section =
        document.getElementById(sectionId);


    if (section) {

        section.classList.remove("hidden");

    }


    /*
     * Active menu
     */

    document
        .querySelectorAll(".nav-item")
        .forEach(button => {

            button.classList.remove("active");

        });


    const clickedButton =
        [...document.querySelectorAll(".nav-item")]
            .find(button =>
                button
                    .getAttribute("onclick")
                    ?.includes(sectionId)
            );


    if (clickedButton) {
        clickedButton.classList.add("active");
    }


    /*
     * Load data
     */

    if (sectionId === "dashboard-section") {
        loadDashboard();
    }

    if (sectionId === "products-section") {
        loadProducts();
    }

    if (sectionId === "categories-section") {
        loadCategories();
    }

    if (sectionId === "suppliers-section") {
        loadSuppliers();
    }

    if (sectionId === "purchases-section") {
        loadPurchases();
    }

    if (sectionId === "sales-section") {
        loadSales();
    }
}


/* =========================
   PRODUCTS
========================= */

async function loadProducts() {

    try {

        const response =
            await fetch(
                `${API_URL}/product/all_products`,
                {
                    method: "GET",
                    headers: getHeaders()
                }
            );


        if (!response.ok) {

            console.error(
                "Products:",
                response.status,
                await response.text()
            );

            return;
        }


        const products =
            await response.json();

        allProducts = products;


        const table =
            document.getElementById(
                "products-table"
            );


        table.innerHTML = "";


        if (products.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="7">
                        No products found.
                    </td>
                </tr>
            `;

            return;
        }


        products.forEach(product => {

            table.innerHTML += `
                <tr>
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.sku}</td>
                    <td>₹${product.price}</td>
                    <td>${product.quantity}</td>
                    <td>${product.category_id}</td>
                    <td class="actions-cell">
                        ${canDo("update", "products") ? `<button class="edit-btn" onclick="openProductForm(${product.id})">Edit</button>` : ""}
                        ${canDo("delete", "products") ? `<button class="delete-btn" onclick="deleteProduct(${product.id})">Delete</button>` : ""}
                    </td>
                </tr>
            `;

        });

    } catch (error) {

        console.error(
            "Product error:",
            error
        );

    }
}


/* =========================
   PRODUCT CRUD
========================= */

function openProductForm(id = null) {

    if (id && !canDo("update", "products")) return;
    if (!id && !canDo("create", "products")) return;

    const product =
        id
            ? allProducts.find(p => p.id === id)
            : null;

    const categoryOptions = allCategories.map(category => ({
        value: category.id,
        label: category.name
    }));

    categoryOptions.unshift({
        value: "",
        label: allCategories.length === 0
            ? "No categories available"
            : "Select category"
    });

    openModal(id ? "Edit Product" : "Add Product");

    document.getElementById("modal-body").innerHTML =
        fieldHTML({
            label: "Name",
            name: "p-name",
            value: product?.name || "",
            required: true
        }) +
        fieldHTML({
            label: "Description",
            name: "p-desc",
            type: "textarea",
            value: product?.description || ""
        }) +
        fieldHTML({
            label: "SKU",
            name: "p-sku",
            value: product?.sku || "",
            required: true
        }) +
        fieldHTML({
            label: "Price (₹)",
            name: "p-price",
            type: "number",
            min: "0",
            step: "0.01",
            value: product?.price ?? "",
            required: true
        }) +
        fieldHTML({
            label: "Quantity",
            name: "p-qty",
            type: "number",
            min: "0",
            value: product?.quantity ?? "",
            required: true
        }) +
        fieldHTML({
            label: "Category",
            name: "p-category",
            options: categoryOptions,
            value: product?.category_id ?? "",
            required: true
        });

    modalState.module = "products";
    modalState.id = id;
    modalState.submitHandler = saveProduct;
}

async function saveProduct() {

    const payload = {
        name: collectField("p-name"),
        description: collectField("p-desc") || null,
        sku: collectField("p-sku"),
        price: parseFloat(collectField("p-price")),
        quantity: parseInt(collectField("p-qty"), 10),
        category_id: parseInt(collectField("p-category"), 10)
    };

    const id = modalState.id;

    try {

        const response =
            await fetch(
                id
                    ? `${API_URL}/product/update/product/${id}`
                    : `${API_URL}/product/create`,
                {
                    method: id ? "PUT" : "POST",
                    headers: getHeaders(),
                    body: JSON.stringify(payload)
                }
            );

        if (!response.ok) {

            const data =
                await response.json().catch(() => ({}));

            showModalError(
                data.detail || "Failed to save product."
            );

            return;
        }

        closeModal();
        loadProducts();

    } catch (error) {

        console.error(
            "Save product error:",
            error
        );

        showModalError(
            "Cannot connect to server."
        );

    }
}

async function deleteProduct(id) {

    if (!confirm(
        "Are you sure you want to delete this product?"
    )) {
        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/product/delete/product/${id}`,
                {
                    method: "DELETE",
                    headers: getHeaders()
                }
            );

        if (!response.ok) {

            console.error(
                "Delete product:",
                response.status
            );

            alert("Failed to delete product.");

            return;
        }

        loadProducts();

    } catch (error) {

        console.error(
            "Delete product error:",
            error
        );

    }
}


/* =========================
   CATEGORIES
========================= */

async function loadCategories() {

    try {

        const response =
            await fetch(
                `${API_URL}/category/all_categories`,
                {
                    headers: getHeaders()
                }
            );


        if (!response.ok) {

            console.error(
                "Categories:",
                response.status,
                await response.text()
            );

            return;
        }


        const categories =
            await response.json();

        allCategories = categories;


        const table =
            document.getElementById(
                "categories-table"
            );


        table.innerHTML = "";


        if (categories.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="5">
                        No categories found.
                    </td>
                </tr>
            `;

            return;
        }


        categories.forEach(category => {

            table.innerHTML += `
                <tr>
                    <td>${category.id}</td>
                    <td>${category.name}</td>
                    <td>${category.description || "-"}</td>
                    <td>${category.created_at || "-"}</td>
                    <td class="actions-cell">
                        ${canDo("update", "categories") ? `<button class="edit-btn" onclick="openCategoryForm(${category.id})">Edit</button>` : ""}
                        ${canDo("delete", "categories") ? `<button class="delete-btn" onclick="deleteCategory(${category.id})">Delete</button>` : ""}
                    </td>
                </tr>
            `;

        });

    } catch (error) {

        console.error(
            "Category error:",
            error
        );

    }
}


/* =========================
   CATEGORY CRUD
========================= */

function openCategoryForm(id = null) {

    if (id && !canDo("update", "categories")) return;
    if (!id && !canDo("create", "categories")) return;

    const category =
        id
            ? allCategories.find(c => c.id === id)
            : null;

    openModal(id ? "Edit Category" : "Add Category");

    document.getElementById("modal-body").innerHTML =
        fieldHTML({
            label: "Name",
            name: "c-name",
            value: category?.name || "",
            required: true
        }) +
        fieldHTML({
            label: "Description",
            name: "c-desc",
            type: "textarea",
            value: category?.description || ""
        });

    modalState.module = "categories";
    modalState.id = id;
    modalState.submitHandler = saveCategory;
}

async function saveCategory() {

    const payload = {
        name: collectField("c-name"),
        description: collectField("c-desc") || null
    };

    const id = modalState.id;

    try {

        const response =
            await fetch(
                id
                    ? `${API_URL}/category/update_category/${id}`
                    : `${API_URL}/category/create`,
                {
                    method: id ? "PUT" : "POST",
                    headers: getHeaders(),
                    body: JSON.stringify(payload)
                }
            );

        if (!response.ok) {

            const data =
                await response.json().catch(() => ({}));

            showModalError(
                data.detail || "Failed to save category."
            );

            return;
        }

        closeModal();
        loadCategories();

    } catch (error) {

        console.error(
            "Save category error:",
            error
        );

        showModalError(
            "Cannot connect to server."
        );

    }
}

async function deleteCategory(id) {

    if (!confirm(
        "Are you sure you want to delete this category?"
    )) {
        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/category/delete_category/${id}`,
                {
                    method: "DELETE",
                    headers: getHeaders()
                }
            );

        if (!response.ok) {

            console.error(
                "Delete category:",
                response.status
            );

            alert("Failed to delete category.");

            return;
        }

        loadCategories();

    } catch (error) {

        console.error(
            "Delete category error:",
            error
        );

    }
}


/* =========================
   SUPPLIERS
========================= */

async function loadSuppliers() {

    try {

        const response =
            await fetch(
                `${API_URL}/supplier/all_suppliers`,
                {
                    headers: getHeaders()
                }
            );


        if (!response.ok) {

            console.error(
                "Suppliers:",
                response.status,
                await response.text()
            );

            return;
        }


        const suppliers =
            await response.json();

        allSuppliers = suppliers;


        const table =
            document.getElementById(
                "suppliers-table"
            );


        table.innerHTML = "";


        if (suppliers.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="7">
                        No suppliers found.
                    </td>
                </tr>
            `;

            return;
        }


        suppliers.forEach(supplier => {

            table.innerHTML += `
                <tr>
                    <td>${supplier.id}</td>
                    <td>${supplier.name}</td>
                    <td>${supplier.company_name}</td>
                    <td>${supplier.email}</td>
                    <td>${supplier.phone}</td>
                    <td>${supplier.address || "-"}</td>
                    <td class="actions-cell">
                        ${canDo("update", "suppliers") ? `<button class="edit-btn" onclick="openSupplierForm(${supplier.id})">Edit</button>` : ""}
                        ${canDo("delete", "suppliers") ? `<button class="delete-btn" onclick="deleteSupplier(${supplier.id})">Delete</button>` : ""}
                    </td>
                </tr>
            `;

        });

    } catch (error) {

        console.error(
            "Supplier error:",
            error
        );

    }
}


/* =========================
   SUPPLIER CRUD
========================= */

function openSupplierForm(id = null) {

    if (id && !canDo("update", "suppliers")) return;
    if (!id && !canDo("create", "suppliers")) return;

    const supplier =
        id
            ? allSuppliers.find(s => s.id === id)
            : null;

    openModal(id ? "Edit Supplier" : "Add Supplier");

    document.getElementById("modal-body").innerHTML =
        fieldHTML({
            label: "Name",
            name: "s-name",
            value: supplier?.name || "",
            required: true
        }) +
        fieldHTML({
            label: "Company",
            name: "s-company",
            value: supplier?.company_name || "",
            required: true
        }) +
        fieldHTML({
            label: "Email",
            name: "s-email",
            type: "email",
            value: supplier?.email || "",
            required: true
        }) +
        fieldHTML({
            label: "Phone",
            name: "s-phone",
            value: supplier?.phone || "",
            required: true
        }) +
        fieldHTML({
            label: "Address",
            name: "s-address",
            value: supplier?.address || ""
        });

    modalState.module = "suppliers";
    modalState.id = id;
    modalState.submitHandler = saveSupplier;
}

async function saveSupplier() {

    const payload = {
        name: collectField("s-name"),
        company_name: collectField("s-company"),
        email: collectField("s-email"),
        phone: collectField("s-phone"),
        address: collectField("s-address") || null
    };

    const id = modalState.id;

    try {

        const response =
            await fetch(
                id
                    ? `${API_URL}/supplier/update/supplier/${id}`
                    : `${API_URL}/supplier/create`,
                {
                    method: id ? "PUT" : "POST",
                    headers: getHeaders(),
                    body: JSON.stringify(payload)
                }
            );

        if (!response.ok) {

            const data =
                await response.json().catch(() => ({}));

            showModalError(
                data.detail || "Failed to save supplier."
            );

            return;
        }

        closeModal();
        loadSuppliers();

    } catch (error) {

        console.error(
            "Save supplier error:",
            error
        );

        showModalError(
            "Cannot connect to server."
        );

    }
}

async function deleteSupplier(id) {

    if (!confirm(
        "Are you sure you want to delete this supplier?"
    )) {
        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/supplier/delete/supplier/${id}`,
                {
                    method: "DELETE",
                    headers: getHeaders()
                }
            );

        if (!response.ok) {

            console.error(
                "Delete supplier:",
                response.status
            );

            alert("Failed to delete supplier.");

            return;
        }

        loadSuppliers();

    } catch (error) {

        console.error(
            "Delete supplier error:",
            error
        );

    }
}


/* =========================
   PURCHASES
========================= */

async function loadPurchases() {

    /*
     * Inventory Manager only
     * according to your current backend
     */

    if (
        currentRole !== "Inventory Manager" &&
        currentRole !== "Admin"
    ) {

        console.log(
            "Purchase access denied for:",
            currentRole
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/purchase/all_purchase`,
                {
                    method: "GET",
                    headers: getHeaders()
                }
            );


        if (!response.ok) {

            console.error(
                "Purchases:",
                response.status,
                await response.text()
            );

            return;
        }


        const purchases =
            await response.json();

        allPurchases = purchases;


        const table =
            document.getElementById(
                "purchases-table"
            );


        table.innerHTML = "";


        if (purchases.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="7">
                        No purchases found.
                    </td>
                </tr>
            `;

            return;
        }


        purchases.forEach(purchase => {

            table.innerHTML += `
                <tr>
                    <td>${purchase.id}</td>
                    <td>${purchase.invoice_number}</td>
                    <td>${purchase.supplier_id}</td>
                    <td>${purchase.purchase_date}</td>
                    <td>₹${purchase.total_amount}</td>
                    <td>${purchase.status}</td>
                    <td class="actions-cell">
                        ${canDo("update", "purchases") ? `<button class="edit-btn" onclick="openPurchaseForm(${purchase.id})">Edit</button>` : ""}
                        ${canDo("delete", "purchases") ? `<button class="delete-btn" onclick="deletePurchase(${purchase.id})">Delete</button>` : ""}
                    </td>
                </tr>
            `;

        });

    } catch (error) {

        console.error(
            "Purchase error:",
            error
        );

    }
}


/* =========================
   ITEM ROWS (PURCHASE / SALE)
========================= */

function productOptionsHTML(selected = "") {

    return `
        <option
            value=""
            ${selected ? "" : "selected"}
        >
            Select product
        </option>
        ${allProducts.map(product => `
            <option
                value="${product.id}"
                ${String(product.id) === String(selected) ? "selected" : ""}
            >
                ${product.name} (${product.sku})
            </option>
        `).join("")}
    `;
}

function todayStr() {

    const date = new Date();

    const year = date.getFullYear();

    const month =
        String(date.getMonth() + 1).padStart(2, "0");

    const day =
        String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
}

function addItemRow(tbodyId, item = {}) {

    const tbody =
        document.getElementById(tbodyId);

    if (!tbody) {
        return;
    }

    const row =
        document.createElement("tr");

    row.innerHTML = `
        <td>
            <select class="item-field item-product">
                ${productOptionsHTML(item.product_id)}
            </select>
        </td>
        <td>
            <input
                type="number"
                class="item-field item-qty"
                min="1"
                value="${item.quantity || 1}"
            >
        </td>
        <td>
            <input
                type="number"
                class="item-field item-price"
                min="0"
                step="0.01"
                value="${item.unit_price ?? ""}"
            >
        </td>
        <td>
            <button
                type="button"
                class="remove-item-btn"
                onclick="this.closest('tr').remove()"
            >
                ✕
            </button>
        </td>
    `;

    tbody.appendChild(row);
}

function collectItems(tbodyId) {

    const rows =
        [...document.querySelectorAll(
            `#${tbodyId} tr`
        )];

    return rows.map(row => ({
        product_id: parseInt(
            row.querySelector(".item-product").value,
            10
        ),
        quantity: parseInt(
            row.querySelector(".item-qty").value,
            10
        ),
        unit_price: parseFloat(
            row.querySelector(".item-price").value
        )
    }));
}


/* =========================
   PURCHASE CRUD
========================= */

function openPurchaseForm(id = null) {

    if (id && !canDo("update", "purchases")) return;
    if (!id && !canDo("create", "purchases")) return;

    const purchase =
        id
            ? allPurchases.find(p => p.id === id)
            : null;

    const supplierOptions =
        allSuppliers.map(supplier => ({
            value: supplier.id,
            label:
                `${supplier.company_name} (${supplier.name})`
        }));

    supplierOptions.unshift({
        value: "",
        label: allSuppliers.length === 0
            ? "No suppliers available"
            : "Select supplier"
    });

    openModal(id ? "Edit Purchase" : "Add Purchase");

    document.getElementById("modal-body").innerHTML =
        fieldHTML({
            label: "Invoice Number",
            name: "pu-invoice",
            value: purchase?.invoice_number || "",
            required: true
        }) +
        fieldHTML({
            label: "Purchase Date",
            name: "pu-date",
            type: "date",
            value: purchase?.purchase_date || todayStr(),
            required: true
        }) +
        fieldHTML({
            label: "Supplier",
            name: "pu-supplier",
            options: supplierOptions,
            value: purchase?.supplier_id ?? "",
            required: true
        }) +
        `
        <div class="form-group">
            <label>Items</label>
            <div class="items-box">
                <table class="items-table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Qty</th>
                            <th>Unit Price</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody id="purchase-items"></tbody>
                </table>
                <button
                    type="button"
                    class="add-button add-item-button"
                    onclick="addPurchaseItemRow()"
                >
                    + Add Item
                </button>
            </div>
        </div>
        `;

    const items =
        (purchase && purchase.items) || [];

    if (items.length === 0) {
        addItemRow("purchase-items");
    } else {
        items.forEach(item =>
            addItemRow("purchase-items", item)
        );
    }

    modalState.module = "purchases";
    modalState.id = id;
    modalState.submitHandler = savePurchase;
}

function addPurchaseItemRow(item = {}) {
    addItemRow("purchase-items", item);
}

async function savePurchase() {

    const items =
        collectItems("purchase-items");

    if (items.length === 0) {

        showModalError(
            "Add at least one item."
        );

        return;
    }

    if (items.some(item =>
        !item.product_id ||
        !item.quantity ||
        !item.unit_price
    )) {

        showModalError(
            "Each item needs a product, quantity and unit price."
        );

        return;
    }

    const payload = {
        invoice_number: collectField("pu-invoice"),
        purchase_date: collectField("pu-date"),
        supplier_id: parseInt(
            collectField("pu-supplier"),
            10
        ),
        items
    };

    const id = modalState.id;

    try {

        const response =
            await fetch(
                id
                    ? `${API_URL}/purchase/update/${id}`
                    : `${API_URL}/purchase/`,
                {
                    method: id ? "PUT" : "POST",
                    headers: getHeaders(),
                    body: JSON.stringify(payload)
                }
            );

        if (!response.ok) {

            const data =
                await response.json().catch(() => ({}));

            showModalError(
                typeof data.detail === "string"
                    ? data.detail
                    : "Failed to save purchase."
            );

            return;
        }

        closeModal();
        loadPurchases();

    } catch (error) {

        console.error(
            "Save purchase error:",
            error
        );

        showModalError(
            "Cannot connect to server."
        );

    }
}

async function deletePurchase(id) {

    if (!confirm(
        "Are you sure you want to delete this purchase?"
    )) {
        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/purchase/delete/${id}`,
                {
                    method: "DELETE",
                    headers: getHeaders()
                }
            );

        if (!response.ok) {

            console.error(
                "Delete purchase:",
                response.status
            );

            alert("Failed to delete purchase.");

            return;
        }

        loadPurchases();

    } catch (error) {

        console.error(
            "Delete purchase error:",
            error
        );

    }
}


/* =========================
   SALES
========================= */

async function loadSales() {

    /*
     * Your backend require_sales_user allows:
     *
     * Admin
     * Sales Executive
     */

    if (
        currentRole !== "Admin" &&
        currentRole !== "Sales Executive"
    ) {

        console.log(
            "Sales access denied for:",
            currentRole
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/sales/all_sales`,
                {
                    method: "GET",
                    headers: getHeaders()
                }
            );


        if (!response.ok) {

            console.error(
                "Sales:",
                response.status,
                await response.text()
            );

            return;
        }


        const sales =
            await response.json();

        allSales = sales;


        const table =
            document.getElementById(
                "sales-table"
            );


        table.innerHTML = "";


        if (sales.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="7">
                        No sales found.
                    </td>
                </tr>
            `;

            return;
        }


        sales.forEach(sale => {

            table.innerHTML += `
                <tr>
                    <td>${sale.id}</td>
                    <td>${sale.invoice_number}</td>
                    <td>${sale.customer_name}</td>
                    <td>${sale.sale_date}</td>
                    <td>₹${sale.total_amount}</td>
                    <td>${sale.status}</td>
                    <td class="actions-cell">
                        ${canDo("update", "sales") ? `<button class="edit-btn" onclick="openSaleForm(${sale.id})">Edit</button>` : ""}
                        ${canDo("delete", "sales") ? `<button class="delete-btn" onclick="deleteSale(${sale.id})">Delete</button>` : ""}
                    </td>
                </tr>
            `;

        });

    } catch (error) {

        console.error(
            "Sales error:",
            error
        );

    }
}


/* =========================
   SALE CRUD
========================= */

function openSaleForm(id = null) {

    if (id && !canDo("update", "sales")) return;
    if (!id && !canDo("create", "sales")) return;

    const sale =
        id
            ? allSales.find(s => s.id === id)
            : null;

    openModal(id ? "Edit Sale" : "Add Sale");

    document.getElementById("modal-body").innerHTML =
        fieldHTML({
            label: "Invoice Number",
            name: "sa-invoice",
            value: sale?.invoice_number || "",
            required: true
        }) +
        fieldHTML({
            label: "Customer Name",
            name: "sa-customer",
            value: sale?.customer_name || "",
            required: true
        }) +
        fieldHTML({
            label: "Sale Date",
            name: "sa-date",
            type: "date",
            value: sale?.sale_date || todayStr(),
            required: true
        }) +
        `
        <div class="form-group">
            <label>Items</label>
            <div class="items-box">
                <table class="items-table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Qty</th>
                            <th>Unit Price</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody id="sales-items"></tbody>
                </table>
                <button
                    type="button"
                    class="add-button add-item-button"
                    onclick="addSaleItemRow()"
                >
                    + Add Item
                </button>
            </div>
        </div>
        `;

    const items =
        (sale && sale.items) || [];

    if (items.length === 0) {
        addItemRow("sales-items");
    } else {
        items.forEach(item =>
            addItemRow("sales-items", item)
        );
    }

    modalState.module = "sales";
    modalState.id = id;
    modalState.submitHandler = saveSale;
}

function addSaleItemRow(item = {}) {
    addItemRow("sales-items", item);
}

async function saveSale() {

    const items =
        collectItems("sales-items");

    if (items.length === 0) {

        showModalError(
            "Add at least one item."
        );

        return;
    }

    if (items.some(item =>
        !item.product_id ||
        !item.quantity ||
        !item.unit_price
    )) {

        showModalError(
            "Each item needs a product, quantity and unit price."
        );

        return;
    }

    const payload = {
        invoice_number: collectField("sa-invoice"),
        customer_name: collectField("sa-customer"),
        sale_date: collectField("sa-date"),
        items
    };

    const id = modalState.id;

    try {

        const response =
            await fetch(
                id
                    ? `${API_URL}/sales/update/${id}`
                    : `${API_URL}/sales/`,
                {
                    method: id ? "PUT" : "POST",
                    headers: getHeaders(),
                    body: JSON.stringify(payload)
                }
            );

        if (!response.ok) {

            const data =
                await response.json().catch(() => ({}));

            showModalError(
                typeof data.detail === "string"
                    ? data.detail
                    : "Failed to save sale."
            );

            return;
        }

        closeModal();
        loadSales();

    } catch (error) {

        console.error(
            "Save sale error:",
            error
        );

        showModalError(
            "Cannot connect to server."
        );

    }
}

async function deleteSale(id) {

    if (!confirm(
        "Are you sure you want to delete this sale?"
    )) {
        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/sales/delete/${id}`,
                {
                    method: "DELETE",
                    headers: getHeaders()
                }
            );

        if (!response.ok) {

            console.error(
                "Delete sale:",
                response.status
            );

            alert("Failed to delete sale.");

            return;
        }

        loadSales();

    } catch (error) {

        console.error(
            "Delete sale error:",
            error
        );

    }
}


/* =========================
   DASHBOARD
========================= */

async function loadDashboard() {

    try {

        /*
         * PRODUCTS
         */

        const productsResponse =
            await fetch(
                `${API_URL}/product/all_products`,
                {
                    headers: getHeaders()
                }
            );


        let products = [];

        if (productsResponse.ok) {

            products =
                await productsResponse.json();

            allProducts = products;

        } else {

            console.error(
                "Products:",
                productsResponse.status,
                await productsResponse.text()
            );

        }


        /*
         * CATEGORIES
         */

        const categoriesResponse =
            await fetch(
                `${API_URL}/category/all_categories`,
                {
                    headers: getHeaders()
                }
            );


        let categories = [];

        if (categoriesResponse.ok) {

            categories =
                await categoriesResponse.json();

            allCategories = categories;

        } else {

            console.error(
                "Categories:",
                categoriesResponse.status,
                await categoriesResponse.text()
            );

        }


        /*
         * SUPPLIERS
         */

        let suppliers = [];


        if (
            currentRole === "Admin" ||
            currentRole === "Inventory Manager"
        ) {

            const suppliersResponse =
                await fetch(
                    `${API_URL}/supplier/all_suppliers`,
                    {
                        headers: getHeaders()
                    }
                );


            if (suppliersResponse.ok) {

                suppliers =
                    await suppliersResponse.json();

                allSuppliers = suppliers;

            } else {

                console.error(
                    "Suppliers:",
                    suppliersResponse.status,
                    await suppliersResponse.text()
                );

            }
        }


        /*
         * SALES
         */

        let sales = [];


        if (
            currentRole === "Admin" ||
            currentRole === "Sales Executive"
        ) {

            const salesResponse =
                await fetch(
                    `${API_URL}/sales/all_sales`,
                    {
                        headers: getHeaders()
                    }
                );


            if (salesResponse.ok) {

                sales =
                    await salesResponse.json();

            } else {

                console.error(
                    "Sales:",
                    salesResponse.status,
                    await salesResponse.text()
                );

            }
        }


        /*
         * PURCHASES
         */

        let purchases = [];


        if (
            currentRole === "Admin" ||
            currentRole === "Inventory Manager"
        ) {

            const purchasesResponse =
                await fetch(
                    `${API_URL}/purchase/all_purchase`,
                    {
                        headers: getHeaders()
                    }
                );


            if (purchasesResponse.ok) {

                purchases =
                    await purchasesResponse.json();

            } else {

                console.error(
                    "Purchases:",
                    purchasesResponse.status,
                    await purchasesResponse.text()
                );

            }
        }


        /*
         * DASHBOARD COUNTS
         */

        const productCount =
            document.getElementById(
                "product-count"
            );

        if (productCount) {
            productCount.textContent =
                products.length;
        }


        const categoryCount =
            document.getElementById(
                "category-count"
            );

        if (categoryCount) {
            categoryCount.textContent =
                categories.length;
        }


        const supplierCount =
            document.getElementById(
                "supplier-count"
            );

        if (supplierCount) {
            supplierCount.textContent =
                suppliers.length;
        }


        const salesCount =
            document.getElementById(
                "sales-count"
            );

        if (salesCount) {
            salesCount.textContent =
                sales.length;
        }


        /*
         * LOW STOCK
         */

        const lowStock =
            products.filter(
                product =>
                    product.quantity <= 5
            );


        const table =
            document.getElementById(
                "low-stock-table"
            );


        if (!table) {
            return;
        }


        table.innerHTML = "";


        if (lowStock.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="5">
                        No low-stock products.
                    </td>
                </tr>
            `;

        } else {

            lowStock.forEach(product => {

                table.innerHTML += `
                    <tr>
                        <td>${product.id}</td>
                        <td>${product.name}</td>
                        <td>${product.sku}</td>
                        <td>₹${product.price}</td>
                        <td>${product.quantity}</td>
                    </tr>
                `;

            });

        }

    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

    }
}


/* =========================
   LOGOUT
========================= */

function logout() {

    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("userName");

    token = null;
    currentRole = "";
    currentName = "";

    document
        .getElementById("app")
        .classList.add("hidden");

    document
        .getElementById("login-page")
        .classList.remove("hidden");

    document
        .getElementById("login-form")
        .reset();
}


/* =========================
   AUTO LOGIN
========================= */

if (token) {

    /*
     * Recover role from JWT
     */

    const payload =
        decodeJWT(token);


    if (payload && payload.role) {

        currentRole =
            payload.role;

        localStorage.setItem(
            "role",
            currentRole
        );

    }


    if (payload && payload.name) {

        currentName =
            payload.name;

        localStorage.setItem(
            "userName",
            currentName
        );

    }


    showApplication();

}