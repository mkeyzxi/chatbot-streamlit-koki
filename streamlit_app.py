# ===== Bagian 1: Imports & Config =====
import streamlit as st
import json
import traceback
from pathlib import Path
from typing import Union, Dict, Any
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------- Konfigurasi ----------
LLM_TEMPERATURE = 0.6
MODEL_NAME = "gemini-2.5-flash"   # Sesuaikan jika perlu
CACHE_FILE = Path("recipe_cache.json")
HISTORY_FILE = Path("history.json")

st.set_page_config(page_title="Koki Mager", page_icon="🍳", layout="wide")
st.title("Koki Mager | Resep & Inspirasi")
st.markdown("""
Masukkan bahan makanan (mis: `nasi, telur`).  
Atau tanyakan terkait masakan, minuman, makanan’** 😄
""")

# ---------- Cache helpers ----------
def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache: dict):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        # jangan crash app kalau gagal simpan cache
        st.warning("⚠️ Gagal menyimpan cache (cek permission).")

recipe_cache = load_cache()
# ===== Bagian 2: Utilities (normalizer, parser, dummy) =====

def generate_dummy_recipe(user_input: str) -> str:
    bahan_list = [b.strip().capitalize() for b in user_input.split(",")]
    return (
        f"### 🍳 Resep Sederhana dari {', '.join(bahan_list)}\n\n"
        f"**Bahan:**\n" + "\n".join([f"- {b}" for b in bahan_list]) + "\n\n"
        "**Langkah:**\n1. Siapkan semua bahan.\n2. Campur dan masak sesuai selera.\n\n"
        "**Tips Koki:** Selalu tambahkan cinta ❤️ saat memasak!"
    )

def normalize_response(raw: Any, rejection: str) -> str:
    """
    Pastikan jawaban yang disimpan/diambil dari cache/agent
    menjadi string markdown rapi — bukan list/dict/object.
    """
    try:
        # Jika sudah string -> bersihkan dan kembalikan
        if isinstance(raw, str):
            return raw.strip()

        # Jika AIMessage instance (langchain style)
        if isinstance(raw, AIMessage):
            if hasattr(raw, "content"):
                c = raw.content
                if isinstance(c, str):
                    return c.strip()
                # kadang content adalah list/dict
                raw = c

        # Jika list -> coba ambil teks paling relevan
        if isinstance(raw, list):
            if len(raw) == 0:
                return rejection
            first = raw[0]
            # jika elemen dict dengan key 'text' atau 'content'
            if isinstance(first, dict):
                if "text" in first:
                    return str(first["text"]).strip()
                if "content" in first:
                    return str(first["content"]).strip()
            # jika string dalam list
            if isinstance(first, str):
                return first.strip()
            # fallback: ubah jadi string
            return str(first).strip()

        # Jika dict -> ambil 'text' atau 'content' jika ada
        if isinstance(raw, dict):
            if "text" in raw and isinstance(raw["text"], str):
                return raw["text"].strip()
            if "content" in raw and isinstance(raw["content"], str):
                return raw["content"].strip()
            # kadang agent menyimpan function_call args -> periksa deeper
            # ambil nilai paling bermakna jika ada
            for k in ("assistant_output", "Output", "output"):
                if k in raw and isinstance(raw[k], str):
                    return raw[k].strip()
            # fallback: serialisasikan supaya tidak tampil raw object di UI
            return json.dumps(raw, ensure_ascii=False, indent=2)

        # Fallback: ubah apa pun jadi string
        return str(raw).strip()

    except Exception:
        # jika apa pun gagal -> kembalikan rejection (jawaban penolakan generik)
        return rejection

