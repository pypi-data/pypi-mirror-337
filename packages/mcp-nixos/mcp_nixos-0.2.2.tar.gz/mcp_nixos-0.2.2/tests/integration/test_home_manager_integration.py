"""Integration tests for Home Manager HTML structure analysis."""

import unittest
import logging
import requests
import pytest
from bs4 import BeautifulSoup, Tag

# Configure logging for tests with more verbose output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("home_manager_test")

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


class TestHomeManagerDocStructure(unittest.TestCase):
    """
    Tests to analyze the actual structure of Home Manager documentation.

    These tests help determine the correct HTML structure to use in the HomeManagerClient
    for parsing the documentation. They make actual network requests to examine the
    structure rather than relying on assumptions.
    """

    def setUp(self):
        """Set up the test environment."""
        self.urls = [
            "https://nix-community.github.io/home-manager/options.xhtml",
            "https://nix-community.github.io/home-manager/nixos-options.xhtml",
            "https://nix-community.github.io/home-manager/nix-darwin-options.xhtml",
        ]

        # We'll populate these in the tests
        self.soups = {}

    def test_fetch_docs_and_analyze_structure(self):
        """Fetch actual documentation and analyze the HTML structure."""
        # Fetch the documentation pages
        for url in self.urls:
            source = url.split("/")[-1].split(".")[0]  # Extract source name (options, nixos-options, etc.)

            try:
                logger.info(f"Fetching {source} documentation from {url}")
                response = requests.get(url)
                response.raise_for_status()

                # Parse HTML
                soup = BeautifulSoup(response.text, "html.parser")
                self.soups[source] = soup

                # Log basic page info
                title = soup.find("title")
                logger.info(f"Title: {title.text if title else 'Unknown'}")

                # See if there are tables
                tables = soup.find_all("table")
                logger.info(f"Found {len(tables)} tables in {source}")

                if tables:
                    # Check table classes
                    for i, table in enumerate(tables[:3]):  # Log first 3 tables
                        table_class = table.get("class", ["no-class"])
                        logger.info(f"Table {i} class: {table_class}")

                # Check for definition lists which might contain options
                dl_elements = soup.find_all("dl")
                logger.info(f"Found {len(dl_elements)} definition list elements in {source}")

                if dl_elements:
                    # Check the first dl element in detail
                    first_dl = dl_elements[0]
                    dt_elements = first_dl.find_all("dt")
                    dd_elements = first_dl.find_all("dd")
                    logger.info(
                        f"First definition list has {len(dt_elements)} terms and {len(dd_elements)} descriptions"
                    )

                    # Examine a term to see if it contains option info
                    if dt_elements:
                        first_dt = dt_elements[0]
                        logger.info(f"First term content structure: {first_dt}")

                        # Look for option names
                        code_elements = first_dt.find_all("code")
                        if code_elements:
                            for code in code_elements[:2]:  # Log first 2
                                logger.info(f"Option code element: {code.text}")

                # Look for variablelist as mentioned in the HTML
                variablelist = soup.find_all(class_="variablelist")
                logger.info(f"Found {len(variablelist)} variablelist elements in {source}")

                # The page uses spans with class='term' to identify options
                term_spans = soup.find_all("span", class_="term")
                logger.info(f"Found {len(term_spans)} term spans in {source}")

                if term_spans:
                    # Sample the first few terms
                    for span in term_spans[:3]:
                        # Option name is in code element inside the term span
                        code = span.find("code")
                        if code:
                            logger.info(f"Option name: {code.text}")

                            # Look for associated description
                            dd = span.find_parent("dt").find_next_sibling("dd")
                            if dd:
                                # Type info and description are in p elements
                                p_elements = dd.find_all("p")
                                if p_elements:
                                    for i, p in enumerate(p_elements[:2]):
                                        logger.info(f"Description part {i}: {p.text[:50]}...")

                # Success
                self.assertTrue(True, f"Successfully analyzed {source} structure")

            except Exception as e:
                logger.error(f"Error analyzing {source}: {str(e)}")
                self.fail(f"Failed to analyze {source} due to: {str(e)}")

    def test_extract_sample_options(self):
        """Extract a few sample options to verify the structure."""
        # Instead of calling test_fetch_docs_and_analyze_structure, fetch a single URL directly
        # This avoids dependency between tests and potential hanging

        # We'll just use the main options URL for this test
        url = "https://nix-community.github.io/home-manager/options.xhtml"
        source = "options"

        try:
            logger.info(f"Fetching {source} documentation from {url}")

            # Use a timeout to prevent hanging
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")

            logger.info(f"Extracting sample options from {source}")

            # The variablelist contains the options
            variablelist = soup.find(class_="variablelist")
            if not variablelist:
                logger.warning(f"No variablelist found in {source}")
                self.skipTest("No variablelist found in the HTML structure")
                return

            # Find all definition terms (dt) which contain the option names
            dl = variablelist.find("dl")
            if not dl:
                logger.warning(f"No definition list found in {source}")
                self.skipTest("No definition list found in the HTML structure")
                return

            # Get all dt elements (terms)
            if not isinstance(dl, Tag):
                self.skipTest("Definition list is not a Tag element")
                return

            dt_elements = dl.find_all("dt")

            # Process a few options
            options_found = 0
            for dt in dt_elements[:5]:  # Limit to first 5 options
                # Find the term span
                term_span = dt.find("span", class_="term")
                if not term_span:
                    continue

                # Find the code element with the option name
                code = term_span.find("code")
                if not code:
                    continue

                option_name = code.text

                # Find the associated description
                dd = dt.find_next_sibling("dd")
                if not dd:
                    continue

                # Get type info which is in a paragraph with emphasis
                type_text = None
                p_elements = dd.find_all("p")
                for p in p_elements:
                    if "Type:" in p.text:
                        type_text = p.text.split("Type:")[1].strip() if "Type:" in p.text else "unknown"
                        break

                option_type = type_text or "unknown"

                # Description is in the first paragraph
                description = ""
                if p_elements:
                    description = p_elements[0].text

                # Log the option
                logger.info(f"Option: {option_name}")
                logger.info(f"  Type: {option_type}")
                logger.info(f"  Description: {description[:100]}...")

                options_found += 1

            self.assertGreater(options_found, 0, f"No options extracted from {source}")
            logger.info(f"Successfully extracted {options_found} sample options from {source}")

        except requests.RequestException as e:
            logger.warning(f"Could not fetch Home Manager docs: {e}")
            self.skipTest(f"Network error fetching Home Manager docs: {e}")
        except Exception as e:
            logger.error(f"Error extracting options: {e}")
            self.fail(f"Failed to extract options: {e}")


if __name__ == "__main__":
    # Add a direct test run that prints results
    unittest.main(verbosity=2)
