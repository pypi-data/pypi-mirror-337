from IPython.display import display, clear_output, Markdown
import ipywidgets as widgets
from autograder.core import JSAutograder

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

    def _send(self, b=None):
        self._display_header()
        self._display_answer()
        feedback = self.autograder.evaluate(self.answer, self.task, self.question, self.answer_type)
        clear_output()
        display(Markdown("### Feedback da avaliação:"))
        display(Markdown(f"```\n{feedback}\n```"))

def sender(answer: str, task: str, question: str, answer_type: str = "js"):
    """
    Função de conveniência para enviar o código do aluno para avaliação interativa.
    Exibe um botão "Enviar" que dispara a avaliação somente quando clicado.
    """
    activity_sender = JSActivitySender(answer, task, question, answer_type)
    send_button = widgets.Button(description="Enviar")
    send_button.on_click(lambda b: activity_sender._send(b))
    display(send_button)


# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de uso
    answer = "console.log('Hello, World!');"
    task = "Exercício 1"
    question = "Imprima 'Hello, World!' no console."
    button = sender(answer, task, question)
    # display(button)