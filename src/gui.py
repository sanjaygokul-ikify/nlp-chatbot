"""
gui.py — Tkinter-based GUI for NLP Chatbot.

Connects with ChatBot (core.py) to provide a user-friendly
chat interface instead of terminal interaction.

PEP 8 compliant, beginner-friendly, clean implementation.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading


class ChatGUI:
    """Main GUI window for the NLP Chatbot."""

    # ── Colour palette ──────────────────────────────────────────────────
    BG_MAIN = "#1e1e2e"       # dark background
    BG_CHAT = "#181825"       # chat area background
    BG_INPUT = "#313244"      # input field background
    BG_BTN = "#89b4fa"        # send button background
    BG_BTN_HOVER = "#74c7ec"  # send button hover

    FG_TEXT = "#cdd6f4"       # general text
    FG_USER = "#a6e3a1"       # user bubble text
    FG_BOT = "#89dceb"        # bot bubble text
    FG_TIMESTAMP = "#6c7086"  # timestamp text

    FONT_CHAT = ("Segoe UI", 11)
    FONT_INPUT = ("Segoe UI", 11)
    FONT_TITLE = ("Segoe UI", 13, "bold")
    FONT_BTN = ("Segoe UI", 11, "bold")
    FONT_TS = ("Segoe UI", 8)

    def __init__(self, chatbot):
        """
        Parameters
        ----------
        chatbot : ChatBot
            An initialised ChatBot instance from core.py.
        """
        self.chatbot = chatbot

        self.root = tk.Tk()
        self.root.title("NLP Chatbot")
        self.root.geometry("600x700")
        self.root.minsize(420, 500)
        self.root.configure(bg=self.BG_MAIN)

        self._build_ui()
        self._display_welcome()

    # ── UI construction ─────────────────────────────────────────────────

    def _build_ui(self):
        """Assemble all widgets."""
        self._build_header()
        self._build_chat_area()
        self._build_input_area()

    def _build_header(self):
        """Top title bar."""
        header = tk.Frame(self.root, bg="#313244", pady=10)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🤖  NLP Chatbot",
            bg="#313244",
            fg=self.FG_TEXT,
            font=self.FONT_TITLE,
        ).pack()

        tk.Label(
            header,
            text="Your friendly AI assistant",
            bg="#313244",
            fg=self.FG_TIMESTAMP,
            font=("Segoe UI", 9),
        ).pack()

    def _build_chat_area(self):
        """Scrollable chat display."""
        frame = tk.Frame(self.root, bg=self.BG_MAIN)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 0))

        self.chat_display = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=self.BG_CHAT,
            fg=self.FG_TEXT,
            font=self.FONT_CHAT,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            cursor="arrow",
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Tag configuration for coloured text
        self.chat_display.tag_config(
            "user_label", foreground=self.FG_USER, font=("Segoe UI", 10, "bold")
        )
        self.chat_display.tag_config("user_msg", foreground=self.FG_USER)
        self.chat_display.tag_config(
            "bot_label", foreground=self.FG_BOT, font=("Segoe UI", 10, "bold")
        )
        self.chat_display.tag_config("bot_msg", foreground=self.FG_BOT)
        self.chat_display.tag_config(
            "timestamp", foreground=self.FG_TIMESTAMP, font=self.FONT_TS
        )
        self.chat_display.tag_config(
            "divider", foreground="#45475a"
        )

    def _build_input_area(self):
        """Message entry field and Send button."""
        frame = tk.Frame(self.root, bg=self.BG_MAIN, pady=10)
        frame.pack(fill=tk.X, padx=12, pady=(6, 12))

        # Text entry
        self.user_entry = tk.Entry(
            frame,
            bg=self.BG_INPUT,
            fg=self.FG_TEXT,
            insertbackground=self.FG_TEXT,
            font=self.FONT_INPUT,
            relief=tk.FLAT,
        )
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
        self.user_entry.bind("<Return>", self._on_send)
        self.user_entry.focus()

        # Send button
        self.send_btn = tk.Button(
            frame,
            text="Send ➤",
            bg=self.BG_BTN,
            fg="#1e1e2e",
            activebackground=self.BG_BTN_HOVER,
            font=self.FONT_BTN,
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=6,
            command=self._on_send,
        )
        self.send_btn.pack(side=tk.RIGHT)

        # Hover effects
        self.send_btn.bind("<Enter>", lambda _: self.send_btn.config(bg=self.BG_BTN_HOVER))
        self.send_btn.bind("<Leave>", lambda _: self.send_btn.config(bg=self.BG_BTN))

        # Clear button
        clear_btn = tk.Button(
            frame,
            text="Clear",
            bg="#45475a",
            fg=self.FG_TEXT,
            activebackground="#585b70",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=6,
            command=self._on_clear,
        )
        clear_btn.pack(side=tk.RIGHT, padx=(0, 6))

    # ── Event handlers ───────────────────────────────────────────────────

    def _on_send(self, event=None):
        """Handle message submission."""
        user_text = self.user_entry.get().strip()
        if not user_text:
            return

        self.user_entry.delete(0, tk.END)
        self._append_message("You", user_text, is_user=True)
        self.send_btn.config(state=tk.DISABLED)

        # Run chatbot in background thread to keep UI responsive
        thread = threading.Thread(
            target=self._fetch_response, args=(user_text,), daemon=True
        )
        thread.start()

    def _fetch_response(self, user_text: str):
        """Call chatbot.respond() off the main thread."""
        response = self.chatbot.respond(user_text)
        self.root.after(0, self._on_response_ready, response)

    def _on_response_ready(self, response: str):
        """Post bot response back on the main thread."""
        self._append_message("Bot", response, is_user=False)
        self.send_btn.config(state=tk.NORMAL)
        self.user_entry.focus()

    def _on_clear(self):
        """Clear the entire chat display."""
        confirmed = messagebox.askyesno(
            "Clear Chat", "Are you sure you want to clear the conversation?"
        )
        if confirmed:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self._display_welcome()

    # ── Display helpers ──────────────────────────────────────────────────

    def _append_message(self, sender: str, message: str, is_user: bool):
        """Insert a formatted message into the chat display."""
        from datetime import datetime

        timestamp = datetime.now().strftime("%H:%M")
        label_tag = "user_label" if is_user else "bot_label"
        msg_tag = "user_msg" if is_user else "bot_msg"

        self.chat_display.config(state=tk.NORMAL)

        # Sender label + timestamp
        self.chat_display.insert(tk.END, f"\n{sender}  ", label_tag)
        self.chat_display.insert(tk.END, f"{timestamp}\n", "timestamp")

        # Message body
        self.chat_display.insert(tk.END, f"  {message}\n", msg_tag)

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _display_welcome(self):
        """Show a welcome message when the app starts or is cleared."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(
            tk.END,
            "Welcome! Type a message below and press Send or Enter.\n",
            "bot_label",
        )
        self.chat_display.insert(
            tk.END,
            "─────────────────────────────────────────\n",
            "divider",
        )
        self.chat_display.config(state=tk.DISABLED)

    # ── Entry point ──────────────────────────────────────────────────────

    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()
