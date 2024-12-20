import psutil
import curses
import time
import math

# Initialize curses
stdscr = curses.initscr()
curses.curs_set(0)
stdscr.nodelay(1)
stdscr.timeout(100)

# Function to draw radar-like animation
def draw_radar(stdscr):
    height, width = stdscr.getmaxyx()
    center_y = height // 2
    center_x = width // 2
    radius = min(center_y, center_x) - 2
    angle_increment = 360 / 12  # 12 segments to simulate radar sweep

    while True:
        stdscr.clear()

        # Get network I/O stats
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_recv = net_io.bytes_recv

        # Calculate traffic intensity (for radar blip strength)
        total_traffic = (bytes_sent + bytes_recv) / 1e6  # in MB
        intensity = min(1.0, total_traffic / 10)  # Normalize to radar intensity

        # Draw the radar circle
        stdscr.addstr(center_y, center_x, "o", curses.color_pair(1))

        # Simulate radar sweep (clockwise)
        for angle in range(0, 360, int(angle_increment)):
            radian = math.radians(angle)
            offset_x = int(radius * math.cos(radian))
            offset_y = int(radius * math.sin(radian))

            # Adjust blip size based on traffic intensity
            blip_size = int(radius * intensity)
            if blip_size > 0:
                stdscr.addstr(center_y + offset_y, center_x + offset_x, ".", curses.color_pair(2))

        # Display network traffic info
        stdscr.addstr(1, 1, f"Sent: {bytes_sent / 1e6:.2f} MB  Recv: {bytes_recv / 1e6:.2f} MB", curses.color_pair(3))

        # Refresh the screen and wait
        stdscr.refresh()
        time.sleep(1)

# Setup color pairs
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Radar circle
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Radar blip
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Traffic info

try:
    draw_radar(stdscr)
finally:
    curses.endwin()
