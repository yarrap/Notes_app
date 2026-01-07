/**
 * fetchcsrf.js - Utility function to get CSRF token from browser cookies.
 *
 * - Provides a helper function `getCookie(name)` that retrieves the value of a cookie by its name.
 * - Used in frontend forms (like Login or Register) to obtain the CSRF token set by Django.
 * - Ensures that POST/PUT/DELETE requests to the Django backend include the proper CSRF token in headers.
 * - Helps prevent CSRF (Cross-Site Request Forgery) attacks when interacting with the Django API.
 */


export async function fetchCsrf() {
    await fetch('http://localhost:8000/csrf-cookie/', {
      method: 'GET',
      credentials: 'include',  // important: lets cookies pass
    });
  }
  