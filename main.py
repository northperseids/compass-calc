import wx
import re

pathToConstants = 'constants.txt'
result = None

def convert(string):
    sections = string.split(' ')
    if sections[0] == "convert":
        arr = []
        for section in sections:
            letters = re.sub(r'[1-9.]', '', section)
            arr.append(letters)
        num = re.sub(r'[A-Za-z!\'\"]\s*', '', string)

        if num != "":

            calcString = float(num)
            if arr[1] == "inch" or arr[1] == "\"":
                if arr[-1] == "mm":
                    return round(calcString * 25.4, 4)
                elif arr[-1] == "cm":
                    return round(calcString * 2.54, 4)
                elif arr[-1] == "feet" or arr[-1] == "ft":
                    return round(calcString / 12, 4)
                elif arr[-1] == "yards":
                    return round(calcString / 36, 4)
                
            if arr[1] == "mm":
                if arr[-1] == "inches" or arr[-1] == "inch":
                    return round(calcString / 25.4, 4)
                elif arr[-1] == "cm":
                    return round(calcString * 10, 4)
                elif arr[-1] == "feet":
                    return round(calcString / 304.8, 4)
                
            if arr[1] == "cm":
                if arr[-1] == "inches" or arr[-1] == "inch":
                    return round(calcString / 2.54, 4)
                elif arr[-1] == "mm":
                    return round(calcString / 10, 4)
                elif arr[-1] == "feet":
                    return round(calcString / 30.48, 4)
                
            if arr[1] == "feet" or arr[1] == "ft" or arr[1] == "\'" or arr[1] == "foot":
                if arr[-1] == "inches" or arr[-1] == "inch":
                    return round(calcString / 12, 4)
                elif arr[-1] == "mm":
                    return round(calcString * 304.8, 4)
                elif arr[-1] == "cm":
                    return round(calcString * 30.48, 4)
                
            if arr[1] == "meter" or arr[1] == "meters" or arr[1] == "m":
                if arr[-1] == "inches" or arr[-1] == "inch":
                    return round(calcString * 39.37, 4)
                elif arr[-1] == "mm":
                    return round(calcString * 1000, 4)
                elif arr[-1] == "feet":
                    return round(calcString * 3.281, 4)
        else:
            calcString = ''
            return calcString
    else:
        return None

class Window(wx.Frame):
    def __init__(self, title):
        super().__init__(parent = None, title = title, style=wx.SYSTEM_MENU|wx.CLOSE_BOX)
        self.panel = wx.Panel(self)

        wrapper = wx.BoxSizer(wx.VERTICAL)

        sizer = wx.FlexGridSizer(rows = 1, cols = 3, vgap = 10, hgap = 10)
        constantsbutton = wx.Button(self.panel, label = 'Const')
        openbutton = wx.Button(self.panel, label = 'Open')
        savebutton = wx.Button(self.panel, label = 'Save')

        sizer.Add(constantsbutton)
        sizer.Add(openbutton)
        sizer.Add(savebutton)

        sizerText = wx.FlexGridSizer(rows = 1, cols = 2, vgap = 5, hgap = 5)
        text_box = wx.TextCtrl(self.panel, style = wx.TE_MULTILINE | wx.TE_DONTWRAP, size = (350,420))
        answersLabel = wx.StaticText(self.panel, label = 'Waiting...')
        sizerText.Add(text_box)
        sizerText.Add(answersLabel)

        def textChanged(e):
            text = text_box.GetValue()
            splitstring = re.split(r'(\n)', text)
            lines = []
            for each in splitstring:
                spl = re.split(r'( )', each)
                lines.append(spl)
            final = []
            result = None
            for each in lines:
                line = ''.join(each)
                # below is where you need to do calculations on each line
                result = convert(line)
                if result == None:
                    num = re.sub(r'[A-Za-z!\'\"]\s*', '', line)
                    if len(line) == 1:
                        final.append(num)
                    elif len(line) > 1 and line[-1] not in ('+', '-', '/', '*', '^','('):
                        try:
                            modified = num.replace('^', '**')
                            resulttotal = eval(str(modified))
                            result = round(resulttotal, 4)
                            final.append(str(result))
                        except SyntaxError:
                            final.append("")
                        except:
                            print('Error!')
                else:
                    final.append(str(result))
            if each[0] == "\n":
                print('fired')
                final.append("\n")
            finalstr = ''.join(final)
        
            answersLabel.SetLabel(finalstr)

        def constantsPressed(e):
            file = open(pathToConstants, 'r')
            constants = file.read()
            dial = wx.Dialog(self, id=-1, title='Constants', size=(500,450))
            dialSizer = wx.BoxSizer(wx.VERTICAL)
            dial.SetSizer(dialSizer)
            text = wx.TextCtrl(dial, value=constants, size=(500,400), style=wx.TE_MULTILINE|wx.TE_DONTWRAP)

            def saveConstants(e):
                f = open(pathToConstants, 'w')
                updatedText=text.GetValue()
                f.write(updatedText)
                f.close()

            saveUpdatedText = wx.Button(dial, label='Save')
            saveUpdatedText.Bind(wx.EVT_BUTTON, saveConstants)

            dialSizer.Add(saveUpdatedText, 0, wx.CENTER)
            dialSizer.Add(text)
            dial.ShowModal()

        def openPressed(e):
            with wx.FileDialog(self, 'Open file', wildcard='TXT files (*.txt)|*.txt', style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as FileDialog:
                if FileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                pathname = FileDialog.GetPath()
                try:
                    with open(pathname, 'r') as f:
                        data = f.read()
                        text_box.SetValue(data)
                except IOError:
                    wx.LogError('Cannot open file.')

        def savePressed(e):
            writeToFile = f'${text_box.GetValue()}'
            with wx.FileDialog(self, 'Save file?', wildcard='TXT files (*.txt)|*.txt', style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as FileDialog:
                if FileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                pathname = FileDialog.GetPath()
                try:
                    with open(pathname, 'w') as file:
                        file.write(writeToFile)
                        file.close()
                except IOError:
                    wx.LogError('Cannot save data.')

        savebutton.Bind(wx.EVT_BUTTON, savePressed)
        openbutton.Bind(wx.EVT_BUTTON, openPressed)
        constantsbutton.Bind(wx.EVT_BUTTON, constantsPressed)
        text_box.Bind(wx.EVT_TEXT, textChanged)

        wrapper.Add(sizer, flag = wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL, border = 5)
        wrapper.Add(sizerText, flag = wx.ALL | wx.EXPAND, border = 5)

        self.panel.SetSizer(wrapper)
        self.SetSize(500,500)

        self.Center()
        self.Show()

app = wx.App()
window = Window("CompassCalc")
app.MainLoop()
