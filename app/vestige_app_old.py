import streamlit as st
import datetime
import uuid
import random
from librarian_llm import query_librarian
from memory_store import load_memories, save_memory


# Initialize memory store in session_state
if "memory_store" not in st.session_state:
    st.session_state.memory_store = load_memories()



# --- Category Mapping ---
category_map = {
    "🤖 Robots": ["robot", "automation", "actuator", "wheels"],
    "💭 Dreams": ["dream", "imagine", "whisper", "subconscious"],
    "🧠 AI": ["AI", "LLM", "intelligence", "Copilot", "model"],
    "🌌 Philosophy": ["self", "identity", "consciousness", "meaning"],
    "🌿 Mundane Joys": ["branch", "lawn", "weather", "riding", "mower"]
}

# --- Categorizer ---
def categorize(fragment):
    cats = []
    lower = fragment.lower()
    for label, keywords in category_map.items():
        if any(k in lower for k in keywords):
            cats.append(label)
    return cats or ["🗂️ Uncategorized"]

# --- Score Generator (placeholder) ---
def score_memory(fragment):
    return round(random.uniform(0.6, 1.5), 2)

# --- UI: Header ---
st.title("🧠 Vestige: Memory Curator")
# Mode selection
mode = st.radio("🧭 Choose an action:", ["📝 Enter a Memory", "🔍 Query the Librarian"], horizontal=True)

st.subheader("Input a memory fragment. Vestige will evaluate, score, and categorize it.")

# --- Input ---
user_input = st.text_area("📥 Memory Fragment", height=150, key="input_text")

if st.button("Submit"):
    if user_input.strip():
        if mode == "📝 Enter a Memory":
            result = query_librarian(user_input)
            memory = {
                "id": str(uuid.uuid4())[:8],
                "content": user_input,
                "score": round(result.get("score", 0.5), 2),
                "timestamp": datetime.datetime.now(),
                "categories": result.get("tags", ["🗂️ Uncategorized"]),
                "reason": result.get("reason", "No reason given.")
            }
            st.session_state.memory_store.append(memory)
            save_memory(memory)
          
            st.success(f"Memory stored in: {', '.join(memory['categories'])}")
            st.caption(f"🧾 Librarian's note: {memory['reason']}")
        else:
            response = query_librarian(user_input)
            st.subheader("📖 Librarian's Reflection:")
            st.markdown(f"**Tags**: {', '.join(response.get('tags', []))}")
            st.markdown(f"**Score**: `{response.get('score', 0.5)}`")
            st.markdown(f"**Insight**: {response.get('reason', 'No reflection provided.')}")




# --- Memory Recall Section ---
st.markdown("---")
st.subheader("📌 Memory Categories")

# Pull all observed categories
all_cats = sorted(set(cat for mem in st.session_state.memory_store for cat in mem["categories"]))

for cat in all_cats:
    if st.button(f"🔍 View {cat}", key=f"button_{cat}"):
        st.markdown(f"### 📂 {cat} Memories")
        for mem in st.session_state.memory_store:
            if cat in mem["categories"]:
                st.markdown(f"**{mem['id']}** | `{mem['score']}` | {mem['timestamp'].strftime('%Y-%m-%d %H:%M')}`")
                st.markdown(f"> {mem['content']}")
                st.markdown("—")

# --- Optional: Full memory archive ---
with st.expander("📜 View All Memories"):
    st.markdown(f"**Total Memories:** `{len(st.session_state.memory_store)}`")
    for mem in sorted(st.session_state.memory_store, key=lambda m: -m["score"]):
        st.markdown(f"**{mem['id']}** | `{mem['score']}` | {', '.join(mem['categories'])} | {mem['timestamp'].strftime('%Y-%m-%d %H:%M')}`")
        st.markdown(f"> {mem['content']}")
        st.markdown("---")

