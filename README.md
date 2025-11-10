# 🍳 Koki Mager - Chatbot Resep Streamlit

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-008080?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTE5LjAyNyAxMi4wMDFjMCAzLjQ0Mi0yLjE4NCA2LjM1OC01LjE1MiA3LjYxOGwtLjE1Ny4wNjYgMS40NzMgMi44NzhjLjA1My4wOTguMDI3LjIxLS4wNjYuMjgzLS4wOTMuMDczLS4yMTUuMDgtLjI4Mi4wMjZsLTEuNTk3LTIuOTU1Yy0uNDQ1LjE2LS45MDguMjkyLTEuMzg0LjM4My0uNDc3LjA5MS0uOTYuMTU1LTEuNDQ4LjE5My0uNDg4LjAzNy0uOTgzLjA1NS0xLjQ4NC4wNTUtMy45MTcgMC03LjM0OC0yLjQyLTguNTAzLTUuODY2LS4wOTYtLjI4Ny4wNzMtLjU4OC4zNi0uNjgxLjI4Ny0uMDk2LjU4OC4wNzMuNjguMzU5QTMuMDYgMTYuMTIgNC45OCAxNy45MDMgOCAxOC4yODhjLjE3NS4wMjEuMzUuMDM0LjUyOC4wNEw0LjA4MyAxMC4yMmEuMjUuMjUgMCAwIDEgLjEyNC0uMjM2bDIuNTU1LDcuNDYyYy4wMy4wODUuMTA4LjE0LjE5Ni4xNC4wMiAwIC4wNC0uMDAyLjA2LS4wMDZsMS4zNjgtLjQzNGMtLjM1OC0uNTU1LS42My0xLjE3LS44MTItMS44MzYtLjE4LS42NTctLjI3Ni0xLjM0My0uMjc2LTIuMDQ1IDAtMy4yOTQgMi4wNjgtNi4xMDQgNC44NzQtNy4zMDFsLjE2LS4wNjYgMS4zNi0yLjgxYy4wNTMtLjA5OC4wMjctLjIxLS4wNjYtLjI4NC0uMDkzLS4wNzMtLjIxNS0uMDgtLjI4Mi0uMDI2bC0xLjQ3MyAyLjg4NGMtLjU1MS0uMTcxLTEuMTE0LS4yNzctMS43LS4zMTYtLjU3LS4wNC0xLjE1LS4wNi0xLjczLS4wNi0zLjc4MyAwLTcuMTAzIDIuMjU1LTguMzQyIDUuNDQxLS4wOTYuMjguMDcyLjU4LjM1My42NzYuMjkuMDk2LjU4OC0uMDcyLjY4MS0uMzUzQzMuNjcgOC42MTUgNS42MjYgNy4wMSA4IDYuNjNjLjE1My0uMDI0LjMwOC0uMDQxLjQ2NC0uMDQxbDIuOTk2LTguNzM1YS4yNS4yNSAwIDAgMSAuMjM1LS4xNzhjLjA0NSAwIC4wOS4wMTIuMTMyLjAzNWwxLjc4MyAxLjE0NmMyLjM0Ny43ODQgNC4zMDcgMi42NiA1LjEyOCA0Ljk5My44MTMgMi4zMiAxLjAyMyA0Ljc5OC42MzMgNy4yNTQtLjAwMi4wMS0uMDA0LjAyLS4wMDYuMDNsMS40NTMtMi44NTVjLjA1NC0uMDk4LjAyOC0uMjEtLjA2NS0uMjgzLS4wOTMtLjA3NC0uMjE1LS4wOC0uMjgzLS4wMjZsLTEuNTY0IDIuOTMyYy4zOC4zMS43My42NjQgMS4wNDQgMS4wNjFsMS4yMSAyLjgxMmMuMDUzLjA5OC4wMjcuMjEtLjA2Ni4yODMtLjA5My4wNzQtLjIxNS4wOC0uMjgyLjAyNmwtMS4zMjUtMi44MTRjLTIuNTEgMi4yMTMtNS43MzcgMy41NS05LjIxMSAzLjc0NC0uMTE2LjAwNy0uMjMyLjAxLS4zNS4wMUwyMC45MTMgNy4yODZhLjI0OC4yNDggMCAwIDEgLjIzNS0uMTI0bC4wMTEuMDAxIDEuMzgxIDguNDgyYy4wMTMuMDg2LjA5Ny4xNDguMTg1Listing4LjAwMi0uMDA0LjAwMy0uMDA4LjAwNS0uMDEybDIuMDM1LTIuNDMzYy4wNjItLjA3NC4wOC0uMTguMDQtLjI3LS4wNC0uMDktLjEzLS4xNS0uMjItLjE1bC0yLjc0OC4wMDVjLjI4NS0uNTQuNDktMS4xMi42Mi0xLjczLjEzLS42LjE5LTEuMjIuMTktMS44NTIgMC0zLjQwOC0yLjE1Mi02LjMyOC01LjA4OC03LjU5bC0uMTU3LS4wNjZMLTguOTMgMTkuNTEzYy0uMDUzLjEtLjAyNy4yMTMuMDY2LjI4My4wMy4wMjQuMDYzLjAzNi4wOTYuMDM2LjA2NyAwIC4xMzQtLjAyLjE4NS0uMDZsMS4zNTgtMi44NzVjLjQ3LjE3Mi45MjguMzA4IDEuMzc3LjQwNy40NS4xLjkuMTc1IDEuMzU0LjIyOS40NDUuMDU2Ljg5My4wODMgMS4zNDUuMDgzIDIuMzU0IDAgNC41MTItLjgxMiA1Ljk0NS0yLjE4OCAxLjQzMy0xLjM3NSAyLjE5OC0zLjE1MiAyLjE5OC00Ljk5N3ptLTcuMzc0IDMuMDQzYy0xLjQyNy0xLjQwMy0zLjM1OC0yLjIwNC01LjQ1LTIuMjA0LS4xNzcgMC0uMzU0LjAwNS0uNTMuMDE3TDE4LjggNC4wMzdjLS4xNzcgMi4xMDQtMS4wMzIgNC4wNjgtMi4zOCA1LjYxNy0xLjM0OCAxLjU1LTEuOTQyIDMuNDQyLTEuNzc0IDUuNDE0bC0xLjY3Ni00LjkwNGMtLjA2Mi0uMTgyLS4yNTgtLjI4LS40NC0uMjEzLS4xOC4wNjctLjI3NS4yNjYtLjIxMy40NDhsMS42OCA0LjkyNGMuMjIgMS45MyAxLjI3IDMuNjcgMi44OCA0Ljc2NCAxLjYxIDEuMDkzIDMuNTc3IDEuNDQxIDUuNDQxIDEuMDEybDEuNTMzLTQuNTAyYy4wNjQtLjE4Mi0uMDI3LS4zOC0uMi0uNDQ1LS4xOC0uMDYyLS4zNzguMDMxLS40NDUuMjE1bC0xLjQ0NCA0LjI0NWMtMS45MjUtLjEwNi0zLjc0Mi0uNzY4LTUuMTcxLTIuMDI4LS4xMi0uMTA2LS4yMy0uMjE1LS4zNC0uMzI2LS4xMS0uMTEzLS4yMTMtLjIyNy0uMzE2LS4zNDFsLTIuNTEzIDcuMzg0Yy41NTQtLjAyMyAxLjEtLjA3OCAxLjYzLS4xNjQgMS4wNzUtLjE3NCAyLjA2LS41NjQgMi45MS0xLjE1NCAxLjcwOC0xLjE4IDIuNzctMy4wNCAyLjc3LTUuMDUgMC0uNTg4LS4xMTUtMS4xNTgtLjMzMi0xLjY5bC0xLjQ0OC0yLjg5M2MuMjQtLjEyLjQ3LS4yNTUuNjktLjR6Ii8+PC9zdmc+)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

