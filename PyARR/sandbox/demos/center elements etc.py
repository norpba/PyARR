import PySimpleGUI as sg
sg.theme('DarkAmber')  

layout = [ 
        [sg.Text('Enter the value',justification='center',size=(100,1))],
        [sg.Input(justification='center',size=(100,1))],
        [sg.Button('Enter','center',size=(1000,1))]
     ]


window = sg.Window('My new window', layout, size=(500,300), grab_anywhere=True)

while True:
    event, values = window.read()   # Read the event that happened and the values dictionary
    print(event, values)
    if event == None or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
        break
    if event == 'Button':
      print('You pressed the button')
    window.close()