/**
 * GymLog Club - Main JavaScript
 * Contains shared functionality across pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add current year to footer
    const footerYear = document.querySelector('.footer .text-muted');
    if (footerYear) {
        const currentYear = new Date().getFullYear();
        footerYear.innerHTML = footerYear.innerHTML.replace('{{ now.year }}', currentYear);
    }
    
    // Enable Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Auto-close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Save and load group code from localStorage
    const groupCodeInput = document.getElementById('group_code');
    if (groupCodeInput) {
        // Load saved group code if available
        const savedGroupCode = localStorage.getItem('gymlog_group_code');
        if (savedGroupCode) {
            groupCodeInput.value = savedGroupCode;
        }
        
        // Save group code on form submission
        const form = groupCodeInput.closest('form');
        form.addEventListener('submit', function() {
            if (groupCodeInput.value.trim()) {
                localStorage.setItem('gymlog_group_code', groupCodeInput.value.trim());
            }
        });
    }
    
    // Add username to dropdown list if already existing
    const usernameInput = document.getElementById('username');
    if (usernameInput) {
        // Create or get datalist for username suggestions
        let datalist = document.getElementById('username-suggestions');
        if (!datalist) {
            datalist = document.createElement('datalist');
            datalist.id = 'username-suggestions';
            usernameInput.after(datalist);
            usernameInput.setAttribute('list', 'username-suggestions');
        }
        
        // Fetch usernames from the API and populate the datalist
        fetch('/api/group_members')
            .then(response => response.json())
            .then(data => {
                datalist.innerHTML = '';
                
                data.forEach(username => {
                    const option = document.createElement('option');
                    option.value = username;
                    datalist.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching group members:', error);
            });
    }
});
