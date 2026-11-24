from langchain_groq import ChatGroq
from config import API_KEY, MODEL


def criar_modelo(ferramentas):
    """Cria o modelo Groq e associa somente as ferramentas autorizadas."""
    modelo = ChatGroq(
        model=MODEL,
        api_key=API_KEY,
        temperature=0.7,
    )
    return modelo.bind_tools(ferramentas)
