import json
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from datetime import datetime


class AppNome(App):
    def build(self):
        self.root_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10,
            size_hint=(None, None),
            width=300,
            height=300,
        )
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.label_nome = Label(text="Nome", size_hint=(1, None), height=30)
        self.input_nome = TextInput(size_hint=(1, None), height=30)

        self.label_email = Label(text="Email", size_hint=(1, None), height=30)
        self.input_email = TextInput(size_hint=(1, None), height=30)

        self.label_data_nascimento = Label(
            text="Data de Nascimento", size_hint=(1, None), height=30
        )
        self.input_data_nascimento = TextInput(size_hint=(1, None), height=30)

        self.botao_salvar = Button(text="Salvar", size_hint=(1, None), height=40)
        self.botao_salvar.bind(on_press=self.validar_e_salvar)

        self.layout.add_widget(self.label_nome)
        self.layout.add_widget(self.input_nome)
        self.layout.add_widget(self.label_email)
        self.layout.add_widget(self.input_email)
        self.layout.add_widget(self.label_data_nascimento)
        self.layout.add_widget(self.input_data_nascimento)
        self.layout.add_widget(self.botao_salvar)

        self.root_layout.add_widget(self.layout)

        return self.root_layout

    def validar_e_salvar(self, instance):
        nome = self.input_nome.text
        email = self.input_email.text
        data_nascimento = self.input_data_nascimento.text

        # Verificar Nome
        if not nome.replace(" ", "").isalpha():
            self.mostrar_mensagem("Nome inválido! Use apenas letras.")
            return

        # Verificar Email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.mostrar_mensagem("Email inválido! Verifique o formato.")
            return

        # Verificar Data de Nascimento
        try:
            datetime.strptime(data_nascimento, "%d/%m/%Y")
        except ValueError:
            self.mostrar_mensagem(
                "Data de Nascimento inválida! Use o formato DD/MM/AAAA."
            )
            return

        # Se todos os dados forem válidos, salve os dados
        self.salvar_dados(nome, email, data_nascimento)

    def salvar_dados(self, nome, email, data_nascimento):
        dados = {"Nome": nome, "Email": email, "Data de Nascimento": data_nascimento}

        with open("dados.json", "w") as arquivo_json:
            json.dump(dados, arquivo_json, indent=4)

        self.mostrar_mensagem("Dados salvos com sucesso!")
        Clock.schedule_once(self.voltar_para_tela_inicial, 25)

    def mostrar_mensagem(self, mensagem):
        self.layout.clear_widgets()  # Limpa os widgets da tela
        label_mensagem = Label(text=mensagem, size_hint=(1, None), height=30)
        self.layout.add_widget(label_mensagem)

    def voltar_para_tela_inicial(self, dt):
        self.layout.clear_widgets()

        self.layout.add_widget(self.label_nome)
        self.layout.add_widget(self.input_nome)
        self.layout.add_widget(self.label_email)
        self.layout.add_widget(self.input_email)
        self.layout.add_widget(self.label_data_nascimento)
        self.layout.add_widget(self.input_data_nascimento)
        self.layout.add_widget(self.botao_salvar)


if __name__ == "__main__":
    AppNome().run()
