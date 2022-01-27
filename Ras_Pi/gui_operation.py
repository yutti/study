import PySimpleGUI as sg

def read_csv_file():

    # GUI color select
    sg.change_look_and_feel('Light Blue 2')

    layout = [[sg.Text('Data'),
               sg.InputText(' file path', key='-file-'),
               sg.FilesBrowse('Read file', target='-file-', file_types=(('csv file', '.csv'),))],
              [sg.Checkbox('GUI', default=False, key='-GUI-'), sg.Checkbox('Open dir', default=False, key='-DIR-')],
              [sg.Submit(), sg.Cancel()]
              ]

    # Make a window
    window = sg.Window('Charting', layout)  # window title

    # Event operation
    while True:
        event, values = window.read()  # Event read       
        if event in 'Submit':
            break
        if event in ('Cancel', sg.WIN_CLOSED):
            return NULL,NULL,NULL
    window.close()
    Get_file = values['-file-']  # Get file path
    Check_GUI = values['-GUI-']
    Check_DIR = values['-DIR-']
    return Get_file, Check_GUI, Check_DIR
