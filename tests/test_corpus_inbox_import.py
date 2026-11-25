"""Checks that the real phrases imported from the inbox are kept verbatim."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "corpus" / "data" / "oye-es-003.jsonl"
INBOX = ROOT / "corpus" / "inbox" / "reales.txt"

# Literal texts: do NOT normalize or fix spelling, typos are the point.
EXPECTED_TEXTS = [
    "Buenas, quiero cancelar el pedido q hice ayer se puede??",
    "a ver es que me he equivocado de talla, como cancelo esto",
    "Cancelame el pedido porfa q ya no lo necesito xd",
    "Hola, se puede anular un pedido si ya pone enviado o ya no",
    "Llevo 3 semanas esperando el paquete y nadie me dice nada, joder",
    "el producto ha llegado roto y encima tarde...",
    "Pues vaya servicio, me cobrais dos veces y ni me contestais",
    "ostia q me ha llegado otra cosa q no es lo q pedi 🤣",
    "Me pasas con una persona?? q esto no hay quien lo entienda",
    "quiero hablar con alguien de verdad no con un bot xd",
    "Hay alguien ahi o solo maquinas",
    "a ver, pasame con un humano porfa",
    "Cuanto me queda en la cuenta?",
    "me dices el saldo q tengo porfa",
    "Tengo pasta en la cuenta o ya no xd",
    "No me deja entrar, creo q he puesto mal la contraseña mil veces",
    "como cambio la contraseña q no me acuerdo",
    "me ha bloqueado la cuenta x poner mal la clave, q hago",
    "sorry pero no me llega el codigo pa entrar",
    "Quiero devolver unas zapas q me quedan pequeñas, como lo hago",
    "se puede devolver algo si ya lo he abierto o no",
    "Buenas, el plazo de devolucion cuanto es?",
    "A que hora abris mañana?",
    "estais abiertos el finde?",
    "Hasta q hora se puede llamar hoy",
    "Quiero pedir cita pa la semana q viene, hay hueco?",
    "me dais cita el jueves x la tarde??",
    "a ver, necesito cambiar la cita del lunes q no puedo ir",
    "Holaa buenas",
    "ey q tal",
    "Vale gracias, ya esta",
    "ok perfe, gracias!!",
    "Donde esta mi pedido? pone q llegaba ayer",
    "sabeis algo del paquete? q no me llega",
    "el pedido sigue en reparto desde el lunes, es normal??",
    "el link de seguimiento no funciona, me sale error random",
    "No me deja pagar con la tarjeta, me da error todo el rato",
    "me ha cobrado pero el pedido no aparece xd",
    "Intento pagar y se queda cargando...",
    "literal llevo una hora intentando pagar",
]


def _rows() -> list[dict]:
    lines = DATA.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def test_imported_texts_are_verbatim() -> None:
    assert len(EXPECTED_TEXTS) == 40
    assert [r["text"] for r in _rows()] == EXPECTED_TEXTS


def test_imported_ids_and_not_synthetic() -> None:
    rows = _rows()
    assert [r["id"] for r in rows] == [f"oye-{i:04d}" for i in range(101, 141)]
    assert all(r["synthetic"] is False for r in rows)


def test_inbox_has_only_comments() -> None:
    lines = INBOX.read_text(encoding="utf-8").splitlines()
    pending = [ln for ln in lines if ln.strip() and not ln.startswith("#")]
    assert pending == []
