from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import random
import math

finalscore = 0

class MathGame(BoxLayout):
    def __init__(self, input_output_app, start_button, **kwargs):
        super(MathGame, self).__init__(**kwargs)
        self.input_output_app = input_output_app 
        self.start_button = start_button
        self.orientation = 'vertical'
        self.score_label = Label(text="Score: 0", size_hint=(1, 1))
        self.timer_label = Label(text="Time: 30", size_hint=(1, 1))
        self.math_problem = Label(text="", size_hint=(1, 2))
        self.answer_input = TextInput(hint_text="Enter your answer", size_hint=(1, 2))
        self.check_button = Button(text="Check Answer", on_press=self.check_answer, size_hint=(1, 2))
        self.add_widget(self.score_label)
        self.add_widget(self.timer_label)
        self.add_widget(self.math_problem)
        self.add_widget(self.answer_input)
        self.add_widget(self.check_button)
        self.score = 0
        self.time_left = 30
        self.is_game_started = False

    def generate_problem(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.answer = num1 + num2
        self.math_problem.text = f"What is {num1} + {num2}?"

    def check_answer(self, instance):
        if not self.is_game_started:
            return

        user_answer = self.answer_input.text
        if user_answer.isdigit() and int(user_answer) == self.answer:
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
        self.answer_input.text = ""
        self.generate_problem()

    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Time: {self.time_left}"
        if self.time_left <= 0:
            self.end_game()

    def start_game(self):
        if not self.is_game_started:
            self.is_game_started = True
            self.start_button.disabled = True
            self.check_button.disabled = False
            self.time_left = 30
            self.score = 0
            self.generate_problem()
            Clock.schedule_interval(self.update_timer, 1)
            self.timer_label.text = f"Time: {self.time_left}"

    def save_score(self):
        global finalscore
        if int(self.score) > int(finalscore):
            finalscore = str(self.score)
        

    def end_game(self):
        self.is_game_started = False
        self.timer_label.text = "Time's up!"
        self.check_button.disabled = True
        self.start_button.disabled = False
        self.save_score()
        self.input_output_app.updatevalues()
        Clock.unschedule(self.update_timer)


class InputOutputApp(App):
    def build(self):

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.input_box = TextInput(hint_text="Deposit Savings (Positive Integers Only)", multiline=False, size_hint=(1, 0.3))
        self.input_box.bind(on_text_validate=self.on_enter)
        self.output_box1 = Label(size_hint=(1, 0.5))
        self.output_box2 = Label(size_hint=(1, 0.5))
        layout.add_widget(self.input_box)
        layout.add_widget(self.output_box1)
        layout.add_widget(self.output_box2)
        start_button = Button(text="Start Math Game", on_press=self.start_math_game, size_hint=(1, 0.3))
        layout.add_widget(start_button)
        self.math_game = MathGame(self, start_button)
        layout.add_widget(self.math_game)

        return layout

    def on_enter(self, instance):
        #Update the text of the output boxes when Enter key is pressed
        #try:
        #    input_text = float(self.input_box.text)
        #    self.output_box1.text = f"Current Amount: £{input_text}  Current Tier: £{math.floor(input_text/10)*10}"
        #    self.updatevalues()
        #except Exception as e:
            
        input_text = int(self.input_box.text)
        self.output_box1.text = f"Current Amount: £{input_text}  Current Tier: £{math.floor(input_text/10)*10}"
        self.updatevalues()

    def updatevalues(self):
        self.output_box2.text = f"Position: {position(int(finalscore))}th  Monthly Winnings: £{conversion(int(self.input_box.text), finalscore)}"

    def start_math_game(self, instance):
        self.math_game.start_game()

def position(score):
    if int(score) >= 15:
        return(1)
    elif int(score) < 15 and int(score) >= 10:
        return(7)
    elif int(score) < 10 and int(score) >= 7:
        return(24)
    elif int(score) < 7 and int(score) >= 5:
        return(57)
    elif int(score) < 5 and int(score) > 0:
        return(73)
    elif int(score) == 0:
        return(100)

def conversion(money, score):
    tier = (money // 10) * 10
    tiertotal = tier*100
    totalwinnings = float((tiertotal*1.035)/12)

    return(round(float((totalwinnings*((1/2)**(position(score))))), 2))

if __name__ == '__main__':
    InputOutputApp().run()
