# QRadar Rule Manager - Enhanced

## Introduction
QRadar Rule Manager - Enhanced is an extended version of the [QRadar-Rule-Manager](https://github.com/Koifman/QRadar-Rule-Manager) tool, designed to manage, import/export, and modify rules in IBM QRadar SIEM. This tool supports integration with GitHub and GitLab for easier rule storage and sharing.

## Installation
### System Requirements
- Python 3.8 or later
- Windows operating system

### Setup Environment
1. **Clone the repository**
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/QRadar-Rule-Manager-Enhanced.git
   cd QRadar-Rule-Manager-Enhanced
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the application**
   ```sh
   python code.py
   ```

## Usage Guide
1. **Connect to QRadar**
   - Enter the QRadar URL.
   - Enter the Security Token for authentication.
   - Click "Get Rules" to fetch the existing rules list.

2. **Import/Export Rules**
   - Select the rule(s) to export and click "Export".
   - To import rules, select a `.zip` file and click "Import".

3. **GitHub/GitLab Integration**
   - Provide your GitHub/GitLab token for authentication.
   - Upload or download rules directly from the repository.

## Notes
- This tool requires API access to QRadar.
- When using GitHub/GitLab, ensure your token has the necessary read/write permissions.

## Acknowledgment
Special thanks to **Mr.Koifman**, the author of [QRadar-Rule-Manager](https://github.com/Koifman/QRadar-Rule-Manager), for allowing the public release of these enhancements. The original tool serves as a crucial foundation for expanding and improving functionalities for managing QRadar SIEM.

---
*For contributions or feedback, please open an issue or create a pull request on this repository.*

