

import wx
import re
import functools
import math

pathToConstants = './constants.txt'
result = None
trig_funcs = ['sin','cos','tan']
operators = ['+','-','*','/','^']

trig_precision = 10
precision = 6

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
                
            if arr[1] == "radian" or arr[1] == "radians" or arr[1] == "rad":
                if arr[-1] == "deg" or arr[-1] == "degrees" or arr[-1] == "°" or arr[-1] == "degree":
                    return round(num_to_convert * 180/3.1416, 4)
            
            if arr[1] == "deg" or arr[1] == "degrees" or arr[1] == "°" or arr[1] == "degree":
                if arr[-1] == "radian" or arr[-1] == "radians" or arr[-1] == "rad":
                    return round(num_to_convert * 3.1416/180, 4)
                
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
    
def expression_split(exp, op):
        result = []
        brackets = 0
        currentChunk = ""
        for char in exp:
            # if character is open-brackets, start recording the in-brackets chunk (see "else" statement at the end of this block);
            # otherwise, if the character is close-brackets, stop recording the in-brackets chunk
            if char == '(':
                brackets += 1
            elif char == ')':
                brackets -= 1
            # if brackets have closed and the next character is the operator, continue the split by sticking the chunk into the result array
            # and reset the currentChunk to empty string.
            if brackets == 0 and op == char:
                result.append(currentChunk)
                currentChunk = ""
            # this is the "record what's in the brackets" bit.
            else:
                currentChunk = currentChunk + char
        # stick chunk into result array if chunk is not empty
        if currentChunk != "":
            result.append(currentChunk)
        return result
    
def arith(expression):

    def unstring(string):
        # this try-except block is more for GUI-handling purposes - the notepad calculator calculates things in real-time so I needed
        # error handling in the case of incomplete expressions (i.e. expressions that are still being typed in). I'm including it just
        # in case that the "return 0" might be messing something up unexpectedly. Probably need to specify an error instead of just a
        # general "except" catcher, but I'm not bothering right this second.
        try:
            return float(string)
        except:
            return 0

    # exponent is LAST CHUNKED, FIRST CALCULATED
    def exponent(exp):
        # split expression along exponent operator, then prepare to calculate each chunk
        number_str = expression_split(exp, '^')
        numbers = []
        for each in number_str:
            # if open-brackets, get the operand and calculate the operand.
            # as I'm reviewing this, I'm trying to bug-test it for weird expressions, I don't know if this breaks if there's too many
            # brackets. ALSO, this is probably where I'd need to put an "if trig, evaluate trig" block so it'll handle if the trig
            # function is included inside brackets.
            if each[0] == '(':
                subexp = each[1:-1]
                # the "addition(subexp)" here technically makes this recursive through the chain - that's how it handles things in brackets
                numbers.append(addition(subexp))
            else:
                numbers.append(unstring(each))
        result = functools.reduce(lambda x, y: x**y, numbers)
        return result

    def division(exp):
        # again, first split expression along operator
        number_str = expression_split(exp, '/')
        # apply exponent-handler to each term in the number string array and return those results as an array itself
        numbers = list(map(exponent, number_str))
        # reduce the resulting numbers array by division
        result = functools.reduce(lambda x, y: x/y, numbers)
        return result

    # same as above but for multiplication, subtraction, addition
    def multiplication(exp):
        number_str = expression_split(exp, '*')
        numbers = list(map(division, number_str))
        result = functools.reduce(lambda x, y: x*y, numbers)
        return result

    def subtraction(exp):
        number_str = expression_split(exp, '-')
        numbers = list(map(multiplication, number_str))
        result = functools.reduce(lambda x, y: x-y, numbers)
        return result

    # ADDITION IS THE FIRST CHUNKED, LAST CALCULATED
    def addition(exp):
        number_str = expression_split(exp, '+')
        numbers = list(map(subtraction, number_str))
        result = functools.reduce(lambda x, y: x+y, numbers)
        return result

    # this is also sorta more GUI-handling shit - since it's a notepad calculator, I want things to be calculated in real-time
    # and in line with notes (I'll send you a screenshot). I'm still working on the text-in-line-with-calculations element.
    def format(exp):
        nowhitespaces = exp.replace(' ', '')
        # this needs to be reworked because it keeps returning "Invalid input" even on text-only lines, which is just annoying.
        if len(nowhitespaces) == 0:
            return ''
        else:
            # handle scientific notation
            if "e-" in nowhitespaces:
                nowhitespaces = nowhitespaces.replace("e-", "*10^-")
            if "e+" in nowhitespaces:
                nowhitespaces = nowhitespaces.replace("e-", "*10^")
            to_calc = []
            already_recorded = []
            for i, char in enumerate(nowhitespaces):
                try:
                    # negative number handling
                    if nowhitespaces[i] in ['+','-','*','/','^','('] and nowhitespaces[i+1] == "-":
                        rest_of_string = nowhitespaces[i+2:]
                        num_term = re.match(r"([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[Ee]([+-]?\d+))?", rest_of_string).group()
                        new_term = f'{nowhitespaces[i]}(0-{num_term})'
                        to_calc.append(new_term)
                        for j in range(i, i+len(num_term)+2):
                            already_recorded.append(j)
                    elif i not in already_recorded:
                        to_calc.append(char)
                except IndexError:
                    pass
            newstr = ''.join(to_calc)
            if newstr[0] in ['+', '-']:
                newstr = '0' + newstr
            answer = addition(newstr)
            return f"{answer}"
    
    return format(expression)

