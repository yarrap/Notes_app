import "../styles/globals.css";


/**
 * Root App component for the Next.js frontend.
 *
 * - Imports the global CSS styles for consistent styling across all pages.
 * - Wraps and renders the current page component (`Component`) with its props (`pageProps`).
 * - This is the main entry point for the Next.js app and ensures global styles are applied.
 */


export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />;
}
