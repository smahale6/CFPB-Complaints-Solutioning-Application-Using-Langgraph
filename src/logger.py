import logging
import os

class Logger:
    _logger_initialized = False  # ✅ Class-level flag

    def __init__(self, log_dir="logs"):
        if not Logger._logger_initialized:  # ✅ Prevent duplicate initialization
            self.setup_logger(log_dir)
            Logger._logger_initialized = True  # ✅ Set flag to True

    def setup_logger(self, log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_filename = os.path.join(log_dir, f"{self.get_timestamp()}.log")
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info("Logger initialized.")

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# Example usage
# if __name__ == "__main__":
#     # Create an instance of the Logger class
#     logger_instance = Logger()
    
#     # Initialize the logger
#     logger_instance.logger()

#     # Test logging
#     #logging.info("This is an info message.")
#     #logging.warning("This is a warning message.")
#     #logging.error("This is an error message.")