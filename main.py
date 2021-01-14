import kivy
kivy.require('1.9.1')

from kivy.app import App as App
from kivy.lang import Builder
from kivy.lang import ParserException
from kivy.core.window import Window
Window.softinput_mode = 'pan'


from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.clock import Clock

import sys

if len(sys.argv) > 1:
    FILE = sys.argv[1]
else:
    FILE = "file.kv"

class VizualizeApp(App):
    
    antigo = """
    Label:
        text: KV Vizualize
        """

    def build(self):
        return ScreenManager()

    def on_start(self):
        Clock.schedule_interval(self.constroi, 1/60)
        
    
    
    def constroi(self, *args):
        try: 
            file = open(FILE, "r")
        except:
            file = open(FILE, "w")
            file.close()
            file = open(FILE, "r")

        novo = file.read()

        if novo == self.antigo:
            return True
        self.antigo = novo
        
        print("nao é igual")
        logs = []
        try:
            self.root.clear_widgets()
            f = self.root.children
            for i in f:
                self.root.remove_widget(i)
            print("filhos antes", self.root.children)
            obj = Builder.load_string(novo)
            
            if issubclass(type(obj), ScreenManager):
               
                filhos = obj.children
                print("aqui", self.root.children)
                for filho in filhos:
                    print("add ", filho)
                    if issubclass(type(filho), Screen):
                        self.root.add_widget(filho)
            
            elif issubclass(type(obj), Screen):
                self.root.add_widget(obj)
            else:
                screen = Screen(name="main")
                screen.add_widget(obj)
                self.root.add_widget(screen)
            print("filhos depois", self.root.children, obj.children)
        
        
        except ParserException as ps:
            logs.append("ParserException\n" + str(ps))
        
        except SyntaxError as se:
            logs.append("SyntaxError\n" + str(se))
        
        except Exception as e:
            logs.append("ERRO!\n"+ "Erro: {} Tipo: {}".format(e, type(e)))
        
        

        if logs:
            box = BoxLayout(orientation="vertical")
            box.padding = ["50sp", "0sp", "0sp", "0sp"]
            for nome in logs:
                label = Label(text = nome)
                label.valign = "middle"
                label.halign = "left"
                
                label.text_size = Window.size
                box.add_widget(label)

            screen = Screen(name="main")
            screen.add_widget(box)
            self.root.add_widget(screen)
            self.root.current = "main"

        

app = None
if __name__ == '__main__':
    app = VizualizeApp()
    app.run()
