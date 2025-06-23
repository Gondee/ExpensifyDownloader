#!/usr/bin/env python3
"""
Stealth Expensify Receipt Downloader

This script uses advanced anti-detection techniques to download receipts
from Expensify without triggering automation detection.

Requirements:
pip install undetected-chromedriver pandas requests pyautogui

"""

import pandas as pd
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import random
from urllib.parse import urlparse
import re
from pathlib import Path
import json


class StealthExpensifyDownloader:
    def __init__(self, csv_file_path, download_folder="receipts", chrome_profile="Default"):
        self.csv_file_path = csv_file_path
        self.download_folder = download_folder
        self.chrome_profile = chrome_profile  # Allow specifying which profile to use
        self.driver = None
        self.session = None

        # Create download folder if it doesn't exist
        Path(self.download_folder).mkdir(exist_ok=True)

    def human_delay(self, min_delay=1, max_delay=3):
        """Add human-like random delays"""
        time.sleep(random.uniform(min_delay, max_delay))

    def human_type(self, element, text, delay_range=(0.05, 0.2)):
        """Type text with human-like delays between keystrokes"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))

    def random_mouse_movement(self):
        """Add random mouse movements to simulate human behavior"""
        try:
            action = ActionChains(self.driver)
            # Get window size
            window_size = self.driver.get_window_size()
            width, height = window_size['width'], window_size['height']

            # Random movements
            for _ in range(random.randint(1, 3)):
                x = random.randint(50, width - 50)
                y = random.randint(50, height - 50)
                action.move_by_offset(x - width // 2, y - height // 2)
                action.perform()
                time.sleep(random.uniform(0.1, 0.5))
        except:
            pass  # Ignore any errors in mouse movement

    def get_chrome_profile_path(self):
        """Find the user's Chrome profile path"""
        import platform

        system = platform.system()
        if system == "Windows":
            base_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
        elif system == "Darwin":  # macOS
            base_path = os.path.expanduser("~/Library/Application Support/Google/Chrome")
        else:  # Linux
            base_path = os.path.expanduser("~/.config/google-chrome")

        return base_path

    def copy_chrome_profile(self, source_profile="Default"):
        """Copy existing Chrome profile to automation directory"""
        import shutil

        # Get source profile path
        chrome_data_dir = self.get_chrome_profile_path()
        source_profile_path = os.path.join(chrome_data_dir, source_profile)

        # Create automation directory
        automation_profile_dir = os.path.join(os.getcwd(), "expensify_automation_profile")
        dest_profile_path = os.path.join(automation_profile_dir, source_profile)

        print(f"📂 Copying Chrome profile from: {source_profile_path}")
        print(f"📁 To automation directory: {dest_profile_path}")

        # Check if source exists
        if not os.path.exists(source_profile_path):
            print(f"❌ Source profile not found: {source_profile_path}")
            available_profiles = []
            if os.path.exists(chrome_data_dir):
                for item in os.listdir(chrome_data_dir):
                    if item.startswith('Profile') or item == 'Default':
                        if os.path.isdir(os.path.join(chrome_data_dir, item)):
                            available_profiles.append(item)

            if available_profiles:
                print("📋 Available profiles found:")
                for profile in available_profiles:
                    print(f"   - {profile}")
            raise FileNotFoundError(f"Chrome profile '{source_profile}' not found")

        # Create automation directory if it doesn't exist
        os.makedirs(automation_profile_dir, exist_ok=True)

        # Copy profile (only if it doesn't exist or is older)
        try:
            if os.path.exists(dest_profile_path):
                print("🔄 Updating existing automation profile...")
                shutil.rmtree(dest_profile_path)

            print("📋 Copying profile data (this may take a moment)...")
            shutil.copytree(source_profile_path, dest_profile_path)
            print("✅ Profile copied successfully!")

        except Exception as e:
            print(f"❌ Error copying profile: {e}")
            if "access is denied" in str(e).lower() or "permission denied" in str(e).lower():
                print("💡 Try closing your main Chrome browser and running again")
            raise

        return automation_profile_dir

    def setup_stealth_browser(self):
        """Initialize undetected Chrome browser using copied profile"""
        print("🕵️ Setting up stealth browser with your existing profile...")

        # Copy the user's existing Chrome profile to automation directory
        try:
            automation_profile_dir = self.copy_chrome_profile(self.chrome_profile)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return False
        except Exception as e:
            print(f"❌ Failed to copy profile: {e}")
            return False

        # Use undetected-chromedriver which bypasses most detection
        options = uc.ChromeOptions()

        # Add arguments to make browser look more legitimate
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")

        # Set a realistic user agent
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Use the copied profile directory
        options.add_argument(f"--user-data-dir={automation_profile_dir}")
        options.add_argument(f"--profile-directory={self.chrome_profile}")

        try:
            print("🤖 Starting automation browser with your copied profile...")
            print(f"📁 Using profile directory: {automation_profile_dir}")
            print(f"👤 Using Chrome profile: {self.chrome_profile}")
            print("✨ Your existing login session should be preserved!")

            # Initialize undetected Chrome
            self.driver = uc.Chrome(options=options, version_main=None)

            # Execute stealth scripts to hide automation
            stealth_js = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });

            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });

            window.chrome = {
                runtime: {}
            };

            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({ state: 'granted' }),
                }),
            });
            """

            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_js
            })

            print("✅ Stealth automation browser initialized with your existing profile")
            return True

        except Exception as e:
            print(f"❌ Error initializing stealth browser: {e}")
            print("Make sure you have undetected-chromedriver installed:")
            print("pip install undetected-chromedriver")
            raise
        """Initialize undetected Chrome browser with dedicated automation profile"""
        print("🕵️ Setting up stealth browser with dedicated automation profile...")

        # Use undetected-chromedriver which bypasses most detection
        options = uc.ChromeOptions()

        # Add arguments to make browser look more legitimate
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")

        # Set a realistic user agent
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Create a dedicated automation profile directory (separate from your main Chrome)
        automation_profile_dir = os.path.join(os.getcwd(), "expensify_automation_profile")
        options.add_argument(f"--user-data-dir={automation_profile_dir}")

        # Use the specified profile within our automation directory
        options.add_argument(f"--profile-directory={self.chrome_profile}")

        try:
            print("🤖 Starting automation browser (separate from your main Chrome)...")
            print(f"📁 Using automation profile directory: {automation_profile_dir}")
            print(f"👤 Using Chrome profile: {self.chrome_profile}")

            # Initialize undetected Chrome
            self.driver = uc.Chrome(options=options, version_main=None)

            # Execute stealth scripts to hide automation
            stealth_js = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });

            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });

            window.chrome = {
                runtime: {}
            };

            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({ state: 'granted' }),
                }),
            });
            """

            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_js
            })

            print("✅ Stealth automation browser initialized successfully")

        except Exception as e:
            print(f"❌ Error initializing stealth browser: {e}")
            print("Make sure you have undetected-chromedriver installed:")
            print("pip install undetected-chromedriver")
            raise

    def stealth_login_to_expensify(self):
        """Navigate to Expensify using copied profile (should already be logged in)"""
        print("🔐 Opening Expensify with your copied profile...")
        print("✨ Your existing login session should be preserved!")

        # Navigate to Expensify homepage first (more natural)
        self.driver.get("https://www.expensify.com")
        self.human_delay(2, 4)
        self.random_mouse_movement()

        # Scroll down a bit like a human would
        self.driver.execute_script("window.scrollTo(0, 300);")
        self.human_delay(1, 2)

        # Check if already logged in by trying to access dashboard
        try:
            self.driver.get("https://www.expensify.com/")
            self.human_delay(3, 5)

            # Look for signs that we're logged in
            page_source = self.driver.page_source.lower()
            if any(indicator in page_source for indicator in ['dashboard', 'expenses', 'reports', 'logout', 'profile']):
                print("🎉 Excellent! Already logged in with copied profile!")
                logged_in = True
            else:
                print("🔐 Profile copied but not logged in. Please log in...")
                logged_in = False
        except:
            logged_in = False

        if not logged_in:
            # Go to login page if not already logged in
            self.driver.get("https://www.expensify.com/signin")
            self.human_delay(2, 4)
            self.random_mouse_movement()

            print("👤 Please log in to your Expensify account in the automation browser")
            print("🎯 (This login will be saved for future runs)")

        # Always ask for manual confirmation before proceeding
        print("⏰ Ready to start downloading receipts?")
        if logged_in:
            print("   ✅ You're already logged in - just press Enter to start!")
        else:
            print("   🔐 Make sure you're logged in first, then press Enter")

        input("Press Enter to start downloading receipts: ")

        # Add a delay to let everything settle
        self.human_delay(2, 3)

        # Create a requests session using the same cookies
        self.session = requests.Session()

        # Copy all cookies from browser to session
        selenium_cookies = self.driver.get_cookies()
        for cookie in selenium_cookies:
            self.session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie.get('domain', ''),
                path=cookie.get('path', '/')
            )

        # Copy headers to look like the same browser
        user_agent = self.driver.execute_script("return navigator.userAgent;")
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        # Test the session
        try:
            test_response = self.session.get("https://www.expensify.com/", timeout=10)
            if test_response.status_code == 200:
                print("✅ Session authenticated successfully - ready to download!")
            else:
                print("⚠️ Session might not be fully authenticated, but continuing...")
        except Exception as e:
            print(f"⚠️ Could not fully test session: {e}, but continuing...")

    def load_csv_data(self):
        """Load and parse the CSV file"""
        try:
            df = pd.read_csv(self.csv_file_path)
            print(f"📊 Loaded CSV with {len(df)} rows")

            # Filter rows that have receipt links
            df_with_links = df[df['Receipt Direct Link'].notna() & (df['Receipt Direct Link'] != '')]
            print(f"🔗 Found {len(df_with_links)} rows with receipt links")

            return df_with_links
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            raise

    def generate_filename(self, row, url):
        """Generate a meaningful filename for the receipt"""
        # Extract the original filename from URL
        parsed_url = urlparse(url)
        original_filename = os.path.basename(parsed_url.path)

        # Get file extension
        _, ext = os.path.splitext(original_filename)
        if not ext:
            ext = '.jpg'  # Default to jpg if no extension

        # Create filename with merchant, date, and amount
        timestamp = row.get('Timestamp', '').replace(':', '-').replace(' ', '_')
        merchant = str(row.get('Merchant', 'Unknown')).replace('/', '-').replace('\\', '-')
        amount = str(row.get('Amount', '')).replace(',', '')

        # Clean up merchant name (remove special characters)
        merchant = re.sub(r'[^\w\s-]', '', merchant).strip()
        merchant = re.sub(r'\s+', '_', merchant)

        # Limit length to avoid filesystem issues
        merchant = merchant[:50] if len(merchant) > 50 else merchant

        # Create filename
        if timestamp and merchant and amount:
            filename = f"{timestamp}_{merchant}_{amount}{ext}"
        elif merchant and amount:
            filename = f"{merchant}_{amount}{ext}"
        elif merchant:
            filename = f"{merchant}_{original_filename}"
        else:
            filename = original_filename

        # Ensure filename is filesystem-safe
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

        return filename

    def download_receipt_with_retries(self, url, filename, max_retries=3):
        """Download a single receipt with retry logic and human-like behavior"""
        for attempt in range(max_retries):
            try:
                # Add random delay between downloads to look more human
                if attempt > 0:
                    delay = random.uniform(2, 5) * attempt  # Increasing delay on retries
                    time.sleep(delay)

                # Add some randomness to the request
                headers = self.session.headers.copy()
                headers['Cache-Control'] = 'no-cache'
                headers['Pragma'] = 'no-cache'

                response = self.session.get(url, headers=headers, timeout=30)
                response.raise_for_status()

                file_path = os.path.join(self.download_folder, filename)

                # Handle duplicate filenames
                counter = 1
                original_path = file_path
                while os.path.exists(file_path):
                    name, ext = os.path.splitext(original_path)
                    file_path = f"{name}_{counter}{ext}"
                    counter += 1

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                return True, file_path

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Attempt {attempt + 1} failed, retrying: {str(e)}")
                    continue
                else:
                    return False, str(e)

        return False, "Max retries exceeded"

    def create_enhanced_csv(self, original_df, filename_mapping):
        """Create a new CSV with original data plus downloaded filename column"""
        # Create a copy of the original dataframe
        enhanced_df = original_df.copy()

        # Add the new column for downloaded filenames
        enhanced_df['Downloaded_Receipt_Filename'] = ''

        # Fill in the filenames for rows that had receipt links
        for index, filename in filename_mapping.items():
            enhanced_df.at[index, 'Downloaded_Receipt_Filename'] = filename

        # Create the enhanced CSV filename
        original_filename = os.path.splitext(self.csv_file_path)[0]
        enhanced_csv_path = f"{original_filename}_with_filenames.csv"

        # Save the enhanced CSV
        enhanced_df.to_csv(enhanced_csv_path, index=False)

        return enhanced_csv_path

    def download_all_receipts(self):
        """Main method to download all receipts with stealth"""
        try:
            # Setup stealth browser and login
            self.setup_stealth_browser()
            self.stealth_login_to_expensify()

            # Load original CSV data (all rows, not just ones with links)
            original_df = pd.read_csv(self.csv_file_path)
            print(f"📊 Loaded original CSV with {len(original_df)} total rows")

            # Filter rows that have receipt links for downloading
            df_with_links = original_df[
                original_df['Receipt Direct Link'].notna() & (original_df['Receipt Direct Link'] != '')]
            print(f"🔗 Found {len(df_with_links)} rows with receipt links to download")

            print(f"🚀 Starting stealth download of {len(df_with_links)} receipts...")
            print("🤖 Using human-like timing to avoid detection...")

            successful_downloads = 0
            failed_downloads = 0
            filename_mapping = {}  # Track original index -> filename mapping

            for df_index, (original_index, row) in enumerate(df_with_links.iterrows()):
                url = row['Receipt Direct Link']
                filename = self.generate_filename(row, url)

                print(f"📥 [{df_index + 1}/{len(df_with_links)}] Downloading: {filename}")

                success, result = self.download_receipt_with_retries(url, filename)

                if success:
                    successful_downloads += 1
                    # Store the actual filename (in case it was modified for duplicates)
                    actual_filename = os.path.basename(result)
                    filename_mapping[original_index] = actual_filename
                    print(f"✅ Saved: {actual_filename}")
                else:
                    failed_downloads += 1
                    # Mark as failed in the mapping
                    filename_mapping[original_index] = f"FAILED: {result}"
                    print(f"❌ Failed: {result}")

                # Human-like delay between downloads (randomized)
                delay = random.uniform(0.5, 2.0)
                if df_index % 10 == 0:  # Longer break every 10 downloads
                    delay = random.uniform(3, 8)
                    print(f"😴 Taking a {delay:.1f}s break...")

                time.sleep(delay)

            # Create enhanced CSV with filename mapping
            print("\n📝 Creating enhanced CSV with filename mapping...")
            enhanced_csv_path = self.create_enhanced_csv(original_df, filename_mapping)

            print(f"\n🎉 Stealth download completed!")
            print(f"✅ Successful downloads: {successful_downloads}")
            print(f"❌ Failed downloads: {failed_downloads}")
            print(f"📁 Receipt files saved to: {os.path.abspath(self.download_folder)}")
            print(f"📊 Enhanced CSV saved as: {enhanced_csv_path}")
            print(
                f"🔗 The enhanced CSV includes a 'Downloaded_Receipt_Filename' column linking each row to its receipt file")

        except KeyboardInterrupt:
            print("\n⏹️ Download interrupted by user")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                print("🔒 Keeping browser open for 10 seconds...")
                time.sleep(10)  # Let you see the final state
                self.driver.quit()
                print("🔒 Browser closed")


