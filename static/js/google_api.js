/**
 * GymLog Club - Google API Integration
 * This file contains utility functions for working with Google Sheets and Drive APIs
 * Note: Most of the Google API integration happens server-side in Flask
 * This file is primarily for client-side helpers
 */

// We're using a custom format for JSON date strings
function formatDate(dateString) {
    const date = new Date(dateString);
    
    if (isNaN(date.getTime())) {
        return 'Invalid date';
    }
    
    // Get today and yesterday dates for comparison
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    // Compare the date
    if (date.getTime() === today.getTime()) {
        return 'Today at ' + formatTime(date);
    } else if (date.getTime() === yesterday.getTime()) {
        return 'Yesterday at ' + formatTime(date);
    } else {
        return date.toLocaleDateString() + ' at ' + formatTime(date);
    }
}

// Helper function to format time
function formatTime(date) {
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    
    hours = hours % 12;
    hours = hours ? hours : 12; // Convert 0 to 12
    
    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
    
    return hours + ':' + formattedMinutes + ' ' + ampm;
}

// Process image URLs from Google Drive to ensure they work properly
function processGoogleDriveImageUrl(url) {
    if (!url || !url.includes('drive.google.com')) {
        return url;
    }
    
    // Extract the file ID from the URL
    const fileIdMatch = url.match(/id=([^&]+)/);
    if (!fileIdMatch || !fileIdMatch[1]) {
        return url;
    }
    
    const fileId = fileIdMatch[1];
    
    // Construct a direct URL using the export=view parameter
    return `https://drive.google.com/uc?export=view&id=${fileId}`;
}
