from rara_tools.normalizers import BibRecordNormalizer, AuthoritiesRecordNormalizer
from tests.test_utils import (get_formatted_sierra_response,
                              check_record_tags_sorted, check_no_dupe_tag_values, check_record_tags_have_values)

from pymarc import Record

import pytest

import os

TEST_LEVEL = os.getenv("TEST_LEVEL", "unit")

EMPTY_SIERRA_RECORDS = [
    {
        "sierraID": "1",
        "leader": "00000nz  a2200000n  4500",
        "fields": []
    },
]

REQUIRED_FIELDS = ["667", "925"]  # always included after normalization
REASON = "Skipped because TEST_LEVEL is set to 'ci'"


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_normalizers_OK():
    """ Test field editing logic & internals"""

    entities = [
        "Paul Keres",  # will find multiple entities
        "Anton Hansen Tammsaare",
        "GIBBBERRISH",
    ]

    test_sierra_data = get_formatted_sierra_response("authorities.json")

    normalizer = AuthoritiesRecordNormalizer(
        entities=entities,
        sierra_data=test_sierra_data,
    )
    assert len(normalizer.records_extra_data) == len(normalizer.data)

    normalizer = BibRecordNormalizer(
        entities=entities,
        sierra_data=test_sierra_data,
    )
    assert len(normalizer.records_extra_data) == len(normalizer.data)

    data = [
        {
            "sierraID": "1",
            "leader": "00000nz  a2200000n  4500",
            "fields": [
                {
                    "667": {
                        "ind1": " ",
                        "ind2": " ",
                        "subfields": [
                            {
                                "a": "Val"
                            }
                        ]
                    }
                },
            ]
        },
    ]

    # default behavior - added if not in record &
    normalizer = AuthoritiesRecordNormalizer(
        sierra_data=data,
        ALLOW_EDIT_FIELDS=[],
        REPEATABLE_FIELDS=[],
    )
    for r in normalizer:
        assert r.get_fields("667")[0].get_subfields("a")[0] == "Val"

    # not edited if exists
    normalizer = AuthoritiesRecordNormalizer(
        sierra_data=data,
        ALLOW_EDIT_FIELDS=[],
        REPEATABLE_FIELDS=[]
    )
    for r in normalizer:
        assert r.get_fields("667")[0].get_subfields("a")[0] == "Val"

    # allow repeatable, new field will be added
    normalizer = AuthoritiesRecordNormalizer(
        sierra_data=data,
        ALLOW_EDIT_FIELDS=[],
        REPEATABLE_FIELDS=["667"]
    )
    for r in normalizer:
        fields_667 = r.get_fields("667")
        assert len(fields_667) == 2
        assert fields_667[0].get_subfields("a")[0] == "Val"
        assert fields_667[1].get_subfields("a")[0] == "Muudetud AI poolt"

    # allow editing, field will be edited
    normalizer = AuthoritiesRecordNormalizer(
        sierra_data=data,
        ALLOW_EDIT_FIELDS=["667"],
        REPEATABLE_FIELDS=[]
    )
    for r in normalizer:
        fields_667 = r.get_fields("667")
        assert len(fields_667) == 1
        assert fields_667[0].get_subfields("a")[0] == "Muudetud AI poolt"


def validate_bibrecord_normalized(record: Record, has_viaf_data=False):
    # source notes
    assert record.get_fields("667")[0].get_subfields("a")[
        0] == "Muudetud AI poolt"