def main():
    # Configuration
    CSV_FILE = "Bulk_Export_id_DIRECT_DOWNLOAD_REPORT.csv"
    DOWNLOAD_FOLDER = "expensify_receipts"

    print("🕵️ Stealth Expensify Receipt Downloader")
    print("=" * 45)
    print("🤖 Uses YOUR existing Chrome profile with login session!")
    print("✨ No need to log in again - copies your current session!")
    print()

    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"❌ CSV file not found: {CSV_FILE}")
        print("Please make sure the CSV file is in the same folder as this script")
        return

    # Help user identify their Chrome profile
    print("🔍 Finding your Chrome profiles...")

    import platform
    system = platform.system()
    if system == "Windows":
        chrome_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
    elif system == "Darwin":  # macOS
        chrome_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    else:  # Linux
        chrome_data_dir = os.path.expanduser("~/.config/google-chrome")

    available_profiles = []
    if os.path.exists(chrome_data_dir):
        for item in os.listdir(chrome_data_dir):
            if item.startswith('Profile') or item == 'Default':
                if os.path.isdir(os.path.join(chrome_data_dir, item)):
                    available_profiles.append(item)

    if available_profiles:
        print("📋 Available Chrome profiles found:")
        for i, profile in enumerate(available_profiles, 1):
            print(f"   {i}. {profile}")
        print()
        print("💡 Tips for identifying your logged-in profile:")
        print("   - 'Default' is usually your main profile")
        print("   - If you use multiple profiles, check which one has Expensify logged in")
        print("   - Open Chrome and check chrome://settings/people to see profile names")
        print()
    else:
        print("⚠️ No Chrome profiles found. Make sure Chrome is installed.")
        return

    # Ask user which profile to use
    print("🔧 Which Chrome profile has Expensify logged in?")
    profile_choice = input("Enter profile name (or press Enter for 'Default'): ").strip()
    if not profile_choice:
        profile_choice = "Default"

    if profile_choice not in available_profiles:
        print(f"❌ Profile '{profile_choice}' not found in available profiles")
        return

    print(f"👤 Using Chrome profile: {profile_choice}")
    print("📋 This will copy your profile (with login session) to automation browser")
    print()

    print("📋 How it works:")
    print("✅ 1. Copies your Chrome profile with existing Expensify login")
    print("✅ 2. Opens automation browser (separate from your main Chrome)")
    print("✅ 3. Should already be logged into Expensify!")
    print("✅ 4. You press Enter when ready to download")
    print("✅ 5. Downloads all receipts and creates enhanced CSV")
    print()

    # Initialize and run stealth downloader with specified profile
    downloader = StealthExpensifyDownloader(CSV_FILE, DOWNLOAD_FOLDER, profile_choice)
    downloader.download_all_receipts()


if __name__ == "__main__":
    main()