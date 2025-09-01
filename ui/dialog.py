import tkinter as tk


def show_info(master, message, title="Подсказка"):
    """Показывает красивый диалог"""
    dialog = tk.Toplevel(master)
    dialog.title("")  # ← УБЕРИ заголовок tkinter
    dialog.geometry("500x400")
    dialog.resizable(False, False)
    dialog.configure(bg="#2c3e50")
    dialog.overrideredirect(True)  # ← УБЕРИ рамку окна

    # Центрируем
    dialog.update_idletasks()
    x = (master.winfo_width() - 500) // 2 + master.winfo_x()
    y = (master.winfo_height() - 400) // 2 + master.winfo_y()
    dialog.geometry(f"500x400+{x}+{y}")

    # Стилизованный фрейм
    frame = tk.Frame(dialog, bg="#2c3e50", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    # Заголовок
    title_label = tk.Label(
        frame,
        text=title,
        font=("Arial", 16, "bold"),
        bg="#2c3e50",
        fg="#3498db",
        pady=10
    )
    title_label.pack()

    # Текст
    text_widget = tk.Text(
        frame,
        font=("Arial", 14),
        bg="#34495e",
        fg="white",
        wrap="word",
        relief="flat",
        padx=10,
        pady=10,
        height=10
    )
    text_widget.insert("1.0", message)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True, pady=10)

    # Кнопка OK
    ok_btn = tk.Button(
        frame,
        text="OK",
        font=("Arial", 12, "bold"),
        bg="#3498db",
        fg="white",
        width=10,
        command=dialog.destroy
    )
    ok_btn.pack(pady=10)

    dialog.transient(master)
    dialog.grab_set()


def ask_string(master, title, prompt):
    """Красивый диалог для ввода текста"""
    dialog = tk.Toplevel(master)
    dialog.title("")
    dialog.geometry("400x200")
    dialog.resizable(False, False)
    dialog.configure(bg="#2c3e50")
    dialog.overrideredirect(True)

    # Центрируем
    dialog.update_idletasks()
    x = (master.winfo_width() - 400) // 2 + master.winfo_x()
    y = (master.winfo_height() - 200) // 2 + master.winfo_y()
    dialog.geometry(f"400x200+{x}+{y}")

    frame = tk.Frame(dialog, bg="#2c3e50", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    # Заголовок
    tk.Label(
        frame,
        text=title,
        font=("Arial", 14, "bold"),
        bg="#2c3e50",
        fg="white",
        pady=5
    ).pack()

    # Поле ввода
    entry = tk.Entry(
        frame,
        font=("Arial", 12),
        bg="#34495e",
        fg="white",
        relief="flat"
    )
    entry.pack(pady=10, fill="x")
    entry.focus()

    # Кнопки
    btn_frame = tk.Frame(frame, bg="#2c3e50")
    btn_frame.pack()

    result = [None]  # Храним результат

    def on_ok():
        result[0] = entry.get()
        dialog.destroy()

    tk.Button(
        btn_frame,
        text="OK",
        font=("Arial", 10, "bold"),
        bg="#3498db",
        fg="white",
        width=8,
        command=on_ok
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        btn_frame,
        text="Отмена",
        font=("Arial", 10, "bold"),
        bg="#e74c3c",
        fg="white",
        width=8,
        command=dialog.destroy
    ).pack(side=tk.RIGHT, padx=5)

    dialog.transient(master)
    dialog.grab_set()
    dialog.wait_window()

    return result[0]
