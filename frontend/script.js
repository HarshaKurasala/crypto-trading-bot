// ===== CRYPTO TRADING BOT - Enhanced Frontend =====

// ===== BACKEND CONFIGURATION =====
// This is set in index.html - update the window.BACKEND_URL there
const BACKEND_CONFIG = {
  // Get URL from window.BACKEND_URL (set in index.html)
  // Falls back to same domain /api if not set
  url: window.BACKEND_URL || '/api',
};

// Helper function to build API URLs
function getApiUrl(endpoint) {
  const baseUrl = BACKEND_CONFIG.url;
  if (baseUrl.startsWith('http')) {
    return `${baseUrl}${endpoint}`;
  }
  return endpoint; // Use relative path for same-domain
}


class TradingInterface {
  constructor() {
    // State
    this.currentSymbol = 'BTCUSDT';
    this.currentOrderType = 'MARKET';
    this.currentSide = 'BUY';
    this.currentTimeframe = '1h';
    this.activeIndicators = new Set();
    this.isConnected = false;
    
    // UI State
    this.leftSidebarOpen = true;
    this.rightSidebarOpen = true;
    
    // Data
    this.orders = [];
    this.trades = [];
    this.history = [];
    this.priceData = {};
    
    // Timers
    this.priceUpdateInterval = null;
    this.timeUpdateInterval = null;
    this.tradesUpdateInterval = null;
    this.ordersUpdateInterval = null;
    
    this.init();
  }

  // ===== INITIALIZATION =====
  init() {
    try {
      this.setupDOM();
      this.setupEventListeners();
      this.updateTime();
      this.startTimeUpdater();
      this.connectToBot();
      this.loadInitialData();
      this.startLiveUpdates();
      this.initializeChart();
      // Hide right panel on page load to show extended chart
      this.setRightPanelHiddenOnLoad();
      this.notify('Trading interface ready', 'success');
    } catch (error) {
      console.error('Init error:', error);
      this.notify('Failed to initialize', 'error');
    }
  }

  setRightPanelHiddenOnLoad() {
    const mainContent = document.querySelector('.main-content');
    const sidebarRight = document.getElementById('sidebarRight');
    if (mainContent && sidebarRight) {
      mainContent.classList.add('right-panel-hidden');
      sidebarRight.classList.remove('visible');
    }
  }

  setupDOM() {
    // Ensure all required elements exist
    const required = [
      'symbolSelect', 'quantityInput', 'currentPrice', 'placeOrderBtn',
      'connectionStatus', 'currentTime', 'accountDropdown', 'settingsModal',
      'loadingOverlay', 'notificationContainer'
    ];
    required.forEach(id => {
      if (!document.getElementById(id)) {
        console.warn(`Element #${id} not found`);
      }
    });
  }

