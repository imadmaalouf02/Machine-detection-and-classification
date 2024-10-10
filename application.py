#le code de l'application avant l'intégration du projet final représente 90% de notre travail. avec le fichier externe my.kv
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager , Screen
from kivy.base import runTouchApp
from kivy.core.window import Window
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
Window.clearcolor = (0,0,0,0)
Window.size = (400,600)

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass
class ThirdWindow(Screen):
    pass
class Error(Screen):
    pass
class CameraPhone(Screen):
    pass

class MyScreen(Screen):
    pass
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('my.kv')
class MyMainApp(App):
    def build(self):
        self.title='imad'
        return kv
if __name__=='__main__':
    MyMainApp().run()

