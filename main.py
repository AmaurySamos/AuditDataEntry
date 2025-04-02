from ttkbootstrap import Window
import Menu 

if __name__ == "__main__":
    
    app = Menu.ttk.Window("Menu", "superhero" ,resizable=(False, False))
    Menu.Menu(app)
    
    app.mainloop()
    
    