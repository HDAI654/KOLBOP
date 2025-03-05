from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from ChatBot.ChatBot import HDAI
from PyQt5.QtTextToSpeech import *
import json

# create text to speech engine
engine = QTextToSpeech()
def text_to_speech(text):
   engine.say(str(text))



class HC_win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.HDAI = HDAI()
        # open bootstrap
        with open("Assets/Databases/bootstrap.css", "r") as f:
            self.bootstrap = f.read()
        
        self.HTML = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        {BootStrap}
        </style>
        </head>
        <body style="background-color: #000000;">

        <div class="container">
        {Messages}
        </div>

        </body>
        </html>
        """

        
        # load saved messages
        with open("Assets/DataBases/HC_saved_messages.json", "r") as f:
            self.saved_messages =  json.load(f)
        
        
        self.UI()
        self.ToolBar()
        self.MessageHtmlMaker()
        
    def UI(self):
        self.main = QWebEngineView()
        self.setCentralWidget(self.main)
    
    def ToolBar(self):
        if not hasattr(self, 'toolbar'):
            self.toolbar = QToolBar("Tools")
            self.toolbar.setMovable(True)
            self.toolbar.setFloatable(True)
            self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
            self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        
            # Clear Messages Action
            self.clear_messages_action = QAction(QIcon(QPixmap("Assets/Images/Clear.png")), "Clear Messages (Ctrl+Shift+Alt+D)",self)
            self.clear_messages_action.setShortcut("Ctrl+Shift+Alt+D")
            self.clear_messages_action.triggered.connect(self.ClearMessages)
            self.toolbar.addAction(self.clear_messages_action)
            
            # Message Input Box
            self.message_input = QLineEdit()
            self.toolbar.addWidget(self.message_input)
            
            # Send Message Action
            self.send_message_action = QAction(QIcon(QPixmap("Assets/Images/Send.png")), "Send Message (Ctrl+Alt+S)",self)
            self.send_message_action.setShortcut("Ctrl+Alt+S")
            self.send_message_action.triggered.connect(self.send_message)
            self.toolbar.addActions([self.send_message_action])
        
        else:
            pass
    
    def MessageHtmlMaker(self):
        HTML = self.HTML
        # Message
        ct = """
        <div class="full-width text-right mb-5">
            <div>
                <div class="card bg-info text-white">
                    <div class="card-body">{C_text}</div>
                </div>
            </div>
        </div>
        """
        # Answer
        clt = """
        <div class="full-width text-left mb-5">
            <div>
                <div class="card bg-dark text-white">
                    <div class="card-body">{CH_text}</div>
                </div>

            </div>
        </div>
        """
        if len(self.saved_messages['messages']) != 0:
            # Messages htmls list
            messages_htmls = []
            for message in self.saved_messages['messages']:
                # Messages
                if message[0] == 0:
                    messages_htmls.append(ct.format(C_text=message[1]))
                # Answers
                else:
                    messages_htmls.append(clt.format(CH_text=message[1]))
            
            # Add new message
            HTML = HTML.format(Messages="\n".join(messages_htmls), BootStrap=self.bootstrap)
            self.main.setHtml(HTML)
        else:
            HTML = HTML.format(Messages=ct.format(C_text="No Message"), BootStrap=self.bootstrap)
            self.main.setHtml(HTML)
         
    def Refresh(self):
        # Destroy All
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, QWidget):
                # delete all except toolbar , action and LineEdit
                if attr_name != 'toolbar' and attr_name != 'send_message_action' and attr_name != 'message_input' and attr_name != 'clear_messages_action':
                    attr.deleteLater()
        # Destroy
        # Remake
        with open("Assets/DataBases/HC_saved_messages.json", "r") as f:
            self.saved_messages =  json.load(f)
        self.UI()
        self.ToolBar()
        self.MessageHtmlMaker()

    def send_message(self):
        # add message to data base
        message = self.message_input.text()
        if message.strip() != "":
            self.saved_messages['messages'].insert(0, [0, str(message)])
            
            # send message to chatbot and get answer
            try:
                answer = self.HDAI.Chat(str(message))
                text_to_speech(answer)
            except :
                answer = "Error"
            
            self.saved_messages['messages'].insert(0, [1, answer])
            
            
            with open("Assets/DataBases/HC_saved_messages.json", "w") as f:
                json.dump(self.saved_messages, f, indent=4)
            self.message_input.clear()    
            self.Refresh()
                
        else:
            text_to_speech("Please Enter A Message")
            self.message_input.clear() 
            self.Refresh()
            
    def Xen(self):
        return self.toolbar
    
    def ClearMessages(self):
        self.saved_messages['messages'] = []
        with open("Assets/DataBases/HC_saved_messages.json", "w") as f:
                json.dump(self.saved_messages, f, indent=4)
        self.Refresh()