def validate_authorities_record_normalized(record: Record, has_viaf_data=False):

    field_667 = record.get_fields("667")[0].get_subfields("a")[0]
    assert field_667 == "Muudetud AI poolt" or field_667 == "Loodud AI poolt"

    field_040_subfields = record.get_fields("040")[0]

    # check that a, b & c subfields have values (can have default or unique)
    assert len(field_040_subfields.get_subfields("a")) > 0
    assert len(field_040_subfields.get_subfields("b")) > 0
    assert len(field_040_subfields.get_subfields("c")) > 0

    # check that 008 field has a value of length 40
    field_008 = record.get_fields("008")[0].data
    assert len(field_008) == 40

    if has_viaf_data:
        field_043 = record.get_fields("043")[0].get_subfields(
            "c")[0]  # check that 043 has subfield c with value "ee"
        assert field_043 == "ee"

        field_024 = record.get_fields("024")
        for f in field_024:
            assert len(f.get_subfields("0")) > 0  # VIAF url

        field_046 = record.get_fields("046")[0]
        assert len(field_046.get_subfields("f")) > 0  # birth date
        assert len(field_046.get_subfields("g")) > 0  # death date
        # assert len(field_046.get_subfields("s")) > 0 # activity start
        # assert len(field_046.get_subfields("t")) > 0 # activity end


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_missing_fields_created_bibrecord_normalization():

    normalizer_entities_only = BibRecordNormalizer(
        entities=["Eduard Vilde", "Linda Vilde"],  # find one match
    )

    normalizer_sierra_data_only = BibRecordNormalizer(
        sierra_data=EMPTY_SIERRA_RECORDS,
    )

    for record in normalizer_entities_only:
        check_record_tags_have_values(
            record, ["008", "046", "245",  # Sierra related, always with bibs
                     "035",  "100",  # VIAf enriched
                     ] + REQUIRED_FIELDS
        )
        validate_bibrecord_normalized(record, has_viaf_data=True)

    for record in normalizer_sierra_data_only:
        check_record_tags_have_values(
            record, ["008", "046", "245",  # Sierra related, always with bibs
                     ] + REQUIRED_FIELDS)
        validate_bibrecord_normalized(record)


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_missing_fields_created_authorities_normalization():

    normalizer_entities_only = AuthoritiesRecordNormalizer(
        entities=["Eduard Vilde"],  # find one match
    )

    normalizer_sierra_data_only = AuthoritiesRecordNormalizer(
        sierra_data=EMPTY_SIERRA_RECORDS,
    )

    for r in normalizer_entities_only:
        check_record_tags_have_values(r, ["008", "040",  # SIERRA related
                                          "024", "043", "046"  # VIAF enriched
                                          ] + REQUIRED_FIELDS)
        validate_authorities_record_normalized(r, True)

    for r in normalizer_sierra_data_only:
        check_record_tags_have_values(
            r, ["040"] + REQUIRED_FIELDS)
        validate_authorities_record_normalized(r)


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_normalized_fields_sorted():

    unsorted_bibdata = [
        {
            "sierraID": "1",
            "leader": "00000nz  a2200000n  4500",
            "fields": [
                {
                        "035": {
                            "ind1": " ",
                            "ind2": " ",
                            "subfields": [
                                {
                                    "a": "(ErESTER)<1>"
                                }
                            ]
                        }
                },
                {
                    "008": "220805|||aznnnaabn          || |||      nz n  "
                },
                {
                    "046": {
                        "ind1": " ",
                        "ind2": " ",
                        "subfields": [
                            {
                                "k": "1912"
                            }

                        ]
                    }
                },
            ]
        }
    ]

    normalizers = (BibRecordNormalizer, AuthoritiesRecordNormalizer)

    for normalizer in normalizers:
        normalizer = normalizer(
            entities=[],
            sierra_data=unsorted_bibdata
        )

        for r in normalizer:
            check_no_dupe_tag_values(r)
            check_record_tags_sorted(r)


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_authority_normrecord_found_in_es_and_normalized():
    """ KATA elastic normkirjete seast leitakse 1 vaste & normaliseerija täiendab leitud normkirjet VIAF infoga.
        - valideeri normaliseerimise mapping, mis autori tabelis. Täiendatud väljad ja VIAFist info
        - Valideeri märge lisatud (TODO) """
    # Presume, author name identified and sent to linker
    name = "Jaan Kross"

    normalizer = AuthoritiesRecordNormalizer(
        entities=[name]
    )

    data = normalizer.data

    assert len(data) == 1

    for r in normalizer:
        check_record_tags_have_values(r, ["040"] + REQUIRED_FIELDS)
        validate_authorities_record_normalized(r, has_viaf_data=True)


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_authority_normrecord_not_found_in_es_and_viaf():
    """KATA elastic normkirjete seast vastet ei leitud & linkija sooritab VIAFisse otsingu
        - Üks vaste leiti - luuakse uus normkirje
        - Ei leitud ühtegi vastet, või on leitud vasteid mitu - AI tuvastatud info põhjal uue kirje loomine(TODO)
    """

    # 1 result found
    normalizer = AuthoritiesRecordNormalizer(entities=["Karl Ristikivi"])

    data = normalizer.data

    assert len(data) == 1  # should create new normalized record

    # Entities not found, es & VIAF
    normalizer = AuthoritiesRecordNormalizer(entities=["asdasd#@2"])
    data = normalizer.data
    assert len(data) == 0  # should create new normalized record

    # multiple entities found, skipped
    normalizer = AuthoritiesRecordNormalizer(entities=["Paul Keres"])
    data = normalizer.data
    assert len(data) == 0  # should not create anything atm


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_matching_sierra_record_viaf_id_found():
    """normkirjelt leitakse VIAF ID, vajadusel normi asukoht, kus see ID sisaldub."""
    pass


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_matching_sierra_record_viaf_id_not_found():
    """kirjelt VIAF IDd ei leitud, soorita otsing VIAFi pihta, et leida _vastutav isik_?. Loo uus vastavalt otsingu tulemusele."""
    pass


@pytest.mark.skipif(TEST_LEVEL == "ci", reason=REASON)
def test_authorities_normalizer_checks():
    """
    - kontrolli kas tuvastatud nimi on SIERRAst leitud vaste 1XX, 4XX väljadel. Kui pole, siis lisa 4XX väljale.
    - kontrolli, kas VIAF andmete nimekujud on normkandes olemas. Kui pole, lisa need 4XX väljale.
    - Kontrolli, kas VIAF kandes on sünni ja surma daatumid ja kas need klapivad normkandes olevaga. Kui pole, siis liiguta normkandest kogu 1XX väli 4XX väljale. Seejärel loo uute daatumitega 1XX väli.
    - Kontrolli, et väljal 046 olevad daatumid klapiksid just 1xx väljale lisatuga. Kui andmeid muudeti, siis märgi, et baasis on normkanne muutunud
    """
    pass
