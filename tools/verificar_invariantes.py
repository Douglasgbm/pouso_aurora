"""Auditoria externa reproduzível; não integra o código acadêmico do MGPEB.
Executar: python tools/verificar_invariantes.py
"""
import copy
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mgpeb as g


def verificar(total=400, seed=20261013):
    rng = random.Random(seed)
    descidas = 0
    for caso in range(total):
        config = [rng.choice([1.0, 3.0, 5.0]), 0.002, 2.0, 0.25]
        modulos = []
        for i in range(rng.randint(0, 12)):
            massa = rng.choice([500.0, 1000.0, 1500.0, 2200.0])
            minimo = config[0] * config[1] * massa + config[2]
            fuel = rng.choice([0.0, minimo - 0.001, minimo, minimo * 1.25, minimo + 30])
            modulos.append([str(i), rng.choice(g.TIPOS), rng.randint(1, 5), fuel,
                            massa, rng.randint(1, 5), float(rng.randint(0, 20)),
                            rng.choice([True, False]), rng.choice([True, False]),
                            rng.random() < 0.1, '', ''])
        eventos = []
        for _ in range(rng.randint(0, 18)):
            tipo = rng.choice(['area', 'clima', 'sensores', 'sistemas'])
            if tipo in ['sensores', 'sistemas'] and not modulos:
                continue
            alvo = rng.choice(modulos)[0] if tipo in ['sensores', 'sistemas'] else ''
            valor = rng.choice(['livre', 'ocupada', 'obstruída']) if tipo == 'area' else rng.choice([True, False])
            eventos.append([float(rng.randint(0, 30)), tipo, valor, alvo])
        ambiente = [rng.choice([True, False]), rng.choice(['livre', 'ocupada', 'obstruída'])]
        antes = copy.deepcopy([modulos, eventos, ambiente, config])
        s = g.simular(modulos, eventos, ambiente, config)
        assert [modulos, eventos, ambiente, config] == antes, ('entrada alterada', caso)
        assert len(s) == 8, ('resultado inválido', caso)
        assert s == g.simular(modulos, eventos, ambiente, config), ('não determinístico', caso)
        inicio = [e.split(' min: ')[1].split()[0] for e in s[2] if 'iniciou descida' in e]
        assert len(inicio) == len(set(inicio)), ('descida duplicada', caso)
        assert len(s[7]) == len(set(s[7])) and len(s[1]) == len(set(s[1]))
        assert not set(s[7]) & set(s[1]), ('espera/solo sobrepostos', caso)
        assert s[4] == s[2] and s[4] is not s[2], ('pilha', caso)
        for i, m in enumerate(s[0]):
            voou = m[0] in inicio
            consumo = modulos[i][g.MASSA] * config[0] * config[1] if voou else 0
            assert abs(m[g.COMBUSTIVEL] - (modulos[i][g.COMBUSTIVEL] - consumo)) < 1e-8, ('combustível', caso)
            if voou:
                assert m[g.COMBUSTIVEL] >= config[2] - 1e-8, ('reserva', caso)
                assert (i in s[7]) != m[g.ACIDENTE], ('registro de pouso', caso)
            if m[g.ESTADO] == 'operacional':
                assert m[g.SENSORES] and m[g.SISTEMAS] and not m[g.ACIDENTE]
                assert i in s[7]
                if m[g.TIPO] != 'Energia':
                    assert any(x[g.TIPO] == 'Energia' and x[g.ESTADO] == 'operacional' for x in s[0])
                if m[g.TIPO] == 'Laboratório':
                    assert any(x[g.TIPO] == 'Habitação' and x[g.ESTADO] == 'operacional' for x in s[0])
            if i in s[1]:
                assert m[g.ESTADO] == 'espera' and m[g.MOTIVO]
        tempos = [float(e.split(' min: ')[0]) for e in s[2] if ' min: ' in e]
        assert tempos == sorted(tempos), ('relógio retrocedeu', caso)
        descidas += len(inicio)
    return {'seed': seed, 'cenarios': total, 'descidas': descidas, 'resultado': 'aprovado',
            'escopo': 'Conservação, determinismo, combustível, reserva, unicidade, dependências, pilha e relógio.'}


if __name__ == '__main__':
    print(json.dumps(verificar(), ensure_ascii=False, indent=2))
