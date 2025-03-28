import json
from functools import lru_cache
from pathlib import Path
from typing import Any, ClassVar

import numpy as np
from numpy.typing import NDArray

from media_analyzer.data.anaylzer_config import FullAnalyzerConfig
from media_analyzer.data.enums.analyzer_module import AnalyzerModule, VisualModule
from media_analyzer.data.enums.classification.activity_type import ActivityType
from media_analyzer.data.enums.classification.animal_type import AnimalType
from media_analyzer.data.enums.classification.document_type import DocumentType
from media_analyzer.data.enums.classification.event_type import EventType
from media_analyzer.data.enums.classification.object_type import ObjectType
from media_analyzer.data.enums.classification.people_type import PeopleType
from media_analyzer.data.enums.classification.scene_type import SceneType
from media_analyzer.data.enums.classification.weather_condition import (
    WeatherCondition,
    weather_condition_descriptions,
)
from media_analyzer.data.interfaces.frame_data import (
    ClassificationData,
    FrameData,
)
from media_analyzer.machine_learning.classifier.base_classifier import BaseClassifier
from media_analyzer.processing.pipeline.pipeline_module import PipelineModule


@lru_cache
def get_scenes() -> dict[str, str]:
    """Get the scene types from the scenes.json file."""
    scenes_path = Path(__file__).parents[2] / "assets/scenes.json"
    with scenes_path.open(encoding="utf-8") as f:
        result = json.load(f)
    assert isinstance(result, dict)
    return result


def classify_image_scene(
    image_embedding: NDArray[Any], classifier: BaseClassifier
) -> tuple[SceneType, float]:
    """Classify the scene of an image."""
    scenes = get_scenes()
    best_index, confidence = classifier.classify_image(
        image_embedding,
        list(scenes.values()),
    )
    # confidence threshold 0.003 or something could be good
    best_label = SceneType(list(scenes.keys())[best_index])
    pretty_low_confidence = 0.003
    if confidence < pretty_low_confidence:
        best_label = SceneType.UNKNOWN  # pragma: no cover
    return best_label, confidence


def binary_classifications(
    image_embedding: NDArray[Any],
    classifier: BaseClassifier,
) -> tuple[
    PeopleType | None,
    AnimalType | None,
    DocumentType | None,
    ObjectType | None,
    ActivityType | None,
    EventType | None,
    WeatherCondition | None,
    bool,
    bool,
    bool,
    bool,
]:
    """Perform binary classifications on the image."""
    people_type = classifier.classify_to_enum_with_descriptions(
        image_embedding,
        "This image contains people or a person.",
        "There are no people in this image.",
        {
            PeopleType.SELFIE: "This is a selfie where a person holds the camera, showing their "
            "face prominently.",
            PeopleType.GROUP: "This is a group photo",
            PeopleType.PORTRAIT: "This is a portrait photo of a person or persons",
            PeopleType.CROWD: "This is a crowd of people",
        },
    )

    animal_type = classifier.classify_to_enum(
        image_embedding,
        "This photo shows an animal or a pet, such as a cat, dog, guinea pig, rabbit, "
        "hamster, rat, chicken, or bird.",
        "There is no pet or animal here.",
        AnimalType,
    )

    document_type = classifier.classify_to_enum_with_descriptions(
        image_embedding,
        "This is a document, such as a receipt, book, "
        "ID card, passport, payment method, screenshot, event ticket, menu, "
        "recipe, or notes.",
        "This is not a document.",
        {
            DocumentType.BOOK_OR_MAGAZINE: "This is a book or a magazine.",
            DocumentType.RECEIPT: "This is a receipt or proof of payment.",
            DocumentType.SCREENSHOT: "This is a digital screenshot from a phone or a computer.",
            DocumentType.TICKET: "This is an event ticket, with information about the event and "
            "or the ticket holder.",
            DocumentType.IDENTITY: "This is an identity document, such as an ID card, "
            "passport, drivers license, or other identifiable "
            "card.",
            DocumentType.NOTES: "This is a person's notes, notebook, or homework.",
            DocumentType.PAYMENT_METHOD: "This is a payment method, such as a credit card or "
            "debit card.",
            DocumentType.MENU: "This is a restaurant menu.",
            DocumentType.RECIPE: "This is a recipe to create a meal.",
        },
    )

    object_type = classifier.classify_to_enum(
        image_embedding,
        "This is object-focused photo, such as food, a vehicle, artwork,"
        " a device, a piece of clothing, a drink, sports equipment, or a toy.",
        "The focus is not an object.",
        ObjectType,
    )

    activity_type = classifier.classify_to_enum(
        image_embedding,
        "An activity is performed in this image, such as "
        "sports, fitness, dancing, photography, writing, "
        "leisure activities, traveling, camping or water activities.",
        "No activity is actively performed in this image.",
        ActivityType,
    )

    event_type = classifier.classify_to_enum(
        image_embedding,
        "An event is taking place in this image, such as "
        "a wedding, birthday, other celebration, party, concert, work conference, "
        "meeting, funeral, christmas, halloween, new years, a sports game, "
        "competition, marathon, protest, parade, carnival, trip or picnic.",
        "No specific event or celebration is happening.",
        EventType,
    )

    is_outside, _ = classifier.binary_classify_image(
        image_embedding,
        "This is outside.",
        "This is inside.",
    )
    is_landscape, _ = classifier.binary_classify_image(
        image_embedding,
        "This is a landscape featuring natural scenery such as mountains, dunes, "
        "forests, or lakes.",
        "This is not a landscape or does not feature natural scenery.",
    )
    is_cityscape, _ = classifier.binary_classify_image(
        image_embedding,
        "This is a cityscape showing urban buildings, streets, or skylines.",
        "This is not a cityscape or does not feature urban areas.",
    )
    is_travel, _ = classifier.binary_classify_image(
        image_embedding,
        "This photo was taken during travel, featuring landmarks, airports, "
        "campsites, or exotic locations..",
        "This photo was not taken during travel or does not suggest a travel context.",
    )

    weather_type: WeatherCondition | None = None
    if is_outside:
        weather_type = classifier.classify_to_enum_with_descriptions(
            image_embedding,
            "The type of weather can be clearly determined from this photo.",
            "The weather conditions in this photo can not be determined.",
            weather_condition_descriptions,
        )

    return (
        people_type,
        animal_type,
        document_type,
        object_type,
        activity_type,
        event_type,
        weather_type,
        is_outside,
        is_landscape,
        is_cityscape,
        is_travel,
    )


class ClassificationModule(PipelineModule[FrameData]):
    """Classify an image based on its visual content."""

    depends: ClassVar[set[AnalyzerModule]] = {VisualModule.EMBEDDING}

    # pylint: disable-next=R0914
    def process(self, data: FrameData, config: FullAnalyzerConfig) -> None:
        """Classify an image based on its visual content."""
        (
            people_type,
            animal_type,
            document_type,
            object_type,
            activity_type,
            event_type,
            weather_type,
            is_outside,
            is_landscape,
            is_cityscape,
            is_travel,
        ) = binary_classifications(np.array(data.embedding), config.classifier)
        scene, _conf = classify_image_scene(np.array(data.embedding), config.classifier)

        data.classification = ClassificationData(
            people_type=people_type,
            animal_type=animal_type,
            document_type=document_type,
            object_type=object_type,
            activity_type=activity_type,
            event_type=event_type,
            weather_condition=weather_type,
            is_outside=is_outside,
            is_landscape=is_landscape,
            is_cityscape=is_cityscape,
            is_travel=is_travel,
            scene_type=scene,
        )
