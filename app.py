import tkinter as tk
from tkinter import ttk
from frames import Container


COLOUR_PRIMARY = "#2e3f4f"
COLOUR_SECONDARY = "#293846"
COLOUR_LIGHT_BACKGROUND = "#fff"
COLOUR_LIGHT_TEXT = "#eee"
COLOUR_DARK_TEXT = "#8095a8"


class Todo(tk.Tk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    """
    This method is responsible for creating the styles of the app,
    the basic widgets (e.g. the frames), putting them on the UI and
    initializing variables like `self.checkbutton_rows`.

    Parameters:
      *args (tuple): Variable length argument list. Arguments passed
        to the parent class `tk.Tk`.

      **kwargs (dict): Arbitrary keyword arguments. Used to pass
        additional options to the parent class `tk.Tk`.

    Returns: None
    """

    style = ttk.Style(self)
    style.theme_use('clam')

    # Custom styles.
    style.configure("Background.TFrame", background=COLOUR_PRIMARY)
    
    style.configure(
      "Title.TLabel",
      background=COLOUR_LIGHT_BACKGROUND,
      foreground=COLOUR_DARK_TEXT,
      font=("Segoe UI", 48)
    )

    style.configure(
      "LightText.TLabel",
      background=COLOUR_LIGHT_BACKGROUND,
      foreground=COLOUR_DARK_TEXT,
      padding=(0, 1)
    )

    style.configure(
      "Checkbutton.TCheckbutton",
      font=("Segoe UI", 24)
    )

    style.configure(
      "Add.TButton",
      background=COLOUR_SECONDARY,
      foreground=COLOUR_LIGHT_TEXT,
      font=("Segoe UI", 18)
    )

    style.map(
      "Add.TButton",
      background=[("active", COLOUR_PRIMARY)]
    )

    self.geometry("1400x700")
    self.title("My Todo app")

    # Store rows for dynamically added Checkbuttons.
    self.checkbutton_rows = []
    # Store variables in order to keep them from getting garbage collected.
    self.checkbutton_vars = []
    # Dictionary to store checkbuttons.
    self.checkbutton_map = {}
    # Dictionary to store the `after` deletion timers.
    self.deletion_timers = {}

    # Configure `Todo`s rows and columns.
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=3)

    # The title frame.
    self.title_frame = Container(self)
    self.title_frame.grid(row=0, column=0, sticky="NSEW", columnspan=2)

    # Configure `title_frame`s rows and columns.
    self.title_frame.columnconfigure(0, weight=1)
    self.title_frame.rowconfigure(0, weight=1)

    # The title label.
    self.title_label = ttk.Label(self.title_frame,text="My Todo List" ,font=("Segoe UI", 48), anchor="center", style="Title.TLabel")
    self.title_label.grid(row=0, column=0, sticky="NSEW")

    # The tasks frame.
    self.task_frame = Container(self)
    self.task_frame.grid(row=1, column=0, sticky="NSEW", columnspan=2)

    # Configure `task_frame`s rows and columns.
    self.task_frame.columnconfigure(0, weight=1)
    self.task_frame.columnconfigure(1, weight=2)
    self.task_frame.columnconfigure(2, weight=1)

    # Task entry, entry label and entry button.
    self.entry_label_task = ttk.Label(self.task_frame, text="Add task:", font=("Segoe UI", 24), borderwidth=2, relief="groove", style="LightText.TLabel")
    self.entry_task = ttk.Entry(self.task_frame, font=("Segoe UI", 24), width=55)
    self.entry_button = ttk.Button(self.task_frame, text="Add",style="Add.TButton" ,command=self.entry_btn_fun, cursor="hand2")

    self.entry_label_task.grid(row=0, column=0, sticky="NW", padx=(5, 0), pady=5)
    self.entry_task.grid(row=0, column=1, sticky="NEW", pady=5)
    self.entry_button.grid(row=0, column=2, sticky="NEW", padx=(28, 5), pady=5)
  

  def entry_btn_fun(self):
    """
    This method takes the text from `self.entry_task`. If it's empty,
    it returns. If it's not, it creates a new checkbutton, `new_checkbutton`
    with the text from the entry and adds it on top of the other ones, pushing
    them one row down each time. It also assigns it a lambda function, the
    method `self.on_checkbutton_toggle`.

    Parameters: None

    Returns: None
    """

    task_text = self.entry_task.get().strip()

    # Variable for the new checkbutton.
    variable = tk.BooleanVar()
    self.checkbutton_vars.append(variable)
    variable.trace_add("write", lambda *args: self.on_checkbutton_toggle(variable))

    if not task_text:
      return

    for widget, current_row in reversed(self.checkbutton_rows):
      widget.grid(row=current_row + 1, column=1, sticky="W", columnspan=3)

      self.checkbutton_rows[self.checkbutton_rows.index((widget, current_row))] = (widget, current_row + 1)

    new_checkbutton = ttk.Checkbutton(self.task_frame, text=task_text, variable=variable, style="Checkbutton.TCheckbutton")
    new_checkbutton.grid(row=1, column=1, sticky="W", columnspan=3, padx=5, pady=5)

    self.checkbutton_map[id(variable)] = new_checkbutton
    self.checkbutton_rows.insert(0, (new_checkbutton, 1))

    self.entry_task.delete(0, tk.END)


  def on_checkbutton_toggle(self, variable):
    """
    This method is responsible for checking if a checkbutton is checked. If yes
    it creates `deletion_id` which runs `after()` with 7 seconds and the
    `self.delete_checkbutton` method as parameters. If it's not checked (if it's
    no longer checked) it deletes `deletion_id` from the `self.deletion_timers`
    list.

    Parameters:
      variable (bool): It represents `variable` from `entry_btn_fun` which is a boolean
        value that is used to check if a checkbutton is checked or not.

    Returns: None
    """

    # Check if the checkbutton is checked.
    checkbutton = self.checkbutton_map.get(id(variable))

    # If checked, start the timer.
    if variable.get():
      if checkbutton:
        deletion_id = self.after(7000, lambda *args: self.delete_checkbutton(checkbutton))
        self.deletion_timers[id(variable)] = deletion_id
    else:
      deletion_id = self.deletion_timers.get(id(variable))
      if deletion_id:
        # Cancel the deletion and remove from timer dictionary.
        self.after_cancel(deletion_id)
        del self.deletion_timers[id(variable)]

  
  def delete_checkbutton(self, checkbutton):
    """
    This method removes the checkbutton from the UI and deletes it from
    `self.checkbutton_rows`.

    Parameters:
      checkbutton: This represents the `checkbutton` from `on_checkbutton_toggle`.
    
    Returns: None
    """

    # Delete the checkbutton from the UI.
    checkbutton.destroy()
    # Also delete it from `self.checkbutton_rows`.
    self.checkbutton_rows = [(w, row) for w, row in self.checkbutton_rows if w != checkbutton ]


root = Todo()
root.mainloop()