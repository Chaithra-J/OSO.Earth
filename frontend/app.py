# import streamlit as st
# import requests
# import json
# import re
# from backend.main import answer_user_question


# API = "http://localhost:8000"

# st.title("🌱 OSO Habit Coach")

# # -------------------------
# # Add Habit
# # -------------------------
# with st.sidebar:
#     st.header("Add a Habit")
#     # st.subheader("Add a habit")
#     new_habit = st.text_input("Habit name", key="habit_input")

#     if st.button("Add habit"):
#         if new_habit.strip():
#             requests.post(f"{API}/habits/{new_habit}")
#             st.success("Habit added!")
#             st.rerun()

# # -------------------------
# # Show Habits
# # -------------------------
#     st.header("Your habits")
#     habits = requests.get(f"{API}/habits").json()

#     for h in habits:
#         st.write(f"🔥 **{h['name']}** — Streak: {h['streak']}")
#         if st.button("Mark done", key=f"done_{h['id']}"):
#             requests.post(f"{API}/habits/{h['id']}/complete")
#             st.rerun()

#         if st.button("Delete habit", key=f"delete_{h['id']}"):
#             requests.delete(f"{API}/habit/{h['id']}")
#             st.success("Habit deleted!")
#             st.rerun()

# # -------------------------
# # Helper: extract JSON suggestion
# # -------------------------
#     def extract_json(text):
#         match = re.search(r"\{[\s\S]*\}", text)
#         if match:
#             try:
#                 return json.loads(match.group())
#             except json.JSONDecodeError:
#                 return None
#         return None

# # -------------------------
# # Chatbot
# # -------------------------
# st.subheader("🤖 Chat with your habit coach")

# msg = st.text_input("Say something", key="chat_input")

# if st.button("Send", key="send_btn"):
#     if msg.strip():
#         res = requests.get(
#             f"{API}/chat",
#             params={"message": msg}
#         ).json()

#     if msg:
#         with st.spinner("Thinking..."):
#             res = answer_user_question(msg)
#             st.markdown("### 🤖 Response")
#             st.write(res)


#         reply = res["response"]
#         st.markdown("### Coach says:")
#         st.write(reply)

#         # ---- Habit suggestion handling ----
#         suggestion = extract_json(reply)

#         if suggestion and suggestion.get("action") == "add":
#             st.info(f"**Suggested habit:** {suggestion['habit_name']}")
#             st.caption(suggestion.get("reason", ""))

#             col1, col2 = st.columns(2)

#             with col1:
#                 if st.button("✅ Add habit", key="confirm_add"):
#                     requests.post(
#                         f"{API}/habits/{suggestion['habit_name']}"
#                     )
#                     st.success("Habit added!")
#                     st.rerun()

#             with col2:
#                 if st.button("❌ Ignore", key="ignore_add"):
#                     st.info("No changes made.")


import streamlit as st
import requests
import json
import re

API = "http://localhost:8000"
st.title("🌱 OSO Habit Coach")

def extract_json(text):
    match = re.search(r"\{[\s\S]*\}", text)
    return json.loads(match.group()) if match else None

# Sidebar Habit Management
with st.sidebar:
    st.header("Your Habits")
    new_habit = st.text_input("New Habit Name")
    if st.button("Add"):
        requests.post(f"{API}/habits/{new_habit}")
        st.rerun()
    
    try:
        for h in requests.get(f"{API}/habits").json():
            st.write(f"🔥 {h['name']} ({h['streak']})")
            if st.button("Check", key=f"c_{h['id']}"):
                requests.post(f"{API}/habits/{h['id']}/complete")
                st.rerun()
    except:
        st.warning("Connect to Backend")

# Chat
st.subheader("🤖 Chat with Coach")
msg = st.text_input("Ask a question based on your PDFs")
if st.button("Send"):
    with st.spinner("Thinking..."):
        res = requests.get(f"{API}/chat", params={"message": msg}).json()
        st.write(res["response"])