Koki Mager adalah chatbot resep cerdas yang dibangun menggunakan Streamlit dan LangChain. Didesain untuk para 'kaum mager' yang butuh inspirasi memasak cepat berdasarkan bahan-bahan yang ada di rumah.

Cukup masukkan bahan yang Anda punya (mis: `nasi, telur, kecap`), dan Koki Mager akan memberikan ide resep yang simpel dan kreatif.

**( Opsional: Ganti placeholder ini dengan screenshot aplikasi Anda )**


---

## 🌟 Fitur Utama

* **Antarmuka Chat Interaktif:** Dibangun dengan Streamlit untuk pengalaman pengguna yang bersih dan responsif.
* **Resep Cerdas (AI):** Menggunakan Google Gemini (`gemini-2.5-flash`) melalui LangChain ReAct Agent untuk menghasilkan resep yang relevan dan kreatif.
* **Fokus Topik:** Koki Mager secara spesifik di-prompt untuk **hanya** menjawab pertanyaan seputar makanan dan minuman. Pertanyaan di luar topik akan ditolak dengan jenaka.
* **Caching Resep:** Menyimpan resep yang pernah diminta ke file `recipe_cache.json` untuk mempercepat respons jika pertanyaan yang sama muncul lagi.
* **Riwayat Percakapan:** Menyimpan riwayat obrolan di sidebar (`st.session_state`) dan juga ke file `history.json` untuk persistensi.
* **Manajemen API Key:** Input API Key Google AI yang aman menggunakan *sidebar password input* Streamlit.

