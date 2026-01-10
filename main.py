"""
DRAKTHARR MOBILE - Selfbot Discord
Deletar mensagens automaticamente
Tema: Vinho e Preto
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
import requests
import json
import os
import time
from threading import Thread

# ==================== API DISCORD ====================

class DiscordAPI:
    BASE_URL = "https://discord.com/api/v10"
    
    @staticmethod
    def validate_token(token):
        """Valida o token e retorna informações do usuário"""
        headers = {'Authorization': token}
        try:
            response = requests.get(f"{DiscordAPI.BASE_URL}/users/@me", 
                                   headers=headers, timeout=10)
            if response.status_code == 200:
                user_info = response.json()
                return {'success': True, 'token': token, 'user': user_info}
            return {'success': False, 'error': 'Token inválido'}
        except Exception as e:
            return {'success': False, 'error': f'Erro: {str(e)}'}
    
    @staticmethod
    def get_dms(token):
        """Busca todas as DMs do usuário"""
        headers = {'Authorization': token}
        try:
            response = requests.get(f"{DiscordAPI.BASE_URL}/users/@me/channels", 
                                   headers=headers, timeout=10)
            if response.status_code == 200:
                channels = response.json()
                return [ch for ch in channels if ch.get('type') in [1, 3]]
            return []
        except:
            return []
    
    @staticmethod
    def get_messages(channel_id, token, limit=100):
        """Busca mensagens de um canal"""
        headers = {'Authorization': token}
        try:
            response = requests.get(
                f"{DiscordAPI.BASE_URL}/channels/{channel_id}/messages?limit={limit}", 
                headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    @staticmethod
    def delete_message(channel_id, message_id, token):
        """Deleta uma mensagem específica"""
        headers = {'Authorization': token}
        try:
            response = requests.delete(
                f"{DiscordAPI.BASE_URL}/channels/{channel_id}/messages/{message_id}", 
                headers=headers, timeout=10)
            return response.status_code == 204
        except:
            return False


class DataManager:
    """Gerencia armazenamento local de dados"""
    
    @staticmethod
    def get_data_path():
        try:
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), "user_data.json")
        except:
            return "user_data.json"
    
    @staticmethod
    def save_token(token, user_info):
        try:
            filepath = DataManager.get_data_path()
            with open(filepath, 'w') as f:
                json.dump({'token': token, 'user': user_info}, f)
            return True
        except:
            return False
    
    @staticmethod
    def load_token():
        try:
            filepath = DataManager.get_data_path()
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except:
            pass
        return None
    
    @staticmethod
    def clear_data():
        try:
            filepath = DataManager.get_data_path()
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        except:
            return False


# ==================== COMPONENTES ====================

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


# ==================== TELAS ====================

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        scroll = ScrollView(size_hint=(1, 1))
        center_box = BoxLayout(orientation='vertical', padding=30, spacing=15, 
                              size_hint=(0.9, None), height=600, 
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        # Título
        title = Label(text='[b]DRAKTHARR[/b]', markup=True, font_size='48sp', 
                     size_hint=(1, None), height=80, 
                     color=(0.7, 0.2, 0.3, 1))
        center_box.add_widget(title)
        
        subtitle = Label(text='Discord Selfbot - Delete Messages', font_size='14sp', 
                        size_hint=(1, None), height=30, 
                        color=(0.7, 0.7, 0.7, 1))
        center_box.add_widget(subtitle)
        
        # Campo Token
        token_label = Label(text='Discord Token', font_size='14sp', 
                           size_hint=(1, None), height=30, halign='left')
        token_label.bind(size=token_label.setter('text_size'))
        center_box.add_widget(token_label)
        
        self.token_input = StyledTextInput(hint_text='Cole seu token aqui', 
                                          size_hint=(1, None), height=50)
        center_box.add_widget(self.token_input)
        
        # Botão Login
        btn_login = GradientButton(text='ENTRAR', size_hint=(1, None), height=50)
        btn_login.bind(on_press=self.do_login)
        center_box.add_widget(btn_login)
        
        # Botão Tutorial
        btn_help = Button(text='❓ Como obter token', size_hint=(1, None), height=50, 
                         background_color=(0.3, 0.3, 0.4, 1))
        btn_help.bind(on_press=self.show_token_help)
        center_box.add_widget(btn_help)
        
        # Status
        self.status_label = Label(text='', font_size='12sp', size_hint=(1, None), 
                                 height=80, color=(1, 0.3, 0.3, 1))
        center_box.add_widget(self.status_label)
        
        scroll.add_widget(center_box)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def on_enter(self):
        """Auto-login se já tiver token salvo"""
        data = DataManager.load_token()
        if data and data.get('token'):
            user_info = DiscordAPI.validate_token(data['token'])
            if user_info.get('success'):
                self.manager.current_token = data['token']
                self.manager.current_user = user_info['user']
                self.manager.current = 'home'
    
    def do_login(self, instance):
        token = self.token_input.text.strip()
        
        if not token:
            self.status_label.text = '❌ Cole seu token'
            return
        
        self.status_label.text = '🔄 Validando token...'
        self.status_label.color = (0.9, 0.7, 0.3, 1)
        Thread(target=self._login_thread, args=(token,), daemon=True).start()
    
    def _login_thread(self, token):
        result = DiscordAPI.validate_token(token)
        Clock.schedule_once(lambda dt: self._handle_login_result(result))
    
    def _handle_login_result(self, result):
        if result['success']:
            DataManager.save_token(result['token'], result['user'])
            self.manager.current_token = result['token']
            self.manager.current_user = result['user']
            self.status_label.text = '✅ Login bem-sucedido!'
            self.status_label.color = (0.3, 0.8, 0.3, 1)
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'home'), 1)
        else:
            self.status_label.text = f"❌ {result['error']}"
            self.status_label.color = (1, 0.3, 0.3, 1)
    
    def show_token_help(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        scroll = ScrollView(size_hint=(1, 0.9))
        help_text = Label(
            text='[b]Como obter seu token:[/b]\n\n'
                 '1. Abra Discord no navegador\n'
                 '2. Faça login normalmente\n'
                 '3. Pressione F12 (DevTools)\n'
                 '4. Vá na aba "Console"\n'
                 '5. Cole este código:\n\n'
                 '[color=00ff00](webpackChunkdiscord_app.push([[\'\'  ],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()[/color]\n\n'
                 '6. Copie o resultado\n'
                 '7. Cole no campo Token acima!\n\n'
                 '[color=ff6666]⚠️ NUNCA compartilhe seu token![/color]',
            markup=True,
            font_size='14sp',
            size_hint_y=None,
            halign='left'
        )
        help_text.bind(width=lambda *x: setattr(help_text, 'text_size', (help_text.width, None)))
        help_text.bind(texture_size=lambda *x: setattr(help_text, 'height', help_text.texture_size[1]))
        scroll.add_widget(help_text)
        content.add_widget(scroll)
        
        btn_ok = GradientButton(text='ENTENDI', size_hint=(1, 0.1))
        popup = Popup(title='Tutorial: Obter Token', content=content, size_hint=(0.95, 0.8))
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        
        popup.open()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        self.user_label = Label(text='Carregando...', font_size='18sp', 
                               halign='left', size_hint=(0.7, 1))
        self.user_label.bind(size=self.user_label.setter('text_size'))
        header.add_widget(self.user_label)
        
        btn_logout = Button(text='Sair', size_hint=(0.3, 1), 
                           background_color=(0.8, 0.2, 0.2, 1))
        btn_logout.bind(on_press=self.logout)
        header.add_widget(btn_logout)
        layout.add_widget(header)
        
        # Título
        title = Label(text='[b]Gerenciar Mensagens[/b]', markup=True, 
                     font_size='24sp', size_hint=(1, 0.1),
                     color=(0.7, 0.2, 0.3, 1))
        layout.add_widget(title)
        
        # Lista de conversas
        scroll = ScrollView(size_hint=(1, 0.65))
        self.chats_list = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=5)
        self.chats_list.bind(minimum_height=self.chats_list.setter('height'))
        scroll.add_widget(self.chats_list)
        layout.add_widget(scroll)
        
        # Botão atualizar
        btn_refresh = GradientButton(text='ATUALIZAR CONVERSAS', size_hint=(1, 0.1))
        btn_refresh.bind(on_press=self.load_chats)
        layout.add_widget(btn_refresh)
        
        self.add_widget(layout)
    
    def on_enter(self):
        if hasattr(self.manager, 'current_user'):
            user = self.manager.current_user
            self.user_label.text = f"Olá, {user.get('username', 'Usuário')}!"
            self.load_chats(None)
    
    def load_chats(self, instance):
        self.chats_list.clear_widgets()
        loading = Label(text='🔄 Carregando conversas...', size_hint_y=None, height=40)
        self.chats_list.add_widget(loading)
        Thread(target=self._load_chats_thread, daemon=True).start()
    
    def _load_chats_thread(self):
        dms = DiscordAPI.get_dms(self.manager.current_token)
        Clock.schedule_once(lambda dt: self._display_chats(dms))
    
    def _display_chats(self, dms):
        self.chats_list.clear_widgets()
        
        if not dms:
            label = Label(text='Nenhuma conversa encontrada', size_hint_y=None, height=40)
            self.chats_list.add_widget(label)
            return
        
        for dm in dms:
            card = Card()
            
            if dm.get('type') == 1:
                recipient = dm.get('recipients', [{}])[0]
                chat_name = recipient.get('username', 'Desconhecido')
                chat_type = 'DM'
            else:
                chat_name = dm.get('name', 'Grupo sem nome')
                chat_type = 'Grupo'
            
            name_label = Label(text=f'[b]{chat_name}[/b]', markup=True, 
                             font_size='16sp', size_hint=(1, 0.4), halign='left')
            name_label.bind(size=name_label.setter('text_size'))
            card.add_widget(name_label)
            
            type_label = Label(text=chat_type, font_size='12sp', 
                             size_hint=(1, 0.3), halign='left', 
                             color=(0.7, 0.7, 0.7, 1))
            type_label.bind(size=type_label.setter('text_size'))
            card.add_widget(type_label)
            
            btn_delete = Button(text='APAGAR MINHAS MENSAGENS', size_hint=(1, 0.3),
                              background_color=(0.9, 0.3, 0.3, 1))
            btn_delete.bind(on_press=lambda x, channel=dm: self.confirm_delete(channel))
            card.add_widget(btn_delete)
            
            self.chats_list.add_widget(card)
    
    def confirm_delete(self, channel):
        channel_id = channel['id']
        
        if channel.get('type') == 1:
            recipient = channel.get('recipients', [{}])[0]
            chat_name = recipient.get('username', 'Desconhecido')
        else:
            chat_name = channel.get('name', 'Grupo sem nome')
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        msg = Label(text=f'Deseja apagar suas mensagens em:\n[b]{chat_name}[/b]?', 
                   markup=True, font_size='16sp')
        content.add_widget(msg)
        
        warning = Label(text='⚠️ Esta ação não pode ser desfeita!', 
                       font_size='12sp', color=(1, 0.5, 0.3, 1))
        content.add_widget(warning)
        
        btn_box = BoxLayout(spacing=10, size_hint=(1, 0.3))
        popup = Popup(title='Confirmar Exclusão', content=content, size_hint=(0.9, 0.4))
        
        btn_confirm = Button(text='SIM, APAGAR', background_color=(0.9, 0.3, 0.3, 1))
        btn_confirm.bind(on_press=lambda x: self.delete_messages(channel_id, popup))
        btn_box.add_widget(btn_confirm)
        
        btn_cancel = Button(text='CANCELAR', background_color=(0.4, 0.4, 0.4, 1))
        btn_cancel.bind(on_press=popup.dismiss)
        btn_box.add_widget(btn_cancel)
        
        content.add_widget(btn_box)
        popup.open()
    
    def delete_messages(self, channel_id, popup):
        popup.dismiss()
        
        progress_content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.progress_label = Label(text='🔍 Buscando mensagens...', font_size='14sp')
        progress_content.add_widget(self.progress_label)
        
        self.progress_bar = ProgressBar(max=100, size_hint=(1, 0.2))
        progress_content.add_widget(self.progress_bar)
        
        self.progress_popup = Popup(title='Apagando Mensagens', content=progress_content, 
                                   size_hint=(0.9, 0.3), auto_dismiss=False)
        self.progress_popup.open()
        
        Thread(target=self._delete_messages_thread, args=(channel_id,), daemon=True).start()
    
    def _delete_messages_thread(self, channel_id):
        token = self.manager.current_token
        user_id = self.manager.current_user['id']
        
        messages = DiscordAPI.get_messages(channel_id, token)
        my_messages = [m for m in messages if m.get('author', {}).get('id') == user_id]
        
        total = len(my_messages)
        deleted = 0
        
        Clock.schedule_once(lambda dt: setattr(self.progress_label, 'text', 
                                              f'📊 Encontradas {total} mensagens'))
        
        for i, msg in enumerate(my_messages):
            success = DiscordAPI.delete_message(channel_id, msg['id'], token)
            if success:
                deleted += 1
            
            progress = int((i + 1) / total * 100) if total > 0 else 100
            Clock.schedule_once(lambda dt, p=progress, d=deleted: 
                              self._update_progress(p, d, total))
            time.sleep(0.5)  # Evitar rate limit
        
        Clock.schedule_once(lambda dt: self._finish_deletion(deleted, total))
    
    def _update_progress(self, progress, deleted, total):
        self.progress_bar.value = progress
        self.progress_label.text = f'🗑️ Apagando: {deleted}/{total} mensagens'
    
    def _finish_deletion(self, deleted, total):
        self.progress_popup.dismiss()
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        msg = Label(text=f'✅ [b]{deleted}[/b] de {total} mensagens apagadas!', 
                   markup=True, font_size='16sp')
        content.add_widget(msg)
        
        btn_ok = GradientButton(text='OK', size_hint=(1, 0.3))
        result_popup = Popup(title='Concluído', content=content, size_hint=(0.8, 0.3))
        btn_ok.bind(on_press=result_popup.dismiss)
        content.add_widget(btn_ok)
        result_popup.open()
    
    def logout(self, instance):
        DataManager.clear_data()
        self.manager.current = 'login'


# ==================== APP ====================

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
