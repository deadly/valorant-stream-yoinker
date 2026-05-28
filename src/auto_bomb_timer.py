import os
import sys
import tkinter as tkr
import numpy as np

import cv2
from PIL import ImageGrab

# Chemin vers l'image du spike (PyInstaller: _MEIPASS, sinon dossier du script)
SCRIPT_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
SPIKE_IMAGE = os.path.join(SCRIPT_DIR, "img", "Spike.png")

# Couleur cible du spike : #AA0000 (R=170, G=0, B=0)
SPIKE_R, SPIKE_G, SPIKE_B = 170, 0, 0
# Tolérance pour accepter des pixels proches (compression, rendu)
COLOR_TOLERANCE = 35  # R dans [170±35], G et B dans [0, 35]

# Seuil de similarité pour la détection (0.5 = plus permissif, 0.8 = plus strict)
MATCH_THRESHOLD = 0.55


def red_mask_bgr(img_bgr):
    """Garde uniquement les pixels proches de #AA0000 (R=170, G=0, B=0) en blanc, le reste en noir (BGR)."""
    b, g, r = cv2.split(img_bgr)
    r, g, b = r.astype(np.int32), g.astype(np.int32), b.astype(np.int32)
    # Pixels proches de (170, 0, 0)
    match_r = (r >= SPIKE_R - COLOR_TOLERANCE) & (r <= SPIKE_R + COLOR_TOLERANCE)
    match_g = (g >= 0) & (g <= COLOR_TOLERANCE)
    match_b = (b >= 0) & (b <= COLOR_TOLERANCE)
    is_target = match_r & match_g & match_b
    out = np.zeros_like(r, dtype=np.uint8)
    out[is_target] = 255
    return out


_template_red_cache = None


def load_template_red():
    """Charge le template Spike.png et retourne sa version 'rouge uniquement' (cache)."""
    global _template_red_cache
    if _template_red_cache is not None:
        return _template_red_cache
    template_bgr = cv2.imread(SPIKE_IMAGE)
    if template_bgr is None:
        return None
    _template_red_cache = red_mask_bgr(template_bgr)
    return _template_red_cache


def search_spike_red():
    """Capture l'écran, ne garde que le rouge, cherche le template spike, retourne (x,y) ou (-1,-1)."""
    template_red = load_template_red()
    if template_red is None:
        return (-1, -1)
    img_rgb = np.array(ImageGrab.grab())
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    screen_red = red_mask_bgr(img_bgr)
    if template_red.shape[0] > screen_red.shape[0] or template_red.shape[1] > screen_red.shape[1]:
        return (-1, -1)
    res = cv2.matchTemplate(screen_red, template_red, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val >= MATCH_THRESHOLD:
        return (int(max_loc[0]), int(max_loc[1]))
    return (-1, -1)

def set_click_through_win():
    """Rend la fenêtre cliquable à travers : les clics passent au jeu en dessous."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)
    except Exception:
        pass


root = tkr.Tk()
root.geometry("+0+0")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0.01)
root.resizable(0, 0)

timer_display = tkr.Label(root, font=('Trebuchet MS', 30, 'bold'), bg='black')
timer_display.pack()

seconds = 44
COOLDOWN_MS = 10_000  # 10 secondes avant de pouvoir relancer le chrono après la fin

print("^|______________________________________________________________^|")
print("^|                                                              ^|")
print("^|      ======== Valorant Bomb Time Indicator ==========        ^|")
print("^|   =====This is not a hack its made for practicing =====      ^|")
print("^|           your skills so you can get better at               ^|")
print("^|            estimating the bomb on/off timings                ^|")
print("^|                                                              ^|")
print("^|      ___________________________________________________     ^|")
print("^|     This is an AI version it auto detects the bomb plant     ^|")
print("^|                                                              ^|")
print("^|______________________________________________________________^|")


def countdown(time):
    if time > 0:
        mins, secs = divmod(time, 60)

        def color_change(t_time):
            if t_time > 10:
                return 'green'
            elif 7 <= t_time <= 10:
                return 'yellow'
            elif t_time < 7:
                return 'red'

        timer_display.config(text="{:02d}:{:02d}".format(mins, secs),
                             fg=color_change(time)), root.after(1000, countdown, time - 1)
    else:
        root.wm_attributes('-alpha', 0.01)
        root.after(COOLDOWN_MS, search_image)  # attendre 10 s avant de pouvoir relancer


def start_countdown():
    root.wm_attributes('-alpha', 0.7)
    countdown(seconds)


def search_image():
    pos = search_spike_red()
    if pos[0] != -1 and pos[1] != -1:
        start_countdown()
    else:
        root.after(100, search_image)


def run_bomb_timer():
    """Lance l'overlay du chrono bombe (bloquant : mainloop tkinter)."""
    root.after(100, search_image)
    root.update_idletasks()
    set_click_through_win()
    root.mainloop()


if __name__ == "__main__":
    run_bomb_timer()
