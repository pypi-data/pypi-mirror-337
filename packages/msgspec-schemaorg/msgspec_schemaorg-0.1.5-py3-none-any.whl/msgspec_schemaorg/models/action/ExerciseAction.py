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
    opponent: Union[List['Person'], 'Person', None] = None
    sportsTeam: Union[List['SportsTeam'], 'SportsTeam', None] = None
    distance: Union[List['Distance'], 'Distance', None] = None
    sportsEvent: Union[List['SportsEvent'], 'SportsEvent', None] = None
    sportsActivityLocation: Union[List['SportsActivityLocation'], 'SportsActivityLocation', None] = None
    fromLocation: Union[List['Place'], 'Place', None] = None
    exercisePlan: Union[List['ExercisePlan'], 'ExercisePlan', None] = None
    course: Union[List['Place'], 'Place', None] = None
    exerciseRelatedDiet: Union[List['Diet'], 'Diet', None] = None
    diet: Union[List['Diet'], 'Diet', None] = None
    exerciseType: Union[List[str], str, None] = None
    exerciseCourse: Union[List['Place'], 'Place', None] = None
    toLocation: Union[List['Place'], 'Place', None] = None