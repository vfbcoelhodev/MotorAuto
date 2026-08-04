from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Cliente:
    _nome: str = field(repr=False)
    _telefone: str = field(repr=False)

    _possui_whatsapp: bool = False
    _cpf: str | None = None
    _endereco: str | None = None
    _observacoes: str | None = None

    _id: int | None = field(default=None, init=False)
    _data_cadastro: datetime = field(default_factory=datetime.now, init=False)
    _ativo: bool = field(default=True, init=False)

    def __post_init__(self) -> None:
        self._preparar_atributos()

    def _preparar_atributos(self) -> None:
        self._nome = self._validar_texto_obrigatorio(self._nome, "nome")
        self._telefone = self._validar_texto_obrigatorio(self._telefone, "telefone")
        self._endereco = self._normalizar_texto_opcional(self._endereco)
        self._observacoes = self._normalizar_texto_opcional(self._observacoes)
        self._cpf = self._normalizar_texto_opcional(self._cpf)

    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def telefone(self) -> str:
        return self._telefone
    
    @property
    def possui_whatsapp(self) -> bool:
        return self._possui_whatsapp
    
    @property
    def cpf(self) -> str | None:
            return self._cpf

    @property
    def endereco(self) -> str | None:
        return self._endereco
    
    @property
    def observacoes(self) -> str | None:   
        return self._observacoes
    
    @property
    def id(self) -> int | None:
        return self._id
    
    @property
    def data_cadastro(self) -> datetime:
        return self._data_cadastro
    
    @property
    def ativo(self) -> bool:
        return self._ativo
    
    def atualizar_nome(self, novo_nome: str) -> None:
        self._nome = self._validar_texto_obrigatorio(novo_nome, "nome")

    def atualizar_telefone(self, novo_telefone: str) -> None:
        self._telefone = self._validar_texto_obrigatorio(novo_telefone, "telefone")

    def ativar_whatsapp(self) -> None:
        self._possui_whatsapp = True
    
    def desativar_whatsapp(self) -> None:   
        self._possui_whatsapp = False

    def atualizar_endereco(self, novo_endereco: str | None) -> None:
        self._endereco = self._normalizar_texto_opcional(novo_endereco)

    def atualizar_observacoes(self, novas_observacoes: str | None) -> None:
        self._observacoes = self._normalizar_texto_opcional(
        novas_observacoes
    )

    def atualizar_cpf(self, novo_cpf: str | None) -> None:
        self._cpf = self._normalizar_texto_opcional(novo_cpf)

    def ativar(self) -> None:
        self._ativo = True
    
    def desativar(self) -> None:
        self._ativo = False

    @staticmethod
    def _validar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError(f"O campo {nome_campo} é obrigatório.")

        return valor
            
    @staticmethod
    def _normalizar_texto_opcional(valor: str | None) -> str | None:
        if valor is None:
            return None

        valor = valor.strip()

        return valor or None
