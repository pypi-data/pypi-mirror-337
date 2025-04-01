# Kamus Bahasa Rejang CLI

Kamus CLI sederhana untuk menerjemahkan kata dari dan ke bahasa Rejang menggunakan API dari [Kamus Rejang](https://kamusrejang.vercel.app/).

## 🚀 Fitur
- Terjemahkan kata dari **Bahasa Indonesia ke Rejang**.
- Terjemahkan kata dari **Bahasa Rejang ke Indonesia**.
- Terjemahkan kata dari **Bahasa Indonesia ke bahasa lain**.
- Terjemahkan kata dari **Bahasa Rejang ke bahasa lain**.

## 📥 Instalasi

Pastikan kamu sudah menginstal **Python 3.x** di sistem kamu.

### 1️⃣ Clone Repository (atau Unduh Kode)
```sh
git clone https://github.com/MFathinHalim/kamus-rejang-cli.git
cd rejang-dict-cli
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

## 🔧 Cara Menggunakan

Jalankan skrip Python:
```sh
python rejang_dict_cli.py
```

Kemudian, gunakan perintah berikut:

| Perintah                          | Fungsi |
|-----------------------------------|--------|
| `translate <kata>`                 | Terjemahkan dari Indonesia ke Rejang |
| `translate-rejang <kata>`           | Terjemahkan dari Rejang ke Indonesia |
| `translate-<kode_bahasa> <kata>`   | Terjemahkan ke bahasa lain (misal `translate-en kamu`) |
| `translate-rejang-<kode_bahasa> <kata>` | Terjemahkan dari Rejang ke bahasa lain |
| `help`                             | Tampilkan daftar perintah |
| `exit`                             | Keluar dari aplikasi |

## 📌 Contoh Penggunaan
```
>>> translate rumah
Translation: umeak'

>>> translate-rejang keracok'
Translation: baju

>>> translate-en village
Translation: sadei
```

## 🛠 Pengembangan
Kamu bisa forking proyek ini dan mengembangkannya lebih lanjut. Jangan lupa untuk memberi credit ya! 😃

