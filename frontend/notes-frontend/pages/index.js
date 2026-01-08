import { useEffect, useState } from "react";


/**
 * Home component for the Notes App frontend.
 *
 * - Fetches all notes from the backend API for the logged-in user.
 * - Manages state for notes, categories, note editor, modal, and delete confirmation.
 * - Supports:
 *    - Viewing notes filtered by category.
 *    - Creating new notes.
 *    - Updating existing notes.
 *    - Deleting notes with confirmation.
 *    - Displaying "Last Edited" timestamp for notes.
 * - Renders the sidebar with categories and counts, main content area with notes grid,
 *   and a full-screen editor modal for creating/editing notes.
 * - Handles interaction with backend via fetch requests to Django APIs.
 * - Includes styling for notes, editor, modals, and category indicators.
 */


export default function Home() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [category, setCategory] = useState("Random Thoughts");
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [editingNote, setEditingNote] = useState(null);

  const [showDeleteDropdown, setShowDeleteDropdown] = useState(null);
  const [confirmDeleteNoteId, setConfirmDeleteNoteId] = useState(null);
  const getLastEditedDate = (note) => {
    if (!note) return "";
    const timestamp = note.modified_at || new Date().toISOString();
    return new Date(timestamp);
  };
  

  useEffect(() => {
    fetch("http://localhost:8000/api/notes/", {
      credentials: "include",
    })
      .then(res => {
        if (!res.ok) throw new Error("Not logged in");
        return res.json();
      })
      .then(data => setNotes(data))
      .catch(() => window.location.href = "/login");
  }, []);

  const handleAddNote = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/add-note/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content, category }),
      });
      if (res.ok) {
        const newNote = await res.json();
        setNotes([newNote, ...notes]);
        setTitle(""); setContent(""); setShowModal(false);
      } else alert("Failed to add note");
    } catch (err) {
      alert("Backend not reachable");
    }
  };

  const handleUpdateNote = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/update-note/${editingNote.id}/`, {
        method: "PUT",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content, category }),
      });
      if (res.ok) {
        const updatedNote = await res.json();
        setNotes(notes.map(n => n.id === editingNote.id ? updatedNote : n));
        setTitle(""); setContent(""); setEditingNote(null);
      } else alert("Failed to update note");
    } catch (err) {
      alert("Backend not reachable");
    }
  };

  const handleConfirmDelete = async (noteId) => {
    try {
      const res = await fetch(`http://localhost:8000/api/delete-note/${noteId}/`, {
        method: "DELETE",
        credentials: "include",
      });
      if (res.ok) setNotes(notes.filter(n => n.id !== noteId));
    } catch (err) {
      console.error("Backend not reachable");
    }
    setConfirmDeleteNoteId(null);
    setShowDeleteDropdown(null);
  };

  const openNote = (note) => {
    setEditingNote(note);
    setTitle(note.title); setContent(note.content); setCategory(note.category);
  };

  const closeModal = () => {
    setShowModal(false); setEditingNote(null);
    setTitle(""); setContent(""); setCategory("Random Thoughts");
  };

  const getDisplayDate = (dateString) => {
    if (!dateString) return 'today';
    const noteDate = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    noteDate.setHours(0,0,0,0); today.setHours(0,0,0,0); yesterday.setHours(0,0,0,0);
    if (noteDate.getTime() === today.getTime()) return 'today';
    else if (noteDate.getTime() === yesterday.getTime()) return 'yesterday';
    else return noteDate.toLocaleDateString('en-US', { month:'long', day:'numeric' });
  };

  const categories = [
    { name: "Random Thoughts", color: "#FF9B85" },
    { name: "School", color: "#FFD99F" },
    { name: "Personal", color: "#8FC5C5" },
  ];

  const getCategoryCount = (catName) => notes.filter(n => n.category === catName).length;
  const sortedNotes = [...notes].sort((a,b) => new Date(b.modified_at || b.created_at || 0) - new Date(a.modified_at || a.created_at || 0));
  const filteredNotes = selectedCategory && selectedCategory !== "All Categories" ? sortedNotes.filter(n => n.category === selectedCategory) : sortedNotes;

  const getCardColor = (cat) => ({
    "Random Thoughts": "#FFBC9F",
    "School": "#FFE6B3",
    "Personal": "#A8D5D5",
  }[cat] || "#FFE6B3");

  const getCategoryDotColor = (catName) => ({
    "Random Thoughts": "#FF9B85",
    "School": "#FFD99F",
    "Personal": "#8FC5C5",
  }[catName] || "#FFD99F");

  const handleSaveNote = () => {
    if (!title || !content) return;
    if (editingNote) {
      handleUpdateNote();
    } else {
      handleAddNote();
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.sidebar}>
        <h3 style={styles.categoryTitle}>All Categories</h3>
        
        {categories.map(cat => (
          <div 
            key={cat.name} 
            style={styles.categoryItem}
            onClick={() => setSelectedCategory(selectedCategory === cat.name ? null : cat.name)}
          >
            <span style={{...styles.categoryDot, backgroundColor:getCategoryDotColor(cat.name)}}></span>
            <span style={{...styles.categoryName, fontWeight: selectedCategory === cat.name ? "700" : "400"}}>{cat.name}</span>
            <span style={styles.categoryCount}>{getCategoryCount(cat.name)}</span>
          </div>
        ))}
      </div>

      <div style={styles.main}>
        <div style={styles.header}>
          <button style={styles.newNoteBtn} onClick={() => setShowModal(true)}>+ New Note</button>
        </div>

        <div style={styles.contentWrapper}>
          {filteredNotes.length === 0 ? (
            <div style={styles.emptyState}>
              <img src="/images/bubble-tea.png" alt="Waiting" style={styles.emptyImage} onError={e=>e.target.style.display='none'} />
              <p style={styles.emptyText}>I'm just here waiting for your charming notes...</p>
            </div>
          ) : (
            <div style={styles.notesGrid}>
              {filteredNotes.map(note => (
                <div 
                  key={note.id}
                  style={{
                    ...styles.noteCard,
                    backgroundColor: getCardColor(note.category),
                    border: `2px solid ${getCategoryDotColor(note.category)}`,
                    position: "relative"
                  }}
                  onClick={() => openNote(note)}
                >
                  <div style={{ position: "relative" }}>
                    <span 
                      style={styles.deleteButton} 
                      onClick={(e) => { 
                        e.stopPropagation(); 
                        setShowDeleteDropdown(showDeleteDropdown === note.id ? null : note.id); 
                      }}
                    >
                      :
                    </span>
                    {showDeleteDropdown === note.id && (
                      <div style={styles.deleteDropdown}>
                        <div 
                          style={styles.deleteOption} 
                          onClick={(e) => {
                            e.stopPropagation();
                            setConfirmDeleteNoteId(note.id);
                          }}
                        >
                          Delete
                        </div>
                      </div>
                    )}
                  </div>

                  <div style={styles.noteHeader}>
                    <span style={styles.noteDate}>{getDisplayDate(note.created_at)}</span>
                    <span style={styles.noteCategory}>{note.category}</span>
                  </div>
                  <h3 style={styles.noteTitle}>{note.title}</h3>
                  <div style={styles.noteContent}>{note.content}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {confirmDeleteNoteId && (
        <div style={styles.confirmOverlay}>
          <div style={styles.confirmBox}>
            <p style={{ fontSize: "16px", color: "#2C2C2C" }}>
              Are you sure you want to delete this note?
            </p>
            <div style={styles.confirmBtns}>
              <button 
                style={{ ...styles.confirmBtn, background: "#B8956A", color: "#fff" }}
                onClick={() => handleConfirmDelete(confirmDeleteNoteId)}
              >
                Yes
              </button>
              <button 
                style={{ ...styles.confirmBtn, background: "#fff", color: "#8B6F47", border: "2px solid #8B6F47" }}
                onClick={() => setConfirmDeleteNoteId(null)}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {(showModal || editingNote) && (
        <div style={styles.fullScreenEditor}>
          <button style={styles.closeButton} onClick={closeModal}>✕</button>
          <div style={styles.editorCategoryDropdown}>
            <div style={styles.editorCategoryButton} onClick={()=>{ 
              const dropdown=document.getElementById('editorCategoryOptions'); 
              dropdown.style.display=dropdown.style.display==='none'?'block':'none';  
            }}>
              <span style={{...styles.editorSelectedDot, backgroundColor:getCategoryDotColor(category)}}></span>
              <span style={styles.editorSelectedText}>{category}</span>
              <span style={styles.editorDropdownArrow}>▼</span>
            </div>
            <div id="editorCategoryOptions" style={styles.editorCategoryOptions}>
              {categories.map(cat => (
                <div key={cat.name} style={styles.editorCategoryOption} onClick={()=>{
                  setCategory(cat.name); 
                  document.getElementById('editorCategoryOptions').style.display='none';
                }}>
                  <span style={{...styles.editorOptionDot, backgroundColor: cat.color}}></span>
                  <span>{cat.name}</span>
                </div>
              ))}
            </div>
          </div>

          <div style={{...styles.editorCard, backgroundColor:getCardColor(category), border:`3px solid ${getCategoryDotColor(category)}`}}>
            <div style={styles.editorTimestamp}>
              Last Edited: {editingNote 
                ? getLastEditedDate(editingNote).toLocaleDateString('en-US', { month:'long', day:'numeric', year:'numeric' })
                : new Date().toLocaleDateString('en-US', { month:'long', day:'numeric', year:'numeric' })
              } at {editingNote 
                ? getLastEditedDate(editingNote).toLocaleTimeString('en-US', { hour:'numeric', minute:'2-digit', hour12:true })
                : new Date().toLocaleTimeString('en-US', { hour:'numeric', minute:'2-digit', hour12:true })
              }
            </div>

            <input type="text" placeholder="Note Title" value={title} onChange={(e)=>setTitle(e.target.value)} style={styles.editorTitle} />
            <textarea placeholder="Pour your heart out..." value={content} onChange={(e)=>setContent(e.target.value)} style={styles.editorContent} />
            <button onClick={handleSaveNote} style={styles.editorSaveBtn}>💾</button>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { display: "flex", minHeight: "100vh", background: "#FFF8E7", fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" },
  sidebar: { width: "280px", background: "#FFF8E7", padding: "90px 0px 40px 40px" },
  categoryTitle: { fontSize: "18px", fontWeight: "700", marginBottom: "24px", color: "#2C2C2C" },
  categoryItem: { display: "flex", alignItems: "center", padding: "12px 16px", marginBottom: "4px", borderRadius: "8px", cursor: "pointer", transition: "background 0.2s", fontSize: "15px", color: "#2C2C2C" },
  categoryActive: { background: "#E8DFD0" },
  categoryDot: { width: "12px", height: "12px", borderRadius: "50%", marginRight: "12px", flexShrink: 0 },
  categoryName: { flex: 1 },
  categoryCount: { fontSize: "14px", color: "#999", fontWeight: "500" },
  main: { flex: 1, padding: "40px 60px", background: "#FFF8E7" },
  header: { display: "flex", justifyContent: "flex-end", marginBottom: "20px" },
  contentWrapper: { marginLeft: "-16px", marginTop: "0px" },
  newNoteBtn: { padding: "12px 28px", background: "transparent", border: "2px solid #B8956A", borderRadius: "30px", fontSize: "15px", color: "#8B6F47", cursor: "pointer", fontWeight: "500", transition: "all 0.2s" },
  emptyState: { display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "60vh" , transform: "translateX(-60px)",},
  emptyImage: { width: "220px", height: "220px", marginBottom: "30px" },
  emptyText: { fontSize: "18px", color: "#8B6F47", fontStyle: "italic" },
  notesGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "24px" },
  noteCard: { padding: "28px", borderRadius: "16px", minHeight: "200px", boxShadow: "0 2px 12px rgba(0,0,0,0.06)", transition: "transform 0.2s, box-shadow 0.2s", cursor: "pointer" },
  noteHeader: { display: "flex",  alignItems: "center", gap: "12px", marginBottom: "16px", fontSize: "13px", color: "#2C2C2C" },
  noteDate: { fontWeight: "700" },
  noteCategory: { fontWeight: "500", opacity: 0.85 },
  noteTitle: { fontSize: "22px", fontWeight: "700", marginBottom: "14px", color: "#2C2C2C", fontFamily: "Georgia, serif", lineHeight: "1.3" },
  noteContent: { fontSize: "15px", lineHeight: "1.7", color: "#3C3C3C", overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 6, WebkitBoxOrient: "vertical", whiteSpace: "pre-wrap" },
  fullScreenEditor: { position: "fixed", top: 0, left: 0, right: 0, bottom: 0, background: "#FFF8E7", zIndex: 1000, padding: "40px", overflow: "auto" },
  closeButton: { position: "absolute", top: "30px", right: "30px", background: "transparent", border: "none", fontSize: "32px", cursor: "pointer", color: "#8B6F47", padding: "10px", zIndex: 10 },
  editorCategoryDropdown: { position: "absolute", top: "30px", left: "40px", width: "250px", zIndex: 10 },
  editorCategoryButton: { width: "100%", padding: "12px 16px", borderRadius: "10px", border: "2px solid #D4C4A8", background: "#FFFFFF", cursor: "pointer", display: "flex", alignItems: "center", gap: "10px" },
  editorSelectedDot: { width: "14px", height: "14px", borderRadius: "50%", flexShrink: 0 },
  editorSelectedText: { flex: 1, fontSize: "15px", color: "#2C2C2C", fontWeight: "500" },
  editorDropdownArrow: { fontSize: "10px", color: "#999" },
  editorCategoryOptions: { position: "absolute", top: "100%", left: 0, right: 0, marginTop: "5px", background: "#FFFFFF", border: "2px solid #D4C4A8", borderRadius: "10px", overflow: "hidden", zIndex: 20, display: "none", boxShadow: "0 4px 12px rgba(0,0,0,0.1)" },
  editorCategoryOption: { padding: "12px 16px", display: "flex", alignItems: "center", gap: "10px", cursor: "pointer", transition: "background 0.2s" },
  editorOptionDot: { width: "14px", height: "14px", borderRadius: "50%", flexShrink: 0 },
  editorCard: { maxWidth: "1400px", margin: "60px auto 40px", padding: "40px", borderRadius: "20px", minHeight: "400px", boxShadow: "0 4px 20px rgba(0,0,0,0.1)", position: "relative", display: "flex", flexDirection: "column" },
  editorTimestamp: { textAlign: "right", fontSize: "11px", color: "#2C2C2C", opacity: 0.7, marginBottom: "30px" },
  editorTitle: { width: "100%", fontSize: "32px", fontWeight: "700", marginBottom: "24px", color: "#2C2C2C", fontFamily: "Georgia, serif", border: "none", background: "transparent", outline: "none", padding: "0" },
  editorContent: { width: "100%", flex: 1, fontSize: "16px", lineHeight: "1.8", color: "#3C3C3C", border: "none", background: "transparent", outline: "none", resize: "none", fontFamily: "inherit", padding: "0", minHeight: "400px" },
  editorSaveBtn: { position: "absolute", bottom: "30px", right: "30px", fontSize: "24px", background: "#2C2C2C", color: "#fff", width: "50px", height: "50px", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", border: "none", boxShadow: "0 4px 12px rgba(0,0,0,0.2)", transition: "transform 0.2s" },
  deleteButton: { position: "absolute", top: "12px", right: "12px", fontSize: "22px", fontWeight: "700", cursor: "pointer", color: "#8B6F47" },
  deleteDropdown: { position: "absolute", top: "38px", right: "0", background: "#fff8f0", border: "1px solid #B8956A", borderRadius: "10px", padding: "8px 0", zIndex: 50, minWidth: "100px", textAlign: "center" },
  deleteOption: { padding: "6px 12px", cursor: "pointer", color: "#8B6F47", fontWeight: "500", transition: "background 0.2s" },
  confirmOverlay: { position: "fixed", top:0, left:0, right:0, bottom:0, background: "rgba(0,0,0,0.2)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 },
  confirmBox: { background: "#FDF5E6", padding: "30px 40px", borderRadius: "16px", boxShadow: "0 8px 20px rgba(0,0,0,0.25)", textAlign: "center" },
  confirmBtns: { display: "flex", gap: "20px", marginTop: "20px", justifyContent: "center" },
  confirmBtn: { padding: "10px 20px", borderRadius: "10px", fontWeight: "600", cursor: "pointer", fontSize: "14px", border: "none" }
};







