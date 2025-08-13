document.addEventListener('DOMContentLoaded', () => {
    const leadersContainer = document.getElementById('leaders-container');
    const searchInput = document.getElementById('searchInput');
    let allLeaders = [];

    // Fetch leader data from the JSON file
    fetch('leaders.json')
        .then(response => response.json())
        .then(data => {
            allLeaders = data;
            displayLeaders(allLeaders);
        })
        .catch(error => console.error('Error fetching leader data:', error));

    // Function to display leaders
    function displayLeaders(leaders) {
        leadersContainer.innerHTML = ''; // Clear existing content
        for (const leader of leaders) {
            const card = document.createElement('div');
            card.className = 'leader-card';

            const skillsHTML = leader.skills.map(skill => `<span>${skill}</span>`).join(' ');
            const activityHTML = leader.latest_activity.map(act => `
                <div class="activity-item">
                    <a href="${act.url}" target="_blank">${act.title}</a>
                    <p>${act.source} - ${act.date}</p>
                </div>`).join('');

            card.innerHTML = `
                <img src="${leader.profile_image_url}" alt="${leader.name}" class="leader-image">
                <div class="leader-info">
                    <h2>${leader.name}</h2>
                    <p>${leader.current_role.title} at <strong>${leader.current_role.company}</strong></p>
                    <div class="skills">${skillsHTML}</div>
                    <div class="activity">
                        <h4>Latest Activity:</h4>
                        ${activityHTML}
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
            return (
                leader.name.toLowerCase().includes(searchTerm) ||
                leader.current_role.company.toLowerCase().includes(searchTerm) ||
                leader.skills.some(skill => skill.toLowerCase().includes(searchTerm))
            );
        });
        displayLeaders(filteredLeaders);
    });
});
