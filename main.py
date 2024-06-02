import wx
import re
import functools

pathToConstants = 'constants.txt'
result = None

def convert(string):
    sections = string.split(' ')
    if sections[0] == "convert" or sections[0] == "cc":
        arr = []
        for section in sections:
            letters = re.sub(r'[1-9.]', '', section)
            arr.append(letters)
        num = re.sub(r'[A-Za-z!\'\"]\s*', '', string)

        if num != "":

            num_to_convert = float(num)
            
            if arr[1] == "inch" or arr[1] == "\"":
                if arr[-1] == "mm":
                    return round(num_to_convert * 25.4, 4)
                elif arr[-1] == "cm":
                    return round(num_to_convert * 2.54, 4)
                elif arr[-1] == "feet" or arr[-1] == "ft":
                    return round(num_to_convert / 12, 4)
                elif arr[-1] == "yards":
                    return round(num_to_convert / 36, 4)
                
            if arr[1] == "mile" or arr[1] == "mi" or arr[1] == "miles":
                if arr[-1] == "km" or arr[-1] == "kilometer":
                    return round(num_to_convert * 1.609, 4)
            
            if arr[1] == "km" or arr[1] == "kilometer" or arr[1] == "kilometers":
                if arr[-1] == "mi" or arr[-1] == "miles" or arr[-1] == "mile":
                    return round(num_to_convert / 1.609, 4)
                
            if arr[1] == "mm":
                if arr[-1] == "inches" or arr[-1] == "inch":
                    return round(num_to_convert / 25.4, 4)
                elif arr[-1] == "cm":
                    return round(num_to_convert * 10, 4)
                elif arr[-1] == "feet":
                    return round(num_to_convert / 304.8, 4)
                
            if arr[1] == "cm":
                if arr[-1] == "inches" or arr[-1] == "inch":
                    return round(num_to_convert / 2.54, 4)
                elif arr[-1] == "mm":
                    return round(num_to_convert / 10, 4)
                elif arr[-1] == "feet":
                    return round(num_to_convert / 30.48, 4)
                
            if arr[1] == "feet" or arr[1] == "ft" or arr[1] == "\'" or arr[1] == "foot":
                if arr[-1] == "inches" or arr[-1] == "inch":
                    return round(num_to_convert / 12, 4)
                elif arr[-1] == "mm":
                    return round(num_to_convert * 304.8, 4)
                elif arr[-1] == "cm":
                    return round(num_to_convert * 30.48, 4)
                
            if arr[1] == "meter" or arr[1] == "meters" or arr[1] == "m":
                if arr[-1] == "inches" or arr[-1] == "inch":
                    return round(num_to_convert * 39.37, 4)
                elif arr[-1] == "mm":
                    return round(num_to_convert * 1000, 4)
                elif arr[-1] == "feet":
                    return round(num_to_convert * 3.281, 4)
                elif arr[-1] == "cm":
                    return round(num_to_convert * 100, 4)
        else:
            num_to_convert = ''
            return num_to_convert
    else:
        return None

def calculate(expression):
    def unstring(string):
        try:
            return float(string)
        except ValueError:
            return None

    def expsplit(exp, op):
        result = []
        braces = 0
        currentChunk = ""
        for i in range(len(exp)):
            current = exp[i]
            if current == '(':
                braces += 1
            elif current == ')':
                braces -= 1
            if braces == 0 and op == current:
                result.append(currentChunk)
                currentChunk = ""
            else:
                currentChunk = currentChunk + current
        if currentChunk != "":
            result.append(currentChunk)
        return result

    def exp_separated(exp):
        number_str = expsplit(exp, '^')
        numbers = []
        for each in number_str:
            if each[0] == '(':
                if each[-1] == ')':
                    subexp = each[1:-1]
                    numbers.append(plus_separated(subexp))
                else:
                    return None
            else:
                numbers.append(unstring(each))
        try:
            result = functools.reduce(lambda x, y: x**y, numbers)
            return result
        except TypeError:
            return None

    def slash_separated(exp):
        number_str = expsplit(exp, '/')
        numbers = list(map(exp_separated, number_str))
        try:
            result = functools.reduce(lambda x, y: x/y, numbers)
            return result
        except TypeError:
            return None

    def mult_separated(exp):
        number_str = expsplit(exp, '*')
        numbers = list(map(slash_separated, number_str))
        try:
            result = functools.reduce(lambda x, y: x*y, numbers)
            return result
        except TypeError:
            return None

    def minus_separated(exp):
        number_str = expsplit(exp, '-')
        numbers = list(map(mult_separated, number_str))
        try:
            result = functools.reduce(lambda x, y: x-y, numbers)
            return result
        except TypeError:
            return None

    def plus_separated(exp):
        number_str = expsplit(exp, '+')
        numbers = list(map(minus_separated, number_str))
        try:
            result = functools.reduce(lambda x, y: x+y, numbers)
            return result
        except TypeError:
            return None

    def format(exp):
        nowhitespaces = exp.replace(' ', '')
        try:
            if nowhitespaces[0] in ['+', '-']:
                nowhitespaces = '0' + nowhitespaces
            answer = plus_separated(nowhitespaces)
            if answer == None:
                return None
            else:
                res = f'{answer:g}'
                return res
        except IndexError:
            return ""
    
    return format(expression)

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
                    if num == '(' or num == '()' or num == ')':
                        pass
                    elif len(line) == 1:
                        final.append(num)
                    elif len(line) > 1 and line[-1] not in ('+', '-', '/', '*', '^','('):
                        answer = calculate(num)
                        if answer == None:
                            final.append('Error!')
                        else:
                            final.append(answer)
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
