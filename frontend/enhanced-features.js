// Enhanced Features for the Dashboard

// Environmental Tracking
async function getEnvironmental() {
    try {
        // Simulated data - in real implementation, this would come from API
        const ecoScore = Math.random() * 100; // 0-100
        const co2Emissions = Math.random() * 500; // kg
        const fuelConsumed = Math.random() * 100; // liters
        const idlingTime = Math.random() * 3600; // seconds
        
        const html = `
            <div class="eco-score">
                <div class="eco-score-number">${ecoScore.toFixed(0)}</div>
                <div class="eco-score-label">Environmental Score</div>
            </div>
            <div class="eco-stat">
                <span class="eco-label"><i class="fas fa-wind"></i> CO2 Emissions</span>
                <span class="eco-value">${co2Emissions.toFixed(1)} kg</span>
            </div>
            <div class="eco-stat">
                <span class="eco-label"><i class="fas fa-gas-pump"></i> Fuel Consumed</span>
                <span class="eco-value">${fuelConsumed.toFixed(1)} L</span>
            </div>
            <div class="eco-stat">
                <span class="eco-label"><i class="fas fa-zzz"></i> Idling Time</span>
                <span class="eco-value">${(idlingTime / 60).toFixed(0)} min</span>
            </div>
        `;
        document.getElementById('environmental').innerHTML = html;
    } catch (e) {
        console.error('Environmental tracking error:', e);
        document.getElementById('environmental').innerHTML = '<div class="loading">Error loading environmental data</div>';
    }
}

// V2I Communication Status
async function getV2IStatus() {
    try {
        // Simulated data - in real implementation, this would come from API
        const connectedVehicles = Math.floor(Math.random() * 50) + 10;
        const emergencyVehicles = Math.floor(Math.random() * 5);
        const communications = Math.floor(Math.random() * 1000) + 100;
        
        const html = `
            <div class="v2i-stat">
                <div class="v2i-icon"><i class="fas fa-car"></i></div>
                <div class="v2i-info">
                    <div class="v2i-label">Connected Vehicles</div>
                    <div class="v2i-value">${connectedVehicles}</div>
                </div>
            </div>
            <div class="v2i-stat">
                <div class="v2i-icon" style="color: var(--danger-color);"><i class="fas fa-ambulance"></i></div>
                <div class="v2i-info">
                    <div class="v2i-label">Emergency Vehicles</div>
                    <div class="v2i-value">${emergencyVehicles}</div>
                </div>
            </div>
            <div class="v2i-stat">
                <div class="v2i-icon" style="color: var(--warning-color);"><i class="fas fa-broadcast-tower"></i></div>
                <div class="v2i-info">
                    <div class="v2i-label">Communications Sent</div>
                    <div class="v2i-value">${communications}</div>
                </div>
            </div>
        `;
        document.getElementById('v2i-status').innerHTML = html;
    } catch (e) {
        console.error('V2I status error:', e);
        document.getElementById('v2i-status').innerHTML = '<div class="loading">Error loading V2I data</div>';
    }
}

// Incident Detection
async function checkIncidents() {
    try {
        // Simulated data - in real implementation, this would come from API
        const hasIncidents = Math.random() > 0.7; // 30% chance of incidents
        
        if (hasIncidents) {
            const incidents = [
                {
                    type: 'Congestion Spike',
                    lane: 'North',
                    severity: Math.floor(Math.random() * 100),
                    time: new Date(Date.now() - Math.random() * 600000).toLocaleTimeString()
                },
                {
                    type: 'Queue Buildup',
                    lane: 'East',
                    severity: Math.floor(Math.random() * 50) + 50,
                    time: new Date(Date.now() - Math.random() * 300000).toLocaleTimeString()
                }
            ];
            
            const html = incidents.map(incident => `
                <div class="incident-item">
                    <div class="incident-title">
                        <i class="fas fa-exclamation-circle"></i> ${incident.type}
                    </div>
                    <div class="incident-detail"><strong>Lane:</strong> ${incident.lane}</div>
                    <div class="incident-detail"><strong>Severity:</strong> ${incident.severity}%</div>
                    <div class="incident-detail"><strong>Detected:</strong> ${incident.time}</div>
                </div>
            `).join('');
            
            document.getElementById('incidents').innerHTML = html;
        } else {
            document.getElementById('incidents').innerHTML = '<div class="no-incidents">✓ No incidents detected</div>';
        }
    } catch (e) {
        console.error('Incident detection error:', e);
        document.getElementById('incidents').innerHTML = '<div class="loading">Error loading incident data</div>';
    }
}

