# from enum import Enum
from graphene import Enum


class PublicPlace(Enum):
    VILA = 1
    LARGO = 2
    TRAVESSA = 3
    VIELA = 4
    LOTEAMENTO = 5
    PÁTIO = 6
    VIADUTO = 7
    ÁREA = 8
    VIA = 9
    AEROPORTO = 10
    VEREDA = 11
    DISTRITO = 12
    VALE = 13
    NÚCLEO = 14
    TREVO = 15
    FAZENDA = 16
    TRECHO = 17
    ESTRADA = 18
    SÍTIO = 19
    FEIRA = 20
    SETOR = 21
    MORRO = 22
    RUA = 23
    CHÁCARA = 24
    RODOVIA = 25
    RESIDENCIAL = 26
    AVENIDA = 27
    COLÔNIA = 28
    RECANTO = 29
    QUADRA = 30
    PRAÇA = 31
    CONDOMÍNIO = 32
    PASSARELA = 33
    PARQUE = 34
    ESPLANADA = 35
    LAGOA = 36
    FAVELA = 37
    LADEIRA = 38
    LAGO = 39
    CONJUNTO = 40
    JARDIM = 41
    ESTAÇÃO = 42
    CAMPO = 43
    ALAMEDA = 44

    @property
    def description(self):
        if self == PublicPlace.VILA:
            return "VILA"
        elif self == PublicPlace.LARGO:
            return "LARGO"
        elif self == PublicPlace.TRAVESSA:
            return "TRAVESSA"
        """..."""


r = PublicPlace.VILA
print(r.description)