def trig(exp):

    # split expression along any of the basic trig functions
    split_expression = re.split(r'(sin|cos|tan)', exp)

    to_calc = []
    term = 0

    # for each piece in the split expression:
    for i, entry in enumerate(split_expression):

        if entry == 'sin':

            rest_of_string = exp[i+2:]
            
            result = []
            brackets = 0
            chunk = ''
            for char in rest_of_string:
                if char == '(':
                    brackets += 1
                elif char == ")":
                    brackets -= 1
                if brackets == 0:
                    try:
                        if chunk[0] == '(':
                            chunk = chunk[1:]
                        result.append(chunk)
                        chunk = ''
                        break
                    except:
                        pass
                else:
                    chunk = chunk + char
            term = ''.join(result)

            if any(tr in term for tr in trig_funcs):
                newterm = calculate(term)
                res = round(math.sin(float(newterm)), trig_precision)
                to_calc.append(arith(str(res)))
                break
            elif any(op in term for op in operators):
                newterm = arith(term)
                res = round(math.sin(float(newterm)), trig_precision)
                to_calc.append(arith(str(res)))
                break
            else:
                res = round(math.sin(float(term)), trig_precision)
                to_calc.append(arith(str(res)))

        # repeat above for both cos and tan

        if entry == 'cos':
            rest_of_string = exp[i+2:]
            
            result = []
            brackets = 0
            chunk = ''
            for char in rest_of_string:
                if char == '(':
                    brackets += 1
                elif char == ")":
                    brackets -= 1
                if brackets == 0:
                    try:
                        if chunk[0] == '(':
                            chunk = chunk[1:]
                        result.append(chunk)
                        chunk = ''
                        break
                    except:
                        pass
                else:
                    chunk = chunk + char
            term = ''.join(result)

            if any(tr in term for tr in trig_funcs):
                newterm = calculate(term)
                res = round(math.cos(float(newterm)), trig_precision)
                to_calc.append(arith(str(res)))
                break
            elif any(op in term for op in operators):
                newterm = arith(term)
                res = round(math.cos(float(newterm)), trig_precision)
                to_calc.append(arith(str(res)))
                break
            else:
                res = round(math.cos(float(term)), trig_precision)
                to_calc.append(arith(str(res)))
                
        if entry == 'tan':
            rest_of_string = exp[i+2:]
            
            result = []
            brackets = 0
            chunk = ''
            for char in rest_of_string:
                if char == '(':
                    brackets += 1
                elif char == ")":
                    brackets -= 1
                if brackets == 0:
                    try:
                        if chunk[0] == '(':
                            chunk = chunk[1:]
                        result.append(chunk)
                        chunk = ''
                        break
                    except:
                        pass
                else:
                    chunk = chunk + char
            term = ''.join(result)

            if any(tr in term for tr in trig_funcs):
                newterm = calculate(term)
                res = round(math.tan(float(newterm)), trig_precision)
                to_calc.append(arith(str(res)))
                break
            elif any(op in term for op in operators):
                newterm = arith(term)
                res = round(math.tan(float(newterm)), trig_precision)
                to_calc.append(arith(str(res)))
                break
            else:
                res = round(math.tan(float(term)), trig_precision)
                to_calc.append(arith(str(res)))
    
    termindex = exp.find(str(term)) + len(str(term))
    rest_of_string2 = exp[termindex+1:]
    to_calc.append(rest_of_string2)

    newstr = ''.join(to_calc)
    return calculate(newstr)
    
def calculate(line):
    # need to redo regex to leave in trig functions but strip out everything else
    expression = ''.join(re.findall(r"[0-9]+\.*|[0-9]+|sin.*[0-9]+\)|cos.*[0-9]+\)|tan.*[0-9]+\)|\+|-|\*|/|\^|e-|e\+|\(|\)", line))
    if expression == '(' or expression == '()' or expression == ')':
        pass
    elif len(line) == 1:
        return expression
    elif any(tr in expression for tr in trig_funcs):
        return trig(expression)
    elif len(line) > 1 and line[-1] not in ('+', '-', '/', '*', '^','('):
        answer = arith(expression)
        if answer == None:
            return "Error!"
        elif answer == '':
            return ''
        else:
            return f'{answer}'

class Window(wx.Frame):
    def __init__(self, title):
        super().__init__(parent = None, title = title, style=wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.STAY_ON_TOP)
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
                    answer = calculate(line)
                    if answer == None:
                        final.append('')
                    else:
                        if len(str(answer)) > precision:
                            answer = f'{round(float(answer), precision)}...'
                        final.append(str(answer))
                else:
                    if len(str(result)) > precision:
                        result = f'{round(float(result), precision)}...'
                    final.append(str(result))
                if each[0] == "\n":
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
