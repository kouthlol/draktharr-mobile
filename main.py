"""
DRAKTHARR MOBILE - Versão de Teste
Gradiente Vinho e Preto
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock

class GradientButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.font_size = '16sp'
        self.bold = True
        
        with self.canvas.before:
            self.bg_color = Color(0.5, 0.1, 0.15, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.1, 0.05, 0.08, 1)
        self.foreground_color = (1, 1, 1, 1)
        self.cursor_color = (0.7, 0.2, 0.3, 1)
        self.padding = [15, 15]
        self.font_size = '16sp'
        self.multiline = False


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 5
        self.size_hint_y = None
        self.height = 100
        
        with self.canvas.before:
            Color(0.12, 0.08, 0.1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        scroll = ScrollView(size_hint=(1, 1))
        center_box = BoxLayout(orientation='vertical', padding=30, spacing=15, 
                              size_hint=(0.9, None), height=500, 
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        title = Label(text='[b]DRAKTHARR[/b]', markup=True, font_size='48sp', 
                     size_hint=(1, None), height=80, 
                     color=(0.7, 0.2, 0.3, 1))
        center_box.add_widget(title)
        
        subtitle = Label(text='Discord Message Manager', font_size='14sp', 
                        size_hint=(1, None), height=30, 
                        color=(0.7, 0.7, 0.7, 1))
        center_box.add_widget(subtitle)
        
        email_label = Label(text='Email (Teste)', font_size='14sp', 
                           size_hint=(1, None), height=30, halign='left')
        email_label.bind(size=email_label.setter('text_size'))
        center_box.add_widget(email_label)
        
        self.email_input = StyledTextInput(hint_text='seu@email.com', 
                                          size_hint=(1, None), height=50)
        center_box.add_widget(self.email_input)
        
        pass_label = Label(text='Senha (Teste)', font_size='14sp', 
                          size_hint=(1, None), height=30, halign='left')
        pass_label.bind(size=pass_label.setter('text_size'))
        center_box.add_widget(pass_label)
        
        self.password_input = StyledTextInput(hint_text='••••••••', password=True, 
                                             size_hint=(1, None), height=50)
        center_box.add_widget(self.password_input)
        
        btn_login = GradientButton(text='ENTRAR (TESTE)', size_hint=(1, None), height=50)
        btn_login.bind(on_press=self.do_test_login)
        center_box.add_widget(btn_login)
        
        self.status_label = Label(text='', font_size='12sp', size_hint=(1, None), 
                                 height=60, color=(1, 0.3, 0.3, 1))
        center_box.add_widget(self.status_label)
        
        scroll.add_widget(center_box)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def do_test_login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        
        if not email or not password:
            self.status_label.text = '❌ Preencha todos os campos'
            self.status_label.color = (1, 0.3, 0.3, 1)
            return
        
        self.status_label.text = '✅ Login simulado com sucesso!\nEntrando...'
        self.status_label.color = (0.3, 0.8, 0.3, 1)
        
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'home'), 1)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        self.user_label = Label(text='Olá, Usuário Teste!', font_size='18sp', 
                               halign='left', size_hint=(0.7, 1))
        self.user_label.bind(size=self.user_label.setter('text_size'))
        header.add_widget(self.user_label)
        
        btn_logout = Button(text='Sair', size_hint=(0.3, 1), 
                           background_color=(0.8, 0.2, 0.2, 1))
        btn_logout.bind(on_press=self.logout)
        header.add_widget(btn_logout)
        layout.add_widget(header)
        
        title = Label(text='[b]Conversas de Teste[/b]', markup=True, 
                     font_size='24sp', size_hint=(1, 0.1),
                     color=(0.7, 0.2, 0.3, 1))
        layout.add_widget(title)
        
        scroll = ScrollView(size_hint=(1, 0.65))
        self.chats_list = BoxLayout(orientation='vertical', spacing=10, 
                                   size_hint_y=None, padding=5)
        self.chats_list.bind(minimum_height=self.chats_list.setter('height'))
        
        for i in range(5):
            card = Card()
            
            name = Label(text=f'[b]Conversa Teste {i+1}[/b]', markup=True, 
                        font_size='16sp', size_hint=(1, 0.4), halign='left')
            name.bind(size=name.setter('text_size'))
            card.add_widget(name)
            
            type_label = Label(text='DM', font_size='12sp', 
                             size_hint=(1, 0.3), halign='left', 
                             color=(0.7, 0.7, 0.7, 1))
            type_label.bind(size=type_label.setter('text_size'))
            card.add_widget(type_label)
            
            btn = Button(text='VER DETALHES', size_hint=(1, 0.3),
                        background_color=(0.5, 0.1, 0.15, 1))
            btn.bind(on_press=lambda x, num=i+1: self.show_info(num))
            card.add_widget(btn)
            
            self.chats_list.add_widget(card)
        
        scroll.add_widget(self.chats_list)
        layout.add_widget(scroll)
        
        btn_refresh = GradientButton(text='ATUALIZAR', size_hint=(1, 0.1))
        btn_refresh.bind(on_press=self.refresh)
        layout.add_widget(btn_refresh)
        
        self.add_widget(layout)
    
    def show_info(self, num):
        self.user_label.text = f'📱 Conversa {num} selecionada!'
    
    def refresh(self, instance):
        self.user_label.text = '🔄 Atualizado! (Teste)'
    
    def logout(self, instance):
        self.manager.current = 'login'


class DraktharrApp(App):
    def build(self):
        from kivy.core.window import Window
        Window.clearcolor = (0.05, 0.03, 0.05, 1)
        
        self.title = 'Draktharr'
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        return sm


if __name__ == '__main__':
    DraktharrApp().run()
