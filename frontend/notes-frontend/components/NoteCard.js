/**
 * NoteCard component for the Notes App frontend.
 *
 * - Displays a single note's title and content in a styled card.
 * - Includes a Delete button that calls the backend delete endpoint for this note.
 * - After deletion, reloads the page to reflect the updated list of notes.
 *
 * Props:
 * - `note`: An object representing a note, expected to have `id`, `title`, and `content`.
 *
 * This component is used to render each note individually in the notes list.
 */


export default function NoteCard({ note }) {
    async function deleteNote() {
      await fetch(`http://localhost:8000/delete_note/${note.id}/`, {
        method: "DELETE",
        credentials: "include",
      });
      window.location.reload();
    }
  
    return (
      <div style={{
        border: "1px solid #ccc",
        padding: "15px",
        marginBottom: "10px"
      }}>
        <h3>{note.title}</h3>
        <p>{note.content}</p>
        <button onClick={deleteNote}>Delete</button>
      </div>
    );
  }
  