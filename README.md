
# Quantum Compressor

Quantum Compress is a full-stack, web-based document compression tool built with Python and Flask. It allows users to upload and compress various file types, including PDFs, images, documents, text files, and videos — all through a clean and intuitive interface.

## 🌟 Features

- ✅ Compress PDFs using PyMuPDF
- 🖼️ Optimize JPEG and PNG images with Pillow
- 📄 Reduce DOCX and PPTX sizes via ZIP-based compression
- 📝 Compress text files using Gzip
- 🎞️ Shrink MP4 videos using FFmpeg
- 🌐 User-friendly web interface powered by Flask
- 📥 Download compressed files instantly

## 🗂️ Supported File Formats

- PDF (.pdf)
- Word (.docx)
- PowerPoint (.pptx)
- Text (.txt)
- Image (.jpg, .jpeg, .png)
- Video (.mp4)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/quantum-compress.git
cd quantum-compress
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## 🛠️ Requirements

- Python 3.7+
- Flask
- Pillow
- PyMuPDF
- Gzip (comes with Python)
- FFmpeg (installed and added to system PATH)

## 📂 Folder Structure

```
quantum-compress/
├── static/
│   ├── uploads/
│   └── compressed/
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
└── README.md
```

## 📌 Note

Make sure FFmpeg is installed and accessible via command line for video compression to work. You can download it from [ffmpeg.org](https://ffmpeg.org).

## 📃 License

This project is licensed under the MIT License.

## 🤝 Contributing

Feel free to fork this repo and submit pull requests. All contributions are welcome!

---

Made with ❤️ by [Akash Dhotre](https://github.com/Akashdhotre10) 
