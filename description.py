from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
import cv2
from ultralytics import YOLO
from kivy.uix.scrollview import ScrollView

model = YOLO('bestN.pt')
class_names = model.names

Window.clearcolor = (0, 0, 0, 0)
Window.size = (400, 600)


class ObjectDetectionApp(App):
    def build(self):
        self.title = 'camera'
        self.layout = BoxLayout(orientation='vertical')
        self.back_button = Button(text="Back",size_hint=(0.1, 0.1), on_press=self.reset_app)
        self.layout.add_widget(self.back_button)

        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)

        self.cap = cv2.VideoCapture(0)
        self.model = YOLO('bestN.pt')
        self.class_names = self.model.names

        self.prev_buttons = {}
        self.update()
        return self.layout

    def reset_app(self, instance):
        # Clear the widgets added dynamically
        self.layout.clear_widgets()

        # Re-add the back button
        self.layout.add_widget(self.back_button)

        # Re-add the image widget
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)

        # Re-initialize the previous buttons dictionary
        self.prev_buttons = {}

    def show_description(self, instance, cls):
        text_scroll_view = ScrollView(size_hint=(1, None), height=400)
        description = f"{self.class_names[cls]} )"
        if self.class_names[cls] == 'perceuse':
            label_text = 'Une perceuse à colonne est une \nperceuse  d atelier fixée sur un\n bâti ou un établi Elle permet des\n perçages précis et importants \n (diamètres pouvant aller à 20 ou 30\n millimètresdans l acier ordinaire)'
        elif self.class_names[cls] == 'fraiseuse':
            label_text = 'Une fraiseuse est une machine-outil\n' \
                        'utilisée pour usiner des pièces mécaniques\n' \
                        ' en enlevant de la matière à partir de\n' \
                        'blocs ou d ébauches, à l aide d un outil\n' \
                        ' coupant appelé fraise.'
        elif self.class_names[cls] == 'tour parallele':
            label_text = 'Comme ses semblables, celui-ci fait tourner\n une pièce afin d obtenir une pièce finie\n cylindrique (si usinée longitudinalement)'
        else:
            label_text = 'Description not available'

        label = Label(text=label_text, size_hint_y=None, height=100)
        self.layout.add_widget(label)

    def update(self, *args):
        ret, frame = self.cap.read()
        if ret:
            detection_result = self.model(frame)

            for r in detection_result:
                boxes = r.boxes
                for box in boxes:
                    if box.conf > 0.5:
                        for box in boxes:
                            if box.conf > 0.5:
                                x1, y1, x2, y2 = box.xyxy[0]
                                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, f"{self.class_names[int(box.cls)]} {round(float(box.conf), 2)}",
                                    (x1 + 20, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                        cls = int(box.cls)
                        key = f"{cls}"

                        if key not in self.prev_buttons:
                            button = Button(text=f"{self.class_names[cls]}", size_hint=(0.5, 0.2), on_press=lambda instance, cls=cls: self.show_description(instance, cls))
                            self.layout.add_widget(button)
                            self.prev_buttons[key] = button

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image_widget.texture = texture

            self.layout.canvas.ask_update()
            self._app_event = Clock.schedule_once(self.update, 1.0 / 30.0)

    def on_stop(self):
        self.cap.release()


if __name__ == '__main__':
    ObjectDetectionApp().run()
