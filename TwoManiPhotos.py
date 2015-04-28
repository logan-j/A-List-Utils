from Tkinter import *
import urllib2, PIL, io, pyperclip
from PIL import Image, ImageTk


class Application(Frame):
    
    def reset(self):
        for image in self.images:
            image["bg"] = "light grey"
            image["activebackground"] = "light grey"
            image["text"] = "off"
            self.count = 1
            
            
            
        for item in self.success:
            item[0] = 0
        self.textbox.delete("0.0", END)
        return 'break'
    
    def toggle(self, index):
        button = self.images[index]
        if button["bg"] == "green":
            button["bg"] = "light grey"
            button["activebackground"] = "light grey"
            num = int(button["text"])            
            button["text"] = "off"
            self.success[index][0] = 0
            self.count -= 1
            for item in self.images:
                if item["text"] != "off":
                    try:
                        temp = int(item["text"])
                        if temp > num:
                            temp -= 1
                            item["text"] = temp
                    except Exception as inst:
                        print type(inst)
                        print inst
                    
        else:
            button["bg"] = "green"
            button["activebackground"] = "green"
            button["text"] = self.count
            self.success[index][0] = self.count
            self.count += 1
            
                
    
    def im(self):
        self.contents = [x for x in pyperclip.paste().split("\t") if x != '']
        if(len(self.images) > 0):
            for image in self.images:
                image.grid_forget()
            self.images, self.success = [], []
        
        self.count = 1
        col, rw = 0, 2
        for item in self.contents:
            try:
                url = urllib2.urlopen(item)
                image_file = io.BytesIO(url.read())
                im = Image.open(image_file)
                size = 200,200
                image = im.resize(size, Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                button = Button(
                                image=photo, 
                                text="off", 
                                compound=TOP, 
                                activebackground="light grey",
                                font="Helvetica 16 bold"
                                )
                                
                button["command"] = lambda x=((rw - 2) * 8 + col): self.toggle(x)
                button.image = photo
                button.grid(row = rw, column = col)
                self.images.append(button)
                self.success.append([0, item])
                col +=1
                if col % 8 == 0:
                    col = 0
                    rw += 1
            except Exception as inst:
                print type(inst)
                print inst
                
    def ex(self):
        try:
            temp = self.success
            temp = sorted(temp, key=lambda pair: pair[0])
            while(len(self.success) > 0 and temp[0][0] == 0):
                temp.pop(0)
            out = ("\t".join(str(x[1]) for x in temp))
            #pyperclip.copy(out)

            self.textbox.delete("0.0", END)
            self.textbox.insert(END, out)
            
        except Exception as inst:
            print type(inst)
            print inst
         

    def createWidgets(self):
        self.images, self.success = [], []

        
        self.RESET = Button(self)
        self.RESET["text"] = "RESET"
        self.RESET["fg"]   = "red"
        self.RESET["command"] =  self.reset
        self.RESET["font"] = "bold"
        self.RESET.grid(row = 0, column = 0)
	
        self.load = Button(self)
        self.load["text"] = "LOAD"
        self.load["command"] = self.im
        self.load["font"] = "bold"
        self.load.grid(row = 0, column = 1)
        
        self.export = Button(self)
        self.export["text"] = "EXPORT"
        self.export["command"] = self.ex
        self.export["font"] = "bold"
        self.export.grid(row = 0, column = 2)
        
        self.textbox = Text(height = 1, width = 30)
        self.textbox.grid(row = 1, column = 0)
        self.textbox.insert(END, "")

        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.wm_title("Two Mani Photos")
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    
main()
