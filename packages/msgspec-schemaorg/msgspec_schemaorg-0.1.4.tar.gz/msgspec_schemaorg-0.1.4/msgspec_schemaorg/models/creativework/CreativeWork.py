from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.AudioObject import AudioObject
    from msgspec_schemaorg.models.creativework.Claim import Claim
    from msgspec_schemaorg.models.creativework.Clip import Clip
    from msgspec_schemaorg.models.creativework.Comment import Comment
    from msgspec_schemaorg.models.creativework.CorrectionComment import CorrectionComment
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
    from msgspec_schemaorg.models.creativework.MusicRecording import MusicRecording
    from msgspec_schemaorg.models.creativework.Review import Review
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.creativework.WebPage import WebPage
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.event.PublicationEvent import PublicationEvent
    from msgspec_schemaorg.models.intangible.AggregateRating import AggregateRating
    from msgspec_schemaorg.models.intangible.AlignmentObject import AlignmentObject
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.IPTCDigitalSourceEnumeration import IPTCDigitalSourceEnumeration
    from msgspec_schemaorg.models.intangible.InteractionCounter import InteractionCounter
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.Rating import Rating
    from msgspec_schemaorg.models.intangible.SizeSpecification import SizeSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Country import Country
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class CreativeWork(Thing):
    """The most generic kind of creative work, including books, movies, photographs, software programs, etc."""
    type: str = field(default_factory=lambda: "CreativeWork", name="@type")
    provider: 'Person' | 'Organization' | None = None
    aggregateRating: 'AggregateRating' | None = None
    citation: str | 'CreativeWork' | None = None
    locationCreated: 'Place' | None = None
    sdPublisher: 'Person' | 'Organization' | None = None
    thumbnail: 'ImageObject' | None = None
    accessModeSufficient: 'ItemList' | None = None
    publishingPrinciples: 'URL' | 'CreativeWork' | None = None
    inLanguage: str | 'Language' | None = None
    abstract: str | None = None
    countryOfOrigin: 'Country' | None = None
    contentLocation: 'Place' | None = None
    dateModified: datetime | date | None = None
    usageInfo: 'URL' | 'CreativeWork' | None = None
    sdDatePublished: date | None = None
    archivedAt: 'URL' | 'WebPage' | None = None
    workTranslation: 'CreativeWork' | None = None
    sdLicense: 'URL' | 'CreativeWork' | None = None
    educationalAlignment: 'AlignmentObject' | None = None
    editor: 'Person' | None = None
    license: 'URL' | 'CreativeWork' | None = None
    maintainer: 'Person' | 'Organization' | None = None
    sourceOrganization: 'Organization' | None = None
    reviews: 'Review' | None = None
    accessibilityHazard: str | None = None
    workExample: 'CreativeWork' | None = None
    pattern: str | 'DefinedTerm' | None = None
    offers: 'Offer' | 'Demand' | None = None
    hasPart: 'CreativeWork' | None = None
    keywords: 'URL' | str | 'DefinedTerm' | None = None
    exampleOfWork: 'CreativeWork' | None = None
    copyrightNotice: str | None = None
    encodingFormat: 'URL' | str | None = None
    mainEntity: 'Thing' | None = None
    editEIDR: 'URL' | str | None = None
    copyrightYear: int | float | None = None
    about: 'Thing' | None = None
    datePublished: datetime | date | None = None
    educationalLevel: 'URL' | str | 'DefinedTerm' | None = None
    accessibilityFeature: str | None = None
    materialExtent: str | 'QuantitativeValue' | None = None
    video: 'Clip' | 'VideoObject' | None = None
    funding: 'Grant' | None = None
    headline: str | None = None
    digitalSourceType: 'IPTCDigitalSourceEnumeration' | None = None
    learningResourceType: str | 'DefinedTerm' | None = None
    alternativeHeadline: str | None = None
    temporal: datetime | str | None = None
    isBasedOnUrl: 'URL' | 'CreativeWork' | 'Product' | None = None
    associatedMedia: 'MediaObject' | None = None
    commentCount: int | None = None
    dateCreated: datetime | date | None = None
    fileFormat: 'URL' | str | None = None
    teaches: str | 'DefinedTerm' | None = None
    accessibilityControl: str | None = None
    isPartOf: 'URL' | 'CreativeWork' | None = None
    accessibilityAPI: str | None = None
    contentReferenceTime: datetime | None = None
    isBasedOn: 'URL' | 'CreativeWork' | 'Product' | None = None
    creativeWorkStatus: str | 'DefinedTerm' | None = None
    award: str | None = None
    educationalUse: str | 'DefinedTerm' | None = None
    isFamilyFriendly: bool | None = None
    interactivityType: str | None = None
    publication: 'PublicationEvent' | None = None
    accountablePerson: 'Person' | None = None
    version: int | float | str | None = None
    expires: datetime | date | None = None
    awards: str | None = None
    text: str | None = None
    producer: 'Person' | 'Organization' | None = None
    thumbnailUrl: 'URL' | None = None
    copyrightHolder: 'Person' | 'Organization' | None = None
    wordCount: int | None = None
    recordedAt: 'Event' | None = None
    audience: 'Audience' | None = None
    spatial: 'Place' | None = None
    interpretedAsClaim: 'Claim' | None = None
    creditText: str | None = None
    material: 'URL' | str | 'Product' | None = None
    translator: 'Person' | 'Organization' | None = None
    character: 'Person' | None = None
    funder: 'Person' | 'Organization' | None = None
    encodings: 'MediaObject' | None = None
    contributor: 'Person' | 'Organization' | None = None
    position: int | str | None = None
    conditionsOfAccess: str | None = None
    review: 'Review' | None = None
    temporalCoverage: datetime | 'URL' | str | None = None
    mentions: 'Thing' | None = None
    interactionStatistic: 'InteractionCounter' | None = None
    schemaVersion: 'URL' | str | None = None
    acquireLicensePage: 'URL' | 'CreativeWork' | None = None
    sponsor: 'Organization' | 'Person' | None = None
    publisher: 'Organization' | 'Person' | None = None
    assesses: str | 'DefinedTerm' | None = None
    spatialCoverage: 'Place' | None = None
    size: str | 'QuantitativeValue' | 'DefinedTerm' | 'SizeSpecification' | None = None
    contentRating: str | 'Rating' | None = None
    accessMode: str | None = None
    creator: 'Person' | 'Organization' | None = None
    releasedEvent: 'PublicationEvent' | None = None
    accessibilitySummary: str | None = None
    translationOfWork: 'CreativeWork' | None = None
    publisherImprint: 'Organization' | None = None
    typicalAgeRange: str | None = None
    comment: 'Comment' | None = None
    encoding: 'MediaObject' | None = None
    discussionUrl: 'URL' | None = None
    timeRequired: 'Duration' | None = None
    isAccessibleForFree: bool | None = None
    audio: 'AudioObject' | 'MusicRecording' | 'Clip' | None = None
    correction: 'URL' | str | 'CorrectionComment' | None = None
    author: 'Person' | 'Organization' | None = None
    genre: 'URL' | str | None = None