from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image  
import re
import handle
import jsonapirequest as jar
import urllib

hwnd = {
    'name':'Visual Novel Text Capture',
    'ver':'0.1a',
    'width':512,
    'maxwidth':720,
    'height':312,
    'maxheight':800,
    'x':0,
    'y':0
}
#Basic window settings

root = Tk()

#Setting up window
root.title('{} version {}'.format(hwnd['name'],hwnd['ver']))
root.geometry('{}x{}'.format(hwnd['width'],hwnd['height']))
root.minsize(hwnd['width'], hwnd['height'])
root.maxsize(hwnd['maxwidth'], hwnd['maxheight'])
mainbgImg = ImageTk.PhotoImage(Image.open('extra/_image_cover.png', 'r'))


root.wm_attributes('-toolwindow', 'True')
root.configure(background='#1e1e1e')
def main_ui():
    root.geometry('{}x{}'.format(hwnd['width'],hwnd['height']))
    root.resizable(False, False)
  
    def receive_dd_value(eventObj):
        dropDownData.get()
    mainFrame = Frame(root, bg='#252526')
    
    bgImgFrame = ttk.Label(mainFrame, image=mainbgImg, border=None)
    bgImgFrame.place(x=(root.winfo_width() - (mainbgImg.width() / 2)),y=(root.winfo_height() - (mainbgImg.height() / 2)))
    bgImgFrame.pack()

    textTitleC = ttk.Label(mainFrame, text='Visual Novel Text Capture Ver {}'.format(hwnd['ver']))
    textTitleC.place(x=(root.winfo_width() - (mainbgImg.width() / 2)),y=(root.winfo_height() - (mainbgImg.height() / 2)))
    textTitleC.configure(border=0, background='#1e1e1e', foreground='white', font='Courier 10')
    textTitleC.pack(side='top', pady=10)

    dropDownData = StringVar()
    textWindowC = ttk.Label(mainFrame, text='Current Window Available', background='white')
    textWindowC.configure(border=0, background='#1e1e1e', foreground='white', font='Courier 9')
    textWindowC.pack(padx=10, side='left')
    wnd_list_full  = handle.get_active_windows()
    windowsDropDown = ttk.Combobox(mainFrame, values=wnd_list_full, textvariable=dropDownData).pack(side='left')

    buttonWindowC = Button(mainFrame, text='Confirm', command= lambda :_next_window(dropDownData.get()))
    buttonWindowC.configure(border=0, background='#1e1e1e', foreground='white', font='Courier 9')
    buttonWindowC.pack(padx=10, side='left')
    def _next_window(wnd):
        wnd = re.sub(r'pid\(\d+\)', '', wnd )
        if handle._get_active_window(wnd) and len(wnd) != 0:
           _clean_window()
           vn_capture_ui(wnd)
        else:
            return False

    root.bind("<<ComboboxSelected>>", receive_dd_value)
    mainFrame.pack(fill='x', expand=False)

