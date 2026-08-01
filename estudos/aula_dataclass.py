from dataclasses import dataclass


@dataclass
class Pessoa:
    nome: str
    idade: int


    def __post_init__(self):
        print(">>> Executando __post_init__")

        if not self.nome:
            raise ValueError("O nome é obrigatório.")

        if self.idade < 0:
            raise ValueError("A idade não pode ser negativa.")

        

def main():
    pessoa = Pessoa("Victor", 31)

    print(pessoa)

if __name__ == "__main__":
    main()