def extract_markdown_from_agent(resp: Union[Dict, AIMessage, Any]) -> str:
    """
    Ambil konten teks utama dari respons agent yaitu markdown.
    Bisa menerima:
    - AIMessage (langgraph/langchain)
    - dict (hasil .invoke())
    - list (kadang response berbentuk list)
    - string
    """
    try:
        # Jika AIMessage, cek content & tool_calls
        if isinstance(resp, AIMessage):
            # 1) jika content adalah string
            if isinstance(resp.content, str) and resp.content.strip():
                return resp.content.strip()
            # 2) jika content adalah list/dict -> normalisasi
            return normalize_response(resp.content, rejection_str())

        # Jika dict (hasil .invoke())
        if isinstance(resp, dict):
            # cek tool calls / messages / content
            # banyak agent menyimpan messages: [HumanMessage, AIMessage, ...]
            if "messages" in resp and isinstance(resp["messages"], list):
                # ambil pesan terakhir yang tampak seperti AIMessage
                for m in reversed(resp["messages"]):
                    if isinstance(m, AIMessage):
                        if isinstance(m.content, str) and m.content.strip():
                            return m.content.strip()
                        # jika m.content dict/list -> normalisasi
                        return normalize_response(m.content, rejection_str())
                # jika messages berisi dicts/strings
                return normalize_response(resp["messages"], rejection_str())

            # jika ada key content atau output
            for k in ("content", "output", "assistant_output", "Output"):
                if k in resp and resp[k]:
                    return normalize_response(resp[k], rejection_str())

            # fallback -> normalisasi keseluruhan dict
            return normalize_response(resp, rejection_str())

        # Jika list atau string -> normalisasi
        return normalize_response(resp, rejection_str())

    except Exception as e:
        return f"❌ Error parsing agent response: {e}\n\n{traceback.format_exc()}"

# helper untuk mendapatkan string rejection secara konsisten
def rejection_str() -> str:
    return "Aku Koki loh, bukan ahli dunia 🌍🍳 Lukira AI gak punya bidang kali yah!"
# ===== Bagian 3: LLM, Agent, dan Tool =====

# Inisialisasi LLM (butuh API key dari UI sidebar nantinya)
# Kita definisikan llm setelah mendapat google_api_key di sidebar,
# tetapi buat fungsi pembuatannya di sini agar rapi.

def create_llm(google_api_key: str):
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=google_api_key,
        temperature=LLM_TEMPERATURE
    )

# Tool simpan history: simpan ke session_state.history dan file lokal (history.json)
@tool
def tool_save_history(payload: str) -> str:
    """
    Payload diharapkan JSON string: {"user_input": "...", "assistant_output": "..."}
    Kita simpan ke st.session_state.history dan HISTORY_FILE.
    """
    try:
        obj = json.loads(payload)
    except Exception as e:
        return f"ERROR_SAVE_HISTORY_PARSE: {e}"

    # simpan ke session state (untuk sidebar)
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({"role": "user", "content": obj.get("user_input", "")})
    st.session_state.history.append({"role": "assistant", "content": obj.get("assistant_output", "")})

    # simpan ke file HISTORY_FILE
    try:
        hist = []
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    hist = json.load(f)
                except Exception:
                    hist = []
        hist.append(obj)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # jangan crash app jika file tidak bisa ditulis
        return f"ERROR_SAVE_HISTORY_WRITE: {e}"

    return "SAVED_HISTORY_OK"
# ===== Bagian 3: LLM, Agent, dan Tool =====

# Inisialisasi LLM (butuh API key dari UI sidebar nantinya)
# Kita definisikan llm setelah mendapat google_api_key di sidebar,
# tetapi buat fungsi pembuatannya di sini agar rapi.

def create_llm(google_api_key: str):
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=google_api_key,
        temperature=LLM_TEMPERATURE
    )

# Tool simpan history: simpan ke session_state.history dan file lokal (history.json)
@tool
def tool_save_history(payload: str) -> str:
    """
    Payload diharapkan JSON string: {"user_input": "...", "assistant_output": "..."}
    Kita simpan ke st.session_state.history dan HISTORY_FILE.
    """
    try:
        obj = json.loads(payload)
    except Exception as e:
        return f"ERROR_SAVE_HISTORY_PARSE: {e}"

    # simpan ke session state (untuk sidebar)
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({"role": "user", "content": obj.get("user_input", "")})
    st.session_state.history.append({"role": "assistant", "content": obj.get("assistant_output", "")})

    # simpan ke file HISTORY_FILE
    try:
        hist = []
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    hist = json.load(f)
                except Exception:
                    hist = []
        hist.append(obj)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # jangan crash app jika file tidak bisa ditulis
        return f"ERROR_SAVE_HISTORY_WRITE: {e}"

    return "SAVED_HISTORY_OK"
# ===== Bagian 4: Sidebar & Agent creation =====

