// ===== PROFILE PAGE - User Profile Management =====

class ProfileManager {
  constructor() {
    this.userData = {};
    this.init();
  }

  async init() {
    try {
      await this.loadUserProfile();
      this.setupEventListeners();
      this.loadRecentActivity();
    } catch (error) {
      console.error('Profile initialization error:', error);
    }
  }

  async loadUserProfile() {
    try {
      // Load account information
      const accountResponse = await fetch('/api/account');
      if (!accountResponse.ok) throw new Error('Failed to fetch account data');
      const accountData = await accountResponse.json();
      
      this.userData = {
        name: accountData.name || 'Crypto Trader',
        email: accountData.email || 'trader@cryptobot.com',
        totalBalance: accountData.totalBalance || 10000,
        availableBalance: accountData.availableBalance || 9500,
        unrealizedPnl: accountData.unrealizedPnl || 250,
        joinDate: accountData.joinDate || new Date().getFullYear(),
        ...accountData
      };

      this.updateProfileUI();
    } catch (error) {
      console.error('Error loading profile:', error);
      this.showErrorMessage('Failed to load profile data');
    }
  }

  updateProfileUI() {
    // Update basic info
    document.getElementById('userName').textContent = this.userData.name;
    document.getElementById('memberSince').textContent = this.userData.joinDate;
    
    // Update account overview
    document.getElementById('totalBalance').textContent = `$${this.userData.totalBalance.toFixed(2)}`;
    document.getElementById('availableBalance').textContent = `$${this.userData.availableBalance.toFixed(2)}`;
    
    // Update P&L
    const pnlElement = document.getElementById('unrealizedPnl');
    pnlElement.textContent = `${this.userData.unrealizedPnl >= 0 ? '+' : ''}$${this.userData.unrealizedPnl.toFixed(2)}`;
    pnlElement.classList.toggle('positive', this.userData.unrealizedPnl >= 0);
    pnlElement.classList.toggle('negative', this.userData.unrealizedPnl < 0);
  }

