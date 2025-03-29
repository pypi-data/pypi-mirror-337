import imageio
import time
from PIL import ImageGrab
import argparse
import numpy as np

from threading import Timer
import sys

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    shcore = ctypes.windll.shcore

    # Define necessary constants and functions
    PROCESS_PER_MONITOR_DPI_AWARE = 2
    shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

    def get_dpi_for_window(hwnd):
        """Get the DPI scaling factor for the given window."""
        try:
            return shcore.GetDpiForWindow(hwnd)
        except Exception:
            # Fallback to 96 DPI (100% scaling) if GetDpiForWindow fails
            return 96

    def get_active_window_info():
        hwnd = user32.GetForegroundWindow()

        if not hwnd:
            return None

        # Get the DPI scaling factor for the window
        dpi = get_dpi_for_window(hwnd)
        scaling_factor = dpi / 96.0  # 96 DPI is 100% scaling

        # Get the client area dimensions
        client_rect = wintypes.RECT()
        user32.GetClientRect(hwnd, ctypes.byref(client_rect))

        # Convert client coordinates to screen coordinates
        client_point = wintypes.POINT()
        client_point.x = client_rect.left
        client_point.y = client_rect.top
        user32.ClientToScreen(hwnd, ctypes.byref(client_point))

        # Get the window dimensions and adjust for DPI scaling
        x = int(client_point.x / scaling_factor)
        y = int(client_point.y / scaling_factor)
        width = int((client_rect.right - client_rect.left) / scaling_factor)
        height = int((client_rect.bottom - client_rect.top) / scaling_factor)

        return x, y, width, height

    def screensize():
        """Returns the width and height of the screen as a two-integer tuple."""
        # Get the screen dimensions and adjust for DPI scaling
        hwnd = user32.GetDesktopWindow()
        dpi = get_dpi_for_window(hwnd)
        scaling_factor = dpi / 96.0

        width = int(user32.GetSystemMetrics(0) / scaling_factor)
        height = int(user32.GetSystemMetrics(1) / scaling_factor)

        return width, height


if sys.platform == "darwin":
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
    )
    from AppKit import NSWorkspace
    import Quartz

    def get_active_window_info():
        # Get the currently active application
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        active_pid = active_app.processIdentifier()

        # Get the list of all on-screen windows
        window_list = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly, kCGNullWindowID
        )

        # Filter windows belonging to the active application
        for window in window_list:
            if window.get("kCGWindowOwnerPID") == active_pid:
                window_title = window.get("kCGWindowName", "Unknown")
                window_bounds = window.get("kCGWindowBounds", {})
                returndict = {
                    "application": active_app.localizedName(),
                    "pid": active_pid,
                    "title": window_title,
                    "bounds": window_bounds,
                }
                return (
                    window_bounds["X"],
                    window_bounds["Y"],
                    window_bounds["Width"],
                    window_bounds["Height"],
                )

        return None

    def screensize():
        return (
            Quartz.CGDisplayPixelsWide(Quartz.CGMainDisplayID()),
            Quartz.CGDisplayPixelsHigh(Quartz.CGMainDisplayID()),
        )


def get_win_size():

    if sys.platform == "darwin":
        screen_width, screen_height = screensize()
    else:
        screen_width, screen_height = ImageGrab.grab().size

    window = get_active_window_info()
    # Get window geometry
    win_x, win_y, win_width, win_height = window

    # Calculate as a percentage of screen size
    width = round((win_width / screen_width) * 100, 2)
    height = round((win_height / screen_height) * 100, 2)
    left = round((win_x / screen_width) * 100, 2)
    top = round((win_y / screen_height) * 100, 2)
    return left, top, width, height


def get_window(args):
    print("Starting in 5 secs....")

    def wrapper():
        main_active(args)

    t = Timer(5.0, wrapper)
    t.start()


def create_parser():
    parser = argparse.ArgumentParser(
        prog="record", description="Screen Recording with python"
    )
    parser.add_argument(
        "filename",
        type=str,
        default="test.gif",
        help="filename can be mp4 or gif or mov",
    )
    parser.add_argument(
        "-i",
        "--initdelay",
        type=int,
        default=5,
        help="Initial delay in seconds, default 5 s",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0.1,
        help="Delay between frames in seconds, default 0.1 s",
    )
    parser.add_argument(
        "-dur",
        "--duration",
        type=int,
        default=20,
        help="Duration of capture, default 20s",
    )
    parser.add_argument(
        "--bbox",
        type=float,
        nargs="+",
        default=[0, 0, 50, 50],
        help="Bounding box, default (0, 0, 50, 50)",
    )
    parser.add_argument("-f", "--fullscreen", action="store_true")
    parser.add_argument("-aw", "--activewindow", action="store_true")

    return parser


def record(outfilename, initdelay=5, delay=0.1, duration=5, area=None):

    area_pix = area
    if area:
        screen_width, screen_height = ImageGrab.grab().size
        left_percent, top_percent, width_percent, height_percent = area
        # Convert percentages to pixel values
        left = int(screen_width * (left_percent / 100))
        top = int(screen_height * (top_percent / 100))
        right = int(screen_width * ((left_percent + width_percent) / 100))
        bottom = int(screen_height * ((top_percent + height_percent) / 100))
        area_pix = (left, top, right, bottom)

    img = []
    time.sleep(initdelay)
    print("Started..\a")
    t0 = time.time()
    while True:
        t1 = time.time()
        still = ImageGrab.grab()
        if area:
            still = still.crop(area_pix)
        img.append(still)
        t2 = time.time()
        time.sleep(abs(delay - (t2 - t1)))
        if t2 - t0 > duration:
            break
    print("Ended..\a\a")
    imageio.mimsave(outfilename, img, fps=2)


def main_active(args):
    active_window_info = get_win_size()
    record(
        args.filename,
        initdelay=0,
        duration=args.duration,
        delay=args.delay,
        area=active_window_info,
    )


def main():
    parser = create_parser()
    args = parser.parse_args()
    mainrun(args)


def mainrun(args):
    if args.activewindow:
        print("Please select active window")
        get_window(args)
    else:
        area = args.bbox
        if args.fullscreen:
            area = None

        record(
            args.filename,
            initdelay=args.initdelay,
            duration=args.duration,
            delay=args.delay,
            area=area,
        )


if __name__ == "__main__":
    main()
