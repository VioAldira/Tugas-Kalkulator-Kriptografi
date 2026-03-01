import streamlit as st
import base64

#FUNGSI VIGENERE CIPHER
def vigenere_cipher(text, key, mode):
    res = ""
    key = key.upper()
    if not key:
        return text
    
    ki = 0
    is_decrypt = (mode == "Dekripsi") 
    
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[ki % len(key)]) - ord('A')
            
            if is_decrypt:
                new_char = chr((ord(char) - start - shift + 26) % 26 + start)
            else:
                new_char = chr((ord(char) - start + shift) % 26 + start)
            
            res += new_char
            ki += 1
        else:
            res += char 
    return res

#FUNGSI AFFINE CIPHER
def modInverse(a, m):
    for x in range(1, m):
        if (((a % m) * (x % m)) % m == 1):
            return x
    return -1

def affine_cipher(text, a, b, mode):
    res = ""
    is_decrypt = (mode == "Dekripsi")
    a_inv = modInverse(a, 26)
    
    if is_decrypt and a_inv == -1:
        return "Error: Kunci 'a' tidak memiliki invers. Pilih angka ganjil selain 13."

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            p = ord(char) - start
            if is_decrypt:
                res += chr(((a_inv * (p - b)) % 26) + start)
            else:
                res += chr(((a * p + b) % 26) + start)
        else:
            res += char
    return res

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Proyek Kriptografi", layout="centered")
st.title("🔐 Kalkulator Kriptografi Klasik")

# --- UI UTAMA ---
tab1, tab2 = st.tabs(["Input Teks", "Input File (Gambar/Audio/Video)"])

with tab1:
    st.markdown("**Algoritma**")
    algo = st.selectbox("Pilih Algoritma", ["Vigenere", "Affine", "Playfair", "Hill", "Enigma"], label_visibility="collapsed")
    
    st.markdown("**Mode**")
    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"], label_visibility="collapsed", key="mode_teks")
    
    st.markdown("**Input Teks**")
    text_input = st.text_area("Input Teks", label_visibility="collapsed")
    
    st.markdown("**Kunci**")
    if algo == "Vigenere":
        key = st.text_input("Kunci Alfabet", value="buaya", label_visibility="collapsed")
    elif algo == "Affine":
        col1, col2 = st.columns(2)
        a = col1.number_input("Kunci a (Ganjil selain 13)", value=3)
        b = col2.number_input("Kunci b", value=5)
    else:
        st.info("Algoritma ini sedang disiapkan...")
    
    if st.button("Proses Teks"):
        if algo == "Vigenere":
            hasil = vigenere_cipher(text_input, key, mode)
            st.success("Hasil:")
            st.code(hasil)
        elif algo == "Affine":
            hasil = affine_cipher(text_input, a, b, mode)
            st.success("Hasil:")
            st.code(hasil)

with tab2:
    st.write("Unggah **file asli** untuk dienkripsi, atau unggah **file .txt hasil enkripsi** untuk didekripsi.")
    
    mode_f = st.radio("Mode File", ["Enkripsi", "Dekripsi"], key="mode_file")
    key_f = st.text_input("Kunci Alfabet", value="buaya", key="key_file")
    
    
    ext = ""
    if mode_f == "Dekripsi":
        ext = st.text_input("Ekstensi file asli setelah didekripsi (misal: .jpg, .png, .mp3)", value=".jpg")

    uploaded_file = st.file_uploader("Pilih File", key="file_uploader")
    
    if uploaded_file is not None:
        if st.button("Proses File"):
            if mode_f == "Enkripsi":
                
                file_bytes = uploaded_file.read()
                b64_string = base64.b64encode(file_bytes).decode('utf-8')
                
                hasil_f = vigenere_cipher(b64_string, key_f, mode_f)
                
                st.success("File berhasil dienkripsi! Silakan unduh ciphertext-nya.")
                st.download_button(
                    label="Download Ciphertext (.txt)", 
                    data=hasil_f, 
                    file_name="encrypted_file.txt",
                    mime="text/plain"
                )
                
            elif mode_f == "Dekripsi":

                try:
                    cipher_text = uploaded_file.read().decode('utf-8')
                    
                    decrypted_b64 = vigenere_cipher(cipher_text, key_f, mode_f)
                    
                    data_asli = base64.b64decode(decrypted_b64)
                    
                    st.success("File berhasil didekripsi! Silakan unduh file aslinya.")
                    st.download_button(
                        label=f"Download File Asli ({ext})", 
                        data=data_asli, 
                        file_name=f"decrypted_file{ext}",
                        mime="application/octet-stream"
                    )
                except Exception as e:
                    st.error("Gagal dekripsi. Pastikan file yang diunggah adalah file .txt hasil enkripsi dan kunci benar.")
