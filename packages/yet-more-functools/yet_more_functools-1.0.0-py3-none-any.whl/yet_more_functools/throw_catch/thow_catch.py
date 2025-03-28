# SPDX-FileCopyrightText: © 2025 Roger Wilson
#
# SPDX-License-Identifier: MIT

import contextlib as cl
import contextvars as cv
import typing as ty
import warnings

# This contextvar must be created on main thread.
_THROW_CATCH_CONTEXT = cv.ContextVar('THROW_CATCH_CONTEXT', default={})

CATCHER_TAG_TYPE = ty.Union[ty.Hashable, ty.Tuple[ty.Hashable, bool]]


class ThrowCatchException(Exception):
    """
    This is a carrier exception which transports the object "thrown" to a catch/catcher listening for the same tag.
    """

    def __init__(self, thrown, tag=None):
        super().__init__()
        self.thrown = thrown
        self.tag = tag


def throw(x: ty.Any, tag: ty.Union[ty.Hashable, ty.Sequence[ty.Hashable]] = None):
    """
    Calls to sow work in conjunction with calls to "catch" or "catcher".  Together they allow intermediate values to
    be returned from arbitrarily deep in the call hierarchy, interrupting the execution flow.

    throw(x, [tag=None])

    See also: catch, catcher.

    Example.

    .. code-block:: python

        def f(x):
            if x==0:
                throw(x)
            return x+1

        catch(f, 0)

    will return (None, 0) : As the throw executed, so f did not return,  and None is the default tag for both throw
    and catch.

    catch(f, 1)

    will return 2 : As the throw didn't execute so f returned normally.

    Execution flow is interrupted by raising a special type of exception but only if throw knows an encapsulating
    catcher or catch is waiting to handle it with a matching tag.

    :param x: The value being thrown.
    :param tag: The (hashable) tag value or sequence of tags for which the value x is to be thrown, matching tag or
        tags in an enclosing catch or catcher.
        Default is None.
    :return: None.
    """
    if not isinstance(tag, str) and not isinstance(tag, tuple) and isinstance(tag, ty.Sequence):
        for t in tag:
            throw(x, tag=t)
    else:
        if tag in _THROW_CATCH_CONTEXT.get():
            if _THROW_CATCH_CONTEXT.get()[tag][-1]:
                raise ThrowCatchException(x, tag=tag)
            else:
                return None
        elif None in _THROW_CATCH_CONTEXT.get():
            if _THROW_CATCH_CONTEXT.get()[None][-1]:
                warnings.warn(
                    f'No tag {tag} found as there is no outer catch for this specific tag.  Values will be sent to the '
                    f'tag=None catch which does exist as tuples of (tag, value).')
                raise ThrowCatchException((tag, x), tag=None)
        else:
            warnings.warn(f'No tag {tag} found as there is no outer catch for this tag OR tag=None.',
                          category=UserWarning)
            return None


@cl.contextmanager
def catcher(tag: ty.Union[CATCHER_TAG_TYPE, ty.Sequence[CATCHER_TAG_TYPE]] = None) -> \
        ty.Generator[ty.Callable, None, None]:
    """
    Catcher is a context manager which wraps around the execution of arbitrary code and catches the values 'thrown'
    by any calls to throw made inside the managed block.  It emits a callable which may be called after the block
    completes that carries any value thrown, as a 2-tuple: (tag, value), or None is nothing was thrown.

    catcher([tag=None])

    Example:

    .. code-block:: python

        def f(x):
            if x==0:
                throw(x)
            return x+1

        with catcher() as ct:
            print(f"The return value was {f(0)}.")
        print(f"The caught value was {ct()}")

        with catcher() as ct:
            print(f"The return value was {f(1)}.")
        print(f"The caught value was {ct()}")


    Will produce:
    .. code-block:: text

        The caught value was (None, 0)
        The return value was 2.
        The caught value was None

    Note that the first print in the first context-managed block does not actually run.  Execution is interrupted
    inside f and returns into the context-manager catcher.

    :param tag: A hashable tag, a 2-tuple: (hashable tag, boolean) or a mixed sequence of these.
    :return: A zero-argument executable which will return a 2-tuple: (tag, value thrown) or None if no throw on any
        of the tags given occurs.
    """
    tag = reform_tag(tag)

    def return_caught():
        """This is the callable that is returned by the context manager to carry the caught data."""
        if not return_caught.status:
            raise RuntimeError("Context manager 'catcher' context manager block has not exited: Nothing to catch.")
        return return_caught.caught

    return_caught.status = False
    return_caught.caught = None

    _tce = None
    try:
        scatter(tag)
        try:
            yield return_caught
        except ThrowCatchException as tce:
            _tce = tce
    finally:
        # The True lets us know that gather has been executed, and we are therefore out of the context try block.
        # Different to reaper, as in reaper the result of gather will always be something, whereas here it can be None.
        return_caught.status = True
        return_caught.caught = gather(tag, _tce)
        # Reraise the exception if we were not checking for the relevant tag.
        if return_caught.caught is None and _tce is not None:
            raise _tce


