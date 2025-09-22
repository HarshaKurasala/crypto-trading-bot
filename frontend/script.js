// Crypto Trading Bot Frontend
class TradingInterface {
    constructor() {
        this.currentSymbol = 'BTCUSDT';
        this.currentOrderType = 'MARKET';
        this.currentSide = 'BUY';
        this.currentInterval = '1h';
        this.currentChartType = 'line';
        this.activeIndicators = new Set();
        this.isConnected = false;
        this.priceUpdateInterval = null;
        this.tradesUpdateInterval = null;
        this.ordersUpdateInterval = null;
        this.priceChart = null;
        this.priceAlerts = [];
        this.alertMonitoring = null;
        this.filterSelections = {
            timeframe: '1h',
            chartType: 'line'
        };
        this.chartSettings = {
            smaPeriod: 20,
            emaPeriod: 20,
            rsiPeriod: 14,
            macdFast: 12,
            macdSlow: 26,
            macdSignal: 9,
            bbPeriod: 20,
            bbStdDev: 2
        };
        
        this.init();
    }

    init() {
        try {
            this.setupEventListeners();
            this.updateTime();
            this.connectToBot();
            this.loadInitialData();
            this.startRealTimeUpdates();
            this.showNotification('Trading interface loaded successfully', 'success');
            this.renderIndicatorChips();
        } catch (error) {
            console.error('Error initializing trading interface:', error);
            this.showNotification('Error initializing interface', 'error');
        }
    }

