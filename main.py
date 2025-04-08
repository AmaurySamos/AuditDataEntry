from ttkbootstrap import Window
import Menu 

if __name__ == "__main__":
    
    app = Menu.ttk.Window("Menu","darkly",resizable=(False, False))
    Menu.MenuM(app)
    
    app.mainloop()

        