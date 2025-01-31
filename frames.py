import tkinter as tk
from tkinter import ttk


class Container(ttk.Frame):
  def __init__(self, container, **kwargs):
    super().__init__(container, **kwargs)

    """
    I just wanted to practice using classes so instead
    of just using `ttk.Frame` I created my own class to
    do just that.

    Parameters:
      container (tk.Widget): The parent widget where this
        container will be placed. This could be a `Tk`
        instance or another container widget like a `Frame`.

      **kwargs (dict): Arbitrary keyword arguments. Used to
        pass additional options to the parent class `tk.Tk`.
      
    Returns: None
    """