def catch(f: ty.Callable, *args, tag: ty.Union[CATCHER_TAG_TYPE, ty.Sequence[CATCHER_TAG_TYPE]] = None, **kwargs) -> \
        ty.Any:
    """
    Catch executes the function f with the given args and kwargs within a catcher context managed block and returns
    either the result of the call to f or any value thrown during the execution of f on any of the tags given.

    catch(f, *args, **kwargs, [tag=None])

    examples:

    .. code-block:: python

        def f(x):
            if x==0:
                throw(x)
            return x+1

        print(f"catch(f, 0) = {catch(f, 0)}")

        print(f"catch(f, 1) = {catch(f, 1)}")

    Will produce:

    .. code-block:: text

        catch(f, 0) = (None, 0)
        catch(f, 1) = 2

    In the first case throw is executed and f is interrupted so the return from catch is a 2-tuple of (None,
    0) where None is the default tag and 0 is the value thrown.  In the second case 2 returned as f executes to the end.

    :param f: An executable function.
    :param args: Passed to f.
    :param tag: A hashable tag, a 2-tuple: (hashable tag, boolean) or a mixed sequence of these.
    :param kwargs: Passed to f.
    :return: The value returned by f (if no throw occurs) or a 2-tuple: (tag, value thrown) if a throw does occur.
    """
    if not callable(f):
        raise TypeError('First argument to catch must be a callable.')

    with catcher(tag) as ct:
        result = f(*args, **kwargs)

    if (caught := ct()) is not None:
        return caught
    return result


def reform_tag(tag: ty.Union[CATCHER_TAG_TYPE, ty.Sequence[CATCHER_TAG_TYPE]]) -> \
        ty.Sequence[ty.Tuple[ty.Hashable, bool]]:
    """
    Turn an arbitrary tag, either hashable (strings most likely) OR a 2-tuple of (hashable tag,  boolean) to turn the
    tag on or off or any mixed sequence of these,  into a uniform sequence of 2-tuples: (hashable, bool).
    :param tag: An individual hashable tag, 2-tuple of (hashable tag, bool) or mixed sequence of same.
    :return: An explicit list of 2-tuples: (hashable tag, bool)
    """
    if isinstance(tag, tuple) and len(tag) == 2 and isinstance(tag[0], ty.Hashable) and isinstance(tag[1], bool):
        # noinspection PyTypeChecker
        return [tag]
    elif isinstance(tag, ty.Hashable):
        return [(tag, True)]
    if not isinstance(tag, tuple) and isinstance(tag, ty.Sequence):
        # noinspection PyTypeChecker
        return sum((reform_tag(t) for t in tag), [])
    raise ValueError(
        f"Reap cannot handle tag of type {tag}. Note as tags can be tuples, any sequences of tags must not be "
        f"tuples themselves, use list.")


def scatter(tag: ty.Sequence[ty.Tuple[ty.Hashable, bool]]) -> None:
    """
    Appends the on/off state bool for each given tag onto the FIFO stacks for each tag. Setting up a stack for any
    unknown tag.
    :param tag:  An explicit list of 2-tuples: (hashable tag, bool)
    :return: None
    """
    for t, s in tag:
        if not t in _THROW_CATCH_CONTEXT.get():
            _THROW_CATCH_CONTEXT.get()[t] = [s]
        else:
            _THROW_CATCH_CONTEXT.get()[t].append(s)


def gather(tag: ty.Sequence[ty.Tuple[ty.Hashable, bool]], tce: ty.Union[None, ThrowCatchException]) -> \
        ty.Union[None, ty.Tuple[ty.Hashable, ty.Any]]:
    """
    Loop through the tags we're looking for and pop (their on/off state) them off the context stacks AND if any match
    the tag of the ThrowCatchException thrown return that tag and the thrown value.
    :param tag:  An explicit list of 2-tuples: (hashable tag, bool)
    :param tce: None if no exception has been thrown (by a deeper throw) or a ThrowCatchException if one was thrown.
    :return:  None if nothing is caught or a 2-tuple: (tag, thrown value).
    """
    gathered = None
    for t, s in tag:
        if s:
            # At most only one thing will be caught as there can only be one exception at a time.
            gathered = gathered if (tce is None or t != tce.tag) else (tce.tag, tce.thrown)
        # ... dropping them from the context...
        _THROW_CATCH_CONTEXT.get()[t].pop(-1)
        # ...and tidying it up if necessary.
        if len(_THROW_CATCH_CONTEXT.get()[t]) == 0:
            _THROW_CATCH_CONTEXT.get().pop(t)
    return gathered


def _peek():
    # This is used within tests to check that we have tidied up properly.
    return _THROW_CATCH_CONTEXT.get().keys()
