# Utiliser la caméra de l'application pour la détection des machines
import cv2
from ultralytics import YOLO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
from ultralytics import YOLO

model= YOLO('bestN.pt') 
class_names = model.names


#Les dimensions de l'interface 
Window.clearcolor = (0,0,0,0)
Window.size = (400,600)

class ObjectDetectionApp(App):
    def build(self):
        self.title='camera'
        self.layout = BoxLayout(orientation='vertical')

         # Ajouter le widget Image pour afficher les images
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)

        # Initialiser la caméra OpenCV
        self.cap = cv2.VideoCapture(0)

         # Initialiser le modèle YOLO
        self.model = YOLO('bestN.pt')
        self.class_names = self.model.names

        # Planifier la mise à jour de l'image à chaque trame
        self.update()
        return self.layout
    def update(self, *args):

        # Lire la trame de la caméra
        ret, frame = self.cap.read()
        if ret:

            # Effectuer la détection d'objet avec YOLO
            detection_result = self.model(frame)

            # Dessiner des rectangles et du texte sur l'image
            for r in detection_result:

                boxes = r.boxes
                for box in boxes:
                    if box:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"{self.class_names[int(box.cls)]} {round(float(box.conf), 2)}",
                                    (x1 + 20, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
           
            # Mettre à jour l'image dans le widget Image de Kivy
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image_widget.texture = texture
            
            # Planifier la prochaine mise à jour
            self.layout.canvas.ask_update()
            self._app_event = Clock.schedule_once(self.update, 1.0 / 30.0)
    
    def on_stop(self):
        
        # Libérer la capture de la caméra à la fermeture de l'application
        self.cap.release()

if __name__ == '__main__':
    ObjectDetectionApp().run()