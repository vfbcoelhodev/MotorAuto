from dataclasses import dataclass, field

from motorauto.domain.entities.cliente import Cliente

ANO_MINIMO = 1886
ANO_MAXIMO = 2100
@dataclass
class Veiculo:
    # Obrigatórios
    _cliente: Cliente = field(repr=False)
    _marca: str = field(repr=False)
    _modelo: str = field(repr=False)

    # Opcionais
    _ano: int | None = None
    _placa: str | None = None
    _combustivel: str | None = None
    _observacoes: str | None = None

    # Gerados automaticamente
    id: int | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        self._preparar_atributos()
        
    def _preparar_atributos(self) -> None:
        self._cliente = self._validar_cliente(self._cliente)

        self._marca = self._validar_texto_obrigatorio(
            valor=self._marca,
            nome_campo="marca",
        )

        self._modelo = self._validar_texto_obrigatorio(
            valor=self._modelo,
            nome_campo="modelo",
        )

        self._ano = self._validar_ano(self._ano)
        self._placa = self._normalizar_placa(self._placa)

        self._combustivel = self._normalizar_texto_opcional(
            self._combustivel
        )

        self._observacoes = self._normalizar_texto_opcional(
            self._observacoes
        )
    

    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def marca(self) -> str:
        return self._marca
    
    @property
    def modelo(self) -> str:
        return self._modelo
    
    @property
    def ano(self) -> int | None:
        return self._ano

    @property
    def placa(self) -> str | None:
        return self._placa

    @property
    def combustivel(self) -> str | None:
        return self._combustivel

    @property
    def observacoes(self) -> str | None:
        return self._observacoes

    def corrigir_marca(self, nova_marca: str) -> None:
        self._marca = self._validar_texto_obrigatorio(
            valor=nova_marca,
            nome_campo="marca",
        )
    
    def corrigir_modelo(self, novo_modelo: str) -> None:
        self._modelo = self._validar_texto_obrigatorio(
            valor=novo_modelo,
            nome_campo="modelo",
        )
    
    def corrigir_ano(self, novo_ano: int | None) -> None:
        self._ano = self._validar_ano(novo_ano)
    
    def atualizar_placa(self, nova_placa: str | None) -> None:
        self._placa = self._normalizar_placa(nova_placa)
    
    def atualizar_combustivel(self, novo_combustivel: str | None) -> None:
        self._combustivel = self._normalizar_texto_opcional(novo_combustivel)
    
    def atualizar_observacoes(self, novas_observacoes: str | None) -> None:
        self._observacoes = self._normalizar_texto_opcional(novas_observacoes)
    
    def transferir_propriedade(self, novo_cliente: Cliente) -> None:
        self._cliente = self._validar_cliente(novo_cliente)
    
    @staticmethod
    def _validar_cliente(cliente: Cliente) -> Cliente:
        if not isinstance(cliente, Cliente):
            raise TypeError(
                "O veículo deve estar associado a um cliente válido."
            )

        return cliente
    
    @staticmethod
    def _validar_texto_obrigatorio(valor: str, nome_campo: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError(f"O campo {nome_campo} é obrigatório.")

        return valor
    
    @staticmethod
    def _validar_ano(ano: int | None) -> int | None:
        if ano is None:
            return None

        if not isinstance(ano, int):
            raise TypeError(
                "O ano do veículo deve ser um número inteiro."
            )

        if ano < ANO_MINIMO or ano > ANO_MAXIMO:
            raise ValueError(
                f"O ano do veículo deve estar entre "
                f"{ANO_MINIMO} e {ANO_MAXIMO}."
            )

        return ano

    @staticmethod
    def _normalizar_placa(placa: str | None) -> str | None:
        if placa is None:
            return None

        placa = placa.strip().replace(" ", "").replace("-", "").upper()

        if not placa:
            return None

        return placa
    
    @staticmethod
    def _normalizar_texto_opcional(valor: str | None) -> str | None:
        if valor is None:
            return None

        valor = valor.strip()

        return valor or None
