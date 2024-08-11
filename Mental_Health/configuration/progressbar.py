from progressbar import ProgressBar, Percentage, Bar, FormatLabel

class ProgressBarManager:
    def __init__(self):
        self._progress_bar = None
        self._total_steps = 0
        self._current_step = 0
        self._title = ""

    def initialize(self, total_steps, title=""):
        if self._progress_bar is not None and self._current_step < self._total_steps:
            raise RuntimeError("Progress bar already initialized and not finished.")
        self._total_steps = total_steps
        self._title = title
        self._progress_bar = ProgressBar(widgets=[
            FormatLabel(f'{title}: '),  # Display the title
            Percentage(), ' ', Bar(), ' ', '(%s/%s)' % (total_steps, total_steps)
        ], max_value=total_steps)
        self._current_step = 0

    def update(self, step_increment):
        if self._progress_bar is None:
            raise RuntimeError("Progress bar not initialized.")
        self._current_step += step_increment
        if self._current_step > self._total_steps:
            raise ValueError(f"Current step ({self._current_step}) exceeds total steps ({self._total_steps}).")
        self._progress_bar.update(self._current_step)

    def finish(self):
        if self._progress_bar is None:
            raise RuntimeError("Progress bar not initialized.")
        self._progress_bar.finish()
        # Reset for next use
        self._progress_bar = None
        self._total_steps = 0
        self._current_step = 0
        self._title = ""


# Instantiate the progress bar singleton
