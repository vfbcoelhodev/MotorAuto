from copy import deepcopy

from motorauto.application.repositories.veiculo import RepositorioVeiculo
from motorauto.domain.entities.cliente import Cliente
from motorauto.domain.entities.veiculo import Veiculo


class _NaoInformado:
    pass


_NAO_INFORMADO = _NaoInformado()


def cadastrar_veiculo(
    repositorio: RepositorioVeiculo,
    cliente: Cliente,
    marca: str,
    modelo: str,
    ano: int | None = None,
    placa: str | None = None,
    combustivel: str | None = None,
    observacoes: str | None = None,
) -> Veiculo:
    veiculo = Veiculo(
        _cliente=cliente,
        _marca=marca,
        _modelo=modelo,
        _ano=ano,
        _placa=placa,
        _combustivel=combustivel,
        _observacoes=observacoes,
    )

    repositorio.adicionar(veiculo)

    return veiculo


def buscar_veiculo_por_id(
    repositorio: RepositorioVeiculo,
    veiculo_id: int,
) -> Veiculo:
    if isinstance(veiculo_id, bool) or not isinstance(veiculo_id, int):
        raise TypeError(
            "O ID do veículo deve ser do tipo int."
        )
    
    if veiculo_id <= 0:
        raise ValueError(
            "O ID do veículo deve ser maior que zero."
        )
    
    veiculo = repositorio.buscar_por_id(veiculo_id)
    
    if veiculo is None:
        raise ValueError(
            "Veículo não encontrado."
        )

    return veiculo
    

def listar_veiculos(
    repositorio: RepositorioVeiculo,
) -> tuple[Veiculo, ...]:
    return repositorio.listar()


def atualizar_veiculo(
    repositorio: RepositorioVeiculo,
    veiculo_id: int,
    placa: str | None | _NaoInformado = _NAO_INFORMADO,
    combustivel: str | None | _NaoInformado = _NAO_INFORMADO,
    observacoes: str | None | _NaoInformado = _NAO_INFORMADO,
) -> Veiculo:
    veiculo_atual = buscar_veiculo_por_id(
            repositorio,
            veiculo_id,
        )

    veiculo = deepcopy(veiculo_atual)

    if not isinstance(placa, _NaoInformado):
        veiculo.atualizar_placa(placa)

    if not isinstance(combustivel, _NaoInformado):
        veiculo.atualizar_combustivel(combustivel)

    if not isinstance(observacoes, _NaoInformado):
        veiculo.atualizar_observacoes(observacoes)

    repositorio.atualizar(veiculo)

    return veiculo


def corrigir_dados_veiculo(
    repositorio: RepositorioVeiculo,
    veiculo_id: int,
    marca: str | _NaoInformado = _NAO_INFORMADO,
    modelo: str | _NaoInformado = _NAO_INFORMADO,
    ano: int | None | _NaoInformado = _NAO_INFORMADO,
) -> Veiculo:
    veiculo_atual = buscar_veiculo_por_id(
        repositorio,
        veiculo_id,
    )

    veiculo = deepcopy(veiculo_atual)

    if not isinstance(marca, _NaoInformado):
        veiculo.corrigir_marca(marca)

    if not isinstance(modelo, _NaoInformado):
        veiculo.corrigir_modelo(modelo)

    if not isinstance(ano, _NaoInformado):
        veiculo.corrigir_ano(ano)

    repositorio.atualizar(veiculo)

    return veiculo


def transferir_propriedade_veiculo(
    repositorio: RepositorioVeiculo,
    veiculo_id: int,
    novo_cliente: Cliente,
) -> Veiculo:
    veiculo = buscar_veiculo_por_id(
        repositorio,
        veiculo_id,
    )

    veiculo.transferir_propriedade(novo_cliente)

    repositorio.atualizar(veiculo)

    return veiculo

    