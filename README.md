# Expensify Receipt Downloader

**Automated tool to download all receipt images from Expensify exports with advanced anti-detection capabilities.**

## 🎯 Overview

This Python script automates the process of downloading receipt images from Expensify using your CSV export file. It uses advanced stealth techniques to avoid detection and creates an enhanced CSV that maps each expense to its downloaded receipt file.

### Key Features

- 🕵️ **Stealth Mode**: Uses undetected Chrome driver to bypass automation detection
- 🔐 **Profile Copying**: Copies your existing Chrome profile with saved login sessions
- 📊 **Enhanced CSV**: Creates mapping file linking expenses to receipt filenames
- 🤖 **Human-like Behavior**: Random delays, mouse movements, and natural browsing patterns
- ⏰ **Manual Control**: You control when the download process begins
- 📁 **Smart Naming**: Receipt files named with date, merchant, and amount

## 📋 Prerequisites

### Required Software
- **Python 3.7+**
- **Google Chrome** (any recent version)
- **Chrome Profile** with Expensify already logged in

### Required Python Packages
```bash
pip install undetected-chromedriver pandas requests
```

## 🚀 Installation

1. **Clone or download** the script to your local machine
2. **Install dependencies**:
   ```bash
   pip install undetected-chromedriver pandas requests
   ```
3. **Export your Expensify data** as CSV (must include Receipt Direct Link column)
4. **Ensure you're logged into Expensify** in your regular Chrome browser

## 📖 How to Use

### Step 1: Prepare Your Data

1. **Log into Expensify** in your regular Chrome browser
2. **Export your expense report** as CSV
3. **Save the CSV file** in the same folder as the Python script
4. **Rename the CSV** to `Bulk_Export_id_DIRECT_DOWNLOAD_REPORT.csv` (or update the script)

### Step 2: Run the Script

```bash
python expensify_downloader.py
```

### Step 3: Follow the Interactive Setup

1. **Profile Detection**: Script shows available Chrome profiles
   ```
   📋 Available Chrome profiles found:
      1. Default
      2. Profile 1
      3. Profile 2
   ```

2. **Choose Profile**: Select the profile where Expensify is logged in
   ```
   Enter profile name (or press Enter for 'Default'): Default
   ```

3. **Profile Copying**: Script copies your profile to automation directory
   ```
   📂 Copying Chrome profile from: /Users/yourname/Library/Application Support/Google/Chrome/Default
   📁 To automation directory: ./expensify_automation_profile/Default
   ✅ Profile copied successfully!
   ```

4. **Browser Opens**: Automation browser opens with your copied profile
   - Should already be logged into Expensify
   - If not, log in manually (will be saved for future runs)

5. **Manual Confirmation**: Press Enter when ready to start downloading
   ```
   ⏰ Ready to start downloading receipts?
      ✅ You're already logged in - just press Enter to start!
   Press Enter to start downloading receipts:
   ```

6. **Download Process**: Script downloads all receipts with progress updates
   ```
   📥 [1/397] Downloading: 2025-06-20_08-07-13_The_Home_Depot_13.34.jpg
   ✅ Saved: 2025-06-20_08-07-13_The_Home_Depot_13.34.jpg
   📥 [2/397] Downloading: 2025-06-12_03-45-52_Notion_Labs_Inc_2274.60.jpg
   ✅ Saved: 2025-06-12_03-45-52_Notion_Labs_Inc_2274.60.jpg
   ```

### Step 4: Results

After completion, you'll have:

1. **Downloaded Receipts**: `./expensify_receipts/` folder with all receipt images
2. **Enhanced CSV**: `Bulk_Export_id_DIRECT_DOWNLOAD_REPORT_with_filenames.csv` with filename mapping

## 📁 File Structure

```
your-project/
├── expensify_downloader.py                                    # Main script
├── Bulk_Export_id_DIRECT_DOWNLOAD_REPORT.csv                 # Your Expensify export
├── Bulk_Export_id_DIRECT_DOWNLOAD_REPORT_with_filenames.csv   # Enhanced CSV (generated)
├── expensify_receipts/                                        # Downloaded receipts (generated)
│   ├── 2025-06-20_08-07-13_The_Home_Depot_13.34.jpg
│   ├── 2025-06-12_03-45-52_Notion_Labs_Inc_2274.60.jpg
│   └── ...
└── expensify_automation_profile/                             # Copied Chrome profile (generated)
    └── Default/
        ├── Cookies
        ├── Preferences
        └── ...
```

## 📊 Enhanced CSV Output

The script creates an enhanced version of your original CSV with an additional column:

| Original Columns | New Column |
|-----------------|------------|
| Timestamp, Merchant, Amount, MCC, Category, Description, Original Amount, Receipt Direct Link, Report ID | **Downloaded_Receipt_Filename** |

