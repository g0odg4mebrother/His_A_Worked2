
import tkinter as tk
from tkinter import messagebox

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Регистрация пользователя")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.btn_color = "#4CAF50"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        self.create_widgets()
    
    def create_widgets(self):
        title_label = tk.Label(
            self.root, 
            text="Регистрация пользователя",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=20)

        form_frame = tk.Frame(self.root, bg=self.bg_color)
        form_frame.pack(pady=20)

        username_label = tk.Label(
            form_frame,
            text="Имя пользователя:",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_color
        )
        username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.username_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            width=25,
            bg="white",
            fg=self.text_color,
            relief="solid",
            borderwidth=1
        )
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        password_label = tk.Label(
            form_frame,
            text="Пароль:",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.text_color
        )
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.password_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            width=25,
            show="*", 
            bg="white",
            fg=self.text_color,
            relief="solid",
            borderwidth=1
        )
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        register_btn = tk.Button(
            self.root,
            text="Зарегистрироваться",
            font=("Arial", 11, "bold"),
            bg=self.btn_color,
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.register_user
        )
        register_btn.pack(pady=30)

        hint_label = tk.Label(
            self.root,
            text="* Оба поля должны быть заполнены",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#666666"
        )
        hint_label.pack(pady=5)

        self.username_entry.focus_set()

        self.root.bind('<Return>', lambda event: self.register_user())
    
    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning(
                "Предупреждение",
                "Пожалуйста, заполните все поля!\n"
                "Имя пользователя и пароль не могут быть пустыми."
            )
            if not username:
                self.highlight_field(self.username_entry)
            if not password:
                self.highlight_field(self.password_entry)
            return

        if len(password) < 4:
            messagebox.showwarning(
                "Предупреждение",
                "Пароль слишком короткий!\n"
                "Рекомендуется использовать пароль длиной не менее 4 символов."
            )
            self.highlight_field(self.password_entry)
            return

        messagebox.showinfo(
            "Успешная регистрация",
            f"Пользователь '{username}' успешно зарегистрирован!\n\n"
            f"Ваши данные:\n"
            f"Имя пользователя: {username}\n"
            f"Длина пароля: {len(password)} символов"
        )

        self.clear_fields()

        self.username_entry.focus_set()
    
    def highlight_field(self, entry_field):
        original_bg = entry_field.cget("bg")
        entry_field.configure(bg="#ffcccc")  
        
        self.root.after(1500, lambda: entry_field.configure(bg=original_bg))
    
    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def run(self):
        self.root.mainloop()


def toggle_password_visibility(password_entry, show_password_var):
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


class EnhancedRegistrationApp(RegistrationApp):
    def __init__(self, root):
        super().__init__(root)
        self.add_extra_features()
    
    def add_extra_features(self):
        options_frame = tk.Frame(self.root, bg=self.bg_color)
        options_frame.pack(pady=10)
        
        self.show_password_var = tk.BooleanVar(value=False)
        
        show_password_check = tk.Checkbutton(
            options_frame,
            text="Показать пароль",
            variable=self.show_password_var,
            command=lambda: self.toggle_password_visibility(),
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.text_color,
            selectcolor=self.bg_color,
            activebackground=self.bg_color
        )
        show_password_check.pack(side="left", padx=5)
        
        clear_btn = tk.Button(
            options_frame,
            text="Очистить",
            font=("Arial", 9),
            bg="#f44336",
            fg="white",
            command=self.clear_fields,
            relief="flat",
            padx=10,
            cursor="hand2"
        )
        clear_btn.pack(side="left", padx=5)
    
    def toggle_password_visibility(self):
        """Переключение видимости пароля"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")


def main():
    root = tk.Tk()
    
    app = EnhancedRegistrationApp(root)  
    
    app.run()


if __name__ == "__main__":

    main()
