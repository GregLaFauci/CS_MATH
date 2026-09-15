import { bits, shift } from './math.mjs';

const $ = id => document.getElementById(id);
let start = 45, current = 45, completed = 0, busy = false, generation = 0;
let animations = [];
const direction = () => $('direction').value;
const places = () => Number($('places').value);
const controls = [...document.querySelectorAll('.controls input, .controls select, .controls button, .presets button'), $('step')];

function lock(value) {
  busy = value;
  controls.forEach(control => { control.disabled = value; });
  document.querySelectorAll('.bit').forEach(button => { button.disabled = value; });
}

function render() {
  const focused = document.activeElement?.dataset.index;
  $('register').replaceChildren(...bits(current).map((bit, index) => {
    const slot = document.createElement('div'); slot.className = 'bit-slot';
    const weight = 2 ** (7 - index);
    const label = document.createElement('span'); label.className = 'weight'; label.textContent = weight;
    const button = document.createElement('button'); button.className = `bit ${bit ? 'on' : ''}`;
    button.dataset.index = index;
    button.setAttribute('aria-label', `Bit ${7 - index}, place value ${weight}`);
    button.setAttribute('aria-pressed', String(Boolean(bit))); button.disabled = busy;
    const glyph = document.createElement('span'); glyph.className = 'glyph'; glyph.textContent = bit;
    button.append(glyph);
    button.addEventListener('click', () => { start = current ^ weight; $('number').value = start; reset(); });
    slot.append(label, button); return slot;
  }));
  if (focused !== undefined) document.querySelector(`[data-index="${focused}"]`)?.focus();
  const terms = bits(current).flatMap((bit, i) => bit ? [2 ** (7 - i)] : []);
  $('sum').textContent = `${terms.join(' + ') || '0'} = ${current}`;
  $('decimal').textContent = current;
  $('stage-label').textContent = completed ? 'SHIFTED REGISTER' : 'STARTING REGISTER';
  $('step-label').textContent = busy ? 'Watch the positions' : 'Click any bit to flip it';
  $('progress').textContent = completed ? `Step ${completed} of ${places()}` : 'Ready to explore';
  $('step').disabled = busy || completed >= places();
  const result = document.querySelector('.result'); result.classList.remove('overflow');
  if (!completed) {
    $('result-title').textContent = 'Every position has a value.';
    $('result-text').textContent = 'Add the highlighted place values to turn binary into decimal. A left shift moves each bit to a position worth twice as much.';
    $('formula').textContent = `${start} = ${bits(start).join('')}₂`;
    return;
  }
  const outcome = shift(start, direction(), completed);
  const operation = `${start} ${direction() === 'left' ? '<<' : '>>'} ${completed} = ${current}`;
  if (outcome.overflow) {
    result.classList.add('overflow');
    $('result-title').textContent = 'A bit fell off the edge.';
    $('result-text').textContent = `The full product is ${outcome.full}, but eight bits only hold 0–255. The high bits are discarded and the value wraps around.`;
    $('formula').textContent = `${operation} · ${outcome.full} mod 256 = ${current}`;
  } else if (direction() === 'right') {
    $('result-title').textContent = 'Each place is worth half as much.';
    $('result-text').textContent = `Divide ${start} by ${2 ** completed} and round down. Bits leaving the right edge are discarded; zeros enter from the left.`;
    $('formula').textContent = operation;
  } else {
    $('result-title').textContent = 'Same bits. Bigger place values.';
    $('result-text').textContent = `Shifting left ${completed} ${completed === 1 ? 'place doubles' : 'places multiplies'} the starting value${completed === 1 ? '' : ` by ${2 ** completed}`}. Zeros fill the positions on the right.`;
    $('formula').textContent = `${operation} · ${start} × ${2 ** completed} = ${current}`;
  }
}

function reset() {
  generation++;
  animations.forEach(animation => animation.cancel()); animations = [];
  current = start; completed = 0; lock(false); render();
}

function readInput() {
  const valid = $('number').value.trim() !== '' && $('number').checkValidity();
  $('input-error').textContent = valid ? '' : 'Enter a whole number from 0 to 255.';
  $('number').setAttribute('aria-invalid', String(!valid));
  if (valid) { start = Number($('number').value); reset(); }
  return valid;
}

async function advance(token) {
  const glyphs = [...document.querySelectorAll('.glyph')];
  const buttons = [...document.querySelectorAll('.bit')];
  const delta = buttons[1].getBoundingClientRect().left - buttons[0].getBoundingClientRect().left;
  const left = direction() === 'left';
  const duration = matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 800;
  animations = glyphs.map((glyph, index) => glyph.animate([
    { transform: 'translateX(0)', opacity: 1 },
    { transform: `translateX(${left ? -delta : delta}px)`, opacity: index === (left ? 0 : 7) ? 0 : 1 }
  ], { duration, easing: 'ease-in-out', fill: 'forwards' }));
  const incoming = document.createElement('span'); incoming.className = 'incoming-zero'; incoming.textContent = '0';
  buttons[left ? 7 : 0].append(incoming);
  animations.push(incoming.animate([
    { transform: `translateX(${left ? delta : -delta}px)`, opacity: 0 },
    { transform: 'translateX(0)', opacity: 1 }
  ], { duration, easing: 'ease-in-out', fill: 'forwards' }));
  await Promise.all(animations.map(animation => animation.finished.catch(() => {})));
  if (token !== generation) return;
  current = shift(current, direction()).value; completed++;
  animations.forEach(animation => animation.cancel()); animations = [];
  render();
}

async function run(all) {
  if (busy) return;
  // Validate without restarting a partially stepped register.
  if (!$('number').checkValidity() || !$('number').value.trim()) { readInput(); return; }
  if (completed >= places()) reset();
  const token = generation;
  lock(true);
  try {
    do { await advance(token); } while (all && completed < places() && token === generation);
  } finally {
    if (token === generation) { lock(false); render(); }
  }
}

$('number').addEventListener('input', readInput);
['direction', 'places'].forEach(id => $(id).addEventListener('change', reset));
document.querySelectorAll('[data-value]').forEach(button => button.addEventListener('click', () => {
  $('number').value = button.dataset.value; $('direction').value = 'left'; $('places').value = '1'; readInput();
}));
$('play').addEventListener('click', () => run(true));
$('step').addEventListener('click', () => run(false));
$('reset').addEventListener('click', () => { $('number').value = start; $('input-error').textContent = ''; $('number').setAttribute('aria-invalid', 'false'); reset(); });
$('quiz').addEventListener('submit', event => {
  event.preventDefault();
  $('feedback').textContent = Number($('answer').value) === 144
    ? 'Exactly! 200 × 2 = 400, then 400 mod 256 = 144. The leading 1 falls off.'
    : 'Try again: 200 × 2 = 400. Subtract 256 to keep only the lowest eight bits.';
});
render();
