# Caesar Cipher Decryptor

A comprehensive Python tool for decrypting Caesar Cipher encrypted messages with multiple decryption modes and intelligent shift detection.

## Features

- **Multiple Decryption Modes**:
  - Manual shift decryption (specify shift value 1-25)
  - Brute force analysis (shows all possible decryptions)
  - Automatic shift detection using frequency analysis
- **User-Friendly GUI** built with Tkinter
- **Smart Detection** using English letter frequency analysis
- **Copy to Clipboard** functionality
- **Input Validation** and error handling
- **Cross-Platform** compatibility

## Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Setup
1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
```bash
python caesar_cipher_decryptor.py
```

### Decryption Modes

#### 1. Manual Shift Mode
- Enter your cipher text
- Select "Manual Shift" mode
- Specify a shift value (1-25)
- Click "Decrypt" to see the result

#### 2. Brute Force Mode
- Enter your cipher text
- Select "Brute Force (All Shifts)" mode
- Click "Decrypt" to see all 25 possible decryptions
- Manually identify the most readable result

#### 3. Auto Detection Mode
- Enter your cipher text
- Select "Auto Detect Best Shift" mode
- Click "Decrypt" to automatically find the most likely plaintext
- View top 5 candidates ranked by frequency analysis

### Example Usage

**Input**: `KHOOR`
**Manual Shift (3)**: `HELLO`
**Auto Detection**: Automatically identifies shift 3 as most likely

## Technical Details

### Algorithm
The decryptor uses the standard Caesar cipher formula:
```
decrypted_char = (encrypted_char - shift) mod 26
```

### Frequency Analysis
Auto detection employs chi-squared statistical analysis comparing letter frequencies against standard English language patterns:
- E: 12.70%, T: 9.06%, A: 8.17%, etc.

### Performance
- Decryption completes in under 1 second
- Memory efficient with O(n) time complexity
- Handles texts of any reasonable length

## File Structure

```
caesar-cipher-decryptor/
├── caesar_cipher_decryptor.py    # Main application
├── requirements.txt              # Python dependencies
├── README.md                    # This file
└── PRD.md                      # Product Requirements Document
```

## Features Overview

| Feature | Status | Description |
|---------|--------|-------------|
| Input Validation | ✅ | Validates cipher text input |
| Manual Shift | ✅ | User-specified shift decryption |
| Brute Force | ✅ | All 25 possible decryptions |
| Auto Detection | ✅ | Frequency analysis for best shift |
| GUI Interface | ✅ | Tkinter-based user interface |
| Copy to Clipboard | ✅ | Easy result copying |
| Case Preservation | ✅ | Maintains original text formatting |
| Error Handling | ✅ | Robust error management |

## Use Cases

### Educational
- **Cryptography Students**: Learn Caesar cipher mechanics
- **Educators**: Demonstrate classical encryption methods
- **Security Training**: Understand basic cryptanalysis

### Practical Applications
- **CTF Challenges**: Quickly solve Caesar cipher puzzles
- **Penetration Testing**: Decrypt discovered Caesar ciphers
- **Historical Research**: Decode historical encrypted documents

## Troubleshooting

### Common Issues

**Import Error with pyperclip**:
```bash
pip install --upgrade pyperclip
```

**GUI Not Displaying**:
- Ensure you're running Python with GUI support
- On Linux, install: `sudo apt-get install python3-tk`

**Permission Errors**:
- Run with elevated privileges if needed
- Check file permissions in your working directory

## Future Enhancements

- [ ] Encryption mode (encode plaintext to cipher)
- [ ] Additional classical ciphers (ROT13, Atbash, etc.)
- [ ] Web-based interface
- [ ] Export results to text files
- [ ] Advanced frequency analysis with bigram/trigram support
- [ ] Multiple language support beyond English

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Version History

- **v1.0** - Initial release with all core features
  - Manual, brute force, and auto detection modes
  - GUI interface with Tkinter
  - Frequency analysis for shift detection
  - Copy to clipboard functionality

## Contact

For bug reports, feature requests, or questions, please open an issue in the repository.

---

**Note**: This tool is designed for educational and legitimate security testing purposes. Always ensure you have proper authorization before attempting to decrypt any encrypted communications.