    setupEventListeners() {
        // Symbol selection
        document.getElementById('symbolSelect').addEventListener('change', (e) => {
            this.currentSymbol = e.target.value;
            this.loadSymbolData();
            this.loadChartData();
        });

        // Order type tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setOrderType(e.target.dataset.type);
            });
        });

        // Side buttons
        document.querySelectorAll('.side-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setSide(e.target.dataset.side);
            });
        });

        // Quantity buttons
        document.querySelectorAll('.qty-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.getElementById('quantityInput').value = e.target.dataset.value;
                this.updateOrderSummary();
            });
        });

        // Quantity input
        document.getElementById('quantityInput').addEventListener('input', () => {
            this.updateOrderSummary();
        });

        // Price inputs
        document.getElementById('priceInput').addEventListener('input', () => {
            this.updateOrderSummary();
        });

        document.getElementById('stopPriceInput').addEventListener('input', () => {
            this.updateOrderSummary();
        });

        // Place order button
        document.getElementById('placeOrderBtn').addEventListener('click', () => {
            this.placeOrder();
        });

        // Settings modal
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.showSettingsModal();
        });

        document.getElementById('closeSettingsModal').addEventListener('click', () => {
            this.hideSettingsModal();
        });

        // Chart settings modal
        document.getElementById('chartSettingsBtn').addEventListener('click', () => {
            this.showChartSettingsModal();
        });

        document.getElementById('closeChartSettingsModal').addEventListener('click', () => {
            this.hideChartSettingsModal();
        });

        document.getElementById('applyChartSettings').addEventListener('click', () => {
            this.applyChartSettings();
        });

        document.getElementById('resetChartSettings').addEventListener('click', () => {
            this.resetChartSettings();
        });

        // Fullscreen button
        document.getElementById('fullscreenBtn').addEventListener('click', () => {
            this.toggleFullscreen();
        });

        // Collapsible sidebars
        const leftToggle = document.getElementById('toggleLeftSidebar');
        const rightToggle = document.getElementById('toggleRightSidebar');
        if (leftToggle) {
            leftToggle.addEventListener('click', () => this.toggleSidebar('left'));
        }
        if (rightToggle) {
            rightToggle.addEventListener('click', () => this.toggleSidebar('right'));
        }

        // Individual order cancel buttons are handled in renderOrders method

        // Timeframe buttons
        document.querySelectorAll('.timeframe-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setTimeframe(e.target.dataset.interval);
            });
        });

        // Chart type buttons
        document.querySelectorAll('.chart-type-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setChartType(e.target.dataset.type);
            });
        });

        // Indicator buttons
        document.querySelectorAll('.indicator-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.toggleIndicator(e.target.dataset.indicator);
            });
        });

        // Refresh buttons
        document.getElementById('refreshTradesBtn').addEventListener('click', () => {
            this.loadRecentTrades();
        });

        document.getElementById('refreshOrdersBtn').addEventListener('click', () => {
            this.loadOpenOrders();
        });

        document.getElementById('cancelAllOrdersBtn').addEventListener('click', () => {
            this.cancelAllOrders();
        });

        // Price alert functionality
        document.getElementById('priceAlertBtn').addEventListener('click', () => {
            this.showPriceAlertModal();
        });

        document.getElementById('closePriceAlertModal').addEventListener('click', () => {
            this.hidePriceAlertModal();
        });

        document.getElementById('setPriceAlert').addEventListener('click', () => {
            this.setPriceAlert();
        });

        document.getElementById('cancelPriceAlert').addEventListener('click', () => {
            this.hidePriceAlertModal();
        });

        // Account dropdown functionality
        document.getElementById('accountMenuBtn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleAccountDropdown();
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.user-menu')) {
                this.hideAccountDropdown();
            }
        });

        // Account dropdown items
        document.getElementById('accountProfileBtn').addEventListener('click', () => {
            this.showNotification('Profile feature coming soon', 'info');
            this.hideAccountDropdown();
        });

        document.getElementById('accountSettingsBtn').addEventListener('click', () => {
            this.showNotification('Account settings feature coming soon', 'info');
            this.hideAccountDropdown();
        });

        document.getElementById('accountSecurityBtn').addEventListener('click', () => {
            this.showNotification('Security settings feature coming soon', 'info');
            this.hideAccountDropdown();
        });

        document.getElementById('accountApiBtn').addEventListener('click', () => {
            this.showNotification('API management feature coming soon', 'info');
            this.hideAccountDropdown();
        });

        document.getElementById('accountLogoutBtn').addEventListener('click', () => {
            this.showNotification('Logout feature coming soon', 'info');
            this.hideAccountDropdown();
        });

        // Chart filters functionality
        // Segmented controls and inline panel
        const segmented = document.getElementById('chartSegmentedControls');
        if (segmented) {
            segmented.querySelectorAll('.segment-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const panel = e.currentTarget.dataset.panel;
                    segmented.querySelectorAll('.segment-btn').forEach(b => b.classList.remove('active'));
                    e.currentTarget.classList.add('active');
                    this.switchControlPanel(panel);
                });
            });
        }

        // Inline filters
        document.querySelectorAll('.filter-option').forEach(option => {
            option.addEventListener('click', (e) => {
                const type = e.currentTarget.dataset.type;
                const value = e.currentTarget.dataset.value;
                this.handleFilterOption(type, value, e.currentTarget);
            });
        });

        // Indicator toggles
        document.querySelectorAll('.indicator-toggle').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const ind = e.currentTarget.dataset.indicator;
                this.toggleIndicator(ind);
                e.currentTarget.classList.toggle('active');
                this.renderIndicatorChips();
            });
        });

        // Inline settings apply
        const applyInline = document.getElementById('applyInlineSettings');
        if (applyInline) {
            applyInline.addEventListener('click', () => {
                const s = parseInt(document.getElementById('smaPeriodInline').value);
                const e = parseInt(document.getElementById('emaPeriodInline').value);
                const r = parseInt(document.getElementById('rsiPeriodInline').value);
                const mf = parseInt(document.getElementById('macdFastInline').value);
                const ms = parseInt(document.getElementById('macdSlowInline').value);
                const mg = parseInt(document.getElementById('macdSignalInline').value);
                this.chartSettings = { smaPeriod: s, emaPeriod: e, rsiPeriod: r, macdFast: mf, macdSlow: ms, macdSignal: mg };
                this.loadChartData();
                this.showNotification('Chart settings applied', 'success');
            });
        }

        // Settings modal
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.showSettingsModal();
        });

        document.getElementById('closeSettingsModal').addEventListener('click', () => {
            this.hideSettingsModal();
        });

        // Chart settings modal
        document.getElementById('chartSettingsBtn').addEventListener('click', () => {
            this.showChartSettingsModal();
        });

        document.getElementById('closeChartSettingsModal').addEventListener('click', () => {
            this.hideChartSettingsModal();
        });

        document.getElementById('applyChartSettings').addEventListener('click', () => {
            this.applyChartSettings();
        });

        document.getElementById('resetChartSettings').addEventListener('click', () => {
            this.resetChartSettings();
        });

        // Fullscreen button
        document.getElementById('fullscreenBtn').addEventListener('click', () => {
            this.toggleFullscreen();
        });

        // Modal backdrop
        document.getElementById('settingsModal').addEventListener('click', (e) => {
            if (e.target.id === 'settingsModal') {
                this.hideSettingsModal();
            }
        });
    }

    async connectToBot() {
        try {
            // Simulate connection to bot
            await this.simulateConnection();
            this.setConnectionStatus(true);
            this.showNotification('Connected to trading bot', 'success');
        } catch (error) {
            this.setConnectionStatus(false);
            this.showNotification('Failed to connect to bot', 'error');
        }
    }

    async simulateConnection() {
        return new Promise((resolve) => {
            setTimeout(resolve, 2000);
        });
    }

    setConnectionStatus(connected) {
        this.isConnected = connected;
        const statusDot = document.getElementById('connectionStatus');
        const statusText = document.getElementById('connectionText');
        
        if (connected) {
            statusDot.classList.add('connected');
            statusText.textContent = 'Connected';
        } else {
            statusDot.classList.remove('connected');
            statusText.textContent = 'Disconnected';
        }
    }

    async loadInitialData() {
        await this.loadSymbols();
        await Promise.all([
            this.loadSymbolData(),
            this.loadAccountInfo(),
            this.loadOpenOrders(),
            this.loadRecentTrades()
        ]);
    }

    async loadSymbols() {
        try {
            const response = await fetch('/api/symbols');
            if (!response.ok) throw new Error('Failed to load symbols');
            const symbols = await response.json();
            const select = document.getElementById('symbolSelect');
            const current = this.currentSymbol;
            select.innerHTML = '';
            symbols.slice(0, 100).forEach(sym => {
                const opt = document.createElement('option');
                opt.value = sym;
                opt.textContent = `${sym.replace('USDT','')}/USDT`;
                select.appendChild(opt);
            });
            if (symbols.includes(current)) {
                select.value = current;
            } else if (symbols.length > 0) {
                this.currentSymbol = symbols[0];
                select.value = symbols[0];
            }
        } catch (e) {
            console.error('Error loading symbols:', e);
            this.showNotification('Using default symbols (failed to load from API)', 'warning');
        }
    }

    async loadSymbolData() {
        try {
            const symbolData = await this.getSymbolPrice(this.currentSymbol);
            this.updatePriceDisplay(symbolData);
            this.updateSymbolDisplay();
        } catch (error) {
            console.error('Error loading symbol data:', error);
            this.showNotification('Failed to load symbol data', 'error');
        }
    }

    async getSymbolPrice(symbol) {
        const response = await fetch(`/api/price/${symbol}`);
        if (!response.ok) throw new Error('Failed to fetch price');
        const data = await response.json();
        return data;
    }

    updatePriceDisplay(data) {
        const current = parseFloat(data.current_price || data.currentPrice || data.lastPrice || data.price || 0);
        const high = parseFloat(data.high_24h || data.highPrice || 0);
        const low = parseFloat(data.low_24h || data.lowPrice || 0);
        const vol = parseFloat(data.volume_24h || data.volume || 0);
        const changePct = parseFloat(data.price_change_percent_24h || data.priceChangePercent || 0);

        document.getElementById('currentPrice').textContent = `$${(current || 0).toLocaleString()}`;

        const priceChange = document.getElementById('priceChange');
        priceChange.textContent = `${changePct >= 0 ? '+' : ''}${(isNaN(changePct)?0:changePct).toFixed(2)}%`;
        priceChange.className = `price-change ${changePct >= 0 ? 'positive' : 'negative'}`;

        document.getElementById('high24h').textContent = `$${(high || 0).toLocaleString()}`;
        document.getElementById('low24h').textContent = `$${(low || 0).toLocaleString()}`;
        document.getElementById('volume24h').textContent = `${(vol || 0).toLocaleString()} ${this.currentSymbol.replace('USDT', '')}`;
    }

    updateSymbolDisplay() {
        const symbolName = this.currentSymbol.replace('USDT', '/USDT');
        document.getElementById('currentSymbol').textContent = symbolName;
    }

    setOrderType(type) {
        this.currentOrderType = type;
        
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.type === type);
        });
        
        // Show/hide price inputs
        const priceGroup = document.getElementById('priceGroup');
        const stopPriceGroup = document.getElementById('stopPriceGroup');
        
        if (type === 'MARKET') {
            priceGroup.style.display = 'none';
            stopPriceGroup.style.display = 'none';
        } else if (type === 'LIMIT') {
            priceGroup.style.display = 'block';
            stopPriceGroup.style.display = 'none';
        } else if (type === 'STOP_LIMIT') {
            priceGroup.style.display = 'block';
            stopPriceGroup.style.display = 'block';
        }
        
        this.updateOrderSummary();
    }

    setSide(side) {
        this.currentSide = side;
        
        // Update side buttons
        document.querySelectorAll('.side-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.side === side);
        });
        
        // Update place order button
        const placeOrderBtn = document.getElementById('placeOrderBtn');
        if (side === 'BUY') {
            placeOrderBtn.style.background = 'linear-gradient(135deg, #00d4aa 0%, #00b894 100%)';
            placeOrderBtn.innerHTML = '<i class="fas fa-arrow-up"></i> Buy';
        } else {
            placeOrderBtn.style.background = 'linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%)';
            placeOrderBtn.innerHTML = '<i class="fas fa-arrow-down"></i> Sell';
        }
        
        this.updateOrderSummary();
    }

    setTimeframe(interval) {
        this.currentInterval = interval;
        
        // Update timeframe buttons
        document.querySelectorAll('.timeframe-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.interval === interval);
        });
        
        // Load chart data for new timeframe
        this.loadChartData();
    }

    setChartType(type) {
        this.currentChartType = type;
        
        // Update UI to reflect the change
        document.querySelectorAll('.chart-type-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-type="${type}"]`)?.classList.add('active');
        
        // Reload chart with new type
        this.loadChartData();
        
        this.showNotification(`Chart type changed to ${type}`, 'info');
        this.syncInlineFilterUI();
    }

    toggleIndicator(indicator) {
        if (this.activeIndicators.has(indicator)) {
            this.activeIndicators.delete(indicator);
        } else {
            this.activeIndicators.add(indicator);
        }
        
        // Reload chart with updated indicators
        this.loadChartData();
        this.renderIndicatorChips();
    }

    updateOrderSummary() {
        const quantity = parseFloat(document.getElementById('quantityInput').value) || 0;
        const price = parseFloat(document.getElementById('priceInput').value) || parseFloat(document.getElementById('currentPrice').textContent.replace(/[$,]/g, ''));
        
        const estimatedValue = quantity * price;
        const fee = estimatedValue * 0.001; // 0.1% fee
        
        document.getElementById('estimatedValue').textContent = `$${estimatedValue.toFixed(2)}`;
        document.getElementById('estimatedFee').textContent = `$${fee.toFixed(2)}`;
    }

    async placeOrder() {
        const quantity = document.getElementById('quantityInput').value;
        const price = document.getElementById('priceInput').value;
        const stopPrice = document.getElementById('stopPriceInput').value;
        
        if (!quantity || parseFloat(quantity) <= 0) {
            this.showNotification('Please enter a valid quantity', 'error');
            return;
        }
        
        if (this.currentOrderType !== 'MARKET' && (!price || parseFloat(price) <= 0)) {
            this.showNotification('Please enter a valid price', 'error');
            return;
        }
        
        if (this.currentOrderType === 'STOP_LIMIT' && (!stopPrice || parseFloat(stopPrice) <= 0)) {
            this.showNotification('Please enter a valid stop price', 'error');
            return;
        }
        
        this.showLoading(true);
        try {
            const payload = {
                symbol: this.currentSymbol,
                side: this.currentSide,
                type: this.currentOrderType,
                quantity: quantity
            };
            if (this.currentOrderType !== 'MARKET') {
                payload.price = price;
            }
            if (this.currentOrderType === 'STOP_LIMIT') {
                payload.stop_price = stopPrice;
            }

            const response = await fetch('/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const err = await response.json().catch(() => ({}));
                throw new Error(err.error || 'Order failed');
            }
            const result = await response.json();
            this.showNotification(`Order placed successfully! Order ID: ${result.order_id || result.orderId || ''}`, 'success');
            this.clearOrderForm();
            await this.loadOpenOrders();
            await this.loadAccountInfo();
        } catch (error) {
            this.showNotification('Failed to place order: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    clearOrderForm() {
        document.getElementById('quantityInput').value = '';
        document.getElementById('priceInput').value = '';
        document.getElementById('stopPriceInput').value = '';
        this.updateOrderSummary();
    }

    async loadAccountInfo() {
        try {
            const response = await fetch('/api/account');
            if (!response.ok) throw new Error('Failed to load account');
            const account = await response.json();

            const usdt = (account.assets || []).find(a => a.asset === 'USDT') || {};
            const total = parseFloat(usdt.marginBalance || usdt.walletBalance || 0);
            const avail = parseFloat(usdt.availableBalance || 0);
            const pnl = parseFloat(usdt.unrealizedPnl || 0);

            document.getElementById('totalBalance').textContent = `$${total.toLocaleString()}`;
            document.getElementById('availableBalance').textContent = `$${avail.toLocaleString()}`;

            const pnlElement = document.getElementById('unrealizedPnl');
            pnlElement.textContent = `${pnl >= 0 ? '+' : ''}$${pnl.toLocaleString()}`;
            pnlElement.className = pnl >= 0 ? 'positive' : 'negative';
        } catch (error) {
            console.error('Error loading account info:', error);
        }
    }

    async loadOpenOrders() {
        try {
            const response = await fetch(`/api/orders?symbol=${this.currentSymbol}`);
            if (!response.ok) throw new Error('Failed to load orders');
            const orders = await response.json();
            const normalized = (orders || []).map(o => ({
                id: o.order_id || o.orderId || '',
                symbol: o.symbol,
                side: o.side,
                type: o.type,
                quantity: o.quantity || o.origQty,
                price: o.price || '',
                status: (o.status || 'NEW').toUpperCase(),
                time: o.time || o.update_time || Date.now()
            }));
            this.renderOrders(normalized);
        } catch (error) {
            console.error('Error loading open orders:', error);
        }
    }

    async cancelAllOrders() {
        if (!confirm('Are you sure you want to cancel all open orders?')) {
            return;
        }

        this.showLoading(true);
        try {
            const response = await fetch(`/api/orders/cancel-all?symbol=${this.currentSymbol}`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('Failed to cancel orders');
            }

            const result = await response.json();
            this.showNotification('All orders cancelled successfully', 'success');
            this.loadOpenOrders();
            this.loadAccountInfo();
        } catch (error) {
            console.error('Error cancelling orders:', error);
            this.showNotification('Failed to cancel orders', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async cancelOrder(orderId, symbol) {
        this.showLoading(true);
        try {
            const response = await fetch(`/api/orders/${orderId}?symbol=${symbol}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to cancel order');
            }

            const result = await response.json();
            this.showNotification('Order cancelled successfully', 'success');
            this.loadOpenOrders();
            this.loadAccountInfo();
        } catch (error) {
            console.error('Error cancelling order:', error);
            this.showNotification('Failed to cancel order', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    renderOrders(orders) {
        const ordersList = document.getElementById('ordersList');
        ordersList.innerHTML = '';
        
        if (orders.length === 0) {
            ordersList.innerHTML = '<div class="empty-state">No open orders</div>';
            return;
        }
        
        orders.forEach(order => {
            const orderElement = document.createElement('div');
            orderElement.className = 'order-item';
            orderElement.innerHTML = `
                <div class="order-header">
                    <span class="order-symbol">${order.symbol}</span>
                    <span class="order-status ${order.status.toLowerCase()}">${order.status}</span>
                </div>
                <div class="order-details">
                    <span>${order.side} ${order.quantity} @ $${order.price}</span>
                    <span>${new Date(order.time).toLocaleTimeString()}</span>
                </div>
                <div class="order-actions">
                    <button class="btn-danger btn-sm" onclick="window.tradingInterface.cancelOrder('${order.id}', '${order.symbol}')" title="Cancel Order">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            ordersList.appendChild(orderElement);
        });
    }

    async loadRecentTrades() {
        try {
            const response = await fetch(`/api/trades/${this.currentSymbol}?limit=20`);
            if (!response.ok) throw new Error('Failed to load trades');
            const tradesRaw = await response.json();
            const trades = (tradesRaw || []).map(t => ({
                price: t.price,
                quantity: t.qty || t.quantity,
                side: t.isBuyerMaker ? 'SELL' : 'BUY',
                time: t.time
            }));
            this.renderTrades(trades);
        } catch (error) {
            console.error('Error loading recent trades:', error);
        }
    }

    renderTrades(trades) {
        const tradesList = document.getElementById('tradesList');
        tradesList.innerHTML = '';
        
        trades.forEach(trade => {
            const tradeElement = document.createElement('div');
            tradeElement.className = 'trade-item';
            tradeElement.innerHTML = `
                <span class="trade-price ${trade.side.toLowerCase()}">$${parseFloat(trade.price).toLocaleString()}</span>
                <span>${trade.quantity}</span>
                <span class="trade-time">${new Date(trade.time).toLocaleTimeString()}</span>
            `;
            tradesList.appendChild(tradeElement);
        });
    }

    loadChartData() {
        // Show loading placeholder
        const chartPlaceholder = document.getElementById('chartPlaceholder');
        const canvas = document.getElementById('priceChart');
        
        chartPlaceholder.style.display = 'block';
        canvas.style.display = 'none';
        
        // Simulate API call to get chart data
        this.fetchChartData().then(data => {
            this.renderChart(data);
            chartPlaceholder.style.display = 'none';
            canvas.style.display = 'block';
        }).catch(error => {
            console.error('Error loading chart data:', error);
            chartPlaceholder.innerHTML = `
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load chart data</p>
            `;
        });
    }

    async fetchChartData() {
        // Simulate fetching chart data from API
        const response = await fetch(`/api/klines/${this.currentSymbol}?interval=${this.currentInterval}&limit=100`);
        if (!response.ok) {
            throw new Error('Failed to fetch chart data');
        }
        return await response.json();
    }

    renderChart(data) {
        const canvas = document.getElementById('priceChart');
        const ctx = canvas.getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.priceChart) {
            this.priceChart.destroy();
        }
        
        // Process the data for Chart.js
        const chartData = this.processChartData(data);
        
        // Create datasets based on chart type and indicators
        const datasets = this.createDatasets(chartData);
        
        // Create new chart
        this.priceChart = new Chart(ctx, {
            type: this.getChartType(),
            data: {
                labels: chartData.labels,
                datasets: datasets
            },
            options: this.getChartOptions()
        });
    }

    getChartType() {
        switch (this.currentChartType) {
            case 'candlestick':
                return 'bar';
            case 'area':
                return 'line';
            case 'ohlc':
                return 'bar';
            case 'bar':
                return 'bar';
            default:
                return 'line';
        }
    }

    createDatasets(chartData) {
        const datasets = [];
        
        // Main price dataset based on chart type
        if (this.currentChartType === 'candlestick' || this.currentChartType === 'ohlc') {
            // Create candlestick datasets
            const candlestickData = this.createCandlestickData(chartData.ohlc);
            datasets.push(...candlestickData);
        } else if (this.currentChartType === 'bar') {
            // Bar chart
            const barDataset = {
                label: `${this.currentSymbol} Price`,
                data: chartData.prices,
                backgroundColor: 'rgba(0, 212, 170, 0.6)',
                borderColor: '#00d4aa',
                borderWidth: 1,
                borderRadius: 2,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#00d4aa'
            };
            datasets.push(barDataset);
        } else {
            // Line/Area chart
            const mainDataset = {
                label: `${this.currentSymbol} Price`,
                data: chartData.prices,
                borderColor: '#00d4aa',
                backgroundColor: this.currentChartType === 'area' ? 'rgba(0, 212, 170, 0.1)' : '#00d4aa',
                borderWidth: 2,
                fill: this.currentChartType === 'area',
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#00d4aa'
            };
            datasets.push(mainDataset);
        }
        
        // Add indicators
        const settings = this.chartSettings || {
            smaPeriod: 20,
            emaPeriod: 20,
            rsiPeriod: 14,
            macdFast: 12,
            macdSlow: 26,
            macdSignal: 9
        };

        if (this.activeIndicators.has('sma')) {
            datasets.push({
                label: `SMA (${settings.smaPeriod})`,
                data: this.calculateSMA(chartData.prices, settings.smaPeriod),
                borderColor: '#ff6b35',
                backgroundColor: 'transparent',
                borderWidth: 2,
                borderDash: [5, 5],
                pointRadius: 0,
                pointHoverRadius: 4
            });
        }
        
        if (this.activeIndicators.has('ema')) {
            datasets.push({
                label: `EMA (${settings.emaPeriod})`,
                data: this.calculateEMA(chartData.prices, settings.emaPeriod),
                borderColor: '#ffd93d',
                backgroundColor: 'transparent',
                borderWidth: 2,
                borderDash: [3, 3],
                pointRadius: 0,
                pointHoverRadius: 4
            });
        }
        
        if (this.activeIndicators.has('rsi')) {
            const rsiData = this.calculateRSI(chartData.prices, settings.rsiPeriod);
            datasets.push({
                label: `RSI (${settings.rsiPeriod})`,
                data: rsiData,
                borderColor: '#ff6b9d',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 4,
                yAxisID: 'rsi'
            });
        }
        
        if (this.activeIndicators.has('macd')) {
            const macdData = this.calculateMACD(chartData.prices, settings.macdFast, settings.macdSlow, settings.macdSignal);
            datasets.push({
                label: 'MACD',
                data: macdData.macd,
                borderColor: '#00d4aa',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 4,
                yAxisID: 'macd'
            });
            datasets.push({
                label: 'Signal',
                data: macdData.signal,
                borderColor: '#ff6b35',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 4,
                yAxisID: 'macd'
            });
        }
        
        if (this.activeIndicators.has('bollinger')) {
            const bbData = this.calculateBollingerBands(chartData.prices, settings.smaPeriod);
            datasets.push({
                label: 'BB Upper',
                data: bbData.upper,
                borderColor: '#ff6b9d',
                backgroundColor: 'transparent',
                borderWidth: 1,
                borderDash: [3, 3],
                pointRadius: 0,
                pointHoverRadius: 4
            });
            datasets.push({
                label: 'BB Lower',
                data: bbData.lower,
                borderColor: '#ff6b9d',
                backgroundColor: 'transparent',
                borderWidth: 1,
                borderDash: [3, 3],
                pointRadius: 0,
                pointHoverRadius: 4
            });
        }
        
        return datasets;
    }

    getChartOptions() {
        const scales = {
            x: {
                display: true,
                grid: {
                    display: false
                },
                ticks: {
                    color: '#666',
                    maxTicksLimit: 8
                }
            },
            y: {
                display: true,
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                    color: '#666',
                    callback: function(value) {
                        return '$' + value.toFixed(2);
                    }
                },
                // For bar charts, ensure proper scaling
                beginAtZero: this.currentChartType === 'bar' || this.currentChartType === 'candlestick'
            }
        };

        // Add RSI y-axis if RSI is active
        if (this.activeIndicators.has('rsi')) {
            scales.rsi = {
                type: 'linear',
                display: true,
                position: 'right',
                grid: {
                    display: false
                },
                ticks: {
                    color: '#ff6b9d',
                    callback: function(value) {
                        return value.toFixed(0);
                    }
                },
                min: 0,
                max: 100
            };
        }

        // Add MACD y-axis if MACD is active
        if (this.activeIndicators.has('macd')) {
            scales.macd = {
                type: 'linear',
                display: true,
                position: 'right',
                grid: {
                    display: false
                },
                ticks: {
                    color: '#00d4aa',
                    callback: function(value) {
                        return value.toFixed(4);
                    }
                }
            };
        }

        return {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: this.activeIndicators.size > 0,
                    labels: {
                        color: '#fff',
                        usePointStyle: true,
                        pointStyle: 'line'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#00d4aa',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            if (context.dataset.yAxisID === 'rsi') {
                                return `${context.dataset.label}: ${context.parsed.y.toFixed(1)}`;
                            } else if (context.dataset.yAxisID === 'macd') {
                                return `${context.dataset.label}: ${context.parsed.y.toFixed(4)}`;
                            } else {
                                return `${context.dataset.label}: $${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                }
            },
            scales: scales
        };
    }

    processChartData(data) {
        // Process klines data for Chart.js
        const labels = [];
        const prices = [];
        const ohlc = [];
        
        data.forEach((candle, index) => {
            const timestamp = new Date(candle[0]);
            labels.push(timestamp.toLocaleTimeString());
            prices.push(parseFloat(candle[4])); // Close price
            
            // OHLC data: [open, high, low, close]
            ohlc.push({
                open: parseFloat(candle[1]),
                high: parseFloat(candle[2]),
                low: parseFloat(candle[3]),
                close: parseFloat(candle[4]),
                volume: parseFloat(candle[5]),
                index: index
            });
        });
        
        return { labels, prices, ohlc };
    }

    switchControlPanel(panel) {
        const container = document.getElementById('chartControlPanel');
        if (!container) return;
        container.querySelectorAll('.panel-content').forEach(el => {
            if (el.dataset.panel === panel) {
                el.classList.remove('hidden');
            } else {
                el.classList.add('hidden');
            }
        });
    }

    renderIndicatorChips() {
        const chips = document.getElementById('indicatorChips');
        const sym = document.getElementById('footerSymbol');
        if (sym) {
            sym.textContent = this.currentSymbol.replace('USDT','/USDT');
        }
        if (!chips) return;
        chips.innerHTML = '';
        const indicators = Array.from(this.activeIndicators);
        if (indicators.length === 0) {
            const chip = document.createElement('span');
            chip.className = 'chip muted';
            chip.textContent = 'No indicators';
            chips.appendChild(chip);
            return;
        }
        indicators.forEach(ind => {
            const chip = document.createElement('span');
            chip.className = 'chip';
            chip.textContent = ind.toUpperCase();
            chip.addEventListener('click', () => {
                this.toggleIndicator(ind);
                const toggleBtn = document.querySelector(`.indicator-toggle[data-indicator="${ind}"]`);
                if (toggleBtn) toggleBtn.classList.toggle('active');
                this.renderIndicatorChips();
            });
            chips.appendChild(chip);
        });
    }

    syncInlineFilterUI() {
        // Sync chart type buttons
        document.querySelectorAll('.filter-option[data-type="chartType"]').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.value === this.currentChartType);
        });
        // Sync timeframe
        document.querySelectorAll('.filter-option[data-type="timeframe"]').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.value === this.currentInterval);
        });
    }

    calculateSMA(prices, period) {
        const sma = [];
        for (let i = 0; i < prices.length; i++) {
            if (i < period - 1) {
                sma.push(null);
            } else {
                const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
                sma.push(sum / period);
            }
        }
        return sma;
    }

    calculateEMA(prices, period) {
        const ema = [];
        const multiplier = 2 / (period + 1);
        
        for (let i = 0; i < prices.length; i++) {
            if (i === 0) {
                ema.push(prices[i]);
            } else {
                ema.push((prices[i] * multiplier) + (ema[i - 1] * (1 - multiplier)));
            }
        }
        return ema;
    }

    calculateRSI(prices, period = 14) {
        const rsi = [];
        const gains = [];
        const losses = [];
        
        // Calculate price changes
        for (let i = 1; i < prices.length; i++) {
            const change = prices[i] - prices[i - 1];
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
        }
        
        // Calculate RSI
        for (let i = 0; i < prices.length; i++) {
            if (i < period) {
                rsi.push(null);
            } else {
                const avgGain = gains.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
                const avgLoss = losses.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
                const rs = avgGain / avgLoss;
                rsi.push(100 - (100 / (1 + rs)));
            }
        }
        
        return rsi;
    }

    calculateMACD(prices, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) {
        const ema12 = this.calculateEMA(prices, fastPeriod);
        const ema26 = this.calculateEMA(prices, slowPeriod);
        
        const macdLine = ema12.map((fast, i) => fast - ema26[i]);
        const signalLine = this.calculateEMA(macdLine.filter(val => val !== null), signalPeriod);
        
        return {
            macd: macdLine,
            signal: signalLine
        };
    }

    calculateBollingerBands(prices, period = 20, stdDev = 2) {
        const sma = this.calculateSMA(prices, period);
        const upperBand = [];
        const lowerBand = [];
        
        for (let i = 0; i < prices.length; i++) {
            if (i < period - 1) {
                upperBand.push(null);
                lowerBand.push(null);
            } else {
                const slice = prices.slice(i - period + 1, i + 1);
                const mean = slice.reduce((a, b) => a + b, 0) / period;
                const variance = slice.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / period;
                const standardDeviation = Math.sqrt(variance);
                
                upperBand.push(mean + (stdDev * standardDeviation));
                lowerBand.push(mean - (stdDev * standardDeviation));
            }
        }
        
        return {
            upper: upperBand,
            lower: lowerBand,
            middle: sma
        };
    }

    createCandlestickData(ohlcData) {
        const datasets = [];
        
        // Create candlestick bodies
        const bodyData = ohlcData.map((candle, index) => {
            const isGreen = candle.close >= candle.open;
            return {
                x: index,
                y: Math.abs(candle.close - candle.open),
                base: Math.min(candle.open, candle.close),
                color: isGreen ? '#00d4aa' : '#ff6b35',
                open: candle.open,
                high: candle.high,
                low: candle.low,
                close: candle.close
            };
        });
        
        // Create high-low wicks
        const wickData = ohlcData.map((candle, index) => ({
            x: index,
            y: candle.high - candle.low,
            base: candle.low,
            color: '#666'
        }));
        
        // Main candlestick dataset
        datasets.push({
            label: 'Candlesticks',
            data: bodyData,
            type: 'bar',
            backgroundColor: bodyData.map(d => d.color),
            borderColor: bodyData.map(d => d.color),
            borderWidth: 1,
            borderRadius: 0,
            pointRadius: 0,
            base: bodyData.map(d => d.base)
        });
        
        // High-low wicks dataset
        datasets.push({
            label: 'Wicks',
            data: wickData,
            type: 'bar',
            backgroundColor: wickData.map(d => d.color),
            borderColor: wickData.map(d => d.color),
            borderWidth: 1,
            borderRadius: 0,
            pointRadius: 0,
            base: wickData.map(d => d.base)
        });
        
        return datasets;
    }

    startRealTimeUpdates() {
        // Update price every 5 seconds
        this.priceUpdateInterval = setInterval(() => {
            this.loadSymbolData();
        }, 5000);
        
        // Update trades every 10 seconds
        this.tradesUpdateInterval = setInterval(() => {
            this.loadRecentTrades();
        }, 10000);
        
        // Update orders every 30 seconds
        this.ordersUpdateInterval = setInterval(() => {
            this.loadOpenOrders();
        }, 30000);
    }

    updateTime() {
        const timeDisplay = document.getElementById('currentTime');
        const updateTime = () => {
            const now = new Date();
            timeDisplay.textContent = now.toLocaleTimeString();
        };
        
        updateTime();
        setInterval(updateTime, 1000);
    }

    showSettingsModal() {
        document.getElementById('settingsModal').classList.add('active');
    }

    hideSettingsModal() {
        document.getElementById('settingsModal').classList.remove('active');
    }

    showChartSettingsModal() {
        document.getElementById('chartSettingsModal').classList.add('active');
    }

    hideChartSettingsModal() {
        document.getElementById('chartSettingsModal').classList.remove('active');
    }

    applyChartSettings() {
        // Get settings from form
        const smaPeriod = parseInt(document.getElementById('smaPeriod').value);
        const emaPeriod = parseInt(document.getElementById('emaPeriod').value);
        const rsiPeriod = parseInt(document.getElementById('rsiPeriod').value);
        const macdFast = parseInt(document.getElementById('macdFast').value);
        const macdSlow = parseInt(document.getElementById('macdSlow').value);
        const macdSignal = parseInt(document.getElementById('macdSignal').value);

        // Store settings
        this.chartSettings = {
            smaPeriod,
            emaPeriod,
            rsiPeriod,
            macdFast,
            macdSlow,
            macdSignal
        };

        // Reload chart with new settings
        this.loadChartData();
        this.hideChartSettingsModal();
        this.showNotification('Chart settings applied successfully', 'success');
    }

    resetChartSettings() {
        document.getElementById('smaPeriod').value = 20;
        document.getElementById('emaPeriod').value = 20;
        document.getElementById('rsiPeriod').value = 14;
        document.getElementById('macdFast').value = 12;
        document.getElementById('macdSlow').value = 26;
        document.getElementById('macdSignal').value = 9;

        this.chartSettings = {
            smaPeriod: 20,
            emaPeriod: 20,
            rsiPeriod: 14,
            macdFast: 12,
            macdSlow: 26,
            macdSignal: 9
        };

        this.loadChartData();
        this.showNotification('Chart settings reset to default', 'info');
    }

    showPriceAlertModal() {
        document.getElementById('priceAlertModal').classList.add('active');
        document.getElementById('alertSymbol').value = this.currentSymbol;
    }

    hidePriceAlertModal() {
        document.getElementById('priceAlertModal').classList.remove('active');
    }

    setPriceAlert() {
        const symbol = document.getElementById('alertSymbol').value;
        const type = document.getElementById('alertType').value;
        const price = parseFloat(document.getElementById('alertPrice').value);
        const notification = document.getElementById('alertNotification').value;

        if (!price || price <= 0) {
            this.showNotification('Please enter a valid price', 'error');
            return;
        }

        // Store the alert
        const alert = {
            id: Date.now(),
            symbol,
            type,
            price,
            notification,
            active: true,
            createdAt: new Date()
        };

        if (!this.priceAlerts) {
            this.priceAlerts = [];
        }
        this.priceAlerts.push(alert);

        // Save to localStorage
        localStorage.setItem('priceAlerts', JSON.stringify(this.priceAlerts));

        this.hidePriceAlertModal();
        this.showNotification(`Price alert set for ${symbol} at $${price}`, 'success');

        // Start monitoring if not already monitoring
        if (!this.alertMonitoring) {
            this.startAlertMonitoring();
        }
    }

    startAlertMonitoring() {
        this.alertMonitoring = setInterval(() => {
            if (this.priceAlerts && this.priceAlerts.length > 0) {
                this.checkPriceAlerts();
            }
        }, 10000); // Check every 10 seconds
    }

    checkPriceAlerts() {
        this.priceAlerts.forEach((alert, index) => {
            if (!alert.active) return;

            const currentPrice = this.getCurrentPrice(alert.symbol);
            if (!currentPrice) return;

            let triggered = false;
            let message = '';

            switch (alert.type) {
                case 'above':
                    if (currentPrice >= alert.price) {
                        triggered = true;
                        message = `${alert.symbol} price is now above $${alert.price}`;
                    }
                    break;
                case 'below':
                    if (currentPrice <= alert.price) {
                        triggered = true;
                        message = `${alert.symbol} price is now below $${alert.price}`;
                    }
                    break;
                case 'change':
                    // Calculate price change percentage
                    const changePercent = ((currentPrice - alert.price) / alert.price) * 100;
                    if (Math.abs(changePercent) >= 5) { // 5% change threshold
                        triggered = true;
                        message = `${alert.symbol} price changed by ${changePercent.toFixed(2)}%`;
                    }
                    break;
            }

            if (triggered) {
                this.triggerPriceAlert(alert, message);
                this.priceAlerts[index].active = false; // Deactivate alert
            }
        });
    }

    triggerPriceAlert(alert, message) {
        // Browser notification
        if (alert.notification === 'browser' || alert.notification === 'both') {
            if ('Notification' in window && Notification.permission === 'granted') {
                new Notification('Price Alert', {
                    body: message,
                    icon: '/favicon.ico'
                });
            }
        }

        // Sound notification
        if (alert.notification === 'sound' || alert.notification === 'both') {
            this.playAlertSound();
        }

        this.showNotification(message, 'warning');
    }

    playAlertSound() {
        // Create a simple beep sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1);

        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    }

    getCurrentPrice(symbol) {
        // This would typically get the current price from your data source
        // For now, we'll simulate with a random price
        return Math.random() * 50000 + 20000; // Simulated price
    }

    toggleAccountDropdown() {
        const dropdown = document.getElementById('accountDropdown');
        dropdown.classList.toggle('active');
    }

    hideAccountDropdown() {
        const dropdown = document.getElementById('accountDropdown');
        dropdown.classList.remove('active');
    }

    toggleChartFilters() {
        const menu = document.getElementById('chartFiltersMenu');
        menu.classList.toggle('active');
    }

    hideChartFilters() {
        const menu = document.getElementById('chartFiltersMenu');
        menu.classList.remove('active');
    }

    handleFilterOption(type, value, element) {
        // Remove active class from all options of the same type
        const options = document.querySelectorAll(`[data-type="${type}"]`);
        options.forEach(option => option.classList.remove('active'));
        
        // Add active class to clicked option
        element.classList.add('active');
        
        // Store the selection
        if (!this.filterSelections) {
            this.filterSelections = {};
        }
        this.filterSelections[type] = value;
    }

    resetChartFilters() {
        // Reset to default values
        this.filterSelections = {
            timeframe: '1h',
            chartType: 'line'
        };
        
        // Update UI
        document.querySelectorAll('.filter-option').forEach(option => {
            option.classList.remove('active');
        });
        
        // Set default active states
        document.querySelector('[data-type="timeframe"][data-value="1h"]').classList.add('active');
        document.querySelector('[data-type="chartType"][data-value="line"]').classList.add('active');
        
        this.showNotification('Filters reset to default', 'info');
    }

    applyChartFilters() {
        if (!this.filterSelections) {
            this.showNotification('No filters selected', 'warning');
            return;
        }

        // Apply timeframe
        if (this.filterSelections.timeframe) {
            this.setTimeframe(this.filterSelections.timeframe);
        }

        // Apply chart type
        if (this.filterSelections.chartType) {
            this.setChartType(this.filterSelections.chartType);
        }

        // Apply indicators
        if (this.filterSelections.indicator) {
            this.toggleIndicator(this.filterSelections.indicator);
        }

        this.hideChartFilters();
        this.showNotification('Chart filters applied successfully', 'success');
    }

    toggleFullscreen() {
        const chartContainer = document.querySelector('.chart-container');
        const fullscreenBtn = document.getElementById('fullscreenBtn');
        const icon = fullscreenBtn.querySelector('i');
        
        if (!document.fullscreenElement) {
            // Enter fullscreen
            if (chartContainer.requestFullscreen) {
                chartContainer.requestFullscreen();
            } else if (chartContainer.webkitRequestFullscreen) {
                chartContainer.webkitRequestFullscreen();
            } else if (chartContainer.msRequestFullscreen) {
                chartContainer.msRequestFullscreen();
            }
            icon.className = 'fas fa-compress';
            fullscreenBtn.title = 'Exit Fullscreen';
        } else {
            // Exit fullscreen
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
            icon.className = 'fas fa-expand';
            fullscreenBtn.title = 'Fullscreen';
        }
    }

    toggleSidebar(side) {
        if (side === 'left') {
            const el = document.querySelector('.sidebar-left');
            if (!el) return;
            el.classList.toggle('collapsed');
        } else if (side === 'right') {
            const el = document.querySelector('.sidebar-right');
            if (!el) return;
            el.classList.toggle('collapsed');
        }
        // Force a chart resize on next frame
        setTimeout(() => {
            if (this.priceChart) {
                this.priceChart.resize();
            }
        }, 100);
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.add('active');
        } else {
            overlay.classList.remove('active');
        }
    }

    showNotification(message, type = 'info') {
        const container = document.getElementById('notificationContainer');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        container.appendChild(notification);
        
        // Remove notification after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // Cleanup method
    destroy() {
        if (this.priceUpdateInterval) clearInterval(this.priceUpdateInterval);
        if (this.tradesUpdateInterval) clearInterval(this.tradesUpdateInterval);
        if (this.ordersUpdateInterval) clearInterval(this.ordersUpdateInterval);
        if (this.priceChart) {
            this.priceChart.destroy();
        }
    }
}

// Initialize the trading interface when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.tradingInterface = new TradingInterface();
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.tradingInterface) {
        window.tradingInterface.destroy();
    }
});

// Add some CSS for empty states
const style = document.createElement('style');
style.textContent = `
    .empty-state {
        text-align: center;
        padding: 20px;
        color: #a0aec0;
        font-size: 14px;
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style); 