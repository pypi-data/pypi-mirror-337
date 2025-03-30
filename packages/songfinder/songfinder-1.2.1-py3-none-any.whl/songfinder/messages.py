import _tkinter
import contextlib
import logging
import traceback
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox

import songfinder


def showerror(title, message, **kwargs):
    if songfinder.__unittest__ is True:
        logging.warning(message)
    else:
        logging.error(f"Error {title}: {message}")
        logging.error(f"{traceback.format_exc()}")
        with contextlib.suppress(_tkinter.TclError):
            tkMessageBox.showerror(title, message, **kwargs)


def showinfo(title, message, **kwargs):
    if songfinder.__unittest__ is True:
        logging.warning(message)
    else:
        logging.info(f"Info {title}: {message}")
        with contextlib.suppress(_tkinter.TclError):
            tkMessageBox.showinfo(title, message, **kwargs)


def askyesno(title, message):
    if songfinder.__unittest__ is True:
        logging.warning(message)
        return False
    else:
        try:
            return tkMessageBox.askyesno(title, message)
        except _tkinter.TclError:
            print(f"Askyesno {title}: {message}")  # noqa: T201
            answer = None
            while answer not in ["y", "Y", "n", "N"]:
                answer = input(f"{message} (y/n)")
                if answer in ["y", "Y"]:
                    return True
                elif answer in ["n", "N"]:
                    return False


def askdirectory(**kwargs):
    if songfinder.__unittest__ is True:
        logging.warning("askdirectory")
        return None
    else:
        try:
            return tkFileDialog.askdirectory(**kwargs)
        except _tkinter.TclError:
            return None


def askopenfilename(**kwargs):
    if songfinder.__unittest__ is True:
        logging.warning("askopenfilename")
        return None
    else:
        try:
            return tkFileDialog.askopenfilename(**kwargs)
        except _tkinter.TclError:
            return None


def askopenfilenames(**kwargs):
    if songfinder.__unittest__ is True:
        logging.warning("askopenfilenames")
        return None
    else:
        try:
            return tkFileDialog.askopenfilenames(**kwargs)
        except _tkinter.TclError:
            return None


def asksaveasfilename(**kwargs):
    if songfinder.__unittest__ is True:
        logging.warning("asksaveasfilename")
        return None
    else:
        try:
            return tkFileDialog.asksaveasfilename(**kwargs)
        except _tkinter.TclError:
            return None