// Time-Based Adaptive Signals
async function getTimeBased() {
    try {
        const hours = new Date().getHours();
        let period = 'afternoon';
        let multiplier = 1.0;
        let strategy = '';
        
        if (hours >= 5 && hours < 7) {
            period = 'early_morning';
            multiplier = 0.6;
            strategy = 'Light traffic - minimal signal changes needed';
        } else if (hours >= 7 && hours < 9.5) {
            period = 'morning_rush';
            multiplier = 1.5;
            strategy = 'Heavy incoming traffic - extended green phases';
        } else if (hours >= 17 && hours < 19.5) {
            period = 'evening_rush';
            multiplier = 1.6;
            strategy = 'Heavy outbound traffic - signal coordination active';
        } else if (hours >= 21 || hours < 5) {
            period = 'night';
            multiplier = 0.4;
            strategy = 'Minimal traffic - flash mode enabled';
        } else {
            strategy = 'Normal traffic flow - balanced timing';
        }
        
        const html = `
            <div class="time-period">
                <div class="time-label">Current Period</div>
                <div class="time-period-name">${period.replace(/_/g, ' ').toUpperCase()}</div>
                <div class="time-multiplier">${multiplier.toFixed(1)}x</div>
                <div class="time-strategy">${strategy}</div>
            </div>
        `;
        document.getElementById('time-based').innerHTML = html;
    } catch (e) {
        console.error('Time-based controller error:', e);
        document.getElementById('time-based').innerHTML = '<div class="loading">Error loading time data</div>';
    }
}

// Heatmap Visualization
function updateHeatmap() {
    const canvas = document.getElementById('heatmapCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, width, height);
    
    // Draw intersection heatmap (4 lanes)
    const lanes = [
        { x: width/2, y: height/4, name: 'North' , data: Math.random() },
        { x: width/2, y: 3*height/4, name: 'South', data: Math.random() },
        { x: 3*width/4, y: height/2, name: 'East', data: Math.random() },
        { x: width/4, y: height/2, name: 'West', data: Math.random() }
    ];
    
    lanes.forEach(lane => {
        // Draw lane as rectangle with color based on congestion
        const intensity = lane.data; // 0-1
        const hue = (1 - intensity) * 120; // Green to Red
        const radius = 30 + intensity * 40;
        
        // Draw circle for each lane
        const gradient = ctx.createRadialGradient(lane.x, lane.y, 5, lane.x, lane.y, radius);
        gradient.addColorStop(0, `hsl(${hue}, 100%, 50%)`);
        gradient.addColorStop(1, `hsl(${hue}, 100%, 70%)`);
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(lane.x, lane.y, radius, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw label
        ctx.fillStyle = '#000';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(lane.name, lane.x, lane.y + 5);
        
        // Draw congestion level
        ctx.fillStyle = 'rgba(0,0,0,0.7)';
        ctx.font = '11px Arial';
        ctx.fillText(`${(intensity * 100).toFixed(0)}%`, lane.x, lane.y - 15);
    });
    
    // Draw center intersection
    ctx.fillStyle = 'rgba(37, 99, 235, 0.3)';
    ctx.beginPath();
    ctx.arc(width/2, height/2, 15, 0, 2 * Math.PI);
    ctx.fill();
    
    ctx.strokeStyle = 'rgba(37, 99, 235, 0.6)';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    showNotification('Heatmap updated', 'success');
}

// Alerts Management
async function showAlerts() {
    // Simulated alert data
    const alerts = [
        {
            id: '1',
            type: 'High Congestion', 
            severity: 'warning',
            message: 'High congestion on North lane: 35 vehicles',
            time: new Date(Date.now() - 120000).toLocaleTimeString()
        },
        {
            id: '2',
            type: 'Long Wait Time',
            severity: 'warning',
            message: 'Long wait time on East: 50 seconds',
            time: new Date(Date.now() - 60000).toLocaleTimeString()
        },
        {
            id: '3',
            type: 'Incident Detected',
            severity: 'critical',
            message: 'Congestion spike detected - possible accident',
            time: new Date().toLocaleTimeString()
        }
    ];
    
    const unacknowledged = alerts.length;
    document.getElementById('unacked-count').textContent = unacknowledged;
    
    const alertsDetail = document.getElementById('alertsDetail');
    alertsDetail.innerHTML = alerts.map(alert => `
        <div class="alert-detail-item ${alert.severity}">
            <div class="alert-header">
                <span class="alert-type">${alert.type}</span>
                <span class="alert-severity ${alert.severity}">${alert.severity.toUpperCase()}</span>
            </div>
            <div class="alert-message">${alert.message}</div>
            <div class="alert-time">${alert.time}</div>
        </div>
    `).join('');
    
    document.getElementById('alertModal').style.display = 'flex';
}

function closeAlerts() {
    document.getElementById('alertModal').style.display = 'none';
}

// Enhanced Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    const bgColor = type === 'success' ? 'var(--success-color)' : 
                   type === 'error' ? 'var(--danger-color)' : 
                   'var(--primary-color)';
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${bgColor};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 3000;
        animation: slideIn 0.3s ease;
        font-weight: 500;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initialize new features on page load
window.addEventListener('load', function() {
    // Add CSS animation for slideIn
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    // Load all new features initially
    getEnvironmental();
    getV2IStatus();
    checkIncidents();
    getTimeBased();
    updateHeatmap();
});
