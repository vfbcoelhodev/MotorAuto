from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Cliente:
    _nome: str = field(repr=False)
    _telefone: str = field(repr=False)

    possui_whatsapp: bool = False
    cpf: str | None = None
    endereco: str | None = None
    observacoes: str | None = None

    id: int | None = field(default=None, init=False)
    data_cadastro: datetime = field(default_factory=datetime.now, init=False)
    ativo: bool = field(default=True, init=False)

    def __post_init__(self) -> None:
        self._validar_atributos()

    def _validar_atributos(self) -> None:
        self._nome = self._validar_nome(self._nome)
        self._telefone = self._validar_telefone(self._telefone)
        self.endereco = self._normalizar_texto_opcional(self.endereco)
        self.observacoes = self._normalizar_texto_opcional(self.observacoes)
        self.cpf = self._normalizar_texto_opcional(self.cpf)
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def telefone(self) -> str:
        return self._telefone
    
    def atualizar_nome(self, novo_nome: str) -> None:
        self._nome = self._validar_nome(novo_nome)

    def atualizar_telefone(self, novo_telefone: str) -> None:
        self._telefone = self._validar_telefone(novo_telefone)
    
    def ativar_whatsapp(self) -> None:
        self.possui_whatsapp = True
    
    def desativar_whatsapp(self) -> None:   
        self.possui_whatsapp = False

    def atualizar_endereco(self, novo_endereco: str | None) -> None:
        self.endereco = self._normalizar_texto_opcional(novo_endereco)

    def atualizar_observacoes(self, novas_observacoes: str | None) -> None:
        self.observacoes = self._normalizar_texto_opcional(
        novas_observacoes
    )

    def atualizar_cpf(self, novo_cpf: str | None) -> None:
        self.cpf = self._normalizar_texto_opcional(novo_cpf)

    def ativar(self) -> None:
        self.ativo = True
    
    def desativar(self) -> None:
        self.ativo = False

    @staticmethod
    def _validar_nome(nome: str) -> str:
        nome = nome.strip()

        if not nome:
            raise ValueError("O nome do cliente é obrigatório.")
        
        return nome
    
    @staticmethod
    def _validar_telefone(telefone: str) -> str:
        telefone = telefone.strip()

        if not telefone:
            raise ValueError("O telefone do cliente é obrigatório.")
        
        return telefone

    @staticmethod
    def _normalizar_texto_opcional(valor: str | None) -> str | None:
        if valor is None:
            return None

        valor = valor.strip()

        return valor or None
