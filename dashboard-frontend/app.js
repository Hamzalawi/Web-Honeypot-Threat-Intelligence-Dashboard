// app.js
const API_BASE_URL = 'http://127.0.0.1:3000';

async function fetchEndpoint(path) {
    try {
        const response = await fetch(`${API_BASE_URL}${path}`);
        return await response.json();
    } catch (error) {
        console.error(`Error fetching from ${path}:`, error);
        return null;
    }
}

// Chart initialization functions
function renderBotChart(botPercentage) {
    const ctx = document.getElementById('botChart').getContext('2d');
    const humanPercentage = 100 - botPercentage;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Bot Traffic', 'Human Traffic'],
            datasets: [{
                data: [botPercentage, humanPercentage],
                backgroundColor: ['#ef4444', '#10b981'], // Red for bot, Green for human
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function renderCountriesChart(countriesData) {
    const ctx = document.getElementById('countriesChart').getContext('2d');
    
    const labels = countriesData.map(row => row.country || 'Unknown');
    const data = countriesData.map(row => row.count);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Attempts',
                data: data,
                backgroundColor: '#3b82f6', // Blue
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false } // Hide legend for clean look
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// Main App Logic
async function loadDashboard() {
    const [recentData, credsData, statsData, countriesData] = await Promise.all([
        fetchEndpoint('/api/recent'),
        fetchEndpoint('/api/creds'),
        fetchEndpoint('/api/stats'),
        fetchEndpoint('/api/countries') 
    ]);

    // 1. Stats & Bot Chart
    if (statsData) {
        // Calculate the percentage
        const botPct = parseFloat(statsData.bot_pourcentage[0].bot_percentage);
        renderBotChart(botPct);

        const toolsBody = document.getElementById('tools-table-body');
        statsData.tools.forEach(tool => {
            toolsBody.innerHTML += `<tr><td>${tool.user_agent}</td><td>${tool.unique_ip}</td></tr>`;
        });
    }

    // 2. Geographic Data Chart
    if (countriesData) {
        renderCountriesChart(countriesData);
    }

    // 3. Credentials
    if (credsData) {
        const usernamesBody = document.getElementById('usernames-table-body');
        credsData.top_usernames.forEach(user => {
            usernamesBody.innerHTML += `<tr><td>${user.username}</td><td>${user.count}</td></tr>`;
        });

        const passwordsBody = document.getElementById('passwords-table-body');
        credsData.top_passwords.forEach(pass => {
            passwordsBody.innerHTML += `<tr><td>${pass.password}</td><td>${pass.count}</td></tr>`;
        });
    }

    // 4. Recent Attacks
    if (recentData) {
        const recentList = document.getElementById('recent-attacks-list');
        recentData.forEach(attack => {
            recentList.innerHTML += `
                <li>
                    <strong>${attack.time || 'Recent'}:</strong> 
                    ${attack.username} / ${attack.password}
                </li>`;
        });
    }
}

// Load automatically when the page is ready
window.onload = loadDashboard;