from functools import cached_property
from itertools import accumulate, product


class NumberGenerator:
    def __init__(self, letters="AB", digits="012", length=3):
        self.letters = letters
        self.digits = digits
        self.length = length
        self.thresholds = list(
            accumulate(
                self.letter_base**i * self.digit_base ** (self.length - i)
                for i in range(1, self.length + 1)
            )
        )

    @property
    def letter_base(self):
        return len(self.letters)

    @property
    def digit_base(self):
        return len(self.digits)

    @cached_property
    def max_combinations(self):
        return sum(
            self.letter_base**i * self.digit_base ** (self.length - i)
            for i in range(1, self.length + 1)
        )

    def format(self, number):
        if number < 0 or number >= self.max_combinations:
            raise IndexError(f"{number} exceeded range [0, {self.max_combinations}\)")

        if not isinstance(number, int):
            raise TypeError(f"{self.__class__.__name__} can only format integers")

        for idx, threshold in enumerate(self.thresholds, start=1):
            if number < threshold:
                number_of_letters = idx
                number_of_digits = self.length - idx

                for i, val in enumerate(
                    product(
                        *(self.letters,) * number_of_letters,
                        *(self.digits,) * number_of_digits,
                    )
                ):
                    if i == number and idx == 1:
                        return "".join(val)

                    normalized_number = number - self.thresholds[idx - 2]
                    if i == normalized_number and idx > 1:
                        return "".join(val)
