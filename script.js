document.addEventListener('DOMContentLoaded', () => {
    const leadersContainer = document.getElementById('leaders-container');
    const searchInput = document.getElementById('searchInput');
    const downloadButton = document.getElementById('downloadCsvButton'); // Get the new button
    
    let allLeaders = [];
    let currentDisplayedLeaders = []; // This will hold the filtered list

    // Fetch leader data from the JSON file
    fetch('leaders.json')
        .then(response => response.json())
        .then(data => {
            allLeaders = data;
            displayLeaders(allLeaders); // Display all leaders initially
        })
        .catch(error => console.error('Error fetching leader data:', error));

    // Function to display leaders
    function displayLeaders(leaders) {
        leadersContainer.innerHTML = ''; // Clear existing content
        currentDisplayedLeaders = leaders; // *** IMPORTANT: Update the currently displayed list

        for (const leader of leaders) {
            const card = document.createElement('div');
            card.className = 'leader-card';

            const skillsHTML = leader.skills.map(skill => `<span>${skill}</span>`).join(' ');
            const activityHTML = leader.latest_activity.map(act => `
                <div class="activity-item">
                    <a href="${act.url}" target="_blank">${act.title}</a>
                    <p>${act.source || 'N/A'} - ${act.date || 'N/A'}</p>
                </div>`).join('');

            card.innerHTML = `
                <img src="${leader.profile_image_url}" alt="${leader.name}" class="leader-image">
                <div class="leader-info">
                    <h2>${leader.name}</h2>
                    <p>${leader.current_role.title} at <strong>${leader.current_role.company}</strong></p>
                    <div class="skills">${skillsHTML}</div>
                    <div class="activity">
                        <h4>Latest Activity:</h4>
                        ${activityHTML || 'No recent activity found.'}
                    </div>
                </div>
            `;
            leadersContainer.appendChild(card);
        }
    }

    // Search filter event
    searchInput.addEventListener('keyup', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const filteredLeaders = allLeaders.filter(leader => {
            const company = leader.current_role.company || '';
            return (
                leader.name.toLowerCase().includes(searchTerm) ||
                company.toLowerCase().includes(searchTerm) ||
                leader.skills.some(skill => skill.toLowerCase().includes(searchTerm))
            );
        });
        displayLeaders(filteredLeaders);
    });

    // --- NEW: CSV Download Logic ---
    function generateCSV(leaders) {
        const headers = ['Name', 'Company', 'Title', 'Region', 'Skills'];
        const rows = leaders.map(leader => {
            // Use "|| ''" as a fallback for potentially missing data
            const name = `"${leader.name || ''}"`;
            const company = `"${leader.current_role.company || ''}"`;
            const title = `"${leader.current_role.title || ''}"`;
            const region = `"${leader.region || ''}"`;
            const skills = `"${(leader.skills || []).join(', ')}"`;
            return [name, company, title, region, skills].join(',');
        });

        return [headers.join(','), ...rows].join('\n');
    }

    downloadButton.addEventListener('click', () => {
        console.log("Download button clicked. Exporting currently displayed leaders.");
        const csvContent = generateCSV(currentDisplayedLeaders);
        
        // Create a Blob (a file-like object)
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        
        // Create a temporary link to trigger the download
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', 'ai-leaders.csv');
        link.style.visibility = 'hidden';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
});
