import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image
import io
import base64

FILE = "notes.json"
DRAWINGS_DIR = "drawings"

# Create drawings directory if it doesn't exist
if not os.path.exists(DRAWINGS_DIR):
    os.makedirs(DRAWINGS_DIR)

# Page Configuration
st.set_page_config(
    page_title="Smart Notes Manager",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .note-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #667eea;
    }
    
    h1, h2, h3 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Load notes
def load_notes():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# Save notes
def save_notes(notes):
    with open(FILE, "w") as f:
        json.dump(notes, f, indent=4)

notes = load_notes()

st.title("📝 Smart Notes Manager")
st.markdown("*Organize your thoughts, capture your ideas*")

# Sidebar with styling
with st.sidebar:
    st.markdown("## 📚 Navigation")
    menu = st.selectbox(
        "Choose an option:",
        ["📝 Add Note", "🎨 Draw Note", "📖 View Notes", "🔍 Search Notes"],
        help="Select what you'd like to do"
    )

# Clean menu name for comparisons
clean_menu = menu.split()[-1]  # Get last word after emoji

# ---------------- ADD NOTE ----------------

if clean_menu == "Note" and "Add" in menu:

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✨ Create a New Note")
    
    with col2:
        st.info(f"📊 Total Notes: {len(notes)}")

    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        title = st.text_input(
            "📌 Note Title",
            placeholder="Give your note a catchy title...",
            help="Enter a descriptive title for your note"
        )
    
    with col2:
        category = st.selectbox(
            "🏷️ Category",
            ["Personal", "Work", "Ideas", "To-Do", "Other"]
        )

    content = st.text_area(
        "✍️ Write your note",
        placeholder="Start typing your thoughts here...",
        height=200,
        help="Write as much as you want"
    )

    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        save_clicked = st.button("💾 Save Note", use_container_width=True)
    
    with col2:
        clear_clicked = st.button("🔄 Clear", use_container_width=True)

    if clear_clicked:
        st.rerun()

    if save_clicked:
        if title and content:
            new_note = {
                "title": title,
                "content": content,
                "category": category,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            notes.append(new_note)
            save_notes(notes)

            st.success("✅ Note saved successfully!")
            st.balloons()
            st.rerun()

        else:
            st.error("❌ Please fill in both title and content!")

# ---------------- DRAW NOTE ----------------

elif clean_menu == "Note" and "Draw" in menu:
    from streamlit_drawable_canvas import st_canvas
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎨 Create a Drawing Note")
    
    with col2:
        st.info(f"📊 Total Notes: {len(notes)}")

    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        title = st.text_input(
            "📌 Drawing Title",
            placeholder="Give your drawing a title...",
            help="Enter a descriptive title for your drawing"
        )
    
    with col2:
        category = st.selectbox(
            "🏷️ Category",
            ["Personal", "Work", "Ideas", "Sketch", "Other"],
            key="draw_category"
        )

    # Drawing canvas settings
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stroke_width = st.slider(
            "✏️ Pen Size",
            1, 30, 5,
            help="Adjust the thickness of your pen"
        )
    
    with col2:
        stroke_color = st.color_picker(
            "🎨 Pen Color",
            "#000000",
            help="Choose your pen color"
        )
    
    with col3:
        bg_color = st.color_picker(
            "📄 Background",
            "#FFFFFF",
            help="Choose background color"
        )
    
    with col4:
        canvas_mode = st.selectbox(
            "🖌️ Mode",
            ["freedraw", "line", "rect", "circle", "transform"],
            help="Select drawing mode"
        )

    # Create canvas for drawing
    canvas_result = st_canvas(
        fill_color=bg_color,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=None,
        drawing_mode=canvas_mode,
        key="drawing_canvas",
    )

    # Display instructions
    st.info("💡 **Tips:** Use the tools on the left to draw, erase, or undo. You can switch between different drawing modes above.")

    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        save_drawing = st.button("💾 Save Drawing", use_container_width=True)
    
    with col2:
        clear_drawing = st.button("🔄 Clear Canvas", use_container_width=True)

    if clear_drawing:
        st.rerun()

    if save_drawing:
        if title and canvas_result.image_data is not None:
            # Convert canvas image to base64
            img = Image.fromarray((canvas_result.image_data).astype('uint8'), 'RGBA')
            
            # Save image to file
            drawing_filename = f"{DRAWINGS_DIR}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img.save(drawing_filename)
            
            new_note = {
                "title": title,
                "content": f"[Drawing saved at {drawing_filename}]",
                "drawing_path": drawing_filename,
                "category": category,
                "type": "drawing",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            notes.append(new_note)
            save_notes(notes)

            st.success("✅ Drawing saved successfully!")
            st.balloons()
            st.rerun()

        elif not title:
            st.error("❌ Please enter a title for your drawing!")
        else:
            st.error("❌ Please draw something before saving!")

# ---------------- VIEW NOTES ----------------

elif clean_menu == "Notes" and "View" in menu:

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📖 Your Notes")
    
    with col2:
        sort_by = st.selectbox("Sort by:", ["Latest", "Oldest"])

    if not notes:
        st.info("📭 No notes yet! Start by creating your first note.")
    else:
        # Sort notes
        sorted_notes = sorted(notes, key=lambda x: x['date'], reverse=(sort_by == "Latest"))
        
        # Display notes count by category
        categories = set(note.get("category", "Other") for note in notes)
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Notes", len(notes))
        
        for idx, cat in enumerate(sorted(categories)):
            count = len([n for n in notes if n.get("category") == cat])
            if idx == 1 and col2:
                st.metric(f"{cat}", count)
            elif idx == 2 and col3:
                st.metric(f"{cat}", count)
            elif idx == 3 and col4:
                st.metric(f"{cat}", count)
            elif idx == 4 and col5:
                st.metric(f"{cat}", count)

        st.markdown("---")

        for i, note in enumerate(sorted_notes):
            # Determine emoji based on type and category
            if note.get("type") == "drawing":
                type_emoji = "🎨"
            else:
                category_emoji_map = {
                    "Personal": "👤",
                    "Work": "💼",
                    "Ideas": "💡",
                    "To-Do": "✓",
                    "Sketch": "🖌️",
                    "Other": "📌"
                }
                type_emoji = category_emoji_map.get(note.get("category", "Other"), "📌")

            with st.expander(f"{type_emoji} {note['title']} — {note['date']}", expanded=False):
                
                # Display drawing if it's a drawing note
                if note.get("type") == "drawing" and os.path.exists(note.get("drawing_path", "")):
                    try:
                        drawing_img = Image.open(note["drawing_path"])
                        st.image(drawing_img, use_column_width=True, caption="Your Drawing")
                    except Exception as e:
                        st.error(f"Could not load drawing: {e}")
                else:
                    st.write(note["content"])
                
                st.caption(f"Category: {note.get('category', 'Other')}")

                col1, col2, col3 = st.columns(3)

                # Delete
                if col1.button("🗑️ Delete", key=f"del{i}", use_container_width=True):
                    # Also delete drawing file if it exists
                    if note.get("type") == "drawing" and os.path.exists(note.get("drawing_path", "")):
                        try:
                            os.remove(note["drawing_path"])
                        except:
                            pass
                    
                    notes.pop(i)
                    save_notes(notes)
                    st.success("Note deleted!")
                    st.rerun()

                # Download drawing
                if note.get("type") == "drawing" and col2.button("📥 Download", key=f"download{i}", use_container_width=True):
                    if os.path.exists(note.get("drawing_path", "")):
                        with open(note["drawing_path"], "rb") as file:
                            st.download_button(
                                label="Download Drawing",
                                data=file.read(),
                                file_name=f"{note['title']}.png",
                                mime="image/png",
                                key=f"down_btn{i}"
                            )

                # Edit (only for text notes)
                if note.get("type") != "drawing" and col2.button("✏️ Edit", key=f"edit{i}", use_container_width=True):
                    st.session_state["edit_index"] = i
                    st.session_state["edit_mode"] = True
                    st.rerun()

                # Copy
                if col3.button("📋 Copy", key=f"copy{i}", use_container_width=True):
                    st.success("Copied to clipboard!")


# ---------------- EDIT NOTE ----------------

if st.session_state.get("edit_mode"):

    idx = st.session_state["edit_index"]
    note = notes[idx]

    st.markdown("---")
    st.subheader("✏️ Edit Note")

    new_title = st.text_input("📌 Title", note["title"])
    
    new_category = st.selectbox(
        "🏷️ Category",
        ["Personal", "Work", "Ideas", "To-Do", "Other"],
        index=["Personal", "Work", "Ideas", "To-Do", "Other"].index(note.get("category", "Other"))
    )
    
    new_content = st.text_area("✍️ Content", note["content"], height=200)

    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💾 Update Note", use_container_width=True):
            notes[idx]["title"] = new_title
            notes[idx]["content"] = new_content
            notes[idx]["category"] = new_category

            save_notes(notes)

            st.success("✅ Note updated!")

            st.session_state["edit_mode"] = False
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state["edit_mode"] = False
            st.rerun()

# ---------------- SEARCH ----------------

elif clean_menu == "Notes" and "Search" in menu:

    st.subheader("🔍 Search Notes")

    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        query = st.text_input(
            "Search by title or content",
            placeholder="Type keywords to search...",
            help="Search across all your notes"
        )
    
    with search_col2:
        search_in = st.selectbox("Search in:", ["All", "Title", "Content"])

    if query:
        if search_in == "Title":
            results = [
                note for note in notes
                if query.lower() in note["title"].lower()
            ]
        elif search_in == "Content":
            results = [
                note for note in notes
                if query.lower() in note["content"].lower()
            ]
        else:
            results = [
                note for note in notes
                if query.lower() in note["title"].lower()
                or query.lower() in note["content"].lower()
            ]

        if results:
            st.success(f"Found {len(results)} note(s)")
            st.markdown("---")
            
            for note in results:
                category_emoji = {
                    "Personal": "👤",
                    "Work": "💼",
                    "Ideas": "💡",
                    "To-Do": "✓",
                    "Other": "📌"
                }.get(note.get("category", "Other"), "📌")
                
                st.markdown(f"### {category_emoji} {note['title']}")
                st.write(note["content"])
                st.caption(f"📅 {note['date']} | Category: {note.get('category', 'Other')}")
                st.markdown("---")

        else:
            st.warning("❌ No notes found matching your search!")