<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOBA CHILL - Quản Lý Hóa Đơn & Tính Tiền</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Quicksand', sans-serif;
            background-color: #F7FAFC;
        }
        /* Custom Scrollbar for Bill List */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #a0aec0;
        }
        
        /* Thermal Receipt Thermal K80 Styling for Print */
        @media print {
            body * {
                visibility: hidden;
            }
            #printable-receipt, #printable-receipt * {
                visibility: visible;
            }
            #printable-receipt {
                position: absolute;
                left: 0;
                top: 0;
                width: 80mm;
                padding: 10px;
                margin: 0;
                background: white;
                color: black;
                font-family: 'Courier New', Courier, monospace;
                box-shadow: none !important;
            }
            .no-print {
                display: none !important;
            }
        }
    </style>
</head>
<body class="bg-amber-50/30 min-h-screen text-slate-800 flex flex-col">

    <header class="bg-gradient-to-r from-amber-500 via-pink-500 to-rose-500 text-white shadow-lg sticky top-0 z-30">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="bg-white p-2 rounded-full text-amber-500 shadow-md">
                    <i class="fa-solid font-bold fa-whiskey-glass text-2xl"></i>
                </div>
                <div>
                    <h1 class="text-2xl font-bold tracking-wide">BOBA CHILL</h1>
                    <p class="text-xs text-amber-100 font-medium">Hệ thống POS Quản Lý & Bán Hàng Trà Sữa</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <div id="live-clock" class="text-right hidden sm:block bg-white/10 px-3 py-1 rounded-lg backdrop-blur-sm text-sm font-semibold">
                    00:00:00
                </div>
                <button onclick="createNewOrder()" class="bg-white text-rose-600 hover:bg-rose-50 font-bold px-4 py-2 rounded-xl shadow transition duration-200 flex items-center gap-2 text-sm">
                    <i class="fa-solid fa-plus-circle"></i> Đơn Hàng Mới
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto w-full px-4 py-6 flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- LEFT COLUMN: MENU & ORDER FORM (7 cols on large screens) -->
        <section class="lg:col-span-7 space-y-6">
            
            <!-- Customer Info Block -->
            <div class="bg-white rounded-2xl p-5 shadow-sm border border-amber-100">
                <h2 class="text-lg font-bold text-amber-800 flex items-center gap-2 mb-3">
                    <i class="fa-solid fa-user-tag text-amber-500"></i> Thông Tin Khách Hàng
                </h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 uppercase mb-1">Tên khách hàng</label>
                        <input type="text" id="cust-name" value="Khách Lẻ" placeholder="Nhập tên khách..." 
                               class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 focus:bg-white text-sm transition">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 uppercase mb-1">Số Bàn / SĐT (Tùy chọn)</label>
                        <input type="text" id="cust-table" placeholder="Vd: Bàn 05 hoặc 090xxx..." 
                               class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 focus:bg-white text-sm transition">
                    </div>
                </div>
            </div>

            <!-- Item Selection Form Block -->
            <div class="bg-white rounded-2xl p-5 shadow-sm border border-amber-100 space-y-4">
                <h2 class="text-lg font-bold text-amber-800 flex items-center gap-2 border-b border-slate-100 pb-3">
                    <i class="fa-solid fa-mug-hot text-pink-500"></i> Chọn Món Nước & Tùy Chỉnh
                </h2>

                <!-- Drink Selection Grid -->
                <div>
                    <label class="block text-xs font-semibold text-gray-600 uppercase mb-2">1. Chọn Thức Uống (*)</label>
                    <div id="drink-options" class="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-56 overflow-y-auto p-1">
                        <!-- Dynamic drink buttons injected here -->
                    </div>
                </div>

                <!-- Size Selection -->
                <div>
                    <label class="block text-xs font-semibold text-gray-600 uppercase mb-2">2. Chọn Size Ly</label>
                    <div class="grid grid-cols-3 gap-3" id="size-options">
                        <button type="button" data-size="S" data-extra="0" onclick="selectSize(this)" 
                                class="size-btn py-2 px-3 rounded-xl border border-slate-200 font-semibold text-sm flex justify-between items-center hover:border-amber-400 transition bg-amber-50 border-amber-500 text-amber-900 shadow-sm">
                            <span>Size S</span> <span class="text-xs text-slate-500">+0đ</span>
                        </button>
                        <button type="button" data-size="M" data-extra="5000" onclick="selectSize(this)" 
                                class="size-btn py-2 px-3 rounded-xl border border-slate-200 font-semibold text-sm flex justify-between items-center hover:border-amber-400 transition bg-white text-slate-700">
                            <span>Size M</span> <span class="text-xs text-slate-500">+5k</span>
                        </button>
                        <button type="button" data-size="L" data-extra="10000" onclick="selectSize(this)" 
                                class="size-btn py-2 px-3 rounded-xl border border-slate-200 font-semibold text-sm flex justify-between items-center hover:border-amber-400 transition bg-white text-slate-700">
                            <span>Size L</span> <span class="text-xs text-slate-500">+10k</span>
                        </button>
                    </div>
                </div>

                <!-- Sugar & Ice Levels -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 uppercase mb-2">Mức Độ Đường</label>
                        <select id="sugar-level" class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
                            <option value="100% Đường">100% Đường (Chuẩn)</option>
                            <option value="70% Đường">70% Đường</option>
                            <option value="50% Đường">50% Đường</option>
                            <option value="30% Đường">30% Đường</option>
                            <option value="0% Đường">Không đường (0%)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-600 uppercase mb-2">Mức Độ Đá</label>
                        <select id="ice-level" class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm font-medium">
                            <option value="100% Đá">100% Đá (Chuẩn)</option>
                            <option value="70% Đá">70% Đá</option>
                            <option value="50% Đá">50% Đá</option>
                            <option value="30% Đá">30% Đá</option>
                            <option value="Không Đá">Không đá (Uống lạnh)</option>
                            <option value="Nóng">Uống Nóng</option>
                        </select>
                    </div>
                </div>

                <!-- Toppings Selection (Checkboxes) -->
                <div>
                    <label class="block text-xs font-semibold text-gray-600 uppercase mb-2">3. Chọn Topping (Có thể chọn nhiều)</label>
                    <div id="topping-options" class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                        <!-- Dynamic toppings injected here -->
                    </div>
                </div>

                <!-- Quantity & Note & Add Button -->
                <div class="pt-2 flex flex-col sm:flex-row gap-3 items-stretch sm:items-center">
                    <div class="flex items-center space-x-2 bg-slate-100 rounded-xl p-1 border border-slate-200 self-start sm:self-auto">
                        <button onclick="adjustFormQty(-1)" class="w-8 h-8 rounded-lg bg-white text-slate-700 font-bold hover:bg-slate-200 flex items-center justify-center shadow-sm">-</button>
                        <input type="number" id="form-qty" value="1" min="1" class="w-12 text-center bg-transparent font-bold text-slate-800 focus:outline-none" readonly>
                        <button onclick="adjustFormQty(1)" class="w-8 h-8 rounded-lg bg-white text-slate-700 font-bold hover:bg-slate-200 flex items-center justify-center shadow-sm">+</button>
                    </div>

                    <input type="text" id="item-note" placeholder="Ghi chú thêm (vd: nhiều thạch, ít bọt...)" 
                           class="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 text-sm">

                    <button onclick="addToCart()" class="bg-gradient-to-r from-amber-500 to-rose-500 hover:from-amber-600 hover:to-rose-600 text-white font-bold px-5 py-2.5 rounded-xl shadow-md hover:shadow-lg transition flex items-center justify-center gap-2">
                        <i class="fa-solid fa-cart-plus"></i> Thêm Vào Đơn
                    </button>
                </div>
            </div>
        </section>

        <!-- RIGHT COLUMN: CART & SUMMARY (5 cols on large screens) -->
        <section class="lg:col-span-5 flex flex-col h-full">
            <div class="bg-white rounded-2xl p-5 shadow-sm border border-amber-100 flex-1 flex flex-col">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3 mb-3">
                    <h2 class="text-lg font-bold text-amber-800 flex items-center gap-2">
                        <i class="fa-solid fa-receipt text-amber-500"></i> Giỏ Hàng Món Đã Chọn
                    </h2>
                    <span id="cart-item-count" class="bg-rose-100 text-rose-600 text-xs font-bold px-2.5 py-1 rounded-full">0 món</span>
                </div>

                <!-- Cart Items Scrollable List -->
                <div class="flex-1 overflow-y-auto max-h-[380px] space-y-3 pr-1" id="cart-list">
                    <!-- Cart Empty Placeholder -->
                    <div id="empty-cart" class="text-center py-12 text-slate-400 space-y-2">
                        <i class="fa-solid fa-mug-saucer text-4xl text-slate-300"></i>
                        <p class="text-sm font-medium">Chưa có món nào trong đơn hàng</p>
                        <p class="text-xs">Vui lòng chọn trà sữa & topping ở bên trái</p>
                    </div>
                </div>

                <!-- Summary & Payment Settings -->
                <div class="border-t border-slate-100 pt-4 mt-4 space-y-3 bg-slate-50/50 p-3 rounded-xl">
                    
                    <!-- Discount & Surcharge -->
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-xs font-semibold text-slate-500 mb-1">Giảm Giá (%)</label>
                            <input type="number" id="discount-percent" value="0" min="0" max="100" onchange="renderCart()" 
                                   class="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded-lg text-sm text-center font-semibold focus:ring-2 focus:ring-amber-400">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-500 mb-1">Hình Thức Thanh Toán</label>
                            <select id="payment-method" class="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded-lg text-sm font-semibold focus:ring-2 focus:ring-amber-400">
                                <option value="Tiền mặt">💵 Tiền Mặt</option>
                                <option value="Chuyển khoản QR">📱 Chuyển Khoản QR</option>
                                <option value="Ví MoMo/ZaloPay">👛 Ví Điện Tử</option>
                            </select>
                        </div>
                    </div>

                    <!-- Financial Summary Lines -->
                    <div class="space-y-1 text-sm pt-2">
                        <div class="flex justify-between text-slate-600">
                            <span>Tạm tính món:</span>
                            <span id="subtotal-val" class="font-semibold">0 đ</span>
                        </div>
                        <div id="discount-row" class="flex justify-between text-rose-600 text-xs hidden">
                            <span>Chiết khấu giảm giá:</span>
                            <span id="discount-val" class="font-semibold">-0 đ</span>
                        </div>
                        <div class="flex justify-between text-base font-bold text-slate-800 pt-2 border-t border-slate-200">
                            <span>TỔNG THANH TOÁN:</span>
                            <span id="grand-total-val" class="text-rose-600 text-xl font-extrabold">0 đ</span>
                        </div>
                    </div>

                    <!-- Checkout Action Button -->
                    <button onclick="checkoutAndPrint()" id="btn-checkout" disabled 
                            class="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-slate-300 text-white font-bold py-3 rounded-xl shadow-md hover:shadow-lg transition flex items-center justify-center gap-2 text-base mt-2">
                        <i class="fa-solid fa-file-invoice-dollar"></i> Thanh Toán & Xuất Hóa Đơn
                    </button>
                </div>
            </div>
        </section>

    </main>

    <!-- RECEIPT PREVIEW & PRINT MODAL -->
    <div id="receipt-modal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] flex flex-col overflow-hidden animate-fade-in">
            <!-- Modal Header -->
            <div class="bg-slate-800 text-white p-4 flex justify-between items-center no-print">
                <h3 class="font-bold flex items-center gap-2"><i class="fa-solid fa-receipt text-amber-400"></i> Xem Trước Hóa Đơn</h3>
                <button onclick="closeModal()" class="text-slate-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
            </div>

            <!-- Receipt Content (Printable Area) -->
            <div class="p-6 overflow-y-auto flex-1 bg-white text-slate-800 text-sm" id="printable-receipt">
                <div class="text-center space-y-1 mb-4 border-b border-dashed border-slate-300 pb-4">
                    <h2 class="text-2xl font-black tracking-wider uppercase text-slate-900">BOBA CHILL</h2>
                    <p class="text-xs text-slate-500">ĐC: 123 Đường Trà Sữa, Q.1, TP.HCM</p>
                    <p class="text-xs text-slate-500">Hotline: 1900 888 999</p>
                    <div class="pt-2 font-bold text-base text-slate-800">HOÁ ĐƠN THANH TOÁN</div>
                    <p id="receipt-id" class="text-xs font-mono text-slate-500">Mã HĐ: #BC0000</p>
                </div>

                <div class="space-y-1 text-xs mb-4 border-b border-dashed border-slate-300 pb-3">
                    <div class="flex justify-between"><span class="text-slate-500">Thời gian:</span> <span id="receipt-date" class="font-medium">--/--/---- --:--</span></div>
                    <div class="flex justify-between"><span class="text-slate-500">Khách hàng:</span> <span id="receipt-cust-name" class="font-bold">Khách lẻ</span></div>
                    <div class="flex justify-between"><span class="text-slate-500">Vị trí/Bàn:</span> <span id="receipt-cust-table" class="font-medium">Mang đi</span></div>
                    <div class="flex justify-between"><span class="text-slate-500">Thanh toán:</span> <span id="receipt-pay-method" class="font-medium">Tiền mặt</span></div>
                </div>

                <!-- Table Header -->
                <table class="w-full text-left text-xs mb-3">
                    <thead>
                        <tr class="border-b border-slate-300 text-slate-600">
                            <th class="py-1">Món</th>
                            <th class="py-1 text-center">SL</th>
                            <th class="py-1 text-right">Đ.Giá</th>
                            <th class="py-1 text-right">T.Tiền</th>
                        </tr>
                    </thead>
                    <tbody id="receipt-items-body" class="divide-y divide-slate-100">
                        <!-- Dynamic receipt rows -->
                    </tbody>
                </table>

                <!-- Total calculations -->
                <div class="border-t border-dashed border-slate-300 pt-3 space-y-1 text-xs">
                    <div class="flex justify-between text-slate-600">
                        <span>Tạm tính:</span>
                        <span id="receipt-subtotal">0 đ</span>
                    </div>
                    <div id="receipt-discount-line" class="flex justify-between text-rose-600 hidden">
                        <span>Giảm giá:</span>
                        <span id="receipt-discount">-0 đ</span>
                    </div>
                    <div class="flex justify-between text-base font-black text-slate-900 pt-2 border-t border-slate-200">
                        <span>TỔNG CỘNG:</span>
                        <span id="receipt-grandtotal" class="text-rose-600 text-lg">0 đ</span>
                    </div>
                </div>

                <div class="text-center pt-6 space-y-1 text-xs text-slate-500 border-t border-slate-100 mt-4">
                    <p class="font-semibold text-slate-700">Cảm ơn quý khách & Hẹn gặp lại! ❤️</p>
                    <p class="text-[10px]">Wifi: BobaChill_FreePass | Pass: 88888888</p>
                </div>
            </div>

            <!-- Modal Action Buttons -->
            <div class="bg-slate-50 p-4 border-t border-slate-200 flex gap-3 no-print">
                <button onclick="window.print()" class="flex-1 bg-amber-500 hover:bg-amber-600 text-white font-bold py-2.5 rounded-xl shadow transition flex items-center justify-center gap-2">
                    <i class="fa-solid fa-print"></i> In Hóa Đơn / Tải PDF
                </button>
                <button onclick="createNewOrder()" class="flex-1 bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-2.5 rounded-xl shadow transition flex items-center justify-center gap-2">
                    <i class="fa-solid fa-plus"></i> Đơn Mới
                </button>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-5 right-5 bg-slate-800 text-white px-4 py-3 rounded-xl shadow-2xl hidden items-center gap-2 z-50 text-sm transition-all duration-300">
        <i class="fa-solid fa-circle-check text-emerald-400 text-lg"></i>
        <span id="toast-message">Thông báo</span>
    </div>

    <script>
        // DATA MENU CONFIGURATION
        const DRINKS_DATA = [
            { id: 1, name: 'Trà Sữa Truyền Thống', price: 25000, icon: '🧋' },
            { id: 2, name: 'Trà Sữa Thái Xanh', price: 28000, icon: '🍵' },
            { id: 3, name: 'Trà Oolong Nướng', price: 32000, icon: '🍂' },
            { id: 4, name: 'Trà Trái Cây Nhiệt Đới', price: 35000, icon: '🍹' },
            { id: 5, name: 'Matcha Latte Thượng Hạng', price: 38000, icon: '🍃' },
            { id: 6, name: 'Trà Sữa Sương Sáo', price: 30000, icon: '🥣' },
            { id: 7, name: 'Trà Sữa Trân Châu Đường Đen', price: 35000, icon: '🧋' },
            { id: 8, name: 'Trà Phô Mai Kem Muối', price: 36000, icon: '🧀' }
        ];

        const TOPPINGS_DATA = [
            { id: 'tp1', name: 'Trân châu đen', price: 5000 },
            { id: 'tp2', name: 'Trân châu trắng', price: 5000 },
            { id: 'tp3', name: 'Thạch trái cây', price: 5000 },
            { id: 'tp4', name: 'Pudding trứng', price: 7000 },
            { id: 'tp5', name: 'Cream cheese', price: 8000 },
            { id: 'tp6', name: 'Sương sáo', price: 5000 }
        ];

        // STATE VARIABLES
        let currentCart = [];
        let selectedDrink = DRINKS_DATA[0];
        let selectedSize = { name: 'S', extraPrice: 0 };

        // INITIALIZE APP
        window.addEventListener('DOMContentLoaded', () => {
            initLiveClock();
            renderDrinkOptions();
            renderToppingOptions();
            renderCart();
        });

        // LIVE CLOCK FUNCTION
        function initLiveClock() {
            const clockEl = document.getElementById('live-clock');
            setInterval(() => {
                const now = new Date();
                clockEl.textContent = now.toLocaleTimeString('vi-VN') + ' - ' + now.toLocaleDateString('vi-VN');
            }, 1000);
        }

        // RENDER DRINK BUTTONS
        function renderDrinkOptions() {
            const container = document.getElementById('drink-options');
            container.innerHTML = DRINKS_DATA.map(drink => `
                <button type="button" onclick="selectDrink(${drink.id})" id="drink-btn-${drink.id}"
                        class="drink-btn text-left p-2.5 rounded-xl border transition flex flex-col justify-between ${selectedDrink.id === drink.id ? 'border-amber-500 bg-amber-50 shadow-sm ring-2 ring-amber-400' : 'border-slate-200 bg-white hover:border-amber-300'}">
                    <div class="flex items-center gap-1.5 font-bold text-sm text-slate-800">
                        <span>${drink.icon}</span> <span class="truncate">${drink.name}</span>
                    </div>
                    <div class="text-xs text-rose-500 font-bold mt-1">${formatVND(drink.price)}</div>
                </button>
            `).join('');
        }

        // RENDER TOPPING CHECKBOXES
        function renderToppingOptions() {
            const container = document.getElementById('topping-options');
            container.innerHTML = TOPPINGS_DATA.map(tp => `
                <label class="flex items-center space-x-2 bg-slate-50 p-2 rounded-xl border border-slate-200 cursor-pointer hover:bg-amber-50/50 transition">
                    <input type="checkbox" value="${tp.id}" data-name="${tp.name}" data-price="${tp.price}" class="topping-checkbox rounded text-amber-500 focus:ring-amber-400 w-4 h-4">
                    <div class="text-xs">
                        <div class="font-medium text-slate-700">${tp.name}</div>
                        <div class="text-slate-400">+${formatVND(tp.price)}</div>
                    </div>
                </label>
            `).join('');
        }

        // SELECT DRINK
        function selectDrink(id) {
            selectedDrink = DRINKS_DATA.find(d => d.id === id);
            renderDrinkOptions();
        }

        // SELECT SIZE
        function selectSize(btnElement) {
            document.querySelectorAll('.size-btn').forEach(btn => {
                btn.classList.remove('bg-amber-50', 'border-amber-500', 'text-amber-900', 'shadow-sm');
                btn.classList.add('bg-white', 'text-slate-700');
            });

            btnElement.classList.remove('bg-white', 'text-slate-700');
            btnElement.classList.add('bg-amber-50', 'border-amber-500', 'text-amber-900', 'shadow-sm');

            selectedSize = {
                name: btnElement.getAttribute('data-size'),
                extraPrice: parseInt(btnElement.getAttribute('data-extra'))
            };
        }

        // QUANTITY ADJUSTER IN FORM
        function adjustFormQty(delta) {
            const qtyInput = document.getElementById('form-qty');
            let current = parseInt(qtyInput.value) || 1;
            current += delta;
            if (current < 1) current = 1;
            qtyInput.value = current;
        }

        // ADD ITEM TO CART
        function addToCart() {
            const qty = parseInt(document.getElementById('form-qty').value) || 1;
            const sugar = document.getElementById('sugar-level').value;
            const ice = document.getElementById('ice-level').value;
            const note = document.getElementById('item-note').value.trim();

            // Collect selected toppings
            const selectedToppings = [];
            let toppingsTotalPrice = 0;
            document.querySelectorAll('.topping-checkbox:checked').forEach(cb => {
                const price = parseInt(cb.getAttribute('data-price'));
                selectedToppings.push({
                    name: cb.getAttribute('data-name'),
                    price: price
                });
                toppingsTotalPrice += price;
            });

            // Calculate unit price for item
            const unitPrice = selectedDrink.price + selectedSize.extraPrice + toppingsTotalPrice;

            const cartItem = {
                cartItemId: Date.now() + Math.random(),
                drinkName: selectedDrink.name,
                size: selectedSize.name,
                sugar: sugar,
                ice: ice,
                toppings: selectedToppings,
                unitPrice: unitPrice,
                quantity: qty,
                totalPrice: unitPrice * qty,
                note: note
            };

            currentCart.push(cartItem);
            renderCart();
            showToast(`Đã thêm ${qty}x ${selectedDrink.name} vào đơn!`);

            // Reset optional inputs
            document.getElementById('item-note').value = '';
            document.querySelectorAll('.topping-checkbox').forEach(cb => cb.checked = false);
            document.getElementById('form-qty').value = 1;
        }

        // UPDATE CART ITEM QUANTITY
        function updateCartQty(cartItemId, delta) {
            const item = currentCart.find(i => i.cartItemId === cartItemId);
            if (item) {
                item.quantity += delta;
                if (item.quantity <= 0) {
                    removeFromCart(cartItemId);
                    return;
                }
                item.totalPrice = item.unitPrice * item.quantity;
                renderCart();
            }
        }

        // REMOVE ITEM FROM CART
        function removeFromCart(cartItemId) {
            currentCart = currentCart.filter(i => i.cartItemId !== cartItemId);
            renderCart();
        }

        // RENDER CART VIEW
        function renderCart() {
            const cartList = document.getElementById('cart-list');
            const cartCount = document.getElementById('cart-item-count');
            const checkoutBtn = document.getElementById('btn-checkout');

            if (currentCart.length === 0) {
                cartList.innerHTML = `
                    <div id="empty-cart" class="text-center py-12 text-slate-400 space-y-2">
                        <i class="fa-solid fa-mug-saucer text-4xl text-slate-300"></i>
                        <p class="text-sm font-medium">Chưa có món nào trong đơn hàng</p>
                        <p class="text-xs">Vui lòng chọn trà sữa & topping ở bên trái</p>
                    </div>
                `;
                cartCount.textContent = '0 món';
                checkoutBtn.disabled = true;
                updateSummary(0);
                return;
            }

            checkoutBtn.disabled = false;
            let totalItems = 0;
            let subtotal = 0;

            cartList.innerHTML = currentCart.map(item => {
                totalItems += item.quantity;
                subtotal += item.totalPrice;

                const toppingsStr = item.toppings.length > 0 
                    ? item.toppings.map(t => t.name).join(', ') 
                    : 'Không topping';

                return `
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 flex justify-between gap-3 items-center relative group hover:border-amber-300 transition">
                        <div class="flex-1">
                            <div class="font-bold text-slate-800 text-sm flex items-center gap-2">
                                <span>${item.drinkName}</span>
                                <span class="bg-amber-200 text-amber-800 text-[10px] px-1.5 py-0.5 rounded font-extrabold">Size ${item.size}</span>
                            </div>
                            <div class="text-xs text-slate-500 mt-0.5">
                                <div>🍬 ${item.sugar} | 🧊 ${item.ice}</div>
                                <div class="text-amber-700">🍡 ${toppingsStr}</div>
                                ${item.note ? `<div class="italic text-slate-400">📝 ${item.note}</div>` : ''}
                            </div>
                            <div class="text-xs font-bold text-rose-500 mt-1">
                                ${formatVND(item.unitPrice)} x ${item.quantity} = ${formatVND(item.totalPrice)}
                            </div>
                        </div>

                        <div class="flex flex-col items-end justify-between space-y-2">
                            <button onclick="removeFromCart(${item.cartItemId})" class="text-slate-400 hover:text-rose-500 text-xs p-1">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                            <div class="flex items-center space-x-1 bg-white rounded-lg border border-slate-200 p-0.5">
                                <button onclick="updateCartQty(${item.cartItemId}, -1)" class="w-6 h-6 rounded bg-slate-100 hover:bg-slate-200 font-bold text-xs flex items-center justify-center">-</button>
                                <span class="w-6 text-center font-bold text-xs">${item.quantity}</span>
                                <button onclick="updateCartQty(${item.cartItemId}, 1)" class="w-6 h-6 rounded bg-slate-100 hover:bg-slate-200 font-bold text-xs flex items-center justify-center">+</button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');

            cartCount.textContent = `${totalItems} món`;
            updateSummary(subtotal);
        }

        // UPDATE FINANCIAL CALCULATIONS
        function updateSummary(subtotal) {
            const discountPercent = parseFloat(document.getElementById('discount-percent').value) || 0;
            const discountAmount = (subtotal * discountPercent) / 100;
            const grandTotal = subtotal - discountAmount;

            document.getElementById('subtotal-val').textContent = formatVND(subtotal);
            
            const discountRow = document.getElementById('discount-row');
            if (discountPercent > 0) {
                discountRow.classList.remove('hidden');
                document.getElementById('discount-val').textContent = `- ${formatVND(discountAmount)}`;
            } else {
                discountRow.classList.add('hidden');
            }

            document.getElementById('grand-total-val').textContent = formatVND(grandTotal);
        }

        // CHECKOUT AND SHOW RECEIPT MODAL
        function checkoutAndPrint() {
            if (currentCart.length === 0) return;

            const custName = document.getElementById('cust-name').value.trim() || 'Khách Lẻ';
            const custTable = document.getElementById('cust-table').value.trim() || 'Mang đi';
            const payMethod = document.getElementById('payment-method').value;
            const discountPercent = parseFloat(document.getElementById('discount-percent').value) || 0;

            let subtotal = 0;
            currentCart.forEach(i => subtotal += i.totalPrice);
            const discountAmount = (subtotal * discountPercent) / 100;
            const grandTotal = subtotal - discountAmount;

            // Fill Receipt Modal Data
            document.getElementById('receipt-id').textContent = `Mã HĐ: #BC${Math.floor(100000 + Math.random() * 900000)}`;
            document.getElementById('receipt-date').textContent = new Date().toLocaleString('vi-VN');
            document.getElementById('receipt-cust-name').textContent = custName;
            document.getElementById('receipt-cust-table').textContent = custTable;
            document.getElementById('receipt-pay-method').textContent = payMethod;

            // Render Bill Rows
            const receiptBody = document.getElementById('receipt-items-body');
            receiptBody.innerHTML = currentCart.map(item => {
                const toppingsStr = item.toppings.map(t => t.name).join(', ');
                return `
                    <tr class="align-top">
                        <td class="py-1.5 pr-2">
                            <div class="font-bold text-slate-800">${item.drinkName} (Size ${item.size})</div>
                            <div class="text-[10px] text-slate-500">${item.sugar}, ${item.ice}</div>
                            ${toppingsStr ? `<div class="text-[10px] text-slate-500">+ Topping: ${toppingsStr}</div>` : ''}
                            ${item.note ? `<div class="text-[10px] italic text-slate-400">Ghi chú: ${item.note}</div>` : ''}
                        </td>
                        <td class="py-1.5 text-center font-bold">${item.quantity}</td>
                        <td class="py-1.5 text-right">${formatVND(item.unitPrice)}</td>
                        <td class="py-1.5 text-right font-bold">${formatVND(item.totalPrice)}</td>
                    </tr>
                `;
            }).join('');

            document.getElementById('receipt-subtotal').textContent = formatVND(subtotal);
            
            const receiptDiscountLine = document.getElementById('receipt-discount-line');
            if (discountPercent > 0) {
                receiptDiscountLine.classList.remove('hidden');
                document.getElementById('receipt-discount').textContent = `- ${formatVND(discountAmount)} (${discountPercent}%)`;
            } else {
                receiptDiscountLine.classList.add('hidden');
            }

            document.getElementById('receipt-grandtotal').textContent = formatVND(grandTotal);

            // Display Modal
            document.getElementById('receipt-modal').classList.remove('hidden');
        }

        // CLOSE MODAL
        function closeModal() {
            document.getElementById('receipt-modal').classList.add('hidden');
        }

        // CREATE NEW ORDER RESET
        function createNewOrder() {
            currentCart = [];
            document.getElementById('cust-name').value = 'Khách Lẻ';
            document.getElementById('cust-table').value = '';
            document.getElementById('discount-percent').value = 0;
            document.getElementById('item-note').value = '';
            document.querySelectorAll('.topping-checkbox').forEach(cb => cb.checked = false);
            renderCart();
            closeModal();
            showToast('Đã khởi tạo đơn hàng mới!');
        }

        // HELPERS
        function formatVND(amount) {
            return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
        }

        function showToast(message) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-message').textContent = message;
            toast.classList.remove('hidden');
            toast.classList.add('flex');
            setTimeout(() => {
                toast.classList.add('hidden');
                toast.classList.remove('flex');
            }, 3000);
        }
    </script>
</body>
</html>
