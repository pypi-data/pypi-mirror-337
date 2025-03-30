import os
import openai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente, incluindo OPENAI_API_KEY
load_dotenv(override=True)

class JSAutograder:
    """
    Classe responsável por avaliar códigos JavaScript utilizando a API do OpenAI.
    Ela constrói um prompt personalizado para que o LLM verifique se o código do aluno
    está correto e, caso esteja incorreto, forneça dicas sem entregar a resposta completa.
    """
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Chave de API não fornecida. Verifique a variável de ambiente OPENAI_API_KEY.")
        openai.api_key = self.api_key
        self.model = model

    def evaluate(self, answer: str, task: str, question: str, answer_type: str = "js") -> str:
        """
        Avalia o código JavaScript do aluno.

        Parâmetros:
          - answer: string contendo o código submetido pelo aluno.
          - task: descrição ou identificador da tarefa.
          - question: descrição ou enunciado da questão.
          - answer_type: tipo de resposta (padrão "js").

        Retorna:
          - feedback: resposta do LLM informando se o código está correto ou dicas para correção.
        """
        prompt = f"""Você é um professor de JavaScript.
        Tarefa: {task}
        Questão: {question}
        Tipo de resposta: {answer_type}

        Código do aluno:
        {answer}

        Avalie o código acima. Se estiver correto, responda apenas com "Correto" e uma breve justificativa. Se estiver incorreto, responda com "Incorreto" e forneça dicas para que o aluno encontre a solução, mas NUNCA forneça a resposta completa.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente que avalia códigos de JavaScript sem dar a resposta completa."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=150
            )
            feedback = response["choices"][0]["message"]["content"].strip()
            return feedback
        except Exception as e:
            return f"Erro ao processar a avaliação: {e}"

def sender(answer, task, question, answer_type="js"):
    """
    Função de conveniência para enviar o código do aluno para avaliação.
    Exibe o feedback retornado pelo avaliador.
    """
    grader = JSAutograder()
    feedback = grader.evaluate(answer, task, question, answer_type)
    print("Feedback da avaliação:")
    print(feedback)

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de código JavaScript submetido pelo aluno
    js_code = """
        function soma(a, b) {
            return a + b;
        }
        console.log(soma(2, 3));
        """
    # Chama a função sender com os parâmetros da tarefa
    sender(answer=js_code, task="função de soma", question="Implemente uma função que some dois números", answer_type="js")

