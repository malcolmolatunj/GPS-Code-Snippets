class Numeric:
    def __init__(self, precision=18, scale=0):
        self.precision = precision
        self.scale = scale

    @staticmethod
    def sum(num):
        return Numeric(38, num.scale)

    @property
    def integral(self):
        return self.precision - self.scale

    def __str__(self):
        return f"({self.precision},{self.scale})"

    def __repr__(self):
        return f"Numeric(precision={self.precision}, scale={self.scale})"

    @staticmethod
    def _mult_overflow(precision, scale):
        if precision > 38:
            integral = precision - scale
            if integral <= 32:
                scale = min(scale, 38 - integral)
            elif scale > 6:
                return Numeric(38, 6)
            precision = min(38, precision)
        return Numeric(precision, scale)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        new_precision = (
            max(self.scale, other.scale) + max(self.integral, other.integral) + 1
        )
        new_scale = max(self.scale, other.scale)

        if max(self.integral, other.integral) > min(38, new_precision) - new_scale:
            new_precision = 38
            new_scale = new_precision - max(self.integral, other.integral)
        return Numeric(new_precision, new_scale)

    def __sub__(self, other):
        return self.__add__(other)

    def __mul__(self, other):

        if not isinstance(other, self.__class__):
            raise NotImplementedError

        new_precision = self.precision + other.precision + 1
        new_scale = self.scale + other.scale

        return self._mult_overflow(new_precision, new_scale)

        # if new_precision > 38:
        #     integral = new_precision - new_scale
        #     if integral <= 32:
        #         new_scale = min(new_scale, 38 - integral)
        #     elif new_scale > 6:
        #         return Numeric(38, 6)
        #     new_precision = min(38, new_precision)
        # return Numeric(new_precision, new_scale)

    def __truediv__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        new_precision = (
            self.integral + other.scale + max(6, self.scale + other.precision + 1)
        )
        new_scale = max(6, self.scale + other.precision + 1)

        return self._mult_overflow(new_precision, new_scale)
        # if new_precision > 38:
        #     integral = new_precision - new_scale
        #     if integral <= 32:
        #         new_scale = min(new_scale, 38 - integral)
        #     elif new_scale > 6:
        #         return Numeric(38, 6)
        #     new_precision = min(38, new_precision)
        # return Numeric(new_precision, new_scale)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError
        return self.precision == other.precision and self.scale == other.scale


print(
    Numeric.sum(Numeric(18, 4) * Numeric(5, 2) / Numeric(3))
    / (Numeric(18, 4) - Numeric(18, 4) - Numeric(18, 4))
    * Numeric(18, 4)
)
