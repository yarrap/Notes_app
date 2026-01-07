import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/router";


/**
 * Login component for the Notes App frontend.
 *
 * - Handles user login via a form that collects username and password.
 * - First fetches the CSRF token from the backend and includes it in the login request.
 * - Sends login credentials to the backend API for authentication.
 * - Redirects the user to the homepage on successful login.
 * - Displays error messages for invalid credentials or backend issues.
 * - Includes a link to the registration page for new users.
 * - Provides styling for the login card, input fields, buttons, and error overlay.
 */


// helper to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (typeof document !== 'undefined') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const router = useRouter();

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      // 1️⃣ Fetch CSRF cookie first
      await fetch("http://localhost:8000/csrf-cookie/", {
        method: "GET",
        credentials: "include",
      });

      // 2️⃣ Get CSRF token from cookie
      const csrftoken = getCookie('csrftoken');

      // 3️⃣ Send login POST with X-CSRFToken header
      const res = await fetch("http://localhost:8000/api/login/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (data.success) {
        router.push("/");
      } else {
        setErrorMessage(data.error || "Invalid username or password");
      }
    } catch (err) {
      setErrorMessage("Backend not reachable. Is Django running?");
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <div style={styles.imageContainer}>
          <img 
            src="/images/cat.png" 
            alt="Cute cat" 
            style={styles.catImage}
          />
        </div>

        <h2 style={styles.title}>Yay, You're Back!</h2>

        <form onSubmit={handleSubmit}>
          <input
            style={styles.input}
            placeholder="Email address"
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <input
            style={styles.input}
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button style={styles.button} type="submit">
            Login
          </button>
        </form>

        <p style={styles.footerText}>
          <Link href="/register" style={styles.link}>
            Oops! I've never been here before
          </Link>
        </p>
      </div>

      {errorMessage && (
        <div 
          style={styles.errorOverlay}
          onClick={() => setErrorMessage("")}
        >
          <div 
            style={styles.errorBox}
            onClick={(e) => e.stopPropagation()}
          >
            <p style={{ fontSize: "16px", color: "#2C2C2C", margin: "0" }}>
              {errorMessage}
            </p>
            <button 
              style={styles.errorBtn}
              onClick={() => setErrorMessage("")}
            >
              OK
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------------- STYLES ---------------- */

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#F5F1E8",
    padding: "20px",
  },
  card: {
    width: "100%",
    maxWidth: "400px",
    padding: "60px 40px 40px 40px",
    background: "#F5F1E8",
    borderRadius: "0px",
    textAlign: "center",
    position: "relative",
  },
  imageContainer: {
    marginBottom: "30px",
    display: "flex",
    justifyContent: "center",
  },
  catImage: {
    width: "120px",
    height: "120px",
    objectFit: "contain",
  },
  title: {
    marginBottom: "40px",
    fontSize: "28px",
    fontWeight: "400",
    color: "#6B5234",
    fontFamily: "Georgia, serif",
  },
  input: {
    width: "100%",
    padding: "14px 16px",
    marginBottom: "16px",
    borderRadius: "25px",
    border: "1px solid #8B6F47",
    fontSize: "14px",
    boxSizing: "border-box",
    outline: "none",
    background: "#FFFFFF",
    color: "#666666",
  },
  button: {
    width: "100%",
    padding: "14px",
    background: "transparent",
    color: "#8B6F47",
    border: "1px solid #8B6F47",
    borderRadius: "25px",
    fontSize: "15px",
    fontWeight: "400",
    cursor: "pointer",
    marginTop: "8px",
    transition: "all 0.2s",
  },
  footerText: {
    marginTop: "24px",
    fontSize: "13px",
  },
  link: {
    color: "#8B6F47",
    fontWeight: "400",
    textDecoration: "underline",
  },
  errorOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: "rgba(0,0,0,0.3)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 1000,
  },
  errorBox: {
    background: "#FDF5E6",
    padding: "30px 40px",
    borderRadius: "16px",
    boxShadow: "0 8px 20px rgba(0,0,0,0.25)",
    textAlign: "center",
    maxWidth: "400px",
  },
  errorBtn: {
    padding: "10px 30px",
    marginTop: "20px",
    borderRadius: "10px",
    fontWeight: "600",
    cursor: "pointer",
    fontSize: "14px",
    border: "none",
    background: "#8B6F47",
    color: "#fff",
  },
};




