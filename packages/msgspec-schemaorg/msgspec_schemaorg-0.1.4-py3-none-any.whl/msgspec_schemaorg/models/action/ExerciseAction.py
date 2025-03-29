from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.PlayAction import PlayAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.ExercisePlan import ExercisePlan
    from msgspec_schemaorg.models.event.SportsEvent import SportsEvent
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.organization.SportsTeam import SportsTeam
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.place.SportsActivityLocation import SportsActivityLocation
    from msgspec_schemaorg.models.thing.Diet import Diet
from typing import Optional, Union, Dict, List, Any


class ExerciseAction(PlayAction):
    """The act of participating in exertive activity for the purposes of improving health and fitness."""
    type: str = field(default_factory=lambda: "ExerciseAction", name="@type")
    opponent: 'Person' | None = None
    sportsTeam: 'SportsTeam' | None = None
    distance: 'Distance' | None = None
    sportsEvent: 'SportsEvent' | None = None
    sportsActivityLocation: 'SportsActivityLocation' | None = None
    fromLocation: 'Place' | None = None
    exercisePlan: 'ExercisePlan' | None = None
    course: 'Place' | None = None
    exerciseRelatedDiet: 'Diet' | None = None
    diet: 'Diet' | None = None
    exerciseType: str | None = None
    exerciseCourse: 'Place' | None = None
    toLocation: 'Place' | None = None