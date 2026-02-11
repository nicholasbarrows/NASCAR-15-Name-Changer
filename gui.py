import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QScrollArea, QCheckBox, QFileDialog
from PyQt6.QtCore import Qt, QTimer

from patcher import drivers, patch_file

class LDAPatcherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NASCAR '15 Name Changer")

        # Stores input widgets and counters
        self.inputs = {}
        self.counters = {}

        layout = QVBoxLayout()

        # Scroll area
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        # Create UI rows by looping over our driver array
        for d in drivers:
            row = QHBoxLayout()

            label = QLabel(d.driver_name)
            label.setMinimumWidth(150)

            edit = QLineEdit()
            edit.setPlaceholderText(d.driver_name)

            counter = QLabel()
            counter.setAlignment(Qt.AlignmentFlag.AlignRight)
            counter.setMinimumWidth(60)

            self.inputs[d.driver_name] = edit
            self.counters[d.driver_name] = counter

            row.addWidget(label)
            row.addWidget(edit, stretch=1)
            row.addWidget(counter)
            scroll_layout.addLayout(row)

        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)

        # Safe Mode checkbox (enabled by default)
        self.safe_mode_checkbox = QCheckBox("Safe Mode")
        self.safe_mode_checkbox.setChecked(True)
        self.safe_mode_checkbox.stateChanged.connect(self.on_safe_mode_changed)

        # Sam Hornish Jr checkbox (disabled by default)
        self.hornish_checkbox = QCheckBox("Overwrite Sam Hornish Jr's name")
        self.hornish_checkbox.setChecked(False)
        self.hornish_checkbox.setVisible(False)
        self.hornish_checkbox.stateChanged.connect(self.on_hornish_changed)

        # Patch button
        patch_btn = QPushButton("Patch Game with New Names")
        patch_btn.clicked.connect(self.patch)

        layout.addWidget(scroll)
        layout.addWidget(self.safe_mode_checkbox)
        layout.addWidget(self.hornish_checkbox)
        layout.addWidget(patch_btn)
        self.setLayout(layout)

        # Initialize limits and character counters
        self.update_limits()

    # For choosing ARCHIVE0.AR file
    def select_archive(self):

        # Info popup
        msg = QMessageBox(self)
        msg.setWindowTitle("Select ARCHIVE0.AR File")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(
            "Navigate to your NASCAR '15 installation, open the \"data\" folder, and select the file named 'ARCHIVE0.AR' \n\n"
            # "The file 'cdfiles.dat' must also exist in the same directory \n\n"
            "The default install location for NASCAR '15 is: \n C:/Program Files (x86)/Steam/steamapps/common/NASCAR 15"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        result = msg.exec()

        # User closed popup or pressed cancel
        if result != QMessageBox.StandardButton.Ok:
            self.clean_exit()

        # File selection dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select ARCHIVE0.AR",
            "",
            "Archive File (ARCHIVE0.AR)"
        )

        # User cancelled file dialog
        if not file_path:
            self.clean_exit()

        filename = os.path.basename(file_path)
        if filename.lower() != "archive0.ar":
            self.clean_exit("Incorrect File","You must select the file named 'ARCHIVE0.AR'.")

        folder = os.path.dirname(file_path)
        cdfiles_path = os.path.join(folder, "cdfiles.dat")

        if not os.path.exists(cdfiles_path):
            self.clean_exit("cdfiles.dat missing", "The file 'cdfiles.dat' appears to be missing from the NASCAR '15 installation.")

        # Store paths
        self.archive_path = file_path
        self.game_dir = folder

    # Safe Mode disable/enable
    def on_safe_mode_changed(self):
        safe = self.safe_mode_checkbox.isChecked()

        # Hornish option only visible when Safe Mode is OFF
        self.hornish_checkbox.setVisible(not safe)

        # If returning to safe mode, hide Hornish button (and disable it)
        if safe:
            hornish_field = self.inputs.get("Sam Hornish Jr.")
            if hornish_field:
                hornish_field.setEnabled(True)
                self.hornish_checkbox.setChecked(False)

        # Update character limits
        self.update_limits()
    
    # Checkbox for Sam Hornish Jr
    def on_hornish_changed(self):
        hornish_field = self.inputs["Sam Hornish Jr."]

        if self.hornish_checkbox.isChecked():
            hornish_field.setEnabled(False)
        else:
            hornish_field.setEnabled(True)

        # Update limits (Harvick's changes)
        self.update_limits()

    # Gets max number of characters, dependent on safe mode
    def get_max_characters(self, driver):
        # Safe Mode means the max length is equal to the number of characters of the driver name
        if self.safe_mode_checkbox.isChecked():
            return len(driver.driver_name)
        
        # If Sam Hornish name is allowed to be overwritten, Kevin Harvick can have a name up to 31 characters
        if (driver.driver_name == "Kevin Harvick" and self.hornish_checkbox.isChecked()):
            return 31

        # Max length is set by given value if safe mode disabled
        return driver.max_length

    # Update max length, counters, and validators for every driver
    def update_limits(self):
        for d in drivers:
            edit = self.inputs[d.driver_name]
            counter = self.counters[d.driver_name]

            max_len = self.get_max_characters(d)
            edit.setMaxLength(max_len)

            # Update counter immediately
            current_len = len(edit.text())
            counter.setText(f"{max_len - current_len}")

            # Rebind textChanged safely
            try:
                edit.textChanged.disconnect()
            except TypeError:
                pass

            edit.textChanged.connect(
                lambda text, name=d.driver_name: self.update_counter(name, text)
            )

    # Update remaining characters counter
    def update_counter(self, name, text):
        d = next(x for x in drivers if x.driver_name == name)
        max_len = self.get_max_characters(d)
        remaining = max_len - len(text)
        self.counters[name].setText(str(remaining))

    # Patch LDA file using user input
    def patch(self):
        replacements = {}

        for name, field in self.inputs.items():
            text = field.text().strip()
            if text:
                replacements[name] = text

        try:
            patch_file(replacements, safe_mode=self.safe_mode_checkbox.isChecked(), game_dir=self.game_dir)
            QMessageBox.information(self, "Success", "Game patched successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    # Close app if dialog boxes are closed
    def clean_exit(self, title=None, message=None):
        if message:
            QMessageBox.critical(self, title, message)
        QApplication.quit()
        self.close()
        sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LDAPatcherGUI()
    win.resize(700, 450)
    win.show()
    QTimer.singleShot(0, win.select_archive)
    sys.exit(app.exec())