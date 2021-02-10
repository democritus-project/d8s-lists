import itertools
from typing import Any, Union, List, Dict, Iterable, Tuple

# TODO: consider applying @decorators.listify_first_arg argument to all/most functions in this module
# TODO: update the type hints on the functions below


def iterable_sort_by_length(list_arg: List[Any], **kwargs) -> List[Any]:
    """."""
    sorted_list = sorted(list_arg, key=lambda x: len(x), **kwargs)
    return sorted_list


def longest(iterable: List[Any]) -> Any:
    """."""
    longest_item = max(iterable, key=len)
    return longest_item


def shortest(iterable: List[Any]) -> Any:
    """."""
    shortest_item = min(iterable, key=len)
    return shortest_item


def flatten(list_arg: list, level: int = None, **kwargs) -> list:
    """Flatten all items in the list_arg so that they are all items in the same list."""
    import more_itertools

    return more_itertools.collapse(list_arg, levels=level, **kwargs)


def has_index(iterable: list, index: int) -> bool:
    """."""
    # TODO: would it be faster to simply try to get the item at index and handle exceptions
    index_int = int(index)
    if index_int >= 0 and index_int <= len(iterable) - 1:
        return True
    else:
        return False


def types(iterable: list) -> List[str]:
    """Return a set containing the types of all items in the list_arg."""
    return map(type, iterable)


def iterable_item_of_types(iterable, item_types) -> bool:
    """Return True if the iterable has any items that are of the types given in item_types. Otherwise, return False."""
    iterable_types = types(iterable)
    for iterable_type in iterable_types:
        if iterable_type in item_types:
            return True
    return False


def iterable_all_items_of_types(iterable, item_types) -> bool:
    """Return True if all items in the iterable are of a type given in item_types. Otherwise, return False."""
    iterable_types = types(iterable)
    for iterable_type in iterable_types:
        if iterable_type not in item_types:
            return False
    return True


def iterable_has_all_items_of_type(iterable: list, type_arg) -> bool:
    """Return whether or not all iterable in iterable are of the type specified by the type_arg."""
    item_types_1, item_types_2 = itertools.tee(types(iterable))
    result = iterable_has_single_item(item_types_1) and next(item_types_2) == type_arg
    return result


def deduplicate(iterable: list) -> list:
    """Deduplicate the iterable."""
    og_iterable, temp_iterable = itertools.tee(iterable)

    if iterable_item_of_types(temp_iterable, (dict, list)):
        deduplicated_list = []
        for i in og_iterable:
            if i not in deduplicated_list:
                deduplicated_list.append(i)
                yield i
    else:
        # TODO: will this work for every type except for dicts and lists???
        yield from list(set(og_iterable))


# TODO: is there a function in more_itertools to do this?
def cycle(list_arg: list, length: Union[int, None] = None) -> list:
    """Cycle through the list_arg as much as needed."""
    import itertools

    if length is None:
        return itertools.cycle(list_arg)
    else:
        full_cycle = cycle(list_arg, None)
        partial_cycle = []
        for index, item in enumerate(full_cycle):
            partial_cycle.append(item)
            if index == length - 1:
                break
        return partial_cycle


def truthy_items(iterable: list) -> list:
    """Return an iterable with only elements of the given iterable which evaluate to True (see https://docs.python.org/3.9/library/stdtypes.html#truth-value-testing)."""
    return filter(lambda x: x, iterable)


def nontruthy_items(iterable: list) -> list:
    """Return an iterable with only elements of the given iterable which evaluate to False (see https://docs.python.org/3.9/library/stdtypes.html#truth-value-testing)."""
    return filter(lambda x: not x, iterable)


def iterable_has_single_item(iterable: list) -> bool:
    """Return whether the iterable has a single item in it."""
    iterable = deduplicate(iterable)
    result = len(tuple(iterable)) == 1
    return result


def iterables_are_same_length(
    a: Iterable[Any], b: Iterable[Any], *args: Iterable[Any], debug_failure: bool = False
) -> bool:
    """Return whether or not the given iterables are the same lengths."""
    from democritus_dicts import dict_values

    consolidated_list = [a, b, *args]
    lengths_1, lengths_2 = itertools.tee(map(len, consolidated_list))

    result = iterable_has_single_item(lengths_1)

    if debug_failure and not result:
        list_length_breakdown = iterable_count(lengths_2)
        minority_list_count = min(dict_values(list_length_breakdown))
        for index, arg in enumerate(consolidated_list):
            if list_length_breakdown[len(arg)] == minority_list_count:
                print(f'Argument {index} is not the same length as the majority of the arguments')

    return result


def iterables_have_same_items(a: Iterable[Any], b: Iterable[Any], *args: Iterable[Any]) -> bool:
    """See if the iterables have identical items (both in the identity of each item and the count of each item present)."""
    first_list = a
    remaining_lists = [b, *args]

    if iterables_are_same_length(a, *remaining_lists):
        for item in first_list:
            first_list_count = first_list.count(item)
            item_counts = [list_.count(item) for list_ in remaining_lists]
            same_count = item_counts[0] == first_list_count
            if not iterable_has_single_item(item_counts) or not same_count:
                return False
    else:
        return False
    return True


def run_length_encoding(iterable: list, output_as_string: bool = False) -> Iterable[str]:
    """Perform run-length encoding on the given array. See https://en.wikipedia.org/wiki/Run-length_encoding for more details."""
    run_length_encodings = (f'{len(tuple(g))}{k}' for k, g in itertools.groupby(iterable))
    return run_length_encodings


def iterable_count(iterable: list) -> Dict[Any, int]:
    """Count each item in the iterable."""
    from democritus_dicts import dict_sort_by_values

    count = {}
    for i in iterable:
        count[i] = count.get(i, 0) + 1
    count = dict_sort_by_values(count)
    return count


def iterable_item_index(iterable: list, item: Any) -> int:
    """Find the given item in the iterable. Return -1 if the item is not found."""
    try:
        return iterable.index(item)
    except ValueError:
        return -1


def iterable_item_indexes(list_arg: list, item: Any) -> Tuple[int, ...]:
    """Find the given item in the iterable. Return -1 if the item is not found."""
    indexes = [index for index, value in enumerate(list_arg) if value == item]
    return indexes


def duplicates(iterable: list) -> list:
    """Find duplicates in the given iterable."""
    duplicates = []
    for item in iterable:
        if iterable.count(item) > 1:
            yield item


def iterable_has_mixed_types(list_arg: list) -> bool:
    """Return whether or not the list_arg has items with two or more types."""
    print(f'tuple(types(list_arg)): {tuple(types(list_arg))}')
    print(tuple(deduplicate(types(list_arg))))
    return len(tuple(deduplicate(types(list_arg)))) >= 2


def iterable_has_single_type(list_arg: list) -> bool:
    """Return whether or not the list_arg has items of only one type."""
    return len(tuple(deduplicate(types(list_arg)))) == 1


def iterable_replace(iterable: list, old_value, new_value, *, replace_in_place: bool = True) -> list:
    """Replace all instances of the old_value with the new_value in the given iterable."""
    for index, value in enumerate(iterable):
        if value == old_value:
            yield new_value
        else:
            yield value


# def list_entropy(list_arg: list):
#     """Find the entropy of the items in the given list."""
#     import math
#     from nlp import frequencyDistribution

#     freqdist = frequencyDistribution(iterable)
#     probs = [freqdist.freq(l) for l in freqdist]
#     return -sum(p * math.log(p, 2) for p in probs)
