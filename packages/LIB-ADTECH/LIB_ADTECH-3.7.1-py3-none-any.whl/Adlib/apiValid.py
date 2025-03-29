import requests

# URL base da API
BASE_URL = "https://services-hml.flexdoc-apis.com.br/services/api/v1"


def obterToken(username: str, password: str) -> str:
    """
    Obtém o token de autenticação usando as credenciais fornecidas.

    :param username: Nome de usuário
    :param password: Senha
    :return: Token de acesso ou None em caso de erro
    """
    auth_url = f"{BASE_URL}/authentication"
    auth_payload = {"username": username, "password": password}
    auth_headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(auth_url, json=auth_payload, headers=auth_headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Erro ao obter token: {response.status_code} - {response.text}")
        return None


def verificarFraude(token: str, cpf: str, imagem_frente: str, imagem_verso: str) -> bool:
    """
    Realiza a análise de fraude e retorna 1 se o score for > 80, senão retorna 0.

    :param token: Token de autenticação
    :param cpf: CPF do usuário
    :param imagem_frente: Caminho para a imagem da frente do documento
    :param imagem_verso: Caminho para a imagem do verso do documento
    :return: 1 se score > 80, senão 0
    """
    fraud_url = f"{BASE_URL}/fraud/analysis"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    files = {
        "cpf": (None, cpf),
        "imageFront": (imagem_frente, open(imagem_frente, "rb"), "image/jpeg"),
        "imageBack": (imagem_verso, open(imagem_verso, "rb"), "image/jpeg"),
    }

    response = requests.post(fraud_url, headers=headers, files=files)

    if response.status_code == 200:
        resultado = response.json()
        score = resultado.get("scoreResult", {}).get("score", 0)
        return score > 80
    else:
        print(f"Erro na análise de fraude: {response.status_code} - {response.text}")
        return False


def main():
    username = "adpromo.api"
    password = "a3d5p-r5o0m0"

    token = obterToken(username, password)

    if token:
        cpf = "01360504257"
        imagem_frente = "rg representante1.jpg"
        imagem_verso = "rg representante (1).jpg"

        status = verificarFraude(token, cpf, imagem_frente, imagem_verso)
        print(f"Resultado da análise: {status}")
    else:
        print("Não foi possível autenticar o usuário.")


if __name__ == "__main__":
    main()