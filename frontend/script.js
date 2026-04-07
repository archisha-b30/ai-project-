let predictionChart;
let autoRefreshInterval = null;
let stepCount = 0;
let isAutoRefreshing = true;

// Vehicle icons for different types
const vehicleIcons = {
    'car': '🚗',
    'truck': '🚚',
    'bus': '🚌',
    'motorcycle': '🏍️'
};

const laneNames = {
    'north': '↑ North',
    'south': '↓ South',
    'east': '→ East',
    'west': '← West'
};

function formatVehicleCounts(data) {
    const counts = data.lane_counts || {};
    const html = Object.entries(counts).map(([lane, vehicles]) => {
        const total = Object.values(vehicles).reduce((a, b) => a + b, 0);
        const vehiclesList = Object.entries(vehicles)
            .map(([type, count]) => `<div class="vehicle-item"><span>${vehicleIcons[type] || type}</span> <span>${type}:</span> <span class="vehicle-count">${count}</span></div>`)
            .join('');
        
        return `
            <div class="lane-card">
                <div class="lane-name"><i class="fas fa-directions"></i> ${laneNames[lane] || lane}</div>
                ${vehiclesList}
                <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #cbd5e1; font-weight: 700; color: var(--primary-color);">Total: ${total}</div>
            </div>
        `;
    }).join('');
    
    return html || '<div class="loading">No data available</div>';
}

function getDensityColor(level) {
    switch(level.toLowerCase()) {
        case 'low':
            return 'density-low';
        case 'medium':
            return 'density-medium';
        case 'high':
            return 'density-high';
        default:
            return '';
    }
}

function formatDensities(data) {
    const densities = data.densities || {};
    const html = Object.entries(densities).map(([lane, stats]) => `
        <div class="density-item">
            <div class="density-label">${laneNames[lane] || lane}</div>
            <div class="density-level ${getDensityColor(stats.level)}">${stats.level.toUpperCase()}</div>
            <div class="density-score">Score: ${(stats.density_score * 100).toFixed(0)}%</div>
        </div>
    `).join('');
    
    return html || '<div class="loading">No data available</div>';
}

function formatSignal(data) {
    return `
        <div class="signal-item">
            <span class="signal-label"><i class="fas fa-road"></i> Active Lane</span>
            <span class="signal-value">${(data.lane || 'N/A').toUpperCase()}</span>
        </div>
        <div class="signal-item">
            <span class="signal-label"><i class="fas fa-hourglass-half"></i> Duration</span>
            <span class="signal-value">${data.duration || 0}s</span>
        </div>
        <div class="signal-item">
            <span class="signal-label"><i class="fas fa-lightbulb"></i> Status</span>
            <span class="signal-value" style="color: var(--success-color);">${data.current_signal || 'ACTIVE'}</span>
        </div>
    `;
}

function formatMetrics(data) {
    if (!data.intersection_0) {
        return '<div class="loading">No metrics available</div>';
    }
    
    const metrics = data.intersection_0;
    const queues = metrics.queue_lengths || {};
    const totalWait = metrics.total_wait_time || 0;
    
    return `
        <table class="metrics-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><i class="fas fa-signal"></i> <strong>Current Signal</strong></td>
                    <td><code>${metrics.signal || 'N/A'}</code></td>
                </tr>
                <tr>
                    <td><i class="fas fa-exclamation-triangle"></i> <strong>Emergency Lane</strong></td>
                    <td><code>${metrics.emergency_lane || 'None'}</code></td>
                </tr>
                <tr>
                    <td><i class="fas fa-hourglass-end"></i> <strong>Total Wait Time</strong></td>
                    <td><code>${totalWait.toFixed(2)}s</code></td>
                </tr>
                <tr>
                    <td><i class="fas fa-chart-area"></i> <strong>Queue Status</strong></td>
                    <td>${Object.entries(queues).map(([lane, count]) => `<code>${laneNames[lane]}=${count}</code>`).join(', ')}</td>
                </tr>
                <tr>
                    <td><i class="fas fa-clock"></i> <strong>Time Step</strong></td>
                    <td><code>${data.time_step || 0}</code></td>
                </tr>
            </tbody>
        </table>
    `;
}

async function refreshDashboard() {
    await detect(false);
    await predict();
    await getSignal();
    await getMetrics();
}

function toggleAutoRefresh() {
    isAutoRefreshing = !isAutoRefreshing;
    const btn = document.querySelector('[onclick="toggleAutoRefresh()"]');
    const text = document.getElementById('auto-refresh-text');
    
    if (isAutoRefreshing) {
        text.textContent = 'Auto-Refresh: ON';
        btn.style.background = 'var(--text-secondary)';
        startAutoRefresh();
    } else {
        text.textContent = 'Auto-Refresh: OFF';
        btn.style.background = '#cbd5e1';
        stopAutoRefresh();
    }
}

function startAutoRefresh() {
    stopAutoRefresh();
    autoRefreshInterval = setInterval(refreshDashboard, 3000);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

window.onload = function() {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    predictionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Predicted Vehicle Count',
                data: [],
                borderColor: 'rgba(37, 99, 235, 1)',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointBackgroundColor: 'rgba(37, 99, 235, 1)',
                pointBorderColor: 'white',
                pointBorderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 13,
                            weight: 'bold'
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false,
                        color: 'rgba(0,0,0,0.05)'
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });
    
    refreshDashboard();
    startAutoRefresh();
};

async function detect(showAlert = true) {
    try {
        const res = await fetch('/detect');
        const data = await res.json();
        document.getElementById('counts').innerHTML = formatVehicleCounts(data);
        document.getElementById('densities').innerHTML = formatDensities(data);
        if (showAlert) {
            showNotification('✓ Detection updated', 'success');
        }
    } catch (e) {
        console.error(e);
        showNotification('✗ Detection failed', 'error');
    }
}

async function predict() {
    try {
        const res = await fetch('/predict');
        const data = await res.json();
        predictionChart.data.labels = data.predictions.map((_, i) => `+${i+1}s`);
        predictionChart.data.datasets[0].data = data.predictions;
        predictionChart.update();
    } catch (e) {
        console.error(e);
    }
}

async function getSignal() {
    try {
        const res = await fetch('/signal');
        const data = await res.json();
        document.getElementById('signal').innerHTML = formatSignal(data);
    } catch (e) {
        console.error(e);
    }
}

async function step() {
    try {
        await fetch('/step');
        stepCount++;
        document.getElementById('step-count').textContent = `Steps: ${stepCount}`;
        await refreshDashboard();
        showNotification('✓ Step executed', 'success');
    } catch (e) {
        console.error(e);
        showNotification('✗ Step failed', 'error');
    }
}

async function getMetrics() {
    try {
        const res = await fetch('/metrics');
        const data = await res.json();
        document.getElementById('metrics').innerHTML = formatMetrics(data);
    } catch (e) {
        console.error(e);
    }
}

function showNotification(message, type = 'info') {
    // Create a simple toast notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? 'var(--success-color)' : 'var(--danger-color)'};
        color: white;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);