const uniform = (a, b) => a + (b - a) * Math.random();

const randRange = (start, stop = undefined, step = 1) => {
  if (stop === undefined) {
    stop = start;
    return Math.floor(Math.random() * stop) * step;
  }

  const multiplier = (stop - start) / step;
  return start + Math.floor(Math.random() * multiplier) * step;
};

const randInt = (start, stop) => randRange(start, stop + 1);

const randomChoice = array => {
  const index = randRange(array.length);
  return array[index];
};
