# 🛡️ Data Grabber Demo

<p align="center">
  <img src="https://img.shields.io/badge/status-research%20only-red?style=flat-square" />
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey?style=flat-square" /> 
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d4/Flag_of_Israel.svg" alt="Israel Flag" width="25"/>

</p>
## 📚 Description

**Data Grabber Demo** is an educational Python project designed for research and training in cybersecurity and malware analysis. It demonstrates how data can be collected from a Windows machine using Python — including:

- ✅ Extracting Chrome saved passwords
- ✅ Collecting Discord tokens and user metadata
- ✅ Gathering system info (IP address, HWID, PC/user name)
- ✅ Sending all data to a Discord webhook in JSON format

> ⚠️ This project is intended **strictly for educational purposes** inside controlled environments. **Do not use on unauthorized systems.**

---

## 🔧 Features

- Chrome password decryption via Windows `CryptUnprotectData`
- Discord token parsing & decryption (AES-GCM + base64)
- HWID and IP address collection
- Organized output in JSON format
- Sends data securely to Discord via webhook

---

## 🚀 Setup

### 1. Clone the project
```bash
git clone https://github.com/yehonatanm1/Data_grabber_demo.git
cd Data_grabber_demo
pip install -r requirements.txt
python docs_tool/Data_grabber.py
