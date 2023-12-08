from typing import List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    id: int
    discipline_id: int
    title_sk: str
    title_en: str
    date: datetime

    @classmethod
    def from_obj(cls, obj):
        obj['date'] = datetime.strptime(obj['date'], '%Y-%m-%d')
        return cls(**obj)


@dataclass
class Document:
    id: int
    doc_name_sk: str
    doc_name_en: str
    link_sk: str
    link_en: str
    type_id: int

    @classmethod
    def from_obj(cls, obj):
        return cls(**obj)


@dataclass
class Competition:
    id: int
    title_sk: str
    title_en: str
    date_from: str
    date_to: str
    cancelled: bool
    place: str
    lat: float
    lon: float
    segment_id: int
    classification_id: int
    organizers: List[int]
    organizer_txt: str
    events: List[Event]
    documents: List[Document]
    www: str
    readonly: bool
    entries_open: bool

    def __post_init__(self):
        self.readonly = self.readonly == "1"
        self.entries_open = self.entries_open == 1
        self.cancelled = self.cancelled == "1"

    @classmethod
    def from_obj(cls, obj):
        obj['events'] = [Event.from_obj(event) for event in obj['events']]
        obj['documents'] = [Document.from_obj(doc) for doc in obj['documents']]
        obj['date_from'] = datetime.strptime(obj['date_from'], '%Y-%m-%d')
        obj['date_to'] = datetime.strptime(obj['date_to'], '%Y-%m-%d')
        return cls(**obj)


@dataclass
class Club:
    id: int
    name: str
    shortcut: str
    country: str
    region_id: int
    city_id: int
    ident_number: str
    web: str
    first_name: str
    surname: str
    phone: str
    email: str
    address: str
    lat: float
    lon: float

    @classmethod
    def from_obj(cls, obj):
        return cls(**obj)


@dataclass
class Registration:
    id: int
    runner_id: int
    registration_type_id: int
    club_id: int
    date_from: str
    date_to: str
    reg_number: str
    runner: Runner

    @classmethod
    def from_obj(cls, obj):
        return cls(**obj)


@dataclass
class Runner:
    id: int
    gender: int
    first_name: str
    surname: str
    birth_name: str
    sportident: int
    has_account: bool
    registrations: List[Registration]

    @classmethod
    def from_obj(cls, obj):
        obj['registrations'] = [Registration.from_obj(reg) for reg in obj['registrations']]
        return cls(**obj)


@dataclass
class Runner:
    id: int
    gender: int
    first_name: str
    surname: str
    birth_name: str
    sportident: int
    has_account: bool
    registrations: List[Registration]

    @classmethod
    def from_obj(cls, obj):
        obj['registrations'] = [Registration.from_obj(reg) for reg in obj['registrations']]
        return cls(**obj)
