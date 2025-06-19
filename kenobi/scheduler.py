#kenobi/scheduler.py

import time
import schedule
import subprocess
import sys
import logging

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_kenobi():
    logger.info("Running Kenobi pipeline.")
    subprocess.run([sys.executable,"-m", "kenobi.core.kenobi"])


#Schedule to run once every day at 9am
schedule.every().friday.at("10:33").do(run_kenobi)

if __name__ == "__main__":
    logger.info("Scheduler started.")
    while True:
        schedule.run_pending()
        next_run = schedule.next_run()
        logger.info(f"Waiting for the time to run:{str(next_run)}")
        time.sleep(300)