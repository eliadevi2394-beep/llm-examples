from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 DMP Care Bot")
st.caption("🚀 Asisten Virtual Layanan Kesehatan Terpadu DMP Clinic")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Halo 👋 Saya DMP Care Bot. Ada yang bisa saya bantu terkait layanan DMP Clinic?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Tanyakan layanan DMP Clinic..."):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[
        {
            "role": "system",
            "content": """
            Anda adalah DMP Care Bot, asisten virtual resmi DMP Clinic.

            Tugas Anda:
            - Menjawab pertanyaan pasien dengan ramah
            - Memberikan informasi layanan kesehatan
            - Memberikan informasi jadwal dokter
            - Membantu pendaftaran pasien
            - Memberikan edukasi kesehatan singkat

            Informasi DMP Clinic:
            - Lokasi: Jl. Anggrek No.24, Sutojayan, Lodoyo, Blitar
            - Layanan:
              * Poli Gigi
              * Klinik Kecantikan
              * Poli Kandungan
              * Khitan
              * Gizi & Obesitas
              * Rawat Inap

            Jawab dengan ramah dan profesional.
            """
        }
    ] + st.session_state.messages
msg = response.choices[0].message.content
st.session_state.messages.append({"role": "assistant", "content": msg})
st.chat_message("assistant").write(msg)
