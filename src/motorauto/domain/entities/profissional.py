from dataclasses import dataclass, field
from datetime import datetime

from motorauto.domain.enums.funcao_profissional import FuncaoProfissional


@dataclass
class Profissional:
    # Obrigatórios
    _nome: str = field(repr=False)
    _telefone: str = field(repr=False)
    _funcao: FuncaoProfissional = field(repr=False)

    # Opcionais
    _observacoes: str | None = None

    # Gerados automaticamente
    _id: int | None = field(default=None, init=False)
    _data_cadastro: datetime = field(default_factory=datetime.now, init=False)
    _ativo: bool = field(default=True, init=False)

    def __post_init__(self) -> None:
        self._preparar_atributos()
    
    def _preparar_atributos(self) -> None:
        self._nome = self._validar_texto_obrigatorio(
            valor=self._nome,
            nome_campo="nome",
        )

        self._telefone = self._validar_texto_obrigatorio(
            valor=self._telefone,
            nome_campo="telefone",
        )

        self._funcao = self._validar_funcao(self._funcao)

        self._observacoes = self._normalizar_texto_opcional(
            self._observacoes
        )
    
    @property
    def nome(self) -> str:
        return self._nome  
    
    @property
    def telefone(self) -> str:  
        return self._telefone   
    
    @property
    def funcao(self) -> FuncaoProfissional:
        return self._funcao
    
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
        self._nome = self._validar_texto_obrigatorio(
            valor=novo_nome,
            nome_campo="nome",
        )

    def atualizar_telefone(self, novo_telefone: str) -> None:
        self._telefone = self._validar_texto_obrigatorio(
            valor=novo_telefone,
            nome_campo="telefone",
        )

    def alterar_funcao(self, nova_funcao: FuncaoProfissional) -> None:
        self._funcao = self._validar_funcao(nova_funcao)

    def atualizar_observacoes(self, novas_observacoes: str | None) -> None:
        self._observacoes = self._normalizar_texto_opcional(novas_observacoes)
    
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
    def _validar_funcao(funcao: FuncaoProfissional) -> FuncaoProfissional:
        if not isinstance(funcao, FuncaoProfissional):
            raise TypeError("A função do profissional deve ser uma instância de FuncaoProfissional.")
        
        return funcao
    
    @staticmethod
    def _normalizar_texto_opcional(valor: str | None) -> str | None:
        if valor is None:
            return None

        valor = valor.strip()

        return valor or None
