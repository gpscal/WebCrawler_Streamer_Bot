#!/usr/bin/env python3
"""
Human-like behavior module for Selenium automation.
Includes realistic scrolling, mouse movements, clicking, and page navigation.
"""

from __future__ import annotations

import random
import time
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.action_chains import ActionChains


class HumanBehavior:
    """Simulates human-like interactions with web pages."""
    
    # Common patterns for "Next Page" buttons/links
    NEXT_PAGE_PATTERNS = [
        # Text-based patterns
        "next",
        "next page",
        "siguiente",  # Spanish
        "suivant",    # French
        "weiter",     # German
        "próxima",    # Portuguese
        "次へ",       # Japanese
        "下一页",     # Chinese
        ">",
        "»",
        "→",
        # Aria labels
        "[aria-label*='next' i]",
        "[aria-label*='siguiente' i]",
        # Common class patterns
        ".next",
        ".pagination-next",
        ".page-next",
        # Common rel attributes
        "[rel='next']",
        # Button patterns
        "button:contains('Next')",
    ]
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.actions = ActionChains(driver)
    
    def random_delay(self, min_seconds: float = 0.5, max_seconds: float = 2.0):
        """Add a random delay to simulate human thinking time."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def smooth_scroll_to_position(self, target_y: int, duration: float = 1.0):
        """Smoothly scroll to a specific Y position."""
        current_y = self.driver.execute_script("return window.pageYOffset;")
        distance = target_y - current_y
        steps = max(10, int(duration * 20))  # 20 steps per second
        
        for step in range(steps):
            progress = (step + 1) / steps
            # Ease-in-out function for smooth acceleration/deceleration
            eased_progress = progress * progress * (3 - 2 * progress)
            new_y = current_y + (distance * eased_progress)
            
            self.driver.execute_script(f"window.scrollTo(0, {new_y});")
            time.sleep(duration / steps)
            
            # Add small random variations
            if random.random() < 0.1:
                time.sleep(random.uniform(0.05, 0.2))
    
    def scroll_down_slowly(
        self,
        scroll_pause_time: float = 1.5,
        num_scrolls: Optional[int] = None,
        scroll_percentage: float = 0.3,
    ):
        """
        Scroll down the page slowly like a human reading.
        
        Args:
            scroll_pause_time: Time to pause between scrolls (randomized)
            num_scrolls: Number of scrolls to perform (None = scroll to bottom)
            scroll_percentage: Percentage of viewport to scroll each time
        """
        viewport_height = self.driver.execute_script("return window.innerHeight;")
        scroll_distance = int(viewport_height * scroll_percentage)
        
        scrolls_performed = 0
        
        while True:
            # Get current scroll position
            current_position = self.driver.execute_script("return window.pageYOffset;")
            page_height = self.driver.execute_script("return document.body.scrollHeight;")
            
            # Check if we've reached the bottom or completed requested scrolls
            if num_scrolls and scrolls_performed >= num_scrolls:
                break
            
            if current_position + viewport_height >= page_height - 100:
                # Reached bottom
                break
            
            # Calculate target position with some randomness
            target_position = current_position + scroll_distance + random.randint(-50, 50)
            
            # Smooth scroll
            self.smooth_scroll_to_position(target_position, duration=random.uniform(0.8, 1.5))
            
            # Random pause like a human reading
            pause = scroll_pause_time + random.uniform(-0.5, 1.0)
            time.sleep(max(0.5, pause))
            
            # Occasionally scroll back up a bit (like re-reading something)
            if random.random() < 0.1:
                scroll_back = random.randint(50, 150)
                self.driver.execute_script(f"window.scrollBy(0, -{scroll_back});")
                time.sleep(random.uniform(0.3, 0.8))
            
            scrolls_performed += 1
    
    def scroll_to_element(self, element, offset: int = 100):
        """Scroll smoothly to bring an element into view."""
        element_y = self.driver.execute_script("return arguments[0].getBoundingClientRect().top + window.pageYOffset;", element)
        target_y = element_y - offset
        self.smooth_scroll_to_position(max(0, target_y), duration=1.2)
    
    def move_to_element_human_like(self, element):
        """Move mouse to element with human-like curve and speed."""
        # Get element location
        location = element.location
        size = element.size
        
        # Random point within the element
        target_x = location['x'] + random.randint(int(size['width'] * 0.3), int(size['width'] * 0.7))
        target_y = location['y'] + random.randint(int(size['height'] * 0.3), int(size['height'] * 0.7))
        
        # Move with slight randomness
        self.actions.move_to_element_with_offset(element, 
                                                  random.randint(-5, 5), 
                                                  random.randint(-5, 5))
        self.actions.pause(random.uniform(0.1, 0.3))
        self.actions.perform()
    
    def human_click(self, element):
        """Click an element with human-like behavior."""
        try:
            # Scroll element into view
            self.scroll_to_element(element)
            self.random_delay(0.3, 0.8)
            
            # Move to element
            self.move_to_element_human_like(element)
            self.random_delay(0.2, 0.5)
            
            # Click
            element.click()
            
        except ElementClickInterceptedException:
            # If click is intercepted, try JavaScript click
            self.driver.execute_script("arguments[0].click();", element)
    
    def find_next_page_button(self, timeout: int = 10) -> Optional[webdriver.remote.webelement.WebElement]:
        """
        Find the "Next Page" button/link using various strategies.
        
        Returns:
            The next page element if found, None otherwise.
        """
        strategies = [
            # Strategy 1: Look for links/buttons with "next" text
            lambda: self._find_by_text_contains(["next", "next page", ">", "»", "→"]),
            
            # Strategy 2: Look for common pagination classes
            lambda: self._find_by_selectors([
                "a.next",
                "a.pagination-next",
                "button.next",
                "a[rel='next']",
                "li.next a",
                ".pagination .next",
                "[aria-label*='next' i]",
            ]),
            
            # Strategy 3: Look in pagination containers
            lambda: self._find_next_in_pagination(),
            
            # Strategy 4: Look for arrows or icons
            lambda: self._find_by_aria_label(["next", "siguiente", "suivant", "weiter"]),
        ]
        
        for strategy in strategies:
            try:
                element = strategy()
                if element and element.is_displayed() and element.is_enabled():
                    return element
            except (NoSuchElementException, StaleElementReferenceException):
                continue
        
        return None
    
    def _find_by_text_contains(self, texts: List[str]) -> Optional[webdriver.remote.webelement.WebElement]:
        """Find element by text content."""
        for text in texts:
            try:
                # Try links first
                xpath = f"//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
                element = self.driver.find_element(By.XPATH, xpath)
                if element.is_displayed():
                    return element
            except NoSuchElementException:
                pass
            
            try:
                # Try buttons
                xpath = f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
                element = self.driver.find_element(By.XPATH, xpath)
                if element.is_displayed():
                    return element
            except NoSuchElementException:
                pass
        
        return None
    
    def _find_by_selectors(self, selectors: List[str]) -> Optional[webdriver.remote.webelement.WebElement]:
        """Find element by CSS selectors."""
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    return element
            except NoSuchElementException:
                continue
        return None
    
    def _find_next_in_pagination(self) -> Optional[webdriver.remote.webelement.WebElement]:
        """Find next button within pagination containers."""
        pagination_selectors = [
            ".pagination",
            ".pager",
            ".page-navigation",
            "[role='navigation']",
            "nav",
        ]
        
        for selector in pagination_selectors:
            try:
                container = self.driver.find_element(By.CSS_SELECTOR, selector)
                # Look for next within this container
                for text in ["next", ">", "»"]:
                    try:
                        xpath = f".//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]"
                        element = container.find_element(By.XPATH, xpath)
                        if element.is_displayed():
                            return element
                    except NoSuchElementException:
                        continue
            except NoSuchElementException:
                continue
        
        return None
    
    def _find_by_aria_label(self, labels: List[str]) -> Optional[webdriver.remote.webelement.WebElement]:
        """Find element by aria-label attribute."""
        for label in labels:
            try:
                element = self.driver.find_element(
                    By.XPATH, 
                    f"//*[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{label.lower()}')]"
                )
                if element.is_displayed():
                    return element
            except NoSuchElementException:
                continue
        return None
    
    def navigate_and_scroll(
        self,
        url: str,
        scroll_count: Optional[int] = None,
        find_next: bool = True,
    ) -> dict:
        """
        Navigate to URL, scroll like a human, and optionally click next page.
        
        Args:
            url: URL to navigate to
            scroll_count: Number of scrolls (None = scroll to bottom)
            find_next: Whether to try finding and clicking next page button
        
        Returns:
            Dictionary with navigation results
        """
        result = {
            "url": url,
            "success": False,
            "scrolled": False,
            "next_page_found": False,
            "next_page_clicked": False,
            "error": None,
        }
        
        try:
            # Navigate to URL
            self.driver.get(url)
            self.random_delay(1.0, 2.5)  # Wait for page load
            
            result["success"] = True
            
            # Scroll down slowly
            self.scroll_down_slowly(
                scroll_pause_time=1.5,
                num_scrolls=scroll_count,
                scroll_percentage=0.3,
            )
            result["scrolled"] = True
            
            # Try to find and click next page button
            if find_next:
                self.random_delay(0.5, 1.5)
                next_button = self.find_next_page_button()
                
                if next_button:
                    result["next_page_found"] = True
                    
                    try:
                        self.human_click(next_button)
                        result["next_page_clicked"] = True
                        result["next_url"] = self.driver.current_url
                        
                        # Wait for new page to load
                        self.random_delay(1.5, 2.5)
                        
                    except Exception as e:
                        result["error"] = f"Failed to click next button: {str(e)}"
                
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
        
        return result
