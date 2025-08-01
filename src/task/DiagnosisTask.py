import time

from ok import Logger
from src.task.BaseCombatTask import BaseCombatTask
from src.task.WWOneTimeTask import WWOneTimeTask

logger = Logger.get_logger(__name__)


class DiagnosisTask(WWOneTimeTask, BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "Diagnosis Problem, Performance Test, Run in Game World"
        self.name = "Diagnosis"
        self.start = 0

    def run(self):
        super().run()
        if not self.in_team()[0]:
            self.log_error('must be in game world and in teams, please check you game resolution is 16:9', notify=True)
            return
        self.load_hotkey(force=True)

        self.start = time.time()
        while True:
            self.load_chars()
            char = self.get_current_char()
            if not char:
                self.info.clear()
                self.info['Current Character'] = "None"
                self.start = time.time()
            else:
                self.info['Capture Frame Count'] = self.info.get('Capture Frame Count', 0) + 1
                self.info['Capture Frame Rate'] = round(
                    self.info['Capture Frame Count'] / ((time.time() - self.start) or 1),
                    2)
                self.info['Game Resolution'] = f'{self.frame.shape[1]}x{self.frame.shape[0]}'
                self.info['Current Character'] = str(char)
                self.info['Resonance CD'] = self.get_cd('resonance')
                self.info['Echo CD'] = self.get_cd('echo')
                self.info['Liberation CD'] = self.get_cd('liberation')
                self.info['Concerto'] = char.get_current_con()
                self.next_frame()

    def choose_level(self, start):
        y = 0.17
        x = 0.15
        distance = 0.08

        logger.info(f'choose level {start}')
        self.click_relative(x, y + (start - 1) * distance)
        self.sleep(0.5)

        self.wait_click_feature('gray_button_challenge', raise_if_not_found=True,
                                click_after_delay=0.5)
        self.wait_click_feature('gray_confirm_exit_button', relative_x=-1, raise_if_not_found=False,
                                time_out=3, click_after_delay=0.5, threshold=0.8)
        self.wait_click_feature('gray_start_battle', relative_x=-1, raise_if_not_found=True,
                                click_after_delay=0.5, threshold=0.8)
