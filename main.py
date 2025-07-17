from kivy.app import App
from kivy.uix.label import Label

class FetalWeightApp(App):
    def build(self):
        return Label(text="Fetal Weight Predictor (Replace with your code)")

if __name__ == "__main__":
    FetalWeightApp().run()
