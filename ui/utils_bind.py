
RELIEF = 'groove'

def bind_mouseover(widget):
    widget.bind('<Enter>', mouse_hoveron)
    widget.bind('<Leave>', mouse_hoveroff)

def mouse_hoveron(event):
    event.widget['background'] = '#aaccff'
    event.widget['relief'] = 'raised'

def mouse_hoveroff(event):
    event.widget['background'] = '#f0f0f0'
    event.widget['relief'] = RELIEF

def bind_mouseclick(widget, callback, radio=None):
    widget.bind('<Button-1>', lambda event: mouse_press(event, callback, radio))
    widget.bind('<Button-3>', lambda event: mouse_press(event, callback, radio))
    widget.bind('<ButtonRelease-1>', mouse_release)
    widget.bind('<ButtonRelease-3>', mouse_release)

def mouse_press(event, callback, radio):
    event.widget['relief'] = 'sunken'
    if radio is None:
        callback(event)
    else:
        callback(event, radio)

def mouse_release(event):
    event.widget['relief'] = 'raised'
