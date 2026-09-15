import { test } from 'node:test';
import assert from 'node:assert/strict';
import { bits, shift } from '../static/math.mjs';

test('original lesson examples', () => {
  assert.equal(bits(45).join(''), '00101101');
  assert.equal(shift(45, 'left').value, 90);
  assert.deepEqual(shift(200, 'left'), {value: 144, full: 400, overflow: true, lost: 1});
});
test('all unsigned bytes and shift counts match binary truncation', () => {
  for (let value = 0; value < 256; value++) {
    for (let count = 1; count <= 8; count++) {
      const binary = bits(value).join('');
      assert.equal(shift(value, 'left', count).value, parseInt((binary + '0'.repeat(count)).slice(-8), 2));
      assert.equal(shift(value, 'right', count).value, parseInt(('0'.repeat(count) + binary).slice(0, 8), 2));
    }
  }
});
test('invalid inputs are rejected', () => {
  for (const value of [-1, 256, 1.5, NaN]) assert.throws(() => shift(value, 'left'), RangeError);
  assert.throws(() => shift(45, 'left', 9), RangeError);
  assert.throws(() => shift(45, 'up'), RangeError);
});
