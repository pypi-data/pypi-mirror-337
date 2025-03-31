import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

def load_tk_image(path: Path, max_width: int, max_height: int) -> ImageTk.PhotoImage:
    """
    Loads and resizes the image from the path and converts it into a `ImageTk.PhotoImage`.
    Aspect ratio of the resized image is same as that of the original.

    Args:
        path (Path): Path of the image
        max_width (int): Max width of the resized image
        max_height (int): Max height of the resized image

    Returns:
        PhotoImage: A `ImageTk.PhotoImage` instance of the resized image
    """

    img = Image.open(path)
    w, h = img.size

    if (w / h) >= (max_width / max_height):
        img = img.resize((max_width, int(h * (max_width / w))))
    else:
        img = img.resize((int(w * (max_height / h)), max_height))
    
    return ImageTk.PhotoImage(img)

class ImageLabeller():
    def __init__(
        self,
        image_paths: list[str | Path],
        labels: list[str],
        *,
        canvas_width: int = 960,
        img_max_height: int = 540
    ) -> None:
        self.image_paths: list[Path] = [Path(img_path).resolve() for img_path in image_paths]
        self.labels = labels

        self.img_labels: dict[str, None | int] = {
            str(p): None for p in self.image_paths
        }
        """
        A dictionary mapping the `self.image_paths` to their label indices in `self.labels`.
        The label index is `None` if the image is unlabelled.
        """

        self.canvas_width = canvas_width
        self.img_max_height = img_max_height
        self._curr_img_index = 0

    @property
    def _curr_img_path(self):
        return self.image_paths[self._curr_img_index]
    
    def run(self, *, start_index: int = None):
        """
        Loads and resizes the image from the path and converts it into a `ImageTk.PhotoImage`.
        Aspect ratio of the resized image is same as that of the original.

        Args:
            start_index (int, optional):
                Index of the image to start the labelling from. Defaults to `None`. 
                If `None`, the labelling restarts from the same image it exited at.
                If starting the labelling for the first time, it starts from the first image.
        """

        if start_index is not None:
            self._curr_img_index = max(int(start_index), 0) % len(self.image_paths)

        window = tk.Tk()
        window.resizable(False, False)

        img_canvas = tk.Canvas(window, width = self.canvas_width, height = self.img_max_height)
        img_canvas.pack()

        detail_canvas = tk.Canvas(window, width = self.canvas_width, height = 30)
        detail_canvas.pack(pady = 5)

        new_label_canvas = tk.Canvas(window, width = self.canvas_width // 3, height = 30, highlightthickness = 0)
        new_label_canvas.pack(pady = 10)

        label_canvas = tk.Canvas(window, width = self.canvas_width, height = 100, highlightthickness = 0)
        label_canvas.pack(pady = 10)

        btn_canvas = tk.Canvas(window, width = self.canvas_width, height = 50)
        btn_canvas.pack(pady = 10)

        current_label = tk.IntVar()
        current_label.set(None)

        img = load_tk_image(self._curr_img_path, self.canvas_width, self.img_max_height)

        img_container = img_canvas.create_image(
            self.canvas_width // 2,
            self.img_max_height // 2,
            anchor = tk.CENTER,
            image = img
        )

        img_title = detail_canvas.create_text(
            self.canvas_width // 2,
            15,
            text = f"{self._curr_img_path.stem} ({img.width()} x {img.height()})",
            fill = "black",
            font = "Helvetica 14 bold",
            anchor = tk.CENTER
        )

        def update_label():
            nonlocal img
            try:
                self.img_labels[str(self._curr_img_path)] = current_label.get()
            except tk.TclError:
                self.img_labels[str(self._curr_img_path)] = None

            self._curr_img_index = (self._curr_img_index + 1) % len(self.image_paths)
            current_label.set(self.img_labels[str(self._curr_img_path)])
            img = load_tk_image(
                self._curr_img_path,
                self.canvas_width,
                self.img_max_height
            )
            img_canvas.itemconfig(img_container, image = img)
            detail_canvas.itemconfig(
                img_title,
                text = f"{self._curr_img_path.stem} ({img.width()} x {img.height()})"
            )
        
        def clear_label():
            current_label.set(None)
        
        def remove_label(i: int):
            for k, v in self.img_labels.items():
                if v is not None:
                    if v == i:
                        self.img_labels[k] = None
                    elif v > i:
                        self.img_labels[k] -= 1
            
            self.labels.pop(i)

            for child in label_canvas.winfo_children():
                child.destroy()
            
            setup_all_labels()
            
            current_label.set(self.img_labels[str(self._curr_img_path)])

        def setup_label(i: int, label: str):
            label_btn_canvas = tk.Canvas(label_canvas, width = self.canvas_width // 3, height = 30)
            label_btn_canvas.grid(
                row = (i // 3) + 1,
                column = i % 3,
                padx = 10,
                pady = 10
            )

            tk.Radiobutton(
                label_btn_canvas,
                text = label,
                indicatoron = 0,
                padx = 5,
                pady = 5,
                variable = current_label,
                value = i,
                overrelief = "raised",
                offrelief = "groove",
                font = "Helvetica 11"
            ).place(x = 0, relwidth = 0.9)

            tk.Button(
                label_btn_canvas,
                text = "X",
                font = "Helvetica 12 bold",
                padx = 5,
                pady = 5,
                command = lambda: remove_label(i)
            ).place(relx = 0.9, relwidth = 0.1)
        
        def setup_all_labels():
            for i, label in enumerate(self.labels):
                setup_label(i, label)
            window.title(f"Image Labeller - {len(self.image_paths)} images, {len(self.labels)} labels")

        setup_all_labels()

        new_label = tk.StringVar()
        new_label.set("New Label")

        def add_label(e):
            label_text = new_label.get().strip()

            if len(label_text) > 0:
                self.labels.append(label_text)
                new_label.set("")
                setup_label(len(self.labels) - 1, label_text)
                window.title(f"Image Labeller - {len(self.image_paths)} images, {len(self.labels)} labels")
        
        new_label_entry = tk.Entry(
            new_label_canvas,
            textvariable = new_label,
            font = "Helvetica 11",
            justify = "center"
        )
        new_label_entry.place(x = 0, relwidth = 1, relheight = 0.9)
        new_label_entry.bind("<Return>", add_label)

        clear_btn = tk.Button(
            btn_canvas,
            text = "Clear",
            font = "Helvetica 12 bold",
            width = 20,
            padx = 10,
            pady = 5,
            command = clear_label
        )
        clear_btn.grid(row = 0, column = 0, padx = 20)
        
        save_btn = tk.Button(
            btn_canvas,
            text = "Save",
            font = "Helvetica 12 bold",
            width = 20,
            padx = 10,
            pady = 5,
            command = update_label
        )
        save_btn.grid(row = 0, column = 1, padx = 20)

        window.mainloop()