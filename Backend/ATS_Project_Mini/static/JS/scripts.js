// JavaScript function to redirect to the login page
function redirectToLogin() {
    window.location.href = 'login.html';
}

// Function to redirect to the editor page with the selected template
function useTemplate(templateName) {
    window.location.href = `editor.html?template=${templateName}`;
}