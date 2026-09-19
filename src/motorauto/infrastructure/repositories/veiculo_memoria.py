from motorauto.domain.entities.veiculo import Veiculo


class RepositorioVeiculoEmMemoria:
    def __init__(self) -> None:
        self._veiculos: list[Veiculo] = []
        self._proximo_id = 1
    

    def adicionar(self, veiculo: Veiculo) -> None:
        if not isinstance(veiculo, Veiculo):
            raise TypeError(
                "O veículo informado deve ser do tipo Veiculo."               
            )

        if any(
            veiculo_existente is veiculo
            for veiculo_existente in self._veiculos
        ):
            raise ValueError(
                "O veículo informado já foi adicionado ao repositório."
            )

        if veiculo.id is not None:
            raise ValueError(
                "Não é possível adicionar um veículo que já possui ID."
            )

        veiculo.id = self._proximo_id
        self._proximo_id += 1
        
        self._veiculos.append(veiculo)


    def buscar_por_id(self, veiculo_id: int) -> Veiculo | None:
        for veiculo in self._veiculos:
            if veiculo.id == veiculo_id:
                return veiculo

        return None 
        
    def listar(self) -> tuple[Veiculo, ...]:
        return tuple(self._veiculos)

    def atualizar(self, veiculo: Veiculo) -> None:
        if not isinstance(veiculo, Veiculo):
            raise TypeError(
                "O veículo informado deve ser do tipo Veiculo."
            )

        if veiculo.id is None:
            raise ValueError(
                "O veículo informado deve possuir ID."
            )

        for i, veiculo_existente in enumerate(self._veiculos):
            if veiculo_existente.id == veiculo.id:
                self._veiculos[i] = veiculo
                return
        
        raise ValueError(
        "Veículo não encontrado no repositório."
        )