with st.sidebar:
    st.subheader("🔐 API Key")
    google_api_key = st.text_input("Google AI API Key (Gemini)", type="password")
    st.markdown("---")
    st.subheader("📚 Riwayat Percakapan")
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.button("🗑 Hapus Semua Percakapan"):
        st.session_state.history.clear()
        st.session_state.messages = []
        # juga clear history local file (opsional)
        try:
            if HISTORY_FILE.exists():
                HISTORY_FILE.unlink()
        except Exception:
            pass
        st.experimental_rerun()

    # tampilkan ringkasan history
    for msg in reversed(st.session_state.history):
        role = "👤 User" if msg.get("role") == "user" else "🍳 Koki"
        with st.expander(f"{role}: {msg.get('content','')[:60]}..."):
            st.markdown(msg.get("content", ""), unsafe_allow_html=True)

# jika belum ada API key -> stop (agar tidak membuat agent tanpa key)
if not google_api_key:
    st.warning("Masukkan Google AI API Key agar Koki bisa mulai masak 🍳")
    st.stop()

# buat LLM & agent sekarang API key sudah ada
llm = create_llm(google_api_key)

agent_prompt = """
Kamu adalah Koki Mager 🍳 — asisten chef yang kreatif, lucu, dan hanya menjawab soal makanan atau minuman.

🎯 Aturan:
1. Jawaban HARUS dalam format **Markdown murni** (bukan JSON, list, atau array).
2. Jika ada lebih dari satu resep atau ide, tampilkan dengan urutan atau poin-poin Markdown (gunakan tanda - atau angka).
3. Jika pertanyaan di luar topik makanan/minuman, jawab dengan kalimat:
   > Aku Koki loh, bukan ahli dunia 🌍🍳 Lukira AI gak punya bidang kali yah!
4. Gunakan bahasa yang ringan, sedikit jenaka, dan mudah dipahami.
5. Jika bahan makanan diberikan, berikan ide hidangan yang bisa dibuat dari bahan itu.
6. Jangan tampilkan format internal seperti “content=…” atau “{type: ...}”.
7. Output akhir harus terlihat seperti obrolan natural antara chef dan pengguna — singkat, lucu, dan menggugah selera.

Contoh gaya respons:
**Telur dadar pedas**  
- Campur telur, garam, dan cabai.  
- Kocok sampai rata, goreng di minyak panas.  
- Sajikan dengan nasi hangat — simple tapi nendang! 🔥
"""


agent = create_react_agent(
    model=llm,
    tools=[tool_save_history],
    prompt=agent_prompt
)
# ===== Bagian 5: Main chat loop =====

# inisialisasi state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rendered" not in st.session_state:
    st.session_state.rendered = False

# render history chat di UI
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"], unsafe_allow_html=True)

# input user
user_input = st.chat_input("Masukkan bahan makanan (mis. nasi, telur)")

if user_input:
    # reset render flag untuk input baru
    st.session_state.rendered = False

    # append pesan user ke chat UI + session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    key = user_input.lower().strip()
    rejection = rejection_str()
    answer = ""

    # Jika ada di cache -> ambil dan normalkan
    if key in recipe_cache:
        raw_cached = recipe_cache[key]
        answer = normalize_response(raw_cached, rejection)
        st.info("💡 Resep diambil dari cache.")
        with st.chat_message("assistant"):
            st.markdown(answer, unsafe_allow_html=True)
        st.session_state.rendered = True

    # Jika belum ada di cache -> panggil agent
    else:
        with st.chat_message("assistant"):
            with st.spinner("👨‍🍳 Koki Mager sedang menyiapkan resep..."):
                try:
                    # panggil agent
                    msg = HumanMessage(content=f"Bahan: {user_input}")
                    resp = agent.invoke({"messages": [msg]})
                    raw = extract_markdown_from_agent(resp)
                    # normalisasi untuk menghindari array/dict di UI
                    answer = normalize_response(raw, rejection)

                    # jika kosong atau hanya whitespace -> berikan dummy
                    if not answer or not answer.strip():
                        answer = generate_dummy_recipe(user_input)

                    # simpan di cache (pastikan string)
                    recipe_cache[key] = answer
                    save_cache(recipe_cache)
                except Exception as e:
                    answer = f"❌ Terjadi error: {e}\n\n{traceback.format_exc()}"

            # tampilkan jawaban
            st.markdown(answer, unsafe_allow_html=True)
            st.session_state.rendered = True

    # append assistant ke messages (untuk persist UI)
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Simpan riwayat hanya jika bukan penolakan
    if rejection not in answer:
        try:
            payload = json.dumps({"user_input": user_input, "assistant_output": answer}, ensure_ascii=False)
            # panggil tool (memanggil fungsi langsung)
            _ = tool_save_history.func(payload)
        except Exception as e:
            st.error(f"Gagal menyimpan riwayat: {e}")
