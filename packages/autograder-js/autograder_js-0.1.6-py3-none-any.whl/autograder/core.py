import os
import openai
from dotenv import load_dotenv

load_dotenv(override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

class JSAutograder:
    """
    Classe responsável por avaliar códigos JavaScript utilizando a API do OpenAI.
    Utiliza a interface ChatCompletion da versão atual do pacote openai.
    """
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Chave de API não fornecida. Verifique a variável de ambiente OPENAI_API_KEY.")
        self.model = model

    def evaluate(self, answer: str, task: str, question: str, answer_type: str = "js") -> str:
        """
        Avalia o código JavaScript do aluno e retorna o feedback.
        
        Parâmetros:
            answer (str): Código submetido pelo aluno.
            task (str): Nome ou descrição da tarefa.
            question (str): Enunciado da questão.
            answer_type (str): Tipo da resposta (padrão "js").
            
        Retorna:
            str: Feedback da avaliação.
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
    
            response = openai.chat.completions.create(model=self.model,
            messages=[
                {"role": "system", "content": "Você é um assistente que avalia códigos de JavaScript sem entregar a resposta completa."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=300)
            feedback = response.choices[0].message.content.strip()
            return feedback
        except Exception as e:
            return f"Erro ao processar a avaliação: {e}"

if __name__ == "__main__":
    # Exemplo de uso
    autograder = JSAutograder()
    feedback = autograder.evaluate("console.log('Hello, World!');", "Tarefa 1", "Imprima 'Hello, World!'", "js")
    print(feedback)
