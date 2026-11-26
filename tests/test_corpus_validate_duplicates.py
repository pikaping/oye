from corpus.loader import Entry
from corpus.validate import find_duplicates, normalize_text


def _e(id_: str, text: str) -> Entry:
    return Entry(id=id_, text=text, intent="x", region="es", features=())


def test_no_duplicates() -> None:
    assert find_duplicates([_e("a-1", "hola tio"), _e("a-2", "que pasa")]) == ([], [])


def test_exact_duplicates() -> None:
    problems, near = find_duplicates([_e("a-1", "hola"), _e("a-1", "hola")])
    assert any("duplicate id" in p for p in problems)
    assert any("duplicate text" in p for p in problems)
    assert near == []


def test_near_duplicates() -> None:
    problems, near = find_duplicates([_e("a-1", "¡Qué tal!"), _e("a-2", "que  tal")])
    assert problems == []
    assert len(near) == 1


def test_normalize_does_not_touch_input() -> None:
    assert normalize_text("  ¡Qué  TAL, tío! ") == "que tal tio"


def test_normalize_empty_and_punctuation_only() -> None:
    assert normalize_text("") == ""
    assert normalize_text("¿¿??!!...") == ""
    assert normalize_text("   \t\n ") == ""


def test_normalize_emoji_underscore_and_repeated_letters() -> None:
    assert normalize_text("holaaa 😂😂 _ qué_tal") == "holaaa quetal"


def test_normalize_is_idempotent() -> None:
    once = normalize_text("  Ñoño!!  Q  pasa,   tío?? ")
    assert normalize_text(once) == once


def test_normalize_unicode_forms_equal() -> None:
    assert normalize_text("qué") == normalize_text("qué") == "que"


def test_normalize_keeps_digits_and_distinct_words() -> None:
    assert normalize_text("xq 2 veces!!") == "xq 2 veces"
    assert normalize_text("tb") != normalize_text("también")


def test_same_id_different_text_only_id_problem() -> None:
    problems, near = find_duplicates([_e("a-1", "wenas"), _e("a-1", "q tal")])
    assert len(problems) == 1 and "duplicate id" in problems[0]
    assert near == []


def test_exact_text_dup_distinct_ids_not_near() -> None:
    problems, near = find_duplicates([_e("a-1", "ola k ase"), _e("a-2", "ola k ase")])
    assert len(problems) == 1 and "a-1, a-2" in problems[0]
    assert near == []


def test_near_group_of_three_is_single_report() -> None:
    _, near = find_duplicates(
        [_e("a-1", "Que tal"), _e("a-2", "qué tal?"), _e("a-3", "¿que tal?")]
    )
    assert len(near) == 1
    assert all(i in near[0] for i in ("a-1", "a-2", "a-3"))


def test_near_duplicate_reports_original_text() -> None:
    _, near = find_duplicates([_e("a-1", "Q TAL tío"), _e("a-2", "q tal tio")])
    assert "Q TAL tío" in near[0] and "q tal tio" in near[0]


def test_empty_input_and_generator() -> None:
    assert find_duplicates([]) == ([], [])
    assert find_duplicates(_e(f"a-{i}", f"frase {i}") for i in range(3)) == ([], [])


def test_exact_dup_with_mixed_near_variant() -> None:
    problems, near = find_duplicates(
        [_e("a-1", "wena"), _e("a-2", "wena"), _e("a-3", "Wena!")]
    )
    assert len(problems) == 1
    assert len(near) == 1
