import numpy as np

from typing import Dict


def build_tokenizer(string: str) -> Dict[str, int]:
    tokens = set(string)
    return {token: token_id for token_id, token in enumerate([""] + list(tokens))}


def tokenize(string: str, tokenizer: Dict[str, int]) -> np.ndarray:
    return np.array([tokenizer.get(c, 0) for c in string])


def markov_model(token_stream: np.ndarray) -> np.ndarray:
    size = np.max(token_stream) + 1
    model = np.ones((size, size), dtype=np.float32)

    for i, j in zip(token_stream[:-1], token_stream[1:]):
        if i != 0 and j != 0:
            model[i, j] += 1

    sum_domain = np.sum(model, axis=1)
    model /= sum_domain[:, None]

    return model


def log_likelihood(token_stream: np.ndarray, model: np.ndarray) -> float:
    prob = 0
    for i, j in zip(token_stream[:-1], token_stream[1:]):
        prob += float(np.log(model[i, j]))

    return prob


sample = "In probability theory and statistics, a Markov chain or Markov process is a stochastic process describing a sequence of possible events in which the probability of each event depends only on the state attained in the previous event. Informally, this may be thought of as, 'What happens next depends only on the state of affairs now.' A countably infinite sequence, in which the chain moves state at discrete time steps, gives a discrete-time Markov chain (DTMC). A continuous-time process is called a continuous-time Markov chain (CTMC). Markov processes are named in honor of the Russian mathematician Andrey Markov."
tokenizer = build_tokenizer(sample)
model = markov_model(tokenize(sample, tokenizer))


def is_keysmash(text: str, threshold: float = 3.5) -> bool:
    ll = log_likelihood(tokenize(text, tokenizer), model)
    return (-ll / len(text)) > threshold
