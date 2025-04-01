""" Convert orthographic text to a stream of IPA phonemes. """

from wrappers import WRAPPER_BACKENDS

def phonemize_utterances(lines, backend, language, keep_word_boundaries, verbose=False, use_folding=True, **wrapper_kwargs):
    """ Phonemizes lines using a specified wrapper and language.

    Args:
        lines (list of str): The lines to phonemize.
        backend (str): The backend to use for phonemization.
        language (str): The language to phonemize.
        keep_word_boundaries (bool): Whether to keep word boundaries.
        verbose (bool): Whether to print debug information.
        use_folding (bool): Whether to use folding dictionaries to correct the wrapper's output.
        **wrapper_kwargs: Additional keyword arguments.
    
    Returns:
        list of str: The phonemized lines.

    Raises:
        ValueError: If the backend is not supported.
        ValueError: If the language is not supported by the backend.
        ValueError: If an argument is not supported by the wrapper.
        ValueError: If an argument is not the correct type.

    The returned list will be the same length as `lines`. Each line will be a string of space-separated IPA phonemes,
    with 'WORD_BOUNDARY' separating words if keep_word_boundaries=True. Lines that could not be phonemized are returned as empty strings.

    E.g:
    Input: ['hello there!', 'this is a test.']
    Output: ['h ə l oʊ WORD_BOUNDARY ð ɛ ɹ WORD_BOUNDARY', 'ð ɪ s WORD_BOUNDARY ɪ z WORD_BOUNDARY ə WORD_BOUNDARY t ɛ s t WORD_BOUNDARY']
    """

    if backend not in WRAPPER_BACKENDS:
        raise ValueError(f'Backend "{backend}" not supported. Supported backends: {list(WRAPPER_BACKENDS.keys())}')
    wrapper = WRAPPER_BACKENDS[backend](language=language, keep_word_boundaries=keep_word_boundaries, verbose=verbose, use_folding=use_folding, **wrapper_kwargs)
    return wrapper.phonemize(lines)

def character_split_utterances(lines):
    """ Used to split a line of orthographic text into characters separated by spaces.
    The resulting representation is similar to what is produced by phonemize_utterance, facilitating comparison.

    E.g:
    Input: ['hello there!', 'this is a test.']
    Output: ['h e l l o  WORD_BOUNDARY t h e r e WORD_BOUNDARY !', 't h i s  WORD_BOUNDARY i s  WORD_BOUNDARY a  WORD_BOUNDARY t e s t  WORD_BOUNDARY .']

    """
    return [' '.join(['WORD_BOUNDARY' if c == ' ' else c for c in list(line.strip())]) + ' WORD_BOUNDARY' for line in lines]
