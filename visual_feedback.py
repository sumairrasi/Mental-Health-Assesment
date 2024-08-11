# import sys
# import time

# def print_progress(iteration, total, bar_length=50):
#     progress = (iteration / total)
#     arrow = '=' * int(round(progress * bar_length) - 1)
#     spaces = ' ' * (bar_length - len(arrow))
#     sys.stdout.write(f'\r[{arrow}{spaces}] {int(progress * 100)}%')
#     sys.stdout.flush()

# def process_data(total_steps):
#     for i in range(total_steps):
#         time.sleep(0.1)  # Simulate processing time
#         print_progress(i + 1, total_steps)
#     print("\nData processing complete.")
    

# process_data(5)


# import curses
# import time

# def display_progress(stdscr, total_steps):
#     curses.curs_set(0)
#     stdscr.nodelay(1)
#     stdscr.clear()
#     for i in range(total_steps):
#         percent_complete = int((i + 1) / total_steps * 100)
#         stdscr.addstr(0, 0, f"Processing: {percent_complete}%")
#         stdscr.refresh()
#         time.sleep(0.1)  # Simulate processing time
#     stdscr.addstr(1, 0, "Data processing complete.")
#     stdscr.refresh()
#     stdscr.getch()

# if __name__ == "__main__":
#     curses.wrapper(display_progress, 100)

import time
from progressbar import ProgressBar

def process_data(total_steps):
    with ProgressBar(max_value=total_steps) as pbar:
        for i in range(total_steps):
            time.sleep(0.1)  # Simulate processing time
            pbar.update(i + 1)
    print("Data processing complete.")

process_data(5)

process_data(10)

process_data(15)