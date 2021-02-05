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


def iterable_contains_item_of_type(iterable, item_types) -> bool:
    """."""
    return any(item_types) in types(iterable)


def deduplicate(iterable: list) -> list:
    """Deduplicate the iterable."""
    og_iterable, temp_iterable = itertools.tee(iterable)

    if iterable_contains_item_of_type(temp_iterable, (dict, list)):
        deduplicated_list = []
        for i in og_iterable:
            if i not in deduplicated_list:
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
        full_cycle = list_cycle(list_arg, None)
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
    result = len(iterable) == 1
    return result


# TODO: This function requires one argument... is the signature for this function correct?
def iterables_are_same_length(*args: list, debug_failure: bool = False) -> bool:
    """Return whether or not the given iterables are the same lengths."""
    from democritus_dicts import dict_values

    lengths = map(len, args)
    result = iterable_has_single_item(lengths)

    if debug_failure and not result:
        list_length_breakdown = iterable_count(lengths)
        minority_list_count = min(dict_values(list_length_breakdown))
        for index, arg in enumerate(args):
            if list_length_breakdown[len(arg)] == minority_list_count:
                print(f'Argument {index} is not the same length as the majority of the arguments')

    return result


def iterables_have_same_items(a: Iterable[Any], b: Iterable[Any], *args: Iterable[Any]) -> bool:
    """See if the iterables have identical items."""
    first_list = a
    remaining_lists = [b]
    remaining_lists.extend(list(args))

    if iterables_are_same_length(a, b) and iterables_are_same_length(*remaining_lists):
        for item in first_list:
            first_list_count = first_list.count(item)
            item_counts = [list_.count(item) for list_ in remaining_lists]
            same_count = item_counts[0] == first_list_count
            if not list_has_single_item(item_counts) or not same_count:
                return False
        return True
    else:
        return False


def run_length_encoding(iterable: list, output_as_string: bool = False) -> Iterable[str]:
    """Perform run-length encoding on the given array. See https://en.wikipedia.org/wiki/Run-length_encoding for more details."""
    run_length_encodings = (f'{len(tuple(g))}{k}' for k, g in itertools.groupby('AAAABBBCCDAABBB'))
    return run_length_encodings


def iterable_count(iterable: list) -> Dict[Any, int]:
    """Count each item in the iterable."""
    from democritus_dicts import dict_sort_by_values

    count = {}
    for i in list_arg:
        count[i] = count.get(i, 0) + 1
    count = dict_sort_by_values(count)
    return count


def list_item_index(list_arg: list, item: Any) -> int:
    """Find the given item in the iterable. Return -1 if the item is not found."""
    try:
        return list_arg.index(item)
    except ValueError:
        return -1


def list_item_indexes(list_arg: list, item: Any) -> Tuple[int, ...]:
    """Find the given item in the iterable. Return -1 if the item is not found."""
    indexes = [index for index, value in enumerate(list_arg) if value == item]
    return indexes


def list_duplicates(list_a: list, list_b: list = None, *, deduplicate_results: bool = True) -> list:
    """Find duplicates. If deduplicate_results is False, all instances of a duplicate will be added to the resulting list."""
    if list_b is not None:
        if deduplicate_results:
            return list(set(list_a).intersection(set(list_b)))
        else:
            duplicates = []
            for item in list_a:
                if list_b.count(item) > 0:
                    duplicates.append(item)
            return duplicates
    else:
        # TODO: I used to use pydash, but have removed it to simplify the required packages
        # import pydash.arrays
        # return pydash.arrays.duplicates(list_a)
        duplicates = []
        for item in list_a:
            if list_a.count(item) > 1:
                duplicates.append(item)

        if deduplicate_results:
            return deduplicate(duplicates)
        else:
            return duplicates


def list_has_item_of_type(list_arg: list, type_arg) -> bool:
    """Return whether or not there is at least one item of the type specified by the type_arg in the list_arg."""
    return type_arg in types(list_arg)


def list_has_all_items_of_type(list_arg: list, type_arg) -> bool:
    """Return whether or not all items in list_arg are of the type specified by the type_arg."""
    item_types = types(list_arg)
    result = item_types[0] == type_arg and list_has_single_item(item_types)
    return result


def list_has_mixed_types(list_arg: list) -> bool:
    """Return whether or not the list_arg has items with two or more types."""
    print(f'tuple(types(list_arg)): {tuple(types(list_arg))}')
    print(tuple(deduplicate(types(list_arg))))
    return len(tuple(deduplicate(types(list_arg)))) >= 2


def list_has_single_type(list_arg: list) -> bool:
    """Return whether or not the list_arg has items of only one type."""
    return len(tuple(deduplicate(types(list_arg)))) == 1


def list_join(list_arg: list, join_characters: str = ',') -> str:
    string_list = [str(item) for item in list_arg]
    return join_characters.join(string_list)


def lists_combine(list_a: list, list_b: list, *args: list) -> list:
    """Combine list_a, list_b, and any args into one list."""
    list_a.extend(list_b)
    for list_ in args:
        list_a.extend(list_)
    return list_a


# TODO: consider renaming this to `list_delete_all_instances_of_item`
def list_delete_item(list_arg: list, item_to_delete: Any) -> list:
    """Remove all instances of the given item_to_delete from the list_arg."""
    from itertools import filterfalse

    result = filterfalse(lambda x: x == item_to_delete, list_arg)
    return result


def list_replace(list_arg: list, old_value, new_value, *, replace_in_place: bool = True) -> list:
    """Replace all instances of the old_value with the new_value in the given list_arg."""
    old_value_indexes = list_item_indexes(list_arg, old_value)
    new_list = list_delete_item(list_arg, old_value)

    for index in old_value_indexes:
        if replace_in_place:
            new_list.insert(index, new_value)
        else:
            new_list.append(new_value)

    return new_list


# def list_entropy(list_arg: list):
#     """Find the entropy of the items in the given list."""
#     import math
#     from nlp import frequencyDistribution

#     freqdist = frequencyDistribution(iterable)
#     probs = [freqdist.freq(l) for l in freqdist]
#     return -sum(p * math.log(p, 2) for p in probs)
