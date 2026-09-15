export function bits(value) {
  return value.toString(2).padStart(8, '0').split('').map(Number);
}

export function shift(value, direction, places = 1) {
  if (!Number.isInteger(value) || value < 0 || value > 255 ||
      !Number.isInteger(places) || places < 1 || places > 8 ||
      !['left', 'right'].includes(direction)) throw new RangeError('Invalid 8-bit shift');
  const full = direction === 'left' ? value * 2 ** places : Math.floor(value / 2 ** places);
  return { value: full % 256, full, overflow: full > 255,
    lost: direction === 'left' ? Math.floor(value / 2 ** (8 - places)) : value % 2 ** places };
}
