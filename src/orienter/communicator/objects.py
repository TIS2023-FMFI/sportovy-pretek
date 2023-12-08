from typing import List
from dataclasses import dataclass


@dataclass
class Event:
    id: int
    discipline_id: int
    title_sk: str
    title_en: str
    date: str

    @classmethod
    def from_obj(cls, obj):
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