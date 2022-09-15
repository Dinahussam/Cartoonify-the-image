import PySimpleGUI as Sg
from cartoonify import MAIN
from image import IMAGE

main = MAIN()
layout = main.components()

window = Sg.Window('Cartoonify Images', layout=layout, font='Helvetica 12 bold italic', icon='Mike.ico', margins=(0, 0),
                   resizable=False, return_keyboard_events=True)

while True:
    try:
        event, values = window.read()
        if event in [None, 'Exit']:
            break

        if event in ('Open (Ctrl+O)', 'o:79'):
            file = main.open_file()
            image = IMAGE(file)
            bio = image.convert()
            window["-IMAGE-"].update(data=bio.getvalue())

        if event == 'Save':
            save_path = Sg.popup_get_file('Save', save_as=True, no_window=True) + '.png'
            main.save_image(save_path)

        if event == 'Cartoonify':
            image.image = main.cartoon(image.image)
            bio = image.convert()
            window["-IMAGE-"].update(data=bio.getvalue())
    except:
        pass