### Example Enhanced CSV:
```csv
Timestamp,Merchant,Amount,Receipt Direct Link,Downloaded_Receipt_Filename
2025-06-20 08:07:13,The Home Depot,13.34,https://www.expensify.com/receipts/w_abc123.jpg,2025-06-20_08-07-13_The_Home_Depot_13.34.jpg
2025-06-12 03:45:52,Notion Labs Inc.,2274.60,,
2025-06-08 09:11:23,Slack,236.15,https://www.expensify.com/receipts/w_def456.jpg,2025-06-08_09-11-23_Slack_236.15.jpg
```

## 🔧 Configuration Options

### Custom File Paths
Edit these variables in `main()` function:
```python
CSV_FILE = "your_custom_filename.csv"
DOWNLOAD_FOLDER = "custom_receipts_folder"
```

### Chrome Profile Selection
- **Default**: Standard Chrome profile
- **Profile 1, 2, 3...**: Additional Chrome profiles
- **Custom**: Any profile name found in Chrome's user data directory

## 🛠️ Troubleshooting

### Common Issues

#### "Chrome profile not found"
**Solution**: Make sure Chrome is installed and you've used it at least once
```bash
# Check available profiles manually
# Windows: %LOCALAPPDATA%\Google\Chrome\User Data
# Mac: ~/Library/Application Support/Google/Chrome  
# Linux: ~/.config/google-chrome
```

#### "Access denied" when copying profile
**Solution**: Close your main Chrome browser completely before running the script

#### "Not logged into Expensify" 
**Solution**: 
1. Manually log into Expensify in the automation browser
2. The login will be saved for future runs
3. Or choose a different Chrome profile that has Expensify logged in

#### Downloads failing
**Solution**:
1. Check your internet connection
2. Verify you're properly logged into Expensify
3. Some receipts may have expired links (marked as FAILED in CSV)

#### "undetected-chromedriver" not found
**Solution**:
```bash
pip install --upgrade undetected-chromedriver
```

### Advanced Troubleshooting

#### Enable Debug Mode
Add these lines after `self.driver = uc.Chrome(...)`:
```python
self.driver.set_window_size(1200, 800)
print("Debug: Browser opened, check for issues manually")
input("Press Enter to continue...")
```

#### Manual Profile Path
If automatic detection fails, manually specify profile path:
```python
# In copy_chrome_profile method, replace auto-detection with:
chrome_data_dir = "/your/custom/path/to/Chrome/User Data"
```

## 🔒 Security & Privacy

### Data Handling
- **No data is uploaded** or sent anywhere
- **All processing is local** on your machine
- **Copied profiles are isolated** from your main browsing
- **Login sessions are preserved** but contained within automation environment

### Best Practices
1. **Run on trusted networks** only
2. **Keep the script updated** for latest security patches
3. **Don't share** the automation profile folder (contains login data)
4. **Review** downloaded files before sharing

## 🚀 Advanced Features

### Batch Processing Multiple Accounts
```python
# Modify main() to loop through multiple profiles
profiles = ["Default", "Profile 1", "Profile 2"]
for profile in profiles:
    downloader = StealthExpensifyDownloader(CSV_FILE, f"receipts_{profile}", profile)
    downloader.download_all_receipts()
```

### Custom Filename Patterns
Modify `generate_filename()` method to customize receipt naming:
```python
# Example: Add report ID to filename
filename = f"{timestamp}_{merchant}_{amount}_{row.get('Report ID', '')}{ext}"
```

### Filtering Downloads
Filter which receipts to download:
```python
# Only download receipts over $100
df_with_links = df_with_links[df_with_links['Amount'].astype(float) > 100]
```

## 📈 Performance Tips

### Optimize for Large Datasets
- **Batch processing**: Process in chunks of 100-200 receipts
- **Parallel downloads**: Modify script to use threading (advanced)
- **Resume capability**: Track completed downloads to resume interrupted sessions

### Reduce Detection Risk
- **Increase delays**: Modify `human_delay()` ranges for slower, more natural timing
- **Use VPN**: Route traffic through different IP addresses
- **Rotate user agents**: Change browser fingerprint periodically

## 🤝 Contributing

### Reporting Issues
When reporting issues, include:
1. **Operating system** and version
2. **Python version** (`python --version`)
3. **Chrome version** (chrome://version)
4. **Error message** (full traceback)
5. **Steps to reproduce**

### Feature Requests
Popular requests:
- [ ] GUI interface
- [ ] Support for other expense platforms
- [ ] OCR text extraction from receipts
- [ ] Automatic categorization
- [ ] Integration with accounting software

## 📄 License

This tool is provided as-is for educational and personal use. Users are responsible for complying with Expensify's Terms of Service and applicable laws regarding automated access to web services.

## 🔗 Related Resources

- [Expensify API Documentation](https://integrations.expensify.com/Integration-Server/doc/)
- [Selenium WebDriver Documentation](https://selenium-python.readthedocs.io/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [undetected-chromedriver GitHub](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

---

**Last Updated**: June 2025  
**Version**: 2.0  
**Tested On**: Windows 10/11, macOS Monterey+, Ubuntu 20.04+