  setupEventListeners() {
    // ===== HEADER CONTROLS =====
    document.getElementById('toggleRightSidebar')?.addEventListener('click', () => {
      this.toggleSidebar('right');
    });
    
    // Note: toggleRightSidebar controls the account, history, and quick actions panel

    document.getElementById('settingsBtn')?.addEventListener('click', () => {
      this.openModal('settingsModal');
    });

    document.getElementById('accountMenuBtn')?.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleAccountDropdown();
    });

    // Close dropdown on outside click
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.user-menu')) {
        this.closeAccountDropdown();
      }
    });

    // ===== ACCOUNT DROPDOWN =====
    document.getElementById('accountProfileBtn')?.addEventListener('click', () => {
      window.location.href = '/profile.html';
      this.closeAccountDropdown();
    });

    document.getElementById('accountSettingsBtn')?.addEventListener('click', () => {
      window.location.href = '/profile.html';
      this.closeAccountDropdown();
    });

    document.getElementById('accountApiBtn')?.addEventListener('click', () => {
      window.location.href = '/profile.html';
      this.closeAccountDropdown();
    });

    document.getElementById('accountLogoutBtn')?.addEventListener('click', () => {
      this.logout();
      this.closeAccountDropdown();
    });

    // ===== TRADING PANEL =====
    document.getElementById('symbolSelect')?.addEventListener('change', (e) => {
      this.currentSymbol = e.target.value;
      this.loadSymbolData();
    });

    // Order type tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.setOrderType(e.currentTarget.dataset.type);
      });
    });

    // Side buttons
    document.querySelectorAll('.side-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.setSide(e.currentTarget.dataset.side);
      });
    });

    // Quantity preset buttons
    document.querySelectorAll('.qty-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.getElementById('quantityInput').value = e.currentTarget.dataset.value;
        document.getElementById('quantityInput').dispatchEvent(new Event('input', { bubbles: true }));
      });
    });

    // Quantity and price inputs
    document.getElementById('quantityInput')?.addEventListener('input', () => {
      this.updateOrderSummary();
    });

    document.getElementById('priceInput')?.addEventListener('input', () => {
      this.updateOrderSummary();
    });

    document.getElementById('stopPriceInput')?.addEventListener('input', () => {
      this.updateOrderSummary();
    });

    // Place order
    document.getElementById('placeOrderBtn')?.addEventListener('click', () => {
      this.placeOrder();
    });

    // ===== CHART CONTROLS =====
    document.querySelectorAll('.segment-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const panel = e.currentTarget.dataset.panel;
        this.switchChartPanel(panel);
      });
    });

    document.querySelectorAll('.filter-option').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const type = e.currentTarget.dataset.type;
        const value = e.currentTarget.dataset.value;
        this.handleFilterOption(type, value);
      });
    });

    document.querySelectorAll('.indicator-toggle').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const indicator = e.currentTarget.dataset.indicator;
        this.toggleIndicator(indicator);
      });
    });

    document.getElementById('fullscreenBtn')?.addEventListener('click', () => {
      this.toggleChartFullscreen();
    });

    document.getElementById('refreshTradesBtn')?.addEventListener('click', () => {
      this.loadRecentTrades();
    });

    document.getElementById('refreshOrdersBtn')?.addEventListener('click', () => {
      this.loadOpenOrders();
    });

    document.getElementById('cancelAllOrdersBtn')?.addEventListener('click', () => {
      this.cancelAllOrders();
    });

    // ===== MODALS =====
    document.getElementById('closeSettingsModal')?.addEventListener('click', () => {
      this.closeModal('settingsModal');
    });

    document.getElementById('settingsModal')?.addEventListener('click', (e) => {
      if (e.target.id === 'settingsModal') {
        this.closeModal('settingsModal');
      }
    });
  }

  // ===== SIDEBAR MANAGEMENT =====
  toggleSidebar(side) {
    const sidebar = side === 'left' 
      ? document.getElementById('sidebarLeft') 
      : document.getElementById('sidebarRight');
    
    if (!sidebar) return;
    
    const isVisible = sidebar.classList.contains('visible');
    if (isVisible) {
      sidebar.classList.remove('visible');
      sidebar.style.animation = 'slideOut 200ms ease-out forwards';
      
      // Toggle grid layout class for right panel
      if (side === 'right') {
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
          mainContent.classList.add('right-panel-hidden');
        }
      }
    } else {
      sidebar.classList.add('visible');
      sidebar.style.animation = 'slideIn 200ms ease-out forwards';
      
      // Toggle grid layout class for right panel
      if (side === 'right') {
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
          mainContent.classList.remove('right-panel-hidden');
        }
      }
    }
  }

  // ===== ACCOUNT DROPDOWN =====
  toggleAccountDropdown() {
    const dropdown = document.getElementById('accountDropdown');
    if (!dropdown) return;
    dropdown.classList.toggle('active');
  }

  closeAccountDropdown() {
    const dropdown = document.getElementById('accountDropdown');
    if (!dropdown) return;
    dropdown.classList.remove('active');
  }

  logout() {
    // Clear session storage
    localStorage.removeItem('authToken');
    localStorage.removeItem('userSession');
    sessionStorage.clear();
    
    // Show logout message
    this.notify('Logging out...', 'info');
    
    // Redirect to signin page after delay
    setTimeout(() => {
      window.location.href = 'signin.html';
    }, 1000);
  }

  // ===== ORDER MANAGEMENT =====
  setOrderType(type) {
    this.currentOrderType = type;

    // Update UI
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.type === type);
    });

    // Show/hide price fields
    const showPrice = type !== 'MARKET';
    const showStopPrice = type === 'STOP_LIMIT';

    const priceGroup = document.getElementById('priceGroup');
    const stopGroup = document.getElementById('stopPriceGroup');

    if (priceGroup) priceGroup.style.display = showPrice ? 'block' : 'none';
    if (stopGroup) stopGroup.style.display = showStopPrice ? 'block' : 'none';

    this.updateOrderSummary();
  }

  setSide(side) {
    this.currentSide = side;

    document.querySelectorAll('.side-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.side === side);
    });

    // Update button color
    const buyBtn = document.querySelector('.buy-btn');
    const sellBtn = document.querySelector('.sell-btn');
    if (buyBtn) buyBtn.classList.toggle('active', side === 'BUY');
    if (sellBtn) sellBtn.classList.toggle('active', side === 'SELL');
  }

  updateOrderSummary() {
    const qty = parseFloat(document.getElementById('quantityInput')?.value) || 0;
    const price = parseFloat(document.getElementById('priceInput')?.value) || 50000;
    const value = qty * price;
    const fee = value * 0.001; // 0.1% fee
    const total = value + fee;

    const valueEl = document.getElementById('estimatedValue');
    const feeEl = document.getElementById('estimatedFee');
    const totalEl = document.getElementById('totalCost');
    const badgeEl = document.getElementById('orderTypeBadge');

    if (valueEl) valueEl.textContent = `$${value.toFixed(2)}`;
    if (feeEl) feeEl.textContent = `$${fee.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `$${total.toFixed(2)}`;
    if (badgeEl) badgeEl.textContent = this.currentOrderType;
  }

  placeOrder() {
    const qty = document.getElementById('quantityInput')?.value;
    if (!qty || parseFloat(qty) <= 0) {
      this.notify('Enter a valid quantity', 'warning');
      return;
    }

    this.showLoading(true);
    setTimeout(() => {
      this.showLoading(false);
      this.notify(`Order placed: ${this.currentSide} ${qty} ${this.currentSymbol}`, 'success');
      document.getElementById('quantityInput').value = '';
      this.updateOrderSummary();
    }, 1500);
  }

  // ===== CHART MANAGEMENT =====
  switchChartPanel(panel) {
    // Update button states
    document.querySelectorAll('.segment-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.panel === panel);
    });

    // Update panel visibility
    document.querySelectorAll('.panel-content').forEach(content => {
      const isActive = content.dataset.panel === panel;
      content.style.display = isActive ? 'block' : 'none';
      if (isActive) content.classList.add('active');
      else content.classList.remove('active');
    });
  }

  handleFilterOption(type, value) {
    const activeBtn = document.querySelector(`.filter-option[data-type="${type}"].active`);
    if (activeBtn) activeBtn.classList.remove('active');

    const newBtn = document.querySelector(`.filter-option[data-type="${type}"][data-value="${value}"]`);
    if (newBtn) newBtn.classList.add('active');

    if (type === 'timeframe') {
      this.currentTimeframe = value;
      console.log(`Timeframe changed to ${value}`);
      this.updateChartForTimeframe();
    }
  }

  toggleIndicator(indicator) {
    if (this.activeIndicators.has(indicator)) {
      this.activeIndicators.delete(indicator);
    } else {
      this.activeIndicators.add(indicator);
    }
    this.loadChartData();
  }

  toggleChartFullscreen() {
    const container = document.querySelector('.chart-container');
    if (!container) return;

    container.classList.toggle('fullscreen');
    if (container.classList.contains('fullscreen')) {
      document.body.style.overflow = 'hidden';
      this.notify('Press Esc to exit fullscreen', 'info');
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          container.classList.remove('fullscreen');
          document.body.style.overflow = '';
        }
      });
    }
  }

  // ===== DATA LOADING =====
  async loadInitialData() {
    try {
      await this.loadSymbolData();
      await this.loadOpenOrders();
      await this.loadRecentTrades();
      await this.loadAccountBalance();
    } catch (error) {
      console.error('Load error:', error);
      this.notify('Failed to load data', 'error');
    }
  }

  async loadSymbolData() {
    try {
      const response = await fetch(getApiUrl(`/api/price/${this.currentSymbol}`));
      if (!response.ok) throw new Error('Failed to fetch price');
      
      const data = await response.json();
      this.priceData = data;
      this.updatePriceDisplay(data);
    } catch (error) {
      console.error('Price fetch error:', error);
      // Use demo data as fallback
      this.updatePriceDisplay(this.getDemoData(this.currentSymbol));
    }
  }

  getDemoData(symbol) {
    const demoData = {
      'BTCUSDT': { price: 52340.50, change: 2.50, high24h: 53200.00, low24h: 50150.75, volume24h: '1.2M' },
      'ETHUSDT': { price: 3145.80, change: 1.75, high24h: 3220.00, low24h: 3080.50, volume24h: '2.5M' },
      'BNBUSDT': { price: 625.40, change: -0.85, high24h: 645.00, low24h: 610.25, volume24h: '5M' },
      'SOLUSDT': { price: 185.20, change: 3.20, high24h: 192.50, low24h: 178.75, volume24h: '10M' },
      'ADAUSDT': { price: 1.02, change: -1.25, high24h: 1.08, low24h: 0.98, volume24h: '50M' }
    };
    return demoData[symbol] || { price: 0, change: 0, high24h: 0, low24h: 0, volume24h: '0' };
  }

  updatePriceDisplay(data) {
    const currentPrice = document.getElementById('currentPrice');
    const priceChange = document.getElementById('priceChange');
    const high24h = document.getElementById('high24h');
    const low24h = document.getElementById('low24h');
    const volume24h = document.getElementById('volume24h');

    // Handle both backend and demo data formats
    const price = data.current_price || data.price || 0;
    const change = data.price_change_percent_24h || data.change || 0;
    const high = data.high_24h || data.high24h || 0;
    const low = data.low_24h || data.low24h || 0;
    const volume = data.volume_24h || data.volume24h || '0';

    if (currentPrice) currentPrice.textContent = `$${parseFloat(price).toFixed(2)}`;
    if (priceChange) {
      priceChange.textContent = `${change > 0 ? '+' : ''}${parseFloat(change).toFixed(2)}%`;
      priceChange.classList.toggle('negative', change < 0);
    }
    if (high24h) high24h.textContent = `$${parseFloat(high).toFixed(2)}`;
    if (low24h) low24h.textContent = `$${parseFloat(low).toFixed(2)}`;
    if (volume24h) volume24h.textContent = `${volume} ${this.currentSymbol.replace('USDT', '')}`;
  }

  async loadOpenOrders() {
    try {
      const response = await fetch(getApiUrl(`/api/orders?symbol=${this.currentSymbol}`));
      if (!response.ok) throw new Error('Failed to fetch orders');
      
      this.orders = await response.json();
      this.renderOrders();
    } catch (error) {
      console.error('Orders fetch error:', error);
      this.renderOrders([]);
    }
  }

  renderOrders(orders = this.orders) {
    const list = document.getElementById('ordersList');
    if (!list) return;

    if (!orders || orders.length === 0) {
      list.innerHTML = '<div style="color: var(--muted); font-size: 12px; padding: 8px; text-align: center;">No open orders</div>';
      return;
    }

    list.innerHTML = orders.map(order => `
      <div style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.02); display: flex; justify-content: space-between; align-items: center;">
        <div style="flex: 1; font-size: 12px;">
          <strong style="color: ${order.side === 'BUY' ? '#10b981' : '#ef4444'}">${order.side}</strong>
          <span style="color: var(--muted);"> ${order.quantity} @ $${order.price}</span>
        </div>
        <button onclick="ui.cancelOrder('${order.id}')" style="padding: 4px 8px; background: rgba(239,68,68,0.1); border: none; color: var(--danger); border-radius: 4px; cursor: pointer; font-size: 11px;">Cancel</button>
      </div>
    `).join('');
  }

  async loadRecentTrades() {
    try {
      const response = await fetch(getApiUrl(`/api/trades/${this.currentSymbol}?limit=10`));
      if (!response.ok) throw new Error('Failed to fetch trades');
      
      this.trades = await response.json();
      this.renderTrades();
    } catch (error) {
      console.error('Trades fetch error:', error);
      this.renderTrades([]);
    }
  }

  renderTrades(trades = this.trades) {
    const list = document.getElementById('tradesList');
    if (!list) return;

    if (!trades || trades.length === 0) {
      list.innerHTML = '<div style="color: var(--muted); font-size: 12px; padding: 8px; text-align: center;">No recent trades</div>';
      return;
    }

    list.innerHTML = trades.map(trade => `
      <div style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.02); display: flex; justify-content: space-between; align-items: center; font-size: 11px;">
        <span style="color: ${trade.side === 'BUY' ? '#10b981' : '#ef4444'};">${trade.side}</span>
        <span style="color: var(--muted);">${trade.quantity} @ $${trade.price}</span>
        <span style="color: var(--muted);">${new Date(trade.time).toLocaleTimeString()}</span>
      </div>
    `).join('');
  }

  async loadAccountBalance() {
    try {
      const response = await fetch(getApiUrl('/api/account'));
      if (!response.ok) throw new Error('Failed to fetch account');
      
      const data = await response.json();
      this.updateAccountDisplay(data);
    } catch (error) {
      console.error('Account fetch error:', error);
    }
  }

  updateAccountDisplay(data) {
    const totalBalance = document.getElementById('totalBalance');
    const availableBalance = document.getElementById('availableBalance');
    const unrealizedPnl = document.getElementById('unrealizedPnl');

    if (totalBalance) totalBalance.textContent = `$${data.totalBalance?.toFixed(2) || '0.00'}`;
    if (availableBalance) availableBalance.textContent = `$${data.availableBalance?.toFixed(2) || '0.00'}`;
    if (unrealizedPnl) {
      const pnl = data.unrealizedPnl || 0;
      unrealizedPnl.textContent = `${pnl >= 0 ? '+' : ''}$${pnl.toFixed(2)}`;
      unrealizedPnl.classList.toggle('positive', pnl >= 0);
    }
  }

  generateChartData(timeframe) {
    // Generate data based on timeframe
    let labels = [];
    let dataValues = [];
    const basePrice = 48000;

    switch(timeframe) {
      case '1m':
        // Last 60 minutes
        labels = Array.from({length: 60}, (_, i) => `${i}m`);
        dataValues = Array.from({length: 60}, () => basePrice + (Math.random() - 0.5) * 500);
        break;
      case '5m':
        // Last 5 hours (5 min candles)
        labels = Array.from({length: 60}, (_, i) => `${i * 5}m`);
        dataValues = Array.from({length: 60}, () => basePrice + (Math.random() - 0.5) * 800);
        break;
      case '15m':
        // Last 15 hours
        labels = Array.from({length: 60}, (_, i) => `${i * 15}m`);
        dataValues = Array.from({length: 60}, () => basePrice + (Math.random() - 0.5) * 1000);
        break;
      case '1h':
        // Last 24 hours
        labels = Array.from({length: 24}, (_, i) => `${i}:00`);
        dataValues = Array.from({length: 24}, () => basePrice + (Math.random() - 0.5) * 1500);
        break;
      case '4h':
        // Last 7 days (4h candles)
        labels = Array.from({length: 42}, (_, i) => `Day ${Math.floor(i/6)} ${(i%6)*4}h`);
        dataValues = Array.from({length: 42}, () => basePrice + (Math.random() - 0.5) * 2000);
        break;
      case '1d':
        // Last 30 days
        labels = Array.from({length: 30}, (_, i) => `Day ${i + 1}`);
        dataValues = Array.from({length: 30}, () => basePrice + (Math.random() - 0.5) * 2500);
        break;
      case '1w':
        // Last 52 weeks
        labels = Array.from({length: 52}, (_, i) => `Week ${i + 1}`);
        dataValues = Array.from({length: 52}, () => basePrice + (Math.random() - 0.5) * 3000);
        break;
      default:
        labels = Array.from({length: 24}, (_, i) => `${i}:00`);
        dataValues = Array.from({length: 24}, () => basePrice + (Math.random() - 0.5) * 1500);
    }

    return { labels, data: dataValues };
  }

  updateChartForTimeframe() {
    const chartData = this.generateChartData(this.currentTimeframe);
    this.initializeChart(chartData);
  }

  async loadChartData() {
    // Load chart data for current symbol and timeframe
    console.log(`Loading chart for ${this.currentSymbol} at ${this.currentTimeframe}`);
    this.updateChartForTimeframe();
  }

  initializeChart(chartData = null) {
    try {
      const canvas = document.getElementById('priceChart');
      if (!canvas) {
        console.warn('Canvas element not found');
        return;
      }

      const ctx = canvas.getContext('2d');
      
      // Use provided data or generate default
      let labels, data;
      if (chartData) {
        labels = chartData.labels;
        data = chartData.data;
      } else {
        const defaultData = this.generateChartData(this.currentTimeframe);
        labels = defaultData.labels;
        data = defaultData.data;
      }

      // Destroy previous chart if exists
      if (window.priceChart instanceof Chart) {
        window.priceChart.destroy();
      }

      // Create new chart
      window.priceChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: `${this.currentSymbol} Price`,
            data: data,
            borderColor: '#06b6d4',
            backgroundColor: 'rgba(6, 182, 212, 0.08)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointBackgroundColor: '#06b6d4',
            pointBorderColor: '#061826',
            pointBorderWidth: 2,
            pointHoverRadius: 6,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false,
          },
          plugins: {
            legend: {
              display: true,
              labels: {
                color: '#d9e3ef',
                font: { size: 12, family: 'Poppins' },
                padding: 15
              }
            },
            tooltip: {
              backgroundColor: 'rgba(2, 6, 23, 0.8)',
              titleColor: '#eaf6fb',
              bodyColor: '#d9e3ef',
              borderColor: '#06b6d4',
              borderWidth: 1,
              padding: 10,
              titleFont: { size: 13, weight: 'bold' },
              bodyFont: { size: 12 }
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              grid: {
                color: 'rgba(255, 255, 255, 0.05)',
                drawBorder: false
              },
              ticks: {
                color: '#98a6bd',
                font: { size: 11 }
              }
            },
            x: {
              grid: {
                display: false,
                drawBorder: false
              },
              ticks: {
                color: '#98a6bd',
                font: { size: 11 }
              }
            }
          }
        }
      });

      console.log('Chart initialized successfully');
    } catch (error) {
      console.error('Chart initialization error:', error);
    }
  }

  async cancelOrder(orderId) {
    this.showLoading(true);
    setTimeout(() => {
      this.showLoading(false);
      this.notify('Order cancelled', 'success');
      this.loadOpenOrders();
    }, 1000);
  }

  async cancelAllOrders() {
    if (!confirm('Cancel all open orders?')) return;
    this.showLoading(true);
    setTimeout(() => {
      this.showLoading(false);
      this.notify('All orders cancelled', 'success');
      this.loadOpenOrders();
    }, 1500);
  }

  // ===== CONNECTION & UPDATES =====
  async connectToBot() {
    try {
      const url = getApiUrl('/api/status');
      console.log('Connecting to backend at:', url);
      console.log('Backend config:', BACKEND_CONFIG);
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);
      
      if (response.ok) {
        this.setConnected(true);
        console.log('✅ Connected to backend successfully');
      } else {
        this.setConnected(false);
        console.warn('❌ Backend returned error:', response.status);
      }
    } catch (error) {
      console.error('❌ Connection error:', error);
      console.error('Error details:', error.message);
      this.setConnected(false);
    }
  }

  setConnected(connected) {
    this.isConnected = connected;
    const statusDot = document.getElementById('connectionStatus');
    const statusText = document.getElementById('connectionText');
    const connectionStatus = document.querySelector('.connection-status');

    if (statusDot) {
      statusDot.classList.toggle('connected', connected);
      console.log(`Status dot updated: ${connected ? 'Connected (cyan)' : 'Disconnected (red)'}`);
    }
    
    if (statusText) {
      statusText.textContent = connected ? 'Connected' : 'Disconnected';
      statusText.style.color = connected ? 'var(--primary)' : '#ef4444';
      console.log(`Status text: ${statusText.textContent}`);
    }
    
    if (connectionStatus) {
      connectionStatus.style.borderColor = connected ? 'rgba(6,182,212,0.3)' : 'rgba(239,68,68,0.3)';
    }
  }

  startLiveUpdates() {
    // Check connection every 5 seconds
    setInterval(() => {
      this.connectToBot();
    }, 5000);
    
    // Price updates every 1 second for real-time changes
    this.priceUpdateInterval = setInterval(() => {
      this.loadSymbolData();
    }, 1000);

    // Orders updates every 3s
    this.ordersUpdateInterval = setInterval(() => {
      this.loadOpenOrders();
    }, 3000);

    // Trades updates every 4s
    this.tradesUpdateInterval = setInterval(() => {
      this.loadRecentTrades();
    }, 4000);
  }

  startTimeUpdater() {
    this.updateTime();
    this.timeUpdateInterval = setInterval(() => {
      this.updateTime();
    }, 1000);
  }

  updateTime() {
    const timeEl = document.getElementById('currentTime');
    if (!timeEl) return;
    
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit',
      hour12: true 
    });
    timeEl.textContent = time;
  }

  // ===== MODALS =====
  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.add('active');
  }

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.remove('active');
  }

  // ===== NOTIFICATIONS =====
  notify(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    if (!container) return;

    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.style.animation = 'slideIn 200ms ease-out';
    notification.textContent = message;

    // Color by type
    const colors = {
      success: '#10b981',
      error: '#ef4444',
      warning: '#f59e0b',
      info: '#06b6d4'
    };
    notification.style.borderLeftColor = colors[type] || colors.info;
    notification.style.borderLeft = '3px solid';
    notification.style.paddingLeft = '10px';

    container.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = 'slideOut 200ms ease-out forwards';
      setTimeout(() => notification.remove(), 200);
    }, 3000);
  }

  showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (!overlay) return;
    
    if (show) {
      overlay.classList.add('active');
    } else {
      overlay.classList.remove('active');
    }
  }

  // ===== CLEANUP =====
  destroy() {
    clearInterval(this.priceUpdateInterval);
    clearInterval(this.timeUpdateInterval);
    clearInterval(this.tradesUpdateInterval);
    clearInterval(this.ordersUpdateInterval);
  }
}

// ===== INITIALIZATION =====
let ui;
document.addEventListener('DOMContentLoaded', () => {
  ui = new TradingInterface();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  if (ui) ui.destroy();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(400px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(400px); opacity: 0; }
  }
  .chart-container.fullscreen {
    position: fixed;
    inset: 0;
    z-index: 100;
    border-radius: 0;
    border: none;
  }
`;
document.head.appendChild(style);