#User Interface for client
def vn_capture_ui(wnd):
    #VN Frame & Size change
    root.resizable(True, True)
    root.geometry('{}x{}'.format(hwnd['maxwidth'],hwnd['maxheight']))

    '''
        BEGIN CODE: LEFT SIDE
    '''
    left_frame = Frame(root)

    def get_entry_value(eventObj):
        #Checks if entry has special characters
        s_Char = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
        if(s_Char.search(entry_data.get()) == None): 
            pass
        else: 
            return 
        
        word_json = jar.Request.find_word(entry_data.get())
        #Arranges each label data from bottom to the top
        for labels in range(4, 0, -1):#Arrange stage
            jisho_label[labels].config(text=jisho_label[labels-1]['text'])
        #Issue: When you search a word, it may only have reading and not a word(kanji) FIXED 
        #This looks hella long but how else im suppose to deserialize other than to create an object class for it which im lazy.
        jp_word = word_json[0]['japanese'][0].get('word') or ''
        jp_hiragana = word_json[0]['japanese'][0].get('reading') or ''
        jp_jlpt = word_json[0]['jlpt'][0] if word_json[0]['jlpt'] else ''
        jp_pos = word_json[0]['senses'][0].get('parts_of_speech') or ''
        jp_definition = word_json[0]['senses'][0].get('english_definitions') or ''

        jisho_label[0].config(text='{}[{}]\n{}\n{}\n{}'.format(
            jp_word,
            jp_hiragana, 
            jp_jlpt,
            jp_pos,  
            jp_definition
        ))
            
        
            
    
    #---Jisho API Widgets---
    jisho_label = Label(left_frame, text='Jisho-API')
    jisho_label.config(background='#252526', foreground='lightgreen', font='Courier 10')
    jisho_label.pack(fill='x')

    entry_data = StringVar()
    jisho_text_input = Entry(left_frame, textvariable=entry_data)
    jisho_text_input.pack()
    root.bind('<Return>', get_entry_value)
    jisho_text_input.update()
    #750px of space
    jisho_label = []#There are only 5 label boxes
    for x in range(5):
        w = Label(left_frame, justify='left', wraplength=200, height=5,text='', width=20, borderwidth=3, relief='solid')
        w.config(background='#252526', foreground='white', font='Courier 10')
        w.pack(anchor='w', fill='x', expand=True)
        jisho_label.append(w)

    
    return_button = Button(left_frame, text='Return\nMenu', command=lambda : return_menu())
    return_button.configure(border=0, background='#1e1e1e', foreground='white', font='Courier 9')
    return_button.pack(side='left', anchor='sw', fill='x', expand=True)
    return_button.update()
    
    left_frame.pack(side='left')
    
    '''
        END CODE: LEFT SIDE
        BEGIN CODE: RIGHT SIDE
    '''
    right_frame = Frame(root, bg='#252526', width=hwnd['width'], height=hwnd['maxheight'])

    #Main picture that is ocr/screnshotted and translated
    vnTempImg = ImageTk.PhotoImage(Image.open('temp/temp.jpg').resize((hwnd['width'], int(hwnd['maxheight']/2))))
    vncWndImg = ttk.Label(right_frame, image=vnTempImg)
    vncWndImg.image = vnTempImg #This ensures the image is saved before it is sent into garbage collection
    vncWndImg.config(background='black', border=0)
    vncWndImg.pack()

    #Code Line: Main Label & Buttons
    wndTitle = ttk.Label(right_frame, text=wnd).pack()
    scrButton = Button(right_frame, text='Screenshot', command=lambda : screenshot_to_translate(wnd))
    scrButton.configure(border=5, relief='flat', background='#1e1e1e', foreground='white', font='Courier 9')
    scrButton.pack(side='top', pady=10)

    #Functions for screenshotting and placing translated text on labels
    def screenshot_to_translate(wnd):
        handle.screenshot_current_window(wnd)
        ocr_text_jp, ocr_text_en = handle.translate_text()
        nextTempImg = ImageTk.PhotoImage(Image.open('temp/temp.jpg').resize((hwnd['width'], int(hwnd['maxheight']/2))))
        vncWndImg.configure(image=nextTempImg)
        vncWndImg.image = nextTempImg
        jpText.delete('1.0', 'end')
        jpText.insert('1.0', ocr_text_jp)
        enText.delete('1.0', 'end')
        enText.insert('1.0', ocr_text_en)

    '''
    ------Code Line:Japanese and English Text Widgets------
    '''
    jpText = Text(right_frame, width=50, height=3)
    enText = Text(right_frame, width=50, height=3)
    jpText.config(border=0, background='#1e1e1e', foreground='white')
    enText.config(border=0, background='#1e1e1e', foreground='white')
    
    jpTextLabel = ttk.Label(right_frame, text='Japanese Text')
    jpTextLabel.config(background='#252526', foreground='white', font='Courier 10')
    jpTextLabel.pack(anchor='w')
    jpText.pack(anchor='w', padx=15)

    enTextLabel = ttk.Label(right_frame, text='English Text')
    enTextLabel.config(background='#252526', foreground='white', font='Courier 10',)
    enTextLabel.pack(anchor='w')
    enText.pack(anchor='w', padx=15)
    '''
    ------Code Line END:Japanese and English Text Widgets------
    '''
    '''
        END CODE: RIGHT SIDE
    '''

    right_frame.pack(fill='y',expand=True)

def _clean_window():
    for child in root.winfo_children():
        child.destroy()
def return_menu():
    _clean_window()
    main_ui()

if __name__ == '__main__': 
    main_ui()
root.mainloop()