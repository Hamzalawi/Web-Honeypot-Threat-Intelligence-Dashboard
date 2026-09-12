// app.js
async function fetchEndpoint(path) {
    try {
        const response = await fetch(path);
        return await response.json();
    } catch (error) {
        console.error(`Error fetching from ${path}:`, error);
        return null;
    }
}

// Helper function to safely create two-column table rows
function createTableRow(col1Text, col2Text) {
    const tr = document.createElement('tr');
    const td1 = document.createElement('td');
    const td2 = document.createElement('td');
    
    td1.textContent = col1Text;
    td2.textContent = col2Text;
    
    tr.append(td1, td2);
    return tr;
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
                backgroundColor: ['#ef4444', '#10b981'],
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
                backgroundColor: '#3b82f6',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// Main App Logic
async function loadDashboard() {
    const [recentData, credsData, statsData, countriesData, sshRecentData, sshCredsData] = await Promise.all([
        fetchEndpoint('/api/recent'),
        fetchEndpoint('/api/creds'),
        fetchEndpoint('/api/stats'),
        fetchEndpoint('/api/countries'),
        fetchEndpoint('/api/ssh/recent'),
        fetchEndpoint('/api/ssh/creds')
    ]);

    // 1. Stats & Bot Chart
    if (statsData) {
        const botPct = parseFloat(statsData.bot_pourcentage[0].bot_percentage);
        renderBotChart(botPct);

        const toolsBody = document.getElementById('tools-table-body');
        toolsBody.textContent = ''; // Clear previous content safely
        statsData.tools.forEach(tool => {
            toolsBody.appendChild(createTableRow(tool.user_agent, tool.unique_ip));
        });
    }
    

    // 2. Geographic Data Chart
    if (countriesData) {
        renderCountriesChart(countriesData);
    }

    // 3. Credentials
    if (credsData) {
        const usernamesBody = document.getElementById('usernames-table-body');
        usernamesBody.textContent = '';
        credsData.top_usernames.forEach(user => {
            usernamesBody.appendChild(createTableRow(user.username, user.count));
        });

        const passwordsBody = document.getElementById('passwords-table-body');
        passwordsBody.textContent = '';
        credsData.top_passwords.forEach(pass => {
            passwordsBody.appendChild(createTableRow(pass.password, pass.count));
        });
    }

    // 4. Recent Attacks
    if (recentData) {
        const recentList = document.getElementById('recent-attacks-list');
        recentList.textContent = '';
        
        recentData.forEach(attack => {
            const li = document.createElement('li');
            const strong = document.createElement('strong');
            
            strong.textContent = `${attack.time || 'Recent'}: `;
            
            li.append(strong, `${attack.username} / ${attack.password}`);
            recentList.appendChild(li);
        });
    }

    // 5. SSH Credentials
    if (sshCredsData) {
        const sshUsernamesBody = document.getElementById('ssh-usernames-table-body');
        sshUsernamesBody.textContent = '';
        sshCredsData.top_usernames.forEach(user => {
            sshUsernamesBody.appendChild(createTableRow(user.username, user.count));
        });

        const sshPasswordsBody = document.getElementById('ssh-passwords-table-body');
        sshPasswordsBody.textContent = '';
        sshCredsData.top_passwords.forEach(pass => {
            sshPasswordsBody.appendChild(createTableRow(pass.password, pass.count));
        });
    }

    // 6. Recent SSH Attacks
    if (sshRecentData) {
        const sshRecentList = document.getElementById('ssh-recent-attacks-list');
        sshRecentList.textContent = '';

        sshRecentData.forEach(attack => {
            const li = document.createElement('li');
            const strong = document.createElement('strong');

            strong.textContent = `${attack.connection_timestamp || 'Recent'}: `;

            li.append(strong, `${attack.username} / ${attack.password}`);
            sshRecentList.appendChild(li);
        });
    }
}

window.onload = loadDashboard;