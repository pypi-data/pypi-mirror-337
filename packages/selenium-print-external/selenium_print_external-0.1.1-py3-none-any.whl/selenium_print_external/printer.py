
import base64
from typing import Union, Optional
# Use a more generic WebDriver type hint to support various drivers
from selenium.webdriver.remote.webdriver import WebDriver

class ExternalSeleniumPrinter:
    """
    Uses an existing Selenium WebDriver instance to print the current page to PDF.

    The user is responsible for creating, navigating, and quitting the driver.
    This class only handles the print-to-PDF action using CDP.
    """

    def __init__(self, driver: WebDriver):
        """
        Initializes the printer with an existing WebDriver instance.

        Args:
            driver: An initialized and ready Selenium WebDriver instance.
                    Must support Chrome DevTools Protocol (CDP) command 'Page.printToPDF'.
        """
        if not isinstance(driver, WebDriver):
            raise TypeError("The provided driver must be an instance of selenium.webdriver.remote.webdriver.WebDriver or its subclass.")
        if not hasattr(driver, 'execute_cdp_cmd'):
             raise AttributeError("The provided driver does not appear to support execute_cdp_cmd, which is required for printing.")

        self.driver = driver

    def _save_bytes_to_file(self, raw_bytes: bytes, file_path: str):
        """
        Saves the specified raw bytes to a file.

        Args:
            raw_bytes (bytes): The raw bytes to save.
            file_path (str): The file path to save to.
        """
        try:
            with open(file_path, "wb") as f:
                f.write(raw_bytes)
        except IOError as e:
            print(f"Error writing PDF to {file_path}: {e}")
            # Re-raise or handle more gracefully depending on desired behavior
            raise

    def print_current_page_to_pdf(
        self,
        output_path: Optional[str] = None,
        cdp_print_options: Optional[dict] = None,
    ) -> Union[bytes, None]:
        """
        Prints the current page loaded in the driver to a PDF.

        Uses the Chrome DevTools Protocol (CDP) command 'Page.printToPDF'.

        Args:
            output_path: If provided, the PDF is saved to this file path
                         and the function returns None. If None, the raw PDF
                         bytes are returned.
            cdp_print_options: Optional dictionary of options to pass directly
                               to the Page.printToPDF CDP command. Defaults include
                               `printBackground: True`. See CDP documentation for options
                               (e.g., paperWidth, paperHeight, scale, landscape etc.).

        Returns:
            bytes: The raw PDF bytes if output_path is None.
            None: If output_path is provided and saving is successful.

        Raises:
            Exception: If the CDP command fails or saving the file fails.
        """
        default_options = {"printBackground": True}
        print_options = default_options
        if cdp_print_options:
            # Merge user options, letting user override defaults
            print_options.update(cdp_print_options)

        try:
            # Execute the CDP command to get PDF data
            result = self.driver.execute_cdp_cmd("Page.printToPDF", print_options)

        except Exception as e:
            print(f"Error executing CDP Page.printToPDF command: {e}")
            # Consider specific exception handling if needed
            raise # Re-raise the exception

        # Decode the base64 PDF data
        pdf_data = base64.b64decode(result["data"])

        if not output_path:
            return pdf_data
        else:
            self._save_bytes_to_file(pdf_data, output_path)
            return None # Indicate success when saving to file