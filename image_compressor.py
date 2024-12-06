import os
import threading
from tkinter import Tk, filedialog, messagebox, Button, Label, StringVar, Entry, ttk, Frame
from PIL import Image

class ImageCompressor:
    def __init__(self):
        self.root = Tk()
        self.setup_gui()

    def compress_images_to_target_size(self, input_folder, output_folder, target_size_kb):
        try:
            os.makedirs(output_folder, exist_ok=True)
            total_files = len([f for f in os.listdir(input_folder)
                             if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            processed = 0

            for filename in os.listdir(input_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    input_path = os.path.join(input_folder, filename)
                    output_path = os.path.join(output_folder, filename)
                    self.compress_image(input_path, output_path, target_size_kb)
                    processed += 1
                    self.update_progress(processed / total_files * 100)

            self.progress_bar.stop()
            self.progress_var.set(0)
            messagebox.showinfo("完了", f"画像圧縮が完了しました！\n出力フォルダ: {output_folder}")

        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました:\n{str(e)}")
        finally:
            self.compress_button.config(state="normal")
            self.progress_label.config(text="")

    def compress_image(self, input_path, output_path, target_size_kb):
        target_size_bytes = target_size_kb * 1024
        with Image.open(input_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            if os.path.getsize(input_path) <= target_size_bytes:
                img.save(output_path, format="JPEG", quality=95)
                return

            quality = 95
            min_quality = 5
            while quality > min_quality:
                img.save(output_path, format="JPEG", quality=quality)
                if os.path.getsize(output_path) <= target_size_bytes:
                    break
                quality -= 5

    def update_progress(self, value):
        self.progress_var.set(str(value))
        self.progress_label.config(text=f"進行状況: {int(value)}%")
        self.root.update_idletasks()

    def update_compress_button_state(self, *args):
        if self.input_folder_path.get() and self.output_folder_path.get():
            self.compress_button.config(state="normal", bg="#4CAF50")
        else:
            self.compress_button.config(state="disabled", bg="grey")

    def select_folder(self, var, title):
        folder = filedialog.askdirectory(title=title)
        if folder:
            var.set(folder)

    def validate_target_size(self, P):
        if P == "": return True
        try:
            value = int(P)
            return value > 0 and value <= 10000
        except ValueError:
            return False

    def start_compression(self):
        input_folder = self.input_folder_path.get()
        output_folder = self.output_folder_path.get()

        try:
            target_kb = int(self.target_size_entry.get())
            if target_kb <= 0 or target_kb > 10000:
                raise ValueError("サイズは1から10000KBの間で指定してください。")
        except ValueError as e:
            messagebox.showerror("エラー", str(e))
            return

        self.compress_button.config(state="disabled")
        threading.Thread(
            target=self.compress_images_to_target_size,
            args=(input_folder, output_folder, target_kb),
            daemon=True
        ).start()

    def setup_gui(self):
        self.root.title("画像圧縮ツール")
        self.root.geometry("600x450")
        self.root.configure(padx=20, pady=20)

        # スタイル設定
        style = ttk.Style()
        style.configure("Custom.TButton", padding=10)

        # 変数初期化
        self.input_folder_path = StringVar()
        self.output_folder_path = StringVar()
        self.progress_var = StringVar()

        # メインフレーム
        main_frame = Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # タイトルと説明
        Label(main_frame, text="画像圧縮ツール", font=("Arial", 20, "bold")).pack(pady=10)
        Label(main_frame, text="画像を指定したサイズに圧縮するツールです。\n"
              "PNG/JPG/JPEG形式の画像に対応しています。",
              font=("Arial", 10), justify="left").pack(pady=5)

        # フォルダ選択フレーム
        folder_frame = Frame(main_frame)
        folder_frame.pack(fill="x", pady=10)

        # インプットフォルダ
        input_frame = Frame(folder_frame)
        input_frame.pack(fill="x", pady=5)
        Button(input_frame, text="入力フォルダを選択",
               command=lambda: self.select_folder(self.input_folder_path, "入力フォルダを選択"),
               width=20).pack(side="left", padx=5)
        Label(input_frame, textvariable=self.input_folder_path,
              wraplength=400, fg="white").pack(side="left", fill="x", expand=True)

        # アウトプットフォルダ
        output_frame = Frame(folder_frame)
        output_frame.pack(fill="x", pady=5)
        Button(output_frame, text="出力フォルダを選択",
               command=lambda: self.select_folder(self.output_folder_path, "出力フォルダを選択"),
               width=20).pack(side="left", padx=5)
        Label(output_frame, textvariable=self.output_folder_path,
              wraplength=400, fg="white").pack(side="left", fill="x", expand=True)

        # サイズ入力フレーム
        size_frame = Frame(main_frame)
        size_frame.pack(pady=10)
        Label(size_frame, text="目標サイズ (KB):",
              font=("Arial", 10)).pack(side="left", padx=5)
        vcmd = (self.root.register(self.validate_target_size), '%P')
        self.target_size_entry = Entry(size_frame, width=10, justify="center",
                                     validate="key", validatecommand=vcmd)
        self.target_size_entry.insert(0, "300")
        self.target_size_entry.pack(side="left")

        # プログレスバー
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var,
                                          mode='determinate', length=400)
        self.progress_bar.pack(pady=10)
        self.progress_label = Label(main_frame, text="")
        self.progress_label.pack()

        # ボタンフレーム
        button_frame = Frame(main_frame)
        button_frame.pack(pady=20)

        # 圧縮ボタン
        self.compress_button = Button(
            button_frame,
            text="圧縮開始",
            command=self.start_compression,
            state="disabled",
            width=20,
            height=2,
            bg="grey",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.compress_button.pack(side="left", padx=10)

        # 終了ボタン
        Button(
            button_frame,
            text="終了",
            command=self.root.quit,
            width=20,
            height=2,
            font=("Arial", 10)
        ).pack(side="left", padx=10)

        # ボタン状態の監視
        self.input_folder_path.trace_add("write", self.update_compress_button_state)
        self.output_folder_path.trace_add("write", self.update_compress_button_state)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageCompressor()
    app.run()