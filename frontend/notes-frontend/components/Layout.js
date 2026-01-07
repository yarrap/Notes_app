import Link from "next/link";

/**
 * Layout component for the Notes App frontend.
 *
 * - Provides a sidebar with navigation links (Home, Login, Register) and note categories.
 * - Includes a Logout button that calls the backend logout endpoint and redirects to the login page.
 * - Wraps all page content in a consistent layout with a sidebar and main content area.
 * - `children` prop is used to render the content of the current page within the main section.
 *
 * This component is intended to be used as a wrapper for all pages to maintain consistent
 * UI and navigation throughout the app.
 */

export default function Layout({ children }) {
  async function logout() {
    await fetch("http://localhost:8000/custom_logout/", {
      credentials: "include",
    });
    window.location.href = "/login";
  }

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      
      <aside style={{ width: "250px", padding: "20px", background: "#f4f4f4" }}>
        <h3>Notes App</h3>
        <ul>
          <li>Random Thoughts</li>
          <li>School</li>
          <li>Personal</li>
        </ul>

        <hr />

        <Link href="/">Home</Link><br />
        <Link href="/login">Login</Link><br />
        <Link href="/register">Register</Link><br />
        <button onClick={logout}>Logout</button>
      </aside>

      <main style={{ flex: 1, padding: "20px" }}>
        {children}
      </main>
    </div>
  );
}
