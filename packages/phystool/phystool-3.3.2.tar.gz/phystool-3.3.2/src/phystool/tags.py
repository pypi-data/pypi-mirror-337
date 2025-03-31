import json
from logging import getLogger
from typing import (
    ClassVar,
    Iterator,
    Self,
)

from phystool.config import config

logger = getLogger(__name__)


class Tags:
    """
    This class allows to tag PDBFiles with user defined tags sorted by custom
    categories.

    :warning: Directly creating an instance without using Tags.validate could
        lead to unwanted tags.

    :param tags: tags sorted by category
    """
    TAGS: ClassVar['Tags']

    @classmethod
    def validate(cls, list_of_tags: str) -> Self:
        """Converts a string of comma separated words into a valid Tags
        instance.

        The string is split after each comma. If the words in the resulting
        list are valid tags, they will be sorted by category.

        :param list_of_tags: string of comma separated words
        :returns: a Tags instance with only valid tags
        """
        if not list_of_tags:
            return cls({})

        tmp: dict[str, set[str]] = dict()
        for tag in [tag.strip() for tag in list_of_tags.split(',')]:
            valid = False
            for category, tags in cls.TAGS:
                if tag in tags:
                    valid = True
                    try:
                        tmp[category].add(tag)
                    except KeyError:
                        tmp[category] = {tag}
            if not valid:
                logger.warning(f"Invalid tag {tag}")

        return cls({cat: sorted(tags) for cat, tags in tmp.items()})

    @classmethod
    def list_valid_tags(cls) -> None:
        for _, tags in cls.TAGS:
            for tag in tags:
                print(tag)

    @classmethod
    def load(cls) -> None:
        if config.TAGS_PATH.exists():
            with config.TAGS_PATH.open() as jsin:
                Tags.TAGS = Tags(json.load(jsin))
        else:
            Tags.reset_all_tags()

    @classmethod
    def save(cls) -> None:
        with config.TAGS_PATH.open("w") as jsout:
            json.dump(cls.TAGS.data, jsout, indent=4, ensure_ascii=False)

    @classmethod
    def reset_all_tags(cls) -> None:
        tmp: dict[str, set[str]] = dict()
        for json_file in config.DB_DIR.glob('*.json'):
            with json_file.open() as jsin:
                for category, tags in json.load(jsin).get('tags', {}).items():
                    if tags:  # so that unused category are removed
                        try:
                            tmp[category] |= set(tags)
                        except KeyError:
                            tmp[category] = set(tags)

        cls.TAGS = Tags({cat: sorted(tags) for cat, tags in tmp.items()})
        cls.save()

    @classmethod
    def create_new_tag(cls, category: str, tag: str) -> None:
        if tags := cls.TAGS[category]:
            tags.append(tag)
            tags.sort()
        else:
            cls.TAGS.data[category] = [tag]
        cls.save()

    def __init__(self, tags: dict[str, list[str]]):
        self.data = tags

    def __getitem__(self, key) -> list[str]:
        return self.data.get(key, [])

    def __iter__(self) -> Iterator[tuple[str, list[str]]]:
        for category, tags in self.data.items():
            yield category, tags

    def __add__(self, other: Self) -> Self:
        out = type(self)(self.data.copy())  # Tags != Self
        out += other
        return out

    def __iadd__(self, other: Self) -> Self:
        self.data = {
            category: tags
            for category in self.TAGS.data.keys()
            if (tags := sorted(set(self[category] + other[category])))
        }
        return self

    def __sub__(self, other: Self) -> Self:
        out = type(self)(self.data.copy())  # Tags != Self
        out -= other
        return out

    def __isub__(self, other: Self) -> Self:
        self.data = {
            category: tags
            for category in self.TAGS.data.keys()
            if (tags := sorted(set(self[category]) - set(other[category])))
        }
        return self

    def __bool__(self) -> bool:
        for tags in self.data.values():
            if tags:
                return True
        return False

    def __str__(self) -> str:
        return ", ".join(
            [
                tag
                for tags in self.data.values()
                for tag in tags
            ]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tags):
            return False

        if len(self.data.keys()) != len(other.data.keys()):
            return False

        for category, tags in self:
            if set(other[category]) != set(tags):
                return False
        return True

    def with_overlap(self, other: Self) -> bool:
        """
        Returns `False` for the first category where there isn't any shared tag
        bewteen this instance and the other instance, otherwise, returns `True`

        :warning: if, for a given category, either set is empty (this should
        not happen), the method will return `False`

        """
        # FIXME: finish this
        if other:
            for category in other.data.keys():
                if set(self[category]).isdisjoint(other[category]):
                    return False
        return True

    def without_overlap(self, other: Self) -> bool:
        """
        Returns `False` for the first category where there is at least one
        shared tag bewteen this instance and the other instance, otherwise,
        returns `True`

        A.isdisjoint(B) return True if either the set A or B is empty
        """
        if other:
            for category in other.data.keys():
                if not set(self[category]).isdisjoint(other[category]):
                    return False
        return True


Tags.load()