---

## 🛠️ Teknologi yang Digunakan

* **Python 3.10+**
* **Streamlit:** Untuk membangun antarmuka web interaktif.
* **LangChain:** Sebagai framework utama untuk membangun agent AI.
    * `langgraph`: Digunakan untuk `create_react_agent`.
    * `langchain-google-genai`: Untuk berinteraksi dengan model Gemini.
* **Google Generative AI:** Sebagai penyedia model LLM (Gemini).

---

## 🚀 Cara Menjalankan Secara Lokal

Ikuti langkah-langkah ini untuk menjalankan Koki Mager di mesin lokal Anda.

### 1. Prasyarat

* [Python](https://www.python.org/downloads/) (versi 3.10 atau lebih baru)
* [Git](https://git-scm.com/downloads/)
* **Google AI API Key:** Anda bisa mendapatkannya dari [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Instalasi

1.  **Clone Repositori**
    Buka terminal Anda dan clone repositori ini:
    ```bash
    git clone [https://github.com/mkeyzxi/chatbot-streamlit-koki.git](https://github.com/mkeyzxi/chatbot-streamlit-koki.git)
    cd chatbot-streamlit-koki
    ```

2.  **Buat Virtual Environment** (Sangat direkomendasikan)
    ```bash
    # Untuk macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Untuk Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependensi**
    Buat file bernama `requirements.txt` di direktori utama proyek Anda dan isi dengan daftar pustaka di bawah ini.

    **`requirements.txt`**:
    ```txt
    streamlit
    langchain
    langgraph
    langchain-google-genai
    langchain-core
    ```

    Kemudian, install menggunakan pip:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Menjalankan Aplikasi

1.  Setelah semua dependensi terinstal, jalankan aplikasi Streamlit:
    ```bash
    streamlit run app.py
    ```

2.  Buka browser Anda dan akses alamat lokal yang ditampilkan di terminal (biasanya `http://localhost:8501`).

3.  Di sidebar aplikasi, masukkan **Google AI API Key** Anda untuk mengaktifkan chatbot.

4.  Mulai memasak! 🍳

---
## 👤 Kontributor

* **[mkeyzxi](https://github.com/mkeyzxi)**

Jangan ragu untuk membuat *Pull Request* atau membuka *Issue* jika Anda menemukan bug atau ingin menambahkan fitur baru!