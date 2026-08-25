from enum import Enum


class FormaPagamento(Enum):
    DINHEIRO = "Dinheiro"
    PIX = "Pix"
    CARTAO_DEBITO = "Cartão de débito"
    CARTAO_CREDITO = "Cartão de crédito"
    CREDITO_CLIENTE = "Crédito do cliente"
    