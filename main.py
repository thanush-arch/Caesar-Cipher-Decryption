#!/usr/bin/env python3
"""
Caesar Cipher Decryptor
A comprehensive tool for decrypting Caesar Cipher encrypted messages.
Supports manual shift, brute force, and automatic detection modes.
"""

import string
import re
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip

class CaesarCipherDecryptor:
    def __init__(self):
        self.english_freq = {
            'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
            'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
            'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
            'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
            'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
        }
        
    def decrypt_with_shift(self, cipher_text, shift):
        """Decrypt cipher text with a specific shift value."""
        result = ""
        for char in cipher_text:
            if char.isalpha():
                # Handle uppercase letters
                if char.isupper():
                    result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                # Handle lowercase letters
                else:
                    result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                # Keep non-alphabetic characters unchanged
                result += char
        return result
    
    def brute_force_decrypt(self, cipher_text):
        """Generate all possible decryptions (shifts 1-25)."""
        results = []
        for shift in range(1, 26):
            decrypted = self.decrypt_with_shift(cipher_text, shift)
            results.append((shift, decrypted))
        return results
    
    def calculate_chi_squared(self, text):
        """Calculate chi-squared statistic for text against English frequency."""
        text = re.sub('[^A-Z]', '', text.upper())
        if len(text) == 0:
            return float('inf')
        
        letter_count = Counter(text)
        chi_squared = 0
        
        for letter in string.ascii_uppercase:
            observed = letter_count.get(letter, 0)
            expected = (self.english_freq.get(letter, 0) / 100) * len(text)
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected
        
        return chi_squared
    
    def auto_detect_shift(self, cipher_text):
        """Automatically detect the most likely shift using frequency analysis."""
        results = self.brute_force_decrypt(cipher_text)
        best_shift = 1
        best_score = float('inf')
        
        for shift, decrypted in results:
            score = self.calculate_chi_squared(decrypted)
            if score < best_score:
                best_score = score
                best_shift = shift
        
        return best_shift, self.decrypt_with_shift(cipher_text, best_shift)

