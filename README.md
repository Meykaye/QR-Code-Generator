# QR Code Generator

A sleek, dark-themed QR code generator built with **PyQt5**, inspired by **Material Design** principles. This desktop app allows users to input URLs, generate QR codes, preview them in the UI, and save them as images.

---

## 🚀 Features

* ⚫ Beautiful dark Material UI theme
* 🌐 URL input validation
* 🔲 Dynamic QR code generation using `qrcode`
* 💾 Save QR codes as PNG or JPEG
* 📦 Lightweight and responsive

---

## 📦 Requirements

* Python 3.7+
* PyQt5
* qrcode
* Pillow

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```txt
PyQt5
qrcode
Pillow
```

---

## 🛠️ How to Run

```bash
python dark_qrcode_generator.py
```

> Ensure the script filename matches the one you're using.

---

## 🧠 How It Works

1. User enters a valid URL.
2. The app validates the input.
3. On click of **Generate QR Code**, a QR image is rendered and displayed in the app.
4. The **Save QR Code** button allows saving the image in various formats.

---

## 📁 Project Structure

```
📁 DarkQRCodeGenerator/
├── qr_main.py
├── requirements.txt
└── README.md
```

---

## 🔒 URL Validation

This app only accepts URLs that:

* Begin with `http://` or `https://`
* Have a valid domain or IP address

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🤝 Contributions

Contributions are welcome! Feel free to fork this project and submit a pull request with your improvements.