  setupEventListeners() {
    // API Key Show/Hide functionality
    document.querySelectorAll('.btn-small').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const text = btn.textContent.trim();
        if (text === 'Show') {
          btn.textContent = 'Hide';
          btn.previousElementSibling.type = 'text';
        } else if (text === 'Hide') {
          btn.textContent = 'Show';
          btn.previousElementSibling.type = 'password';
        } else if (text === 'Copy') {
          this.copyToClipboard(btn.previousElementSibling.value);
          btn.textContent = 'Copied!';
          setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
        }
      });
    });

    // Back button
    const backBtn = document.querySelector('.back-button');
    if (backBtn) {
      backBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = '/';
      });
    }

    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // Remove active from all
        tabButtons.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        // Add active to clicked
        btn.classList.add('active');
        document.getElementById(tabName)?.classList.add('active');
      });
    });

    // Action buttons
    this.setupActionButtons();
  }

  setupActionButtons() {
    // Edit Risk Settings
    document.querySelectorAll('button').forEach(btn => {
      if (btn.textContent.includes('Edit Risk Settings')) {
        btn.addEventListener('click', () => this.openRiskModal());
      }
      if (btn.textContent.includes('Regenerate')) {
        btn.addEventListener('click', () => this.regenerateApiKeys());
      }
      if (btn.textContent.includes('Revoke')) {
        btn.addEventListener('click', () => this.revokeApiKeys());
      }
      if (btn.textContent.includes('Change Password')) {
        btn.addEventListener('click', () => this.openPasswordModal());
      }
      if (btn.textContent.includes('Logout All Devices')) {
        btn.addEventListener('click', () => this.logoutAllDevices());
      }
      if (btn.textContent.includes('Export CSV')) {
        btn.addEventListener('click', () => this.exportData());
      }
      if (btn.textContent.includes('Manage') && btn.parentElement.querySelector('i.fa-bell')) {
        btn.addEventListener('click', () => this.manageNotifications());
      }
      if (btn.textContent.includes('Delete')) {
        btn.addEventListener('click', () => this.deleteAccount());
      }
    });
  }

  async loadRecentActivity() {
    try {
      const response = await fetch('/api/trades/BTCUSDT?limit=5');
      if (response.ok) {
        const trades = await response.json();
        this.displayActivity(trades);
      }
    } catch (error) {
      console.error('Error loading activity:', error);
    }
  }

  displayActivity(trades) {
    // Activity is hardcoded in HTML, but this could be enhanced
    // to dynamically load from the API
  }

  openRiskModal() {
    // Create and show risk management modal
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h3>Risk Management Settings</h3>
          <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Max Position Size (%)</label>
            <input type="number" value="10" min="1" max="100" class="form-control">
          </div>
          <div class="form-group">
            <label>Stop Loss Default (%)</label>
            <input type="number" value="2.5" min="0.1" max="10" step="0.1" class="form-control">
          </div>
          <div class="form-group">
            <label>Take Profit Default (%)</label>
            <input type="number" value="5" min="0.1" max="20" step="0.1" class="form-control">
          </div>
          <div class="form-group">
            <label>Daily Loss Limit ($)</label>
            <input type="number" value="1000" class="form-control">
          </div>
          <div style="display: flex; gap: 8px; margin-top: 16px;">
            <button class="btn-secondary" style="flex: 1;">Cancel</button>
            <button class="btn-primary" style="flex: 1;">Save Changes</button>
          </div>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'flex';
    
    modal.querySelector('.modal-close').addEventListener('click', () => {
      modal.remove();
    });
    
    modal.querySelector('.btn-secondary').addEventListener('click', () => {
      modal.remove();
    });
  }

  async regenerateApiKeys() {
    if (!confirm('Are you sure you want to regenerate API keys? This will invalidate the current keys.')) return;
    
    try {
      // Call API to regenerate keys
      const response = await fetch('/api/regenerate-keys', { method: 'POST' });
      if (response.ok) {
        alert('API keys have been regenerated successfully!');
        // Reload keys display
      }
    } catch (error) {
      console.error('Error regenerating keys:', error);
      alert('Failed to regenerate API keys');
    }
  }

  async revokeApiKeys() {
    if (!confirm('Are you sure you want to revoke API keys? You will need to regenerate them.')) return;
    
    try {
      const response = await fetch('/api/revoke-keys', { method: 'POST' });
      if (response.ok) {
        alert('API keys have been revoked!');
      }
    } catch (error) {
      console.error('Error revoking keys:', error);
    }
  }

  openPasswordModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h3>Change Password</h3>
          <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Current Password</label>
            <input type="password" placeholder="Enter current password" class="form-control">
          </div>
          <div class="form-group">
            <label>New Password</label>
            <input type="password" placeholder="Enter new password" class="form-control">
          </div>
          <div class="form-group">
            <label>Confirm Password</label>
            <input type="password" placeholder="Confirm new password" class="form-control">
          </div>
          <div style="display: flex; gap: 8px; margin-top: 16px;">
            <button class="btn-secondary" style="flex: 1;">Cancel</button>
            <button class="btn-primary" style="flex: 1;">Change Password</button>
          </div>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'flex';
    
    modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
    modal.querySelector('.btn-secondary').addEventListener('click', () => modal.remove());
  }

  async logoutAllDevices() {
    if (!confirm('This will log you out from all devices. Continue?')) return;
    
    try {
      const response = await fetch('/api/logout-all', { method: 'POST' });
      if (response.ok) {
        alert('All sessions have been terminated. Please log in again.');
        window.location.href = '/login';
      }
    } catch (error) {
      console.error('Error logging out:', error);
    }
  }

  async exportData() {
    try {
      const response = await fetch('/api/export');
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'trading_data.csv';
        a.click();
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Error exporting data:', error);
      alert('Failed to export data');
    }
  }

  manageNotifications() {
    alert('Notification management panel would open here.');
  }

  deleteAccount() {
    if (!confirm('Are you sure you want to delete your account? This action cannot be undone!')) return;
    if (!confirm('Please type "DELETE" to confirm account deletion.')) return;
    
    try {
      // Call API to delete account
      alert('Account deletion is in development.');
    } catch (error) {
      console.error('Error deleting account:', error);
    }
  }

  copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
      console.log('Copied to clipboard');
    });
  }

  showErrorMessage(message) {
    const error = document.createElement('div');
    error.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #ef4444;
      color: white;
      padding: 12px 16px;
      border-radius: 8px;
      z-index: 9999;
    `;
    error.textContent = message;
    document.body.appendChild(error);
    
    setTimeout(() => error.remove(), 4000);
  }
}

// Initialize profile manager
document.addEventListener('DOMContentLoaded', () => {
  new ProfileManager();
});
