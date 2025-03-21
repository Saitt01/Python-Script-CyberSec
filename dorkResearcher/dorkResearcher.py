### IMPORTING LIBRARIES ###
import sys                         
import webbrowser
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QFileDialog, QCheckBox

### DICTIONARY FOR FILTERING SYSTEM ###
dorks = {
    "None": "",
    "Login Pages": "inurl:login",
    "Admin Panels": "inurl:admin",
    "Error Messages (SQLi)": '"You have an error in your SQL syntax"',
    "Exposed Directories": "intitle:index.of",
    "Sensitive Files": "ext:log OR ext:txt OR ext:sql OR ext:env",
    "Backup Files": "ext:bak OR ext:old OR ext:swp",
    "WordPress Config": "inurl:wp-config OR ext:env OR ext:ini",
    "Email Lists": "filetype:xls OR filetype:csv OR filetype:txt intext:@",
    "Public Camera Feeds": "inurl:/view.shtml OR inurl:/webcam.html OR inurl:/live.html"
}

countries = {
    "None": "",
    "Italy 🇮🇹": "site:.it",
    "France 🇫🇷": "site:.fr",
    "Germany 🇩🇪": "site:.de",
    "Spain 🇪🇸": "site:.es",
    "UK 🇬🇧": "site:.uk",
    "USA 🇺🇸": "site:.us",
    "Canada 🇨🇦": "site:.ca",
    "Australia 🇦🇺": "site:.au",
    "Japan 🇯🇵": "site:.jp",
    "India 🇮🇳": "site:.in"
}

date_filters = {
    "Any time": "",
    "Last 24 hours": "&tbs=qdr:d",
    "Last week": "&tbs=qdr:w",
    "Last month": "&tbs=qdr:m",
    "Last year": "&tbs=qdr:y",
}

file_types = {
    "None": "",
    "PDF": "filetype:pdf",
    "Excel": "filetype:xlsx",
    "Word": "filetype:doc OR filetype:docx",
    "JSON": "filetype:json",
    "XML": "filetype:xml",
    "SQL": "filetype:sql",
}

search_engines = {
    "Google": "https://www.google.com/search?q=",
    "Bing": "https://www.bing.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/?q=",
}


### MAIN CLASS - DEFING THE GUI AND ITS LOGIC ###
class DorkResearcher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()          #Built the GUI
        self.history = []      #Starts an empty list for saving the history reasearch in case

    def initUI(self):                                   #In this function it's build the GUI and its elements
        self.setWindowTitle("DORK RESEARCHER")          #Title
        self.setGeometry(100, 100, 500, 500)            #Set initial position and dimension of the GUI

        layout = QVBoxLayout()                          #Set the layout vertically

        self.label1 = QLabel("Select Search Engine:")           #Label
        layout.addWidget(self.label1)
        self.engineDropdown = QComboBox()                       #Drop-down menu
        self.engineDropdown.addItems(search_engines.keys())     
        layout.addWidget(self.engineDropdown)

        self.label2 = QLabel("Select Dork Type:")
        layout.addWidget(self.label2)
        self.dorkDropdown = QComboBox()
        self.dorkDropdown.addItems(dorks.keys())
        layout.addWidget(self.dorkDropdown)

        self.label3 = QLabel("Target Domain, IP or Keywords (optional):")
        layout.addWidget(self.label3)
        self.domainInput = QLineEdit()                          #Input 
        layout.addWidget(self.domainInput)

        self.label4 = QLabel("Additional Search Term (optional):")
        layout.addWidget(self.label4)
        self.searchInput = QLineEdit()
        layout.addWidget(self.searchInput)

        self.label5 = QLabel("Select Country (for website filtering):")
        layout.addWidget(self.label5)
        self.countryDropdown = QComboBox()
        self.countryDropdown.addItems(countries.keys())
        layout.addWidget(self.countryDropdown)

        self.label6 = QLabel("Select Date Filter:")
        layout.addWidget(self.label6)
        self.dateDropdown = QComboBox()
        self.dateDropdown.addItems(date_filters.keys())
        layout.addWidget(self.dateDropdown)

        self.label7 = QLabel("Select File Type (optional):")
        layout.addWidget(self.label7)
        self.fileDropdown = QComboBox()
        self.fileDropdown.addItems(file_types.keys())
        layout.addWidget(self.fileDropdown)

        self.multiSearchCheck = QCheckBox("Open Multiple Dorks - for executing all type of dorks(suggested for a specific target)")
        layout.addWidget(self.multiSearchCheck)                 

        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.run_search)      #Button
        layout.addWidget(self.searchButton)

        self.saveButton = QPushButton("Save Search History")
        self.saveButton.clicked.connect(self.save_history)
        layout.addWidget(self.saveButton)

        self.setLayout(layout)         #Set this layout

    ### FUNCTION TO CREATE THE DORKS STRING. OPENING IT ON THE BROWSER AND SAVING THE HISTORY ###
    def run_search(self):
        target = self.domainInput.text().strip()                              #TARGET
        search_term = self.searchInput.text().strip()                         #ADDITIONAL WORDS
        country_filter = countries[self.countryDropdown.currentText()]
        date_filter = date_filters[self.dateDropdown.currentText()]
        file_type = file_types[self.fileDropdown.currentText()]
        search_engine = search_engines[self.engineDropdown.currentText()]

        #FUNCTION FOR GIVING PRIORITIES TO CONDICTIONS
        def format_dork(dork):
            if " OR " in dork or "|" in dork:
                dork = dork.replace("|", "OR")
                return f"({dork})"
            return dork

        #DORKS STRING BUILDER
        def build_query(dork_key, dork_val):
            parts = []   #List for building it

            dork_core = format_dork(dork_val)
            if dork_core:
                parts.append(dork_core)

            if target:
                if "." in target or target.startswith("http"):   #if is 127.0.0.1 or http/https
                    parts.append(f"site:{target}")
                else:
                    parts.append(f"intext:{target}")

            if search_term:
                parts.append(f"intext:{search_term}")

            if country_filter:
                parts.append(country_filter)

            if file_type:
                parts.append(file_type)

            query = " ".join(parts).strip()                      #Sum all in one string
            search_url = f"{search_engine}{query}{date_filter}"
            return query, search_url

        ###IF MULTI SEARCH:
        if self.multiSearchCheck.isChecked():                    
            for dork_name, dork_query in dorks.items():                 #For every dorks of the list, build a query
                query, search_url = build_query(dork_name, dork_query)
                webbrowser.open(search_url)                             #And open it on browser
                self.history.append({                                   #Save then the history
                    "Engine": self.engineDropdown.currentText(),
                    "Dork": dork_name,
                    "Query": query,
                    "URL": search_url
                })
        ###ELSE ONLY THE SELECTED ONE:
        else:                                                               
            selected_dork = dorks[self.dorkDropdown.currentText()]
            dork_key = self.dorkDropdown.currentText()
            query, search_url = build_query(dork_key, selected_dork)
            webbrowser.open(search_url)
            self.history.append({
                "Engine": self.engineDropdown.currentText(),
                "Dork": dork_key,
                "Query": query,
                "URL": search_url
            })

    def save_history(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
        if file_name:
            df = pd.DataFrame(self.history)         #Dataframe convertion with pandas
            df.to_csv(file_name, index=False)       #Daving it .csv
            print("History saved successfully!")    #Show terminal result

###STARTING OF THE GUI:
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DorkResearcher()
    ex.show()
    sys.exit(app.exec_())
