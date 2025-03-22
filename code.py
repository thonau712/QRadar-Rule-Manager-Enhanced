import requests, time, os, json
from pathlib import Path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from github import Github, Auth
import gitlab
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (QListView, QFileDialog, QMessageBox, QComboBox, 
                           QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit)
from PyQt6.QtGui import QStandardItem
from PyQt6.QtCore import Qt
import base64

class Settings:
    def __init__(self):
        self.config_file = os.path.join(str(Path.home()), '.qradar_rule_manager.json')
        self.settings = self._load_settings()

    def _load_settings(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}

    def save_settings(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def delete(self, key):
        if key in self.settings:
            del self.settings[key]
            self.save_settings()

class CustomListView(QListView):
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # Handle right-click menu here if needed
            pass
        super().mousePressEvent(event)

class Ui_MainWindow(object):
    def __init__(self):
        self.settings = Settings()
        self.temp_files = []  # Track temporary files for cleanup

    def cleanup(self):
        """Clean up temporary files on exit"""
        for file in self.temp_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception:
                pass

    def create_temp_file(self, prefix="temp", suffix=".zip"):
        """Create a temporary file and track it for cleanup"""
        temp_path = os.path.join(os.getcwd(), f"{prefix}_{time.strftime('%Y%m%d_%H%M%S')}{suffix}")
        self.temp_files.append(temp_path)
        return temp_path

    def setupUi(self, MainWindow):
        # Initialize settings first
        self.settings = Settings()
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(898, 588)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.TabWidget.setGeometry(QtCore.QRect(0, 0, 901, 561))
        self.TabWidget.setAutoFillBackground(False)
        self.TabWidget.setObjectName("TabWidget")
        self.QRadarTab = QtWidgets.QWidget()
        self.QRadarTab.setObjectName("QRadarTab")
        self.ImportButton = QtWidgets.QPushButton(parent=self.QRadarTab)
        self.ImportButton.setGeometry(QtCore.QRect(630, 170, 81, 31))
        self.ImportButton.setStyleSheet("")
        self.ImportButton.setObjectName("ImportButton")
        self.RuleView = QtWidgets.QTreeView(parent=self.QRadarTab)
        self.RuleView.setGeometry(QtCore.QRect(10, 120, 501, 341))
        self.RuleView.setAutoFillBackground(False)
        self.RuleView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RuleView.setObjectName("RuleView")
        self.RuleView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.ExportButton = QtWidgets.QPushButton(parent=self.QRadarTab)
        self.ExportButton.setGeometry(QtCore.QRect(630, 290, 81, 31))
        self.ExportButton.setStyleSheet("")
        self.ExportButton.setObjectName("ExportButton")
        self.SECTokenEntry = QtWidgets.QLineEdit(parent=self.QRadarTab)
        self.SECTokenEntry.setGeometry(QtCore.QRect(10, 40, 321, 20))
        self.SECTokenEntry.setAutoFillBackground(False)
        self.SECTokenEntry.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SECTokenEntry.setObjectName("SECTokenEntry")
        self.SECTokenEntry.setEchoMode(QLineEdit.EchoMode.Password)
        self.SECTokenLabel = QtWidgets.QLabel(parent=self.QRadarTab)
        self.SECTokenLabel.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.SECTokenLabel.setAutoFillBackground(False)
        self.SECTokenLabel.setObjectName("SECTokenLabel")
        self.FileSelectionLine = QtWidgets.QLineEdit(parent=self.QRadarTab)
        self.FileSelectionLine.setGeometry(QtCore.QRect(530, 140, 261, 21))
        self.FileSelectionLine.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FileSelectionLine.setObjectName("FileSelectionLine")
        self.BrowseButton = QtWidgets.QPushButton(parent=self.QRadarTab)
        self.BrowseButton.setEnabled(True)
        self.BrowseButton.setGeometry(QtCore.QRect(800, 140, 81, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.BrowseButton.setFont(font)
        self.BrowseButton.setStyleSheet("font: 7pt \"MS Shell Dlg 2\";")
        self.BrowseButton.setFlat(False)
        self.BrowseButton.setObjectName("BrowseButton")
        self.GetRulesButton = QtWidgets.QPushButton(parent=self.QRadarTab)
        self.GetRulesButton.setGeometry(QtCore.QRect(210, 470, 81, 31))
        self.GetRulesButton.setStyleSheet("")
        self.GetRulesButton.setObjectName("GetRulesButton")
        self.FiletoImportLabel = QtWidgets.QLabel(parent=self.QRadarTab)
        self.FiletoImportLabel.setGeometry(QtCore.QRect(530, 120, 71, 16))
        self.FiletoImportLabel.setObjectName("FiletoImportLabel")
        self.QRadarURL = QtWidgets.QLineEdit(parent=self.QRadarTab)
        self.QRadarURL.setGeometry(QtCore.QRect(10, 90, 321, 20))
        self.QRadarURL.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.QRadarURL.setObjectName("QRadarURL")
        self.QRadarURLLabel = QtWidgets.QLabel(parent=self.QRadarTab)
        self.QRadarURLLabel.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.QRadarURLLabel.setObjectName("QRadarURLLabel")
        self.FileSelectionLine_Export = QtWidgets.QLineEdit(parent=self.QRadarTab)
        self.FileSelectionLine_Export.setGeometry(QtCore.QRect(530, 260, 261, 20))
        self.FileSelectionLine_Export.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FileSelectionLine_Export.setObjectName("FileSelectionLine_Export")
        self.BrowseButton_Export = QtWidgets.QPushButton(parent=self.QRadarTab)
        self.BrowseButton_Export.setEnabled(True)
        self.BrowseButton_Export.setGeometry(QtCore.QRect(800, 260, 81, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.BrowseButton_Export.setFont(font)
        self.BrowseButton_Export.setStyleSheet("font: 7pt \"MS Shell Dlg 2\";")
        self.BrowseButton_Export.setFlat(False)
        self.BrowseButton_Export.setObjectName("BrowseButton_Export")
        self.ExportLocationLabel = QtWidgets.QLabel(parent=self.QRadarTab)
        self.ExportLocationLabel.setGeometry(QtCore.QRect(530, 240, 91, 16))
        self.ExportLocationLabel.setObjectName("ExportLocationLabel")

        # Add rule management buttons
        self.RuleManagementGroup = QtWidgets.QGroupBox(parent=self.QRadarTab)
        self.RuleManagementGroup.setGeometry(QtCore.QRect(530, 330, 351, 131))
        self.RuleManagementGroup.setObjectName("RuleManagementGroup")
        
        self.EnableButton = QtWidgets.QPushButton(parent=self.RuleManagementGroup)
        self.EnableButton.setGeometry(QtCore.QRect(20, 30, 81, 31))
        self.EnableButton.setObjectName("EnableButton")
        
        self.DisableButton = QtWidgets.QPushButton(parent=self.RuleManagementGroup)
        self.DisableButton.setGeometry(QtCore.QRect(120, 30, 81, 31))
        self.DisableButton.setObjectName("DisableButton")
        
        self.DeleteButton = QtWidgets.QPushButton(parent=self.RuleManagementGroup)
        self.DeleteButton.setGeometry(QtCore.QRect(220, 30, 81, 31))
        self.DeleteButton.setObjectName("DeleteButton")

        self.TabWidget.addTab(self.QRadarTab, "")
        self.GitHubTab = QtWidgets.QWidget()
        self.GitHubTab.setObjectName("GitHubTab")
        
        # GitHub Rules List View
        self.GitHubRulesView = QtWidgets.QListView(parent=self.GitHubTab)
        self.GitHubRulesView.setGeometry(QtCore.QRect(20, 160, 800, 350))
        self.GitHubRulesView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.GitHubRulesView.setObjectName("GitHubRulesView")
        
        # GitHub Authentication Controls
        self.GitHubTokenLabel = QtWidgets.QLabel(parent=self.GitHubTab)
        self.GitHubTokenLabel.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.GitHubTokenLabel.setObjectName("GitHubTokenLabel")
        
        self.GitHubTokenLineEdit = QtWidgets.QLineEdit(parent=self.GitHubTab)
        self.GitHubTokenLineEdit.setGeometry(QtCore.QRect(20, 40, 211, 20))
        self.GitHubTokenLineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.GitHubTokenLineEdit.setObjectName("GitHubTokenLineEdit")
        self.GitHubTokenLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.RepoNameLabel = QtWidgets.QLabel(parent=self.GitHubTab)
        self.RepoNameLabel.setGeometry(QtCore.QRect(20, 70, 71, 16))
        self.RepoNameLabel.setObjectName("RepoNameLabel")
        
        self.RepoNameLine = QtWidgets.QLineEdit(parent=self.GitHubTab)
        self.RepoNameLine.setGeometry(QtCore.QRect(20, 90, 211, 20))
        self.RepoNameLine.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RepoNameLine.setObjectName("RepoNameLine")
        
        self.GitHubAuthenticateButton = QtWidgets.QPushButton(parent=self.GitHubTab)
        self.GitHubAuthenticateButton.setGeometry(QtCore.QRect(20, 120, 111, 23))
        self.GitHubAuthenticateButton.setObjectName("GitHubAuthenticateButton")
        
        self.ImportToQRadarButton = QtWidgets.QPushButton(parent=self.GitHubTab)
        self.ImportToQRadarButton.setGeometry(QtCore.QRect(689, 120, 131, 31))
        self.ImportToQRadarButton.setObjectName("ImportToQRadarButton")
        
        self.TabWidget.addTab(self.GitHubTab, "")
        self.GitLabTab = QtWidgets.QWidget()
        self.GitLabTab.setObjectName("GitLabTab")
        self.gitlab_url = QtWidgets.QLineEdit(parent=self.GitLabTab)
        self.gitlab_url.setGeometry(QtCore.QRect(10, 20, 261, 20))
        self.gitlab_url.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gitlab_url.setObjectName("gitlab_url")
        self.gitlab_token = QtWidgets.QLineEdit(parent=self.GitLabTab)
        self.gitlab_token.setGeometry(QtCore.QRect(10, 60, 261, 20))
        self.gitlab_token.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gitlab_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.gitlab_token.setObjectName("gitlab_token")
        self.gitlab_project = QtWidgets.QLineEdit(parent=self.GitLabTab)
        self.gitlab_project.setGeometry(QtCore.QRect(10, 100, 261, 20))
        self.gitlab_project.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gitlab_project.setObjectName("gitlab_project")
        self.gitlab_connect_btn = QtWidgets.QPushButton(parent=self.GitLabTab)
        self.gitlab_connect_btn.setGeometry(QtCore.QRect(10, 140, 111, 23))
        self.gitlab_connect_btn.setObjectName("gitlab_connect_btn")
        self.gitlab_rules_view = QtWidgets.QListView(parent=self.GitLabTab)
        self.gitlab_rules_view.setGeometry(QtCore.QRect(280, 20, 550, 311))
        self.gitlab_rules_view.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gitlab_rules_view.setObjectName("gitlab_rules_view")
        self.gitlab_rule_description = QtWidgets.QTextBrowser(parent=self.GitLabTab)
        self.gitlab_rule_description.setGeometry(QtCore.QRect(280, 340, 550, 141))
        self.gitlab_rule_description.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gitlab_rule_description.setReadOnly(True)
        self.gitlab_rule_description.setObjectName("gitlab_rule_description")
        self.gitlab_import_btn = QtWidgets.QPushButton(parent=self.GitLabTab)
        self.gitlab_import_btn.setGeometry(QtCore.QRect(280, 490, 131, 31))
        self.gitlab_import_btn.setObjectName("gitlab_import_btn")
        self.TabWidget.addTab(self.GitLabTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        app.setStyle("Fusion")
        app.setStyleSheet("""
        QLineEdit, QTextEdit, QPlainTextEdit, QListView {
            color: #2E2E2E; /* Dark color for user input text */
        }
    """)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Load settings
        # Remove the separate setup calls
        # self.setupQRadarTab()
        # self.setupGitHubTab()
        # self.setupGitLabTab()
        
        # Load saved settings into UI elements after they are created
        if hasattr(self, 'QRadarURL'):
            self.QRadarURL.setText(self.settings.get('qradar_url', ''))
        if hasattr(self, 'SECTokenEntry'):
            self.SECTokenEntry.setText(self.settings.get('qradar_token', ''))
        if hasattr(self, 'GitHubTokenEntry'):
            self.GitHubTokenEntry.setText(self.settings.get('github_token', ''))
        if hasattr(self, 'RepoNameEntry'):
            self.RepoNameEntry.setText(self.settings.get('github_repo', ''))
        if hasattr(self, 'gitlab_url'):
            self.gitlab_url.setText(self.settings.get('gitlab_url', 'https://gitlab.com'))
        if hasattr(self, 'gitlab_token'):
            self.gitlab_token.setText(self.settings.get('gitlab_token', ''))
        if hasattr(self, 'gitlab_project'):
            self.gitlab_project.setText(self.settings.get('gitlab_project', ''))
        
        # Connect buttons
        self.BrowseButton.clicked.connect(self.browseFiles)
        self.BrowseButton_Export.clicked.connect(self.browseFilesExport)
        self.GetRulesButton.clicked.connect(self.getRules)  
        self.ExportButton.clicked.connect(self.exportRules)
        self.ImportButton.clicked.connect(self.importRules)
        self.GitHubAuthenticateButton.clicked.connect(self.github)
        self.ImportToQRadarButton.clicked.connect(self.importRulesFromGitHub)
        self.gitlab_connect_btn.clicked.connect(self.connect_gitlab)
        self.gitlab_import_btn.clicked.connect(self.import_from_gitlab)

        # Connect rule management buttons
        self.EnableButton.clicked.connect(lambda: self.updateRuleState(True))
        self.DisableButton.clicked.connect(lambda: self.updateRuleState(False))
        self.DeleteButton.clicked.connect(self.deleteRule)

        # Set up models first
        self.model = QtGui.QStandardItemModel(self.RuleView)
        self.githubModel = QtGui.QStandardItemModel(self.GitHubRulesView)
        self.gitlab_rules_model = QtGui.QStandardItemModel(self.gitlab_rules_view)
        self.RuleView.setModel(self.model)
        self.GitHubRulesView.setModel(self.githubModel)
        self.gitlab_rules_view.setModel(self.gitlab_rules_model)

        # Now connect selection signals after models are set
        self.RuleView.selectionModel().selectionChanged.connect(self.onRuleSelected)
        self.GitHubRulesView.selectionModel().selectionChanged.connect(self.on_directory_selected)
        self.gitlab_rules_view.selectionModel().selectionChanged.connect(self.on_gitlab_rule_selected)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QRadar Rule Manager"))
        self.ImportButton.setText(_translate("MainWindow", "Import"))
        self.ExportButton.setText(_translate("MainWindow", "Export"))
        self.SECTokenLabel.setText(_translate("MainWindow", "SEC Token"))
        self.BrowseButton.setText(_translate("MainWindow", "Browse"))
        self.GetRulesButton.setText(_translate("MainWindow", "Get Rules"))
        self.FiletoImportLabel.setText(_translate("MainWindow", "File to import"))
        self.QRadarURLLabel.setText(_translate("MainWindow", "QRadar URL"))
        self.BrowseButton_Export.setText(_translate("MainWindow", "Browse"))
        self.ExportLocationLabel.setText(_translate("MainWindow", "Export Location"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.QRadarTab), _translate("MainWindow", "QRadar"))
        self.RuleManagementGroup.setTitle(_translate("MainWindow", "Rule Management"))
        self.EnableButton.setText(_translate("MainWindow", "Enable"))
        self.DisableButton.setText(_translate("MainWindow", "Disable"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete"))
        self.ImportToQRadarButton.setText(_translate("MainWindow", "Import to QRadar"))
        self.GitHubTokenLabel.setText(_translate("MainWindow", "GitHub Token"))
        self.GitHubAuthenticateButton.setText(_translate("MainWindow", "Authenticate"))
        self.RepoNameLabel.setText(_translate("MainWindow", "Repo Name"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.GitHubTab), _translate("MainWindow", "GitHub"))
        self.gitlab_url.setPlaceholderText(_translate("MainWindow", "GitLab URL"))
        self.gitlab_token.setPlaceholderText(_translate("MainWindow", "Access Token"))
        self.gitlab_project.setPlaceholderText(_translate("MainWindow", "Project"))
        self.gitlab_connect_btn.setText(_translate("MainWindow", "Connect"))
        self.gitlab_import_btn.setText(_translate("MainWindow", "Import to QRadar"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.GitLabTab), _translate("MainWindow", "GitLab"))

    def showMessageBox(self, title, message):
          msgBox = QMessageBox()
          msgBox.setWindowTitle(title)
          msgBox.setText(message)
          msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
          msgBox.exec()

    def browseFiles(self):
        fileName , _ = QFileDialog.getOpenFileName(None, "Select File", "", "ZIP Files (*.zip)")
        if fileName:
                self.FileSelectionLine.setText(fileName)  # Display the selected file path in the QLineEdit
    def browseFilesExport(self):
        fileName = QFileDialog.getExistingDirectory(None, "Select Directory")
        if fileName:
                self.FileSelectionLine_Export.setText(fileName)  # Display the selected file path in the QLineEdit

    def github(self):
        try:
            # Clear old data before adding new
            self.githubModel.clear()
            
            self.auth = Auth.Token(self.GitHubTokenLineEdit.text())
            self.g = Github(auth=self.auth)
            self.repo = self.g.get_user().get_repo(self.RepoNameLine.text())
            contents = self.repo.get_contents("")
            
            # Add new data - chỉ hiển thị file .zip
            for item in contents:
                if item.type == "file" and item.name.endswith('.zip'):
                    item_model = QStandardItem(item.name)
                    item_model.setData(item, Qt.ItemDataRole.UserRole)
                    self.githubModel.appendRow(item_model)
            
            self.showMessageBox("Success", "Connected to GitHub successfully")
            
        except Exception as e:
            self.showMessageBox("Error", f"Failed to connect to GitHub: {str(e)}")

    def on_directory_selected(self, selected):
        try:
            for index in selected.indexes():
                # Get the selected file
                selected_item = self.githubModel.itemFromIndex(index).data(Qt.ItemDataRole.UserRole)
                if selected_item and selected_item.name.endswith('.zip'):
                    # No need to process anything else since we're only handling .zip files directly
                    pass
        except Exception as e:
            print(f"Error in directory selection: {str(e)}")

    def on_gitlab_rule_selected(self, selected):
        try:
            for index in selected.indexes():
                # Get the selected rule
                rule_data = self.gitlab_rules_model.itemFromIndex(index).data(Qt.ItemDataRole.UserRole)
                
                if rule_data['type'] == 'blob' and rule_data['name'].endswith('.zip'):
                    # Download file content
                    file_content = self.gitlab_proj.files.get(
                        file_path=rule_data['path'], 
                        ref='main'
                    ).decode()
                    
                    # Display basic information about the rule
                    self.gitlab_rule_description.setText(
                        f"Selected Rule: {rule_data['name']}\n"
                        f"Path: {rule_data['path']}\n"
                        f"Size: {len(file_content)} bytes"
                    )

        except Exception as e:
            self.showMessageBox("Error", f"Failed to get rule details: {str(e)}")

    def buildRequest(self):
            BASE_URL = self.QRadarURL.text()
            header = {
                'SEC': self.SECTokenEntry.text(),
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Version': '20.0'
            }  

            try:
                r = requests.get(f"{BASE_URL}/api/analytics/rules", headers=header, verify=False)
                r.raise_for_status()  # Raise exception for bad status codes
                return r.json()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Failed to get rules: {str(e)}")

    def getRules(self):
        try:
            # Clear existing items
            self.model.clear()
            
            # Set up model with checkbox support
            self.model.setHorizontalHeaderLabels(['Rules'])
            
            # Get rules from QRadar
            response = self.buildRequest()
            
            # Sort rules by name for better display
            rules = sorted(response, key=lambda x: x.get('name', '').lower())
            
            for rule in rules:
                name = rule.get('name', '')
                if name:
                    item = QStandardItem(name)
                    # Make item checkable
                    item.setCheckable(True)
                    # Store the full rule data for later use
                    item.setData(rule, Qt.ItemDataRole.UserRole)
                    # Set tooltip to show enabled/disabled status
                    status = "Enabled" if rule.get('enabled', False) else "Disabled"
                    item.setToolTip(f"Status: {status}")
                    self.model.appendRow(item)
            
        except Exception as e:
            self.showMessageBox("Error", str(e))

    def onRuleSelected(self, selected, deselected):
        try:
            indexes = selected.indexes()
            if not indexes:
                return
                
            # Get the first selected rule
            rule_data = self.model.itemFromIndex(indexes[0]).data(Qt.ItemDataRole.UserRole)
            if not rule_data:
                raise Exception("No rule data found")
                
        except Exception as e:
            print(f"Error in rule selection: {str(e)}")

    def updateRuleState(self, enable):
        try:
            selected_indexes = self.RuleView.selectedIndexes()
            if not selected_indexes:
                self.showMessageBox("Warning", "Please select a rule first")
                return

            BASE_URL = self.QRadarURL.text()
            headers = {
                'SEC': self.SECTokenEntry.text(),
                'Content-Type': 'application/json',
                'Version': '20.0',
                'Accept': 'application/json'
            }

            for index in selected_indexes:
                rule_data = self.model.itemFromIndex(index).data(Qt.ItemDataRole.UserRole)
                rule_id = rule_data['id']
                
                # Update rule state
                data = {'enabled': enable}
                response = requests.post(
                    f"{BASE_URL}/api/analytics/rules/{rule_id}",
                    headers=headers,
                    json=data,
                    verify=False
                )
                response.raise_for_status()

            # Refresh rules list
            self.getRules()
            state = "enabled" if enable else "disabled"
            self.showMessageBox("Success", f"Rule(s) {state} successfully")
        except Exception as e:
            self.showMessageBox("Error", f"Failed to update rule state: {str(e)}")

    def deleteRule(self):
        try:
            selected_indexes = self.RuleView.selectedIndexes()
            if not selected_indexes:
                self.showMessageBox("Warning", "Please select a rule first")
                return

            # Confirm deletion
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setWindowTitle("Confirm Delete")
            msgBox.setText("Are you sure you want to delete the selected rule(s)?")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if msgBox.exec() != QMessageBox.StandardButton.Yes:
                return

            BASE_URL = self.QRadarURL.text()
            headers = {
                'SEC': self.SECTokenEntry.text(),
                'Content-Type': 'application/json',
                'Version': '20.0',
                'Accept': 'application/json'
            }

            for index in selected_indexes:
                rule_data = self.model.itemFromIndex(index).data(Qt.ItemDataRole.UserRole)
                rule_id = rule_data['id']
                
                # Delete rule
                response = requests.delete(
                    f"{BASE_URL}/api/analytics/rules/{rule_id}",
                    headers=headers,
                    verify=False
                )
                response.raise_for_status()

            # Refresh rules list
            self.getRules()
            self.showMessageBox("Success", "Rule(s) deleted successfully")
        except Exception as e:
            self.showMessageBox("Error", f"Failed to delete rule: {str(e)}")

    def importRulesFromGitHub(self):
        temp_file = None
        file_handle = None
        try:
            if self.QRadarURL.text() == "":
                self.showMessageBox("Error", "QRadar URL must not be empty!")
                return

            selected_indexes = self.GitHubRulesView.selectionModel().selectedIndexes()
            if not selected_indexes:
                self.showMessageBox("Warning", "Please select a rule to import")
                return

            selected_item = self.githubModel.itemFromIndex(selected_indexes[0]).data(Qt.ItemDataRole.UserRole)
            if selected_item and selected_item.name.endswith('.zip'):
                # Download file content
                file_content = selected_item.decoded_content
                
                # Create temporary file
                temp_file = self.create_temp_file(prefix="github_import", suffix=".zip")
                with open(temp_file, 'wb') as f:
                    f.write(file_content)

                # Import to QRadar using multipart/form-data
                BASE_URL = self.QRadarURL.text()
                headers = {
                    'SEC': self.SECTokenEntry.text(),
                    'Accept': 'application/json',
                    'Version': '20.0'
                }

                # Open file for upload
                file_handle = open(temp_file, 'rb')
                files = {
                    'file': ('rule.zip', file_handle, 'application/zip')
                }

                params = {
                    'action_type': 'INSTALL',
                    'overwrite': 'true'
                }

                # Upload extension
                response = requests.post(
                    f"{BASE_URL}/api/config/extension_management/extensions",
                    headers=headers,
                    files=files,
                    verify=False
                )

                if not response.ok:
                    raise Exception(f"Failed to upload extension. Status code: {response.status_code}. Response: {response.text}")

                response_body = response.json()
                app_id = str(response_body['id'])

                # Close file handle before proceeding
                file_handle.close()
                file_handle = None

                # Install extension
                url_install = f"{BASE_URL}/api/config/extension_management/extensions/{app_id}"
                response_install = requests.post(url_install, headers=headers, params=params, verify=False)
                
                if not response_install.ok:
                    raise Exception(f"Failed to install extension. Status code: {response_install.status_code}")

                response_install_body = response_install.json()
                status_location = response_install_body["status_location"]

                # Monitor installation progress
                self.showMessageBox("Installing", "Installation in-progress...")
                max_attempts = 30
                attempts = 0

                while attempts < max_attempts:
                    response_status = requests.get(status_location, headers=headers, verify=False)
                    if not response_status.ok:
                        raise Exception(f"Failed to check installation status. Status code: {response_status.status_code}")

                    status_body = response_status.json()
                    
                    if status_body.get("status") == "COMPLETED":
                        self.showMessageBox("Success", "Rule installed successfully")
                        break
                    elif status_body.get("status") == "ERROR":
                        error_message = status_body.get("message", "Unknown error occurred")
                        raise Exception(f"Installation failed: {error_message}")
                    
                    attempts += 1
                    time.sleep(2)

                if attempts >= max_attempts:
                    raise Exception("Installation timed out")

        except Exception as e:
            error_msg = f"Error during rule import: {str(e)}"
            print(error_msg)
            self.showMessageBox("Error", error_msg)
            
        finally:
            # Đảm bảo đóng file handle nếu còn mở
            if file_handle is not None:
                try:
                    file_handle.close()
                except:
                    pass
            
            # Clean up temporary file
            if temp_file and os.path.exists(temp_file):
                try:
                    # Thêm thời gian chờ để đảm bảo file đã được giải phóng
                    time.sleep(1)
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Failed to clean up temporary file: {str(e)}")

    def exportRules(self):
        try:
            # Lấy tất cả các rule được check
            rule_ids = []
            for row in range(self.model.rowCount()):
                item = self.model.item(row)
                if item.checkState() == Qt.CheckState.Checked:
                    rule_data = item.data(Qt.ItemDataRole.UserRole)
                    rule_ids.append(str(rule_data['id']))
            
            if not rule_ids:
                self.showMessageBox("Warning", "Please select rules to export")
                return
                
            # Ask user where to export
            export_dialog = QtWidgets.QDialog()
            export_dialog.setWindowTitle("Export Rules")
            layout = QVBoxLayout()
            
            # Export location
            location_group = QGroupBox("Export Location")
            location_layout = QVBoxLayout()
            
            # Radio buttons for export type
            local_radio = QtWidgets.QRadioButton("Local File")
            github_radio = QtWidgets.QRadioButton("GitHub")
            gitlab_radio = QtWidgets.QRadioButton("GitLab")
            local_radio.setChecked(True)
            
            location_layout.addWidget(local_radio)
            location_layout.addWidget(github_radio)
            location_layout.addWidget(gitlab_radio)
            
            location_group.setLayout(location_layout)
            layout.addWidget(location_group)
            
            # Buttons
            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | 
                QtWidgets.QDialogButtonBox.StandardButton.Cancel
            )
            button_box.accepted.connect(export_dialog.accept)
            button_box.rejected.connect(export_dialog.reject)
            layout.addWidget(button_box)
            
            export_dialog.setLayout(layout)
            
            if export_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                if local_radio.isChecked():
                    self.export_to_local(rule_ids)
                elif github_radio.isChecked():
                    self.export_to_github(rule_ids)
                else:
                    self.export_to_gitlab(rule_ids)
                    
        except Exception as e:
            self.showMessageBox("Error", f"Failed to export rules: {str(e)}")

    def export_to_local(self, rule_ids):
        file_name, _ = QFileDialog.getSaveFileName(
            None,  # Replace self with None
            "Save Rules", 
            "", 
            "ZIP Files (*.zip)"
        )
        if file_name:
            self._export_rules_to_file(rule_ids, file_name)
            self.showMessageBox("Success", "Rules exported successfully")

    def get_custom_filename(self, default_name):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Customize File Name")
        layout = QVBoxLayout()

        # Add label and input for filename
        name_label = QtWidgets.QLabel("Enter file name:")
        name_input = QtWidgets.QLineEdit()
        name_input.setText(default_name)
        
        # Add hint label
        hint_label = QtWidgets.QLabel("(File extension .zip will be added automatically)")
        hint_label.setStyleSheet("color: gray; font-size: 10px;")

        # Add buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | 
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        
        # Add widgets to layout
        layout.addWidget(name_label)
        layout.addWidget(name_input)
        layout.addWidget(hint_label)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        # Connect signals
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            filename = name_input.text().strip()
            # Ensure filename ends with .zip
            if not filename.lower().endswith('.zip'):
                filename += '.zip'
            return filename
        return None

    def export_to_github(self, rule_ids):
        try:
            if not hasattr(self, 'g') or not hasattr(self, 'repo'):
                self.showMessageBox("Error", "Please connect to GitHub first")
                return
                
            # Export to temporary file
            temp_file = self.create_temp_file(prefix="github_export")
            self._export_rules_to_file(rule_ids, temp_file)
            
            # Create default filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            default_filename = f"rules_export_{timestamp}"
            
            # Show dialog for filename input
            custom_filename = self.get_custom_filename(default_filename)
            if custom_filename is None:  # User cancelled
                try:
                    os.remove(temp_file)
                except:
                    pass
                return
            
            # Upload to GitHub
            with open(temp_file, 'rb') as f:
                content = f.read()
            
            self.repo.create_file(
                custom_filename,
                f"Export rules {timestamp}",
                content
            )
            
            # Clean up
            try:
                os.remove(temp_file)
            except:
                pass
                
            self.showMessageBox("Success", f"Rules have been exported to GitHub as {custom_filename}")
            
        except Exception as e:
            self.showMessageBox("Error", f"Failed to export rules to GitHub: {str(e)}")

    def export_to_gitlab(self, rule_ids):
        try:
            if not hasattr(self, 'gl') or not hasattr(self, 'gitlab_proj'):
                self.showMessageBox("Error", "Please connect to GitLab first")
                return
                
            # Export to temporary file
            temp_file = self.create_temp_file(prefix="gitlab_export")
            self._export_rules_to_file(rule_ids, temp_file)
            
            # Create default filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            default_filename = f"rules_export_{timestamp}"
            
            # Show dialog for filename input
            custom_filename = self.get_custom_filename(default_filename)
            if custom_filename is None:  # User cancelled
                try:
                    os.remove(temp_file)
                except:
                    pass
                return
            
            # Upload to GitLab
            with open(temp_file, 'rb') as f:
                content = f.read()
                
            content_encoded = base64.b64encode(content).decode('utf-8')
                
            self.gitlab_proj.files.create({
                'file_path': custom_filename,
                'branch': 'main',
                'content': content_encoded,
                'commit_message': f"Export rules {timestamp}",
                'encoding': 'base64'
            })
            
            # Clean up
            try:
                os.remove(temp_file)
            except:
                pass
                
            self.showMessageBox("Success", f"Rules have been exported to GitLab as {custom_filename}")
            
        except Exception as e:
            self.showMessageBox("Error", f"Failed to export rules to GitLab: {str(e)}")

    def _export_rules_to_file(self, rule_ids, file_path):
        response = self.buildRequest()
        BASE_URL = self.QRadarURL.text()
        SEC_TOKEN = self.SECTokenEntry.text()

        headers_json = {
            'SEC': SEC_TOKEN,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        headers_zip = {
            'SEC': SEC_TOKEN,
            'Content-Type': 'application/zip',
            'Accept': 'application/zip'
        }

        data = {
            "export_contents": [{
                "content_item_ids": rule_ids,
                "content_type": "CUSTOM_RULES",
                "related_content": [{"content_type": "FGROUP_LINKS"}]
            }]
        }

        try:
            # Create export task
            export_response = requests.post(
                f'{BASE_URL}/api/config/extension_management/extension_export_tasks',
                json=data,
                headers=headers_json,
                verify=False
            )
            export_response.raise_for_status()
            task_id = export_response.json().get('task_id')

            # Wait for task completion
            task_status_url = f'{BASE_URL}/api/config/extension_management/extensions_task_status/{task_id}'
            while True:
                status_response = requests.get(task_status_url, headers=headers_json, verify=False)
                status_response.raise_for_status()
                status = status_response.json().get('status')
                if status == "COMPLETED":
                    break
                elif status == "ERROR":
                    raise Exception("Export task failed")
                time.sleep(1)

            # Download the exported file
            download_url = f'{BASE_URL}/api/config/extension_management/extension_export_tasks/{task_id}/extension_export'
            download_response = requests.get(download_url, headers=headers_zip, verify=False)
            download_response.raise_for_status()

            with open(file_path, 'wb') as file:
                file.write(download_response.content)

        except Exception as e:
            raise Exception(f"Failed to export rules: {str(e)}")

    def connect_gitlab(self):
        try:
            # Clear old data before adding new
            self.gitlab_rules_model.clear()
            
            url = self.gitlab_url.text().strip()
            token = self.gitlab_token.text().strip()
            project_path = self.gitlab_project.text().strip()
            
            # Save settings
            self.save_current_settings()

            # Connect to GitLab
            self.gl = gitlab.Gitlab(url, private_token=token, ssl_verify=False)
            self.gl.auth()
            
            try:
                # Try to find project by full path
                self.gitlab_proj = self.gl.projects.get(project_path)
            except:
                try:
                    # If not found, try by ID
                    self.gitlab_proj = self.gl.projects.get(int(project_path))
                except:
                    raise Exception(f"Project not found. Please check:\n1. Project path/ID is correct\n2. Token has correct permissions\n3. Project visibility")
            
            # Get repository items
            try:
                items = self.gitlab_proj.repository_tree(path='', ref='main')
            except:
                try:
                    items = self.gitlab_proj.repository_tree(path='', ref='master')
                except:
                    raise Exception("Could not access repository content")
            
            # Add new items to model
            for item in items:
                if item['type'] == 'tree' or (item['type'] == 'blob' and item['name'].endswith('.zip')):
                    item_model = QStandardItem(item['name'])
                    # Check if item already exists
                    existing_items = self.gitlab_rules_model.findItems(item['name'])
                    if not existing_items:
                        item_model.setData(item, Qt.ItemDataRole.UserRole)
                        self.gitlab_rules_model.appendRow(item_model)
            
            self.showMessageBox("Success", "Connected to GitLab successfully")
            
        except Exception as e:
            self.showMessageBox("Error", f"Failed to connect to GitLab: {str(e)}")

    def import_from_gitlab(self):
        temp_file = None
        file_handle = None
        try:
            if not hasattr(self, 'gl') or not hasattr(self, 'gitlab_proj'):
                self.showMessageBox("Error", "Please connect to GitLab first")
                return
                
            if self.QRadarURL.text() == "":
                self.showMessageBox("Error", "QRadar URL must not be empty!")
                return

            selected = self.gitlab_rules_view.selectedIndexes()
            if not selected:
                self.showMessageBox("Warning", "Please select a rule to import")
                return
                
            item_data = self.gitlab_rules_model.itemFromIndex(selected[0]).data(Qt.ItemDataRole.UserRole)
            
            if item_data['type'] == 'blob' and item_data['name'].endswith('.zip'):
                # Download file content
                file_content = base64.b64decode(
                    self.gitlab_proj.files.get(
                        file_path=item_data['path'], 
                        ref='main'
                    ).content
                )
                
                # Create temporary file
                temp_file = self.create_temp_file(prefix="gitlab_import", suffix=".zip")
                with open(temp_file, 'wb') as f:
                    f.write(file_content)

                # Import to QRadar using multipart/form-data
                BASE_URL = self.QRadarURL.text()
                headers = {
                    'SEC': self.SECTokenEntry.text(),
                    'Accept': 'application/json',
                    'Version': '20.0'
                }

                # Open file for upload
                file_handle = open(temp_file, 'rb')
                files = {
                    'file': ('rule.zip', file_handle, 'application/zip')
                }

                params = {
                    'action_type': 'INSTALL',
                    'overwrite': 'true'
                }

                # Upload extension
                response = requests.post(
                    f"{BASE_URL}/api/config/extension_management/extensions",
                    headers=headers,
                    files=files,
                    verify=False
                )

                if not response.ok:
                    raise Exception(f"Failed to upload extension. Status code: {response.status_code}. Response: {response.text}")

                response_body = response.json()
                app_id = str(response_body['id'])

                # Close file handle before proceeding
                file_handle.close()
                file_handle = None

                # Install extension
                url_install = f"{BASE_URL}/api/config/extension_management/extensions/{app_id}"
                response_install = requests.post(url_install, headers=headers, params=params, verify=False)
                
                if not response_install.ok:
                    raise Exception(f"Failed to install extension. Status code: {response_install.status_code}")

                response_install_body = response_install.json()
                status_location = response_install_body["status_location"]

                # Monitor installation progress
                self.showMessageBox("Installing", "Installation in-progress...")
                max_attempts = 30
                attempts = 0

                while attempts < max_attempts:
                    response_status = requests.get(status_location, headers=headers, verify=False)
                    if not response_status.ok:
                        raise Exception(f"Failed to check installation status. Status code: {response_status.status_code}")

                    status_body = response_status.json()
                    
                    if status_body.get("status") == "COMPLETED":
                        self.showMessageBox("Success", "Rule installed successfully from GitLab")
                        break
                    elif status_body.get("status") == "ERROR":
                        error_message = status_body.get("message", "Unknown error occurred")
                        raise Exception(f"Installation failed: {error_message}")
                    
                    attempts += 1
                    time.sleep(10)  # Changed from 2s to 10s

                if attempts >= max_attempts:
                    raise Exception("Installation timed out")

        except Exception as e:
            error_msg = f"Error during GitLab rule import: {str(e)}"
            print(error_msg)
            self.showMessageBox("Error", error_msg)
            
        finally:
            # Ensure file handle is closed if still open
            if file_handle is not None:
                try:
                    file_handle.close()
                except:
                    pass
            
            # Clean up temporary file
            if temp_file and os.path.exists(temp_file):
                try:
                    # Add delay to ensure file is released
                    time.sleep(1)
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Failed to clean up temporary file: {str(e)}")

    def save_current_settings(self):
        try:
            # Save QRadar settings
            self.settings.set('qradar_url', self.QRadarURL.text())
            self.settings.set('qradar_token', self.SECTokenEntry.text())
            
            # Save GitHub settings
            self.settings.set('github_token', self.GitHubTokenLineEdit.text())
            self.settings.set('github_repo', self.RepoNameLine.text())
            
            # Save GitLab settings
            self.settings.set('gitlab_url', self.gitlab_url.text())
            self.settings.set('gitlab_token', self.gitlab_token.text())
            self.settings.set('gitlab_project', self.gitlab_project.text())
            
        except Exception as e:
            print(f"Error saving settings: {e}")

    def importRules(self):
        try:
            if not self.FileSelectionLine.text():
                self.showMessageBox("Error", "Please select a file to import")
                return

            # Import to QRadar using multipart/form-data
            BASE_URL = self.QRadarURL.text()
            headers = {
                'SEC': self.SECTokenEntry.text(),
                'Accept': 'application/json',
                'Version': '20.0'
            }

            # Open file and prepare for upload
            files = {
                'file': (
                    os.path.basename(self.FileSelectionLine.text()),
                    open(self.FileSelectionLine.text(), 'rb'),
                    'application/zip'
                )
            }

            params = {
                'action_type': 'INSTALL',
                'overwrite': 'true'
            }

            # Upload extension
            response = requests.post(
                f"{BASE_URL}/api/config/extension_management/extensions",
                headers=headers,
                files=files,
                verify=False
            )

            if not response.ok:
                raise Exception(f"Failed to upload extension. Status code: {response.status_code}. Response: {response.text}")

            response_body = response.json()
            app_id = str(response_body['id'])

            # Install extension
            url_install = f"{BASE_URL}/api/config/extension_management/extensions/{app_id}"
            response_install = requests.post(url_install, headers=headers, params=params, verify=False)
            
            if not response_install.ok:
                raise Exception(f"Failed to install extension. Status code: {response_install.status_code}")

            response_install_body = response_install.json()
            status_location = response_install_body["status_location"]

            # Monitor installation progress
            self.showMessageBox("Installing", "Installation in-progress...")
            max_attempts = 30
            attempts = 0

            while attempts < max_attempts:
                response_status = requests.get(status_location, headers=headers, verify=False)
                if not response_status.ok:
                    raise Exception(f"Failed to check installation status. Status code: {response_status.status_code}")

                status_body = response_status.json()
                
                if status_body.get("status") == "COMPLETED":
                    self.showMessageBox("Success", "Rule installed successfully")
                    break
                elif status_body.get("status") == "ERROR":
                    error_message = status_body.get("message", "Unknown error occurred")
                    raise Exception(f"Installation failed: {error_message}")
                
                attempts += 1
                time.sleep(2)

            if attempts >= max_attempts:
                raise Exception("Installation timed out")

        except Exception as e:
            error_msg = f"Error during rule import: {str(e)}"
            print(error_msg)
            self.showMessageBox("Error", error_msg)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())