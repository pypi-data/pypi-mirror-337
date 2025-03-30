# pylint: disable=line-too-long, too-many-arguments, too-many-instance-attributes

"""
Módulo interativo para avaliação de código JavaScript.
Integra o JSAutograder com widgets para facilitar a interação sem depender de um servidor.
"""

from IPython.display import display, clear_output, Markdown
import ipywidgets as widgets
from .core import JSAutograder

class JSActivitySender:
    """
    Classe para enviar e avaliar interativamente o código JavaScript do aluno.
    """
    def __init__(self, answer: str, task: str, question: str, answer_type: str = "js"):
        self.answer = answer
        self.task = task
        self.question = question
        self.answer_type = answer_type
        self.autograder = JSAutograder()

    def _display_header(self):
        display(Markdown(f"### Avaliando exercício `{self.question}` da tarefa `{self.task}`..."))

    def _display_answer(self):
        display(Markdown(f"""
        **Código do aluno enviado**:
        {self.answer}
        Aguarde a avaliação...
        """))

    def _send(self):
        self._display_header()
        self._display_answer()
        feedback = self.autograder.evaluate(self.answer, self.task, self.question, self.answer_type)
        clear_output()
        display(Markdown("### Feedback da avaliação:"))
        display(Markdown(f"```\n{feedback}\n```"))

def sender(answer: str, task: str, question: str, answer_type: str = "js"):
    """
    Função de conveniência para enviar o código do aluno para avaliação interativa.
    Retorna um widget interativo para disparar a avaliação.
    """
    activity_sender = JSActivitySender(answer, task, question, answer_type)
    button = widgets.interactive(activity_sender._send, manual=True, manual_name=f"Avaliar {question}")
    return button