class CaesarGUI:
    def __init__(self, root):
        self.root = root
        self.decryptor = CaesarCipherDecryptor()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI interface."""
        self.root.title("Caesar Cipher Decryptor v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Input section
        ttk.Label(main_frame, text="Cipher Text:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(main_frame, height=4, wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Decryption Mode", padding="5")
        mode_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        mode_frame.columnconfigure(1, weight=1)
        
        self.mode_var = tk.StringVar(value="manual")
        
        ttk.Radiobutton(mode_frame, text="Manual Shift", variable=self.mode_var, 
                       value="manual", command=self.on_mode_change).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Radiobutton(mode_frame, text="Brute Force (All Shifts)", variable=self.mode_var, 
                       value="brute", command=self.on_mode_change).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Radiobutton(mode_frame, text="Auto Detect Best Shift", variable=self.mode_var, 
                       value="auto", command=self.on_mode_change).grid(row=0, column=2, sticky=tk.W)
        
        # Shift input (for manual mode)
        self.shift_frame = ttk.Frame(mode_frame)
        self.shift_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Label(self.shift_frame, text="Shift Value (1-25):").grid(row=0, column=0, sticky=tk.W)
        self.shift_var = tk.StringVar(value="3")
        shift_spinbox = ttk.Spinbox(self.shift_frame, from_=1, to=25, textvariable=self.shift_var, width=5)
        shift_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Decrypt button
        decrypt_btn = ttk.Button(main_frame, text="Decrypt", command=self.decrypt, style='Accent.TButton')
        decrypt_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Copy button
        copy_btn = ttk.Button(main_frame, text="Copy Results to Clipboard", command=self.copy_results)
        copy_btn.grid(row=5, column=0, columnspan=2, pady=(0, 5))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
    def on_mode_change(self):
        """Handle mode selection changes."""
        if self.mode_var.get() == "manual":
            self.shift_frame.grid()
        else:
            self.shift_frame.grid_remove()
    
    def decrypt(self):
        """Main decrypt function based on selected mode."""
        cipher_text = self.input_text.get(1.0, tk.END).strip()
        
        if not cipher_text:
            messagebox.showwarning("Input Error", "Please enter cipher text to decrypt.")
            return
        
        # Validate input contains letters
        if not any(c.isalpha() for c in cipher_text):
            messagebox.showwarning("Input Error", "Cipher text must contain at least some letters.")
            return
        
        self.status_var.set("Processing...")
        self.root.update()
        
        try:
            mode = self.mode_var.get()
            self.results_text.delete(1.0, tk.END)
            
            if mode == "manual":
                self.manual_decrypt(cipher_text)
            elif mode == "brute":
                self.brute_force_decrypt(cipher_text)
            else:  # auto
                self.auto_decrypt(cipher_text)
                
            self.status_var.set("Decryption completed successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during decryption: {str(e)}")
            self.status_var.set("Error occurred")
    
    def manual_decrypt(self, cipher_text):
        """Handle manual shift decryption."""
        try:
            shift = int(self.shift_var.get())
            if not 1 <= shift <= 25:
                messagebox.showwarning("Invalid Shift", "Shift value must be between 1 and 25.")
                return
        except ValueError:
            messagebox.showwarning("Invalid Shift", "Please enter a valid number for shift value.")
            return
        
        decrypted = self.decryptor.decrypt_with_shift(cipher_text, shift)
        
        result = f"=== MANUAL SHIFT DECRYPTION ===\n\n"
        result += f"Original Cipher Text: {cipher_text}\n"
        result += f"Shift Value: {shift}\n"
        result += f"Decrypted Text: {decrypted}\n"
        
        self.results_text.insert(tk.END, result)
    
    def brute_force_decrypt(self, cipher_text):
        """Handle brute force decryption."""
        results = self.decryptor.brute_force_decrypt(cipher_text)
        
        result = f"=== BRUTE FORCE DECRYPTION ===\n\n"
        result += f"Original Cipher Text: {cipher_text}\n\n"
        result += "All possible decryptions:\n"
        result += "-" * 50 + "\n"
        
        for shift, decrypted in results:
            result += f"Shift {shift:2d}: {decrypted}\n"
        
        self.results_text.insert(tk.END, result)
    
    def auto_decrypt(self, cipher_text):
        """Handle automatic shift detection."""
        best_shift, best_decryption = self.decryptor.auto_detect_shift(cipher_text)
        
        result = f"=== AUTO DETECTION DECRYPTION ===\n\n"
        result += f"Original Cipher Text: {cipher_text}\n"
        result += f"Detected Best Shift: {best_shift}\n"
        result += f"Most Likely Plaintext: {best_decryption}\n\n"
        
        # Also show a few other top candidates
        all_results = self.decryptor.brute_force_decrypt(cipher_text)
        scored_results = []
        
        for shift, decrypted in all_results:
            score = self.decryptor.calculate_chi_squared(decrypted)
            scored_results.append((score, shift, decrypted))
        
        scored_results.sort()
        
        result += "Top 5 candidates (by frequency analysis):\n"
        result += "-" * 50 + "\n"
        
        for i, (score, shift, decrypted) in enumerate(scored_results[:5]):
            marker = " ← BEST MATCH" if i == 0 else ""
            result += f"Shift {shift:2d}: {decrypted}{marker}\n"
        
        self.results_text.insert(tk.END, result)
    
    def copy_results(self):
        """Copy results to clipboard."""
        results = self.results_text.get(1.0, tk.END).strip()
        if results:
            try:
                pyperclip.copy(results)
                self.status_var.set("Results copied to clipboard")
            except:
                # Fallback for systems without clipboard support
                self.root.clipboard_clear()
                self.root.clipboard_append(results)
                self.status_var.set("Results copied to clipboard (fallback method)")
        else:
            messagebox.showwarning("No Results", "No results to copy. Please decrypt some text first.")

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = CaesarGUI(root)
    
    # Sample text for testing
    sample_text = "KHOOR"  # "HELLO" with shift 3
    app.input_text.insert(1.0, sample_text)
    
    root.mainloop()

if __name__ == "__main__":
    main()