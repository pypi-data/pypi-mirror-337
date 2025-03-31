import requests

class JSAutograder:
    """
    Classe responsável por avaliar códigos JavaScript utilizando a API do OpenAI.
    Realiza chamadas HTTP diretas com a biblioteca requests.
    """

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Inicializa o autograder com a chave de API obrigatória.

        Parâmetros:
            api_key (str): Chave de API do OpenAI.
            model (str): Modelo a ser utilizado (padrão "gpt-3.5-turbo").
        """
        if not api_key:
            raise ValueError("Chave de API não fornecida. Informe um valor válido para 'api_key'.")
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

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
        prompt = (
            f"Você é um professor de JavaScript.\n"
            f"Tarefa: {task}\n"
            f"Questão: {question}\n"
            f"Tipo de resposta: {answer_type}\n\n"
            f"Código do aluno:\n{answer}\n\n"
            "Avalie o código acima. Se estiver correto, responda apenas com 'Correto' e uma breve justificativa. "
            "Se estiver incorreto, responda com 'Incorreto' e forneça dicas para que o aluno encontre a solução, "
            "mas NUNCA forneça a resposta completa."
        )

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um assistente que avalia códigos de JavaScript sem entregar a resposta completa."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.4,
            "max_tokens": 300
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            feedback = response.json()["choices"][0]["message"]["content"].strip()
            return feedback
        except Exception as e:
            return f"Erro ao processar a avaliação: {e}"
