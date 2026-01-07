/**
 * loginUser.js - Utility function to handle user login via Django backend.
 *
 * - Accepts `username` and `password` as arguments.
 * - Step 1: Fetches the CSRF cookie from the Django backend to ensure CSRF protection.
 * - Step 2: Sends a POST request to the Django login API endpoint (`/api/login/`) with credentials.
 * - Uses `credentials: 'include'` so session cookies are properly sent and received.
 * - Returns the parsed JSON response from the backend, which includes success status and any error messages.
 * 
 * Usage example:
 *   const result = await loginUser('myuser', 'mypassword');
 *   if (result.success) { ... } else { ... }
 */


export async function loginUser(username, password) {
    // 1. Fetch CSRF cookie first
    await fetch('http://localhost:8000/csrf-cookie/', {
      method: 'GET',
      credentials: 'include',
    });
  
    // 2. Send login POST request
    const response = await fetch('http://localhost:8000/api/login/', {
      method: 'POST',
      credentials: 'include',  // important for session cookies
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
  
    const data = await response.json();
    return data;
  }
  