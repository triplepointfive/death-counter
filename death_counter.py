import json
import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(DATA_DIR, "deaths.json")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"games": {}, "current": None}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class DeathCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Death Counter")
        self.root.geometry("500x400")
        self.root.minsize(400, 300)

        self.data = load_data()
        self.current_game = self.data.get("current")
        if self.current_game not in self.data.get("games", {}):
            self.current_game = None

        self._build_ui()
        self._refresh_game_list()
        self._update_display()

    def _build_ui(self):
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)

        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)

        ttk.Label(left_frame, text="Games", font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0, 4))

        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.game_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Segoe UI", 10),
            activestyle="none",
            exportselection=False,
        )
        scrollbar.config(command=self.game_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.game_listbox.pack(fill=tk.BOTH, expand=True)
        self.game_listbox.bind("<<ListboxSelect>>", self._on_game_select)

        add_btn = ttk.Button(left_frame, text="+ Add Game", command=self._add_game)
        add_btn.pack(fill=tk.X, pady=(4, 2))

        remove_btn = ttk.Button(left_frame, text="Remove Game", command=self._remove_game)
        remove_btn.pack(fill=tk.X, pady=(0, 0))

        self.game_label = ttk.Label(
            right_frame, text="No game selected",
            font=("Segoe UI", 14, "bold"), anchor=tk.CENTER
        )
        self.game_label.pack(pady=(10, 5))

        self.count_label = ttk.Label(
            right_frame, text="0",
            font=("Segoe UI", 48, "bold"), anchor=tk.CENTER,
            foreground="#c0392b"
        )
        self.count_label.pack(pady=(0, 15))

        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack()

        death_btn = ttk.Button(
            btn_frame, text="+1 Death",
            command=self._add_death,
            width=15,
        )
        death_btn.pack(pady=3)

        set_btn = ttk.Button(
            btn_frame, text="Set Value",
            command=self._set_value,
            width=15,
        )
        set_btn.pack(pady=3)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _refresh_game_list(self):
        self.game_listbox.delete(0, tk.END)
        games = list(self.data.get("games", {}).keys())
        for name in games:
            self.game_listbox.insert(tk.END, name)

        if self.current_game and self.current_game in games:
            idx = games.index(self.current_game)
            self.game_listbox.selection_clear(0, tk.END)
            self.game_listbox.selection_set(idx)
            self.game_listbox.activate(idx)

    def _update_display(self):
        games = self.data.get("games", {})
        if self.current_game:
            count = games.get(self.current_game, 0)
            self.game_label.config(text=self.current_game)
            self.count_label.config(text=str(count))
        else:
            self.game_label.config(text="No game selected")
            self.count_label.config(text="—")

    def _on_game_select(self, event):
        sel = self.game_listbox.curselection()
        if sel:
            name = self.game_listbox.get(sel[0])
            self.current_game = name
            self.data["current"] = name
            self._update_display()

    def _add_game(self):
        name = simpledialog.askstring("Add Game", "Game name:", parent=self.root)
        if name:
            name = name.strip()
            if not name:
                return
            if name in self.data.setdefault("games", {}):
                messagebox.showwarning("Warning", f"Game '{name}' already exists.", parent=self.root)
                return
            self.data["games"][name] = 0
            self._refresh_game_list()
            if self.current_game is None:
                self.current_game = name
                self.data["current"] = name
                self.game_listbox.selection_clear(0, tk.END)
                self.game_listbox.selection_set(0)
            self._update_display()

    def _remove_game(self):
        if not self.current_game:
            return
        confirm = messagebox.askyesno(
            "Remove Game",
            f"Remove '{self.current_game}' and all its data?",
            parent=self.root,
        )
        if confirm:
            del self.data["games"][self.current_game]
            games = list(self.data["games"].keys())
            self.current_game = games[0] if games else None
            self.data["current"] = self.current_game
            self._refresh_game_list()
            self._update_display()

    def _add_death(self):
        if not self.current_game:
            messagebox.showinfo("Info", "Select a game first.", parent=self.root)
            return
        self.data["games"][self.current_game] += 1
        self._update_display()

    def _set_value(self):
        if not self.current_game:
            messagebox.showinfo("Info", "Select a game first.", parent=self.root)
            return
        current = self.data["games"][self.current_game]
        val = simpledialog.askinteger(
            "Set Value",
            f"Set deaths for '{self.current_game}':",
            initialvalue=current,
            minvalue=0,
            parent=self.root,
        )
        if val is not None:
            self.data["games"][self.current_game] = val
            self._update_display()

    def _on_close(self):
        self.data["current"] = self.current_game
        save_data(self.data)
        self.root.destroy()


def main():
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    app = DeathCounter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
