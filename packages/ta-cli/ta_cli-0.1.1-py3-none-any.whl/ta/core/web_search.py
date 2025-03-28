from playwright.sync_api import sync_playwright, TimeoutError
from typing import List


class WebSearch:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        # Set default timeout to 30 seconds
        self.page.set_default_timeout(30000)

    def search(self, query: str, max_results: int = 5) -> List[str]:
        """
        Perform a web search and return the results as formatted strings
        """
        try:
            # Navigate to Bing with a longer timeout for initial load
            self.page.goto(
                f"https://www.bing.com/search?q={query}", timeout=60000)

            # Wait for results to load with a longer timeout
            try:
                self.page.wait_for_selector("li.b_algo", timeout=60000)
            except TimeoutError:
                print("Timeout waiting for search results to load")
                return []

            # Extract search results
            results = []
            elements = self.page.query_selector_all("li.b_algo")

            for index, element in enumerate(elements[:max_results]):
                try:
                    title_el = element.query_selector("h2 a")
                    desc_el = element.query_selector(".b_caption p")
                    favicon_el = element.query_selector(".wr_fav img")

                    if title_el:
                        title = title_el.inner_text()
                        url = title_el.get_attribute("href")
                        desc = desc_el.inner_text() if desc_el else ""
                        icon = favicon_el.get_attribute(
                            "src") if favicon_el else ""

                        # Format the result as a string
                        result = (
                            f"Title: {title}\n"
                            f"URL: {url}\n"
                            f"Rank: {index + 1}\n"
                            f"Description: {desc}\n"
                            f"Icon: {icon}\n"
                            f"---\n"
                        )
                        results.append(result)
                except Exception as e:
                    print(f"Error processing element: {e}")
                    continue

            return results

        except TimeoutError as e:
            print(f"Timeout during web search: {e}")
            return []
        except Exception as e:
            print(f"Error during web search: {e}")
            return []

        finally:
            self.cleanup()

    def cleanup(self):
        """
        Clean up resources
        """
        try:
            self.context.close()
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            print(f"Error during cleanup: {e}")
