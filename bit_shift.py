from manim import *


# ============================================================
# VISUAL CS — BIT SHIFT V1.3
#
# Fast preview:
#   manim -pql bit_shift.py BitShiftV13
#
# High quality:
#   manim -pqh bit_shift.py BitShiftV13
#
# Lesson:
#   45 << 1  -> 90
#   Why left shift multiplies by two
#
# Then:
#   200 << 1 -> 144 in an unsigned 8-bit integer
#   because the high bit falls off.
# ============================================================


# ------------------------------------------------------------
# THEME
# ------------------------------------------------------------

ACTIVE = YELLOW
DANGER = RED
MUTED = GREY_B
DIM = GREY_D
GHOST = GREY_C

CELL_WIDTH = 0.82
CELL_HEIGHT = 0.82
CELL_GAP = 0.05

BIT_FONT_SIZE = 31
VALUE_FONT_SIZE = 20


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def code_text(
    text: str,
    font_size: int = 42,
):
    return Text(
        text,
        font="Menlo",
        font_size=font_size,
    )


# ------------------------------------------------------------
# REGISTER
# ------------------------------------------------------------

class BitRegister(VGroup):

    def __init__(
        self,
        value: int,
        bit_width: int = 8,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.integer_value = value
        self.bit_width = bit_width

        self.slots = VGroup()
        self.bits = VGroup()

        bit_values = self.to_bits(value)

        for bit in bit_values:

            slot = RoundedRectangle(
                width=CELL_WIDTH,
                height=CELL_HEIGHT,
                corner_radius=0.07,
                stroke_width=2,
                stroke_color=WHITE,
                fill_opacity=0,
            )

            glyph = Text(
                str(bit),
                font_size=BIT_FONT_SIZE,
                weight=BOLD,
            )

            self.slots.add(slot)
            self.bits.add(glyph)

        self.slots.arrange(
            RIGHT,
            buff=CELL_GAP,
        )

        for slot, glyph in zip(
            self.slots,
            self.bits,
        ):
            glyph.move_to(
                slot.get_center()
            )

        self.add(
            self.slots,
            self.bits,
        )

    def to_bits(
        self,
        value: int,
    ):
        return [
            (value >> position) & 1
            for position in reversed(
                range(self.bit_width)
            )
        ]

    def bit_values(self):
        return self.to_bits(
            self.integer_value
        )

    def active_indices(self):
        return [
            index
            for index, bit
            in enumerate(self.bit_values())
            if bit == 1
        ]

    def cell_step(self):
        return (
            CELL_WIDTH
            + CELL_GAP
        )


# ------------------------------------------------------------
# POSITION VALUES
# ------------------------------------------------------------

class PositionalValueRow(VGroup):

    def __init__(
        self,
        register: BitRegister,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.labels = VGroup()

        for index, slot in enumerate(
            register.slots
        ):

            position = (
                register.bit_width
                - 1
                - index
            )

            value = 2 ** position

            label = Text(
                str(value),
                font_size=VALUE_FONT_SIZE,
            )

            label.next_to(
                slot,
                UP,
                buff=0.27,
            )

            self.labels.add(label)

        self.add(
            self.labels
        )


# ------------------------------------------------------------
# SCENE
# ------------------------------------------------------------

class BitShiftV13(Scene):

    def construct(self):

        # ====================================================
        # PART ONE
        # WHAT DOES << DO?
        # ====================================================

        title = Text(
            "What does a bit shift actually do?",
            font_size=43,
            weight=BOLD,
        )

        subtitle = Text(
            "Watch the positions.",
            font_size=25,
            color=MUTED,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.3,
        )

        self.play(
            Write(title),
            FadeIn(
                subtitle,
                shift=UP * 0.12,
            ),
            run_time=1.1,
        )

        self.wait(0.5)

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            run_time=0.5,
        )

        # ----------------------------------------------------
        # DECIMAL 45
        # ----------------------------------------------------

        decimal_label = Text(
            "decimal",
            font_size=21,
            color=MUTED,
        )

        decimal = Integer(
            45,
            font_size=68,
        )

        decimal_group = VGroup(
            decimal_label,
            decimal,
        ).arrange(
            DOWN,
            buff=0.12,
        )

        self.play(
            FadeIn(decimal_label),
            GrowFromCenter(decimal),
            run_time=0.75,
        )

        self.wait(0.4)

        # ----------------------------------------------------
        # BINARY REGISTER
        # ----------------------------------------------------

        register = BitRegister(
            value=45,
            bit_width=8,
        )

        register.move_to(
            DOWN * 0.1
        )

        binary_label = Text(
            "binary",
            font_size=21,
            color=MUTED,
        )

        binary_label.next_to(
            register,
            UP,
            buff=0.45,
        )

        self.play(
            decimal_group.animate.to_edge(
                UP,
                buff=0.55,
            ),
            run_time=0.65,
        )

        self.play(
            FadeIn(binary_label),
            LaggedStart(
                *[
                    FadeIn(
                        slot,
                        shift=UP * 0.08,
                    )
                    for slot in register.slots
                ],
                lag_ratio=0.04,
            ),
            LaggedStart(
                *[
                    FadeIn(bit)
                    for bit in register.bits
                ],
                lag_ratio=0.04,
            ),
            run_time=1,
        )

        self.wait(0.3)

        # ----------------------------------------------------
        # POSITIONAL VALUES
        # ----------------------------------------------------

        values = PositionalValueRow(
            register
        )

        self.play(
            FadeOut(binary_label),
            LaggedStart(
                *[
                    FadeIn(
                        label,
                        shift=DOWN * 0.07,
                    )
                    for label in values.labels
                ],
                lag_ratio=0.04,
            ),
            run_time=0.8,
        )

        original_active = (
            register.active_indices()
        )

        self.play(
            *[
                register.bits[index]
                .animate
                .set_color(ACTIVE)
                .scale(1.08)
                for index in original_active
            ],
            *[
                values.labels[index]
                .animate
                .set_color(ACTIVE)
                .scale(1.08)
                for index in original_active
            ],
            run_time=0.65,
        )

        # ----------------------------------------------------
        # 32 + 8 + 4 + 1
        # ----------------------------------------------------

        equation_45 = MathTex(
            "32",
            "+",
            "8",
            "+",
            "4",
            "+",
            "1",
            "=",
            "45",
            font_size=42,
        )

        equation_45.next_to(
            register,
            DOWN,
            buff=0.62,
        )

        self.play(
            Write(equation_45),
            run_time=0.9,
        )

        self.wait(0.6)

        # ----------------------------------------------------
        # 45 << 1
        # ----------------------------------------------------

        shift_code = code_text(
            "45 << 1",
            font_size=44,
        )

        shift_code.to_edge(
            UP,
            buff=0.48,
        )

        self.play(
            ReplacementTransform(
                decimal_group,
                shift_code,
            ),
            FadeOut(equation_45),
            run_time=0.7,
        )

        # ----------------------------------------------------
        # GHOST STARTING ONES
        # ----------------------------------------------------

        ghost_ones = VGroup()

        for index in original_active:

            ghost = Text(
                "1",
                font_size=BIT_FONT_SIZE,
                weight=BOLD,
                color=GHOST,
            )

            ghost.move_to(
                register.slots[index]
                .get_center()
            )

            ghost.set_opacity(
                0.25
            )

            ghost_ones.add(
                ghost
            )

        self.add(
            ghost_ones
        )

        self.play(
            *[
                values.labels[index]
                .animate
                .set_color(WHITE)
                .scale(1 / 1.08)
                for index in original_active
            ],
            run_time=0.3,
        )

        # ----------------------------------------------------
        # HERO SHIFT
        # ----------------------------------------------------

        step = (
            register.cell_step()
        )

        original_bits = list(
            register.bits
        )

        leftmost_bit = (
            original_bits[0]
        )

        moving_bits = (
            original_bits[1:]
        )

        incoming_zero = Text(
            "0",
            font_size=BIT_FONT_SIZE,
            weight=BOLD,
        )

        incoming_zero.move_to(
            register.slots[-1]
            .get_center()
            + RIGHT * step
        )

        incoming_zero.set_opacity(
            0
        )

        self.add(
            incoming_zero
        )

        self.play(
            *[
                bit.animate.shift(
                    LEFT * step
                )
                for bit in moving_bits
            ],
            leftmost_bit.animate
            .shift(LEFT * step)
            .set_opacity(0),
            incoming_zero.animate
            .move_to(
                register.slots[-1]
                .get_center()
            )
            .set_opacity(1),
            run_time=1.8,
            rate_func=smooth,
        )

        self.play(
            FadeOut(ghost_ones),
            run_time=0.25,
        )

        shifted_active = [
            1,
            3,
            4,
            6,
        ]

        self.play(
            LaggedStart(
                *[
                    values.labels[index]
                    .animate
                    .set_color(ACTIVE)
                    .scale(1.08)
                    for index in shifted_active
                ],
                lag_ratio=0.12,
            ),
            run_time=0.75,
        )

        # ----------------------------------------------------
        # RESULT = 90
        # ----------------------------------------------------

        equation_90 = MathTex(
            "64",
            "+",
            "16",
            "+",
            "8",
            "+",
            "2",
            "=",
            "90",
            font_size=42,
        )

        equation_90.next_to(
            register,
            DOWN,
            buff=0.65,
        )

        self.play(
            Write(equation_90),
            run_time=0.9,
        )

        multiplication = MathTex(
            "45",
            r"\times",
            "2",
            "=",
            "90",
            font_size=46,
        )

        multiplication.next_to(
            equation_90,
            DOWN,
            buff=0.4,
        )

        self.play(
            FadeIn(
                multiplication,
                shift=UP * 0.1,
            ),
            run_time=0.6,
        )

        insight = Text(
            "Each 1 moved into a position worth twice as much.",
            font_size=24,
        )

        insight.next_to(
            multiplication,
            DOWN,
            buff=0.4,
        )

        self.play(
            FadeIn(insight),
            run_time=0.5,
        )

        self.wait(0.9)

        # ====================================================
        # PART TWO
        # FINISH THE CLIFFHANGER
        # ====================================================

        self.play(
            FadeOut(register),
            FadeOut(incoming_zero),
            FadeOut(values),
            FadeOut(equation_90),
            FadeOut(multiplication),
            FadeOut(insight),
            FadeOut(shift_code),
            run_time=0.65,
        )

        cliffhanger = Text(
            "But what if a 1 falls off the edge?",
            font_size=38,
            weight=BOLD,
        )

        self.play(
            FadeIn(
                cliffhanger,
                shift=UP * 0.1,
            ),
            run_time=0.7,
        )

        self.wait(0.8)

        self.play(
            FadeOut(cliffhanger),
            run_time=0.45,
        )

        # ----------------------------------------------------
        # INTRODUCE 200
        # ----------------------------------------------------

        overflow_code = code_text(
            "200 << 1",
            font_size=44,
        )

        overflow_code.to_edge(
            UP,
            buff=0.48,
        )

        overflow_register = BitRegister(
            value=200,
            bit_width=8,
        )

        overflow_register.move_to(
            DOWN * 0.05
        )

        overflow_values = PositionalValueRow(
            overflow_register
        )

        self.play(
            FadeIn(overflow_code),
            FadeIn(overflow_register),
            FadeIn(overflow_values),
            run_time=0.8,
        )

        # ----------------------------------------------------
        # SHOW 200
        # ----------------------------------------------------

        active_200 = (
            overflow_register
            .active_indices()
        )

        self.play(
            *[
                overflow_register.bits[index]
                .animate
                .set_color(ACTIVE)
                .scale(1.08)
                for index in active_200
            ],
            *[
                overflow_values.labels[index]
                .animate
                .set_color(ACTIVE)
                .scale(1.08)
                for index in active_200
            ],
            run_time=0.65,
        )

        equation_200 = MathTex(
            "128",
            "+",
            "64",
            "+",
            "8",
            "=",
            "200",
            font_size=42,
        )

        equation_200.next_to(
            overflow_register,
            DOWN,
            buff=0.65,
        )

        self.play(
            Write(equation_200),
            run_time=0.8,
        )

        self.wait(0.6)

        # ----------------------------------------------------
        # MARK THE DANGEROUS BIT
        # ----------------------------------------------------

        high_bit = (
            overflow_register.bits[0]
        )

        high_value = (
            overflow_values.labels[0]
        )

        self.play(
            high_bit.animate
            .set_color(DANGER)
            .scale(1.18),
            high_value.animate
            .set_color(DANGER)
            .scale(1.12),
            run_time=0.5,
        )

        edge_label = Text(
            "no position left of 128",
            font_size=21,
            color=DANGER,
        )

        edge_label.next_to(
            overflow_register.slots[0],
            LEFT,
            buff=0.5,
        )

        self.play(
            FadeIn(edge_label),
            run_time=0.4,
        )

        self.wait(0.5)

        self.play(
            FadeOut(equation_200),
            FadeOut(edge_label),
            run_time=0.35,
        )

        # ----------------------------------------------------
        # OVERFLOW SHIFT
        # ----------------------------------------------------

        overflow_step = (
            overflow_register
            .cell_step()
        )

        overflow_bits = list(
            overflow_register.bits
        )

        falling_one = (
            overflow_bits[0]
        )

        surviving_bits = (
            overflow_bits[1:]
        )

        overflow_zero = Text(
            "0",
            font_size=BIT_FONT_SIZE,
            weight=BOLD,
        )

        overflow_zero.move_to(
            overflow_register
            .slots[-1]
            .get_center()
            + RIGHT * overflow_step
        )

        overflow_zero.set_opacity(
            0
        )

        self.add(
            overflow_zero
        )

        # Arrow showing the bit leaving the register.
        overflow_arrow = Arrow(
            start=(
                overflow_register
                .slots[0]
                .get_center()
                + LEFT * 0.1
            ),
            end=(
                overflow_register
                .slots[0]
                .get_center()
                + LEFT * 1.35
            ),
            buff=0.05,
            stroke_width=3,
            color=DANGER,
        )

        overflow_text = Text(
            "overflow",
            font_size=20,
            color=DANGER,
        )

        overflow_text.next_to(
            overflow_arrow,
            UP,
            buff=0.12,
        )

        self.play(
            GrowArrow(
                overflow_arrow
            ),
            FadeIn(
                overflow_text
            ),
            run_time=0.45,
        )

        # THE FALL
        self.play(
            *[
                bit.animate.shift(
                    LEFT * overflow_step
                )
                for bit in surviving_bits
            ],
            falling_one.animate
            .shift(
                LEFT * overflow_step
            )
            .set_opacity(0),
            overflow_zero.animate
            .move_to(
                overflow_register
                .slots[-1]
                .get_center()
            )
            .set_opacity(1),
            run_time=1.8,
            rate_func=smooth,
        )

        self.wait(0.35)

        self.play(
            FadeOut(
                overflow_arrow
            ),
            FadeOut(
                overflow_text
            ),
            run_time=0.3,
        )

        # ----------------------------------------------------
        # NEW ACTIVE VALUES = 144
        # ----------------------------------------------------

        # 10010000
        #
        # 128 + 16 = 144

        for label in (
            overflow_values.labels
        ):
            label.set_color(
                WHITE
            )

        self.play(
            overflow_values.labels[0]
            .animate
            .set_color(ACTIVE),

            overflow_values.labels[3]
            .animate
            .set_color(ACTIVE),

            run_time=0.55,
        )

        result_144 = MathTex(
            "128",
            "+",
            "16",
            "=",
            "144",
            font_size=44,
        )

        result_144.next_to(
            overflow_register,
            DOWN,
            buff=0.65,
        )

        self.play(
            Write(result_144),
            run_time=0.8,
        )

        self.wait(0.7)

        # ----------------------------------------------------
        # WAIT... SHOULDN'T IT BE 400?
        # ----------------------------------------------------

        expected = MathTex(
            "200",
            r"\times",
            "2",
            "=",
            "400",
            font_size=44,
        )

        expected.next_to(
            result_144,
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(expected),
            run_time=0.7,
        )

        question = Text(
            "So why did we get 144?",
            font_size=25,
        )

        question.next_to(
            expected,
            DOWN,
            buff=0.38,
        )

        self.play(
            FadeIn(question),
            run_time=0.4,
        )

        self.wait(0.8)

        # ====================================================
        # 8-BIT LIMIT
        # ====================================================

        self.play(
            FadeOut(
                overflow_register
            ),
            FadeOut(
                overflow_zero
            ),
            FadeOut(
                overflow_values
            ),
            FadeOut(
                result_144
            ),
            FadeOut(
                expected
            ),
            FadeOut(
                question
            ),
            FadeOut(
                overflow_code
            ),
            run_time=0.6,
        )

        limit_title = Text(
            "An unsigned 8-bit integer has a limit.",
            font_size=34,
            weight=BOLD,
        )

        range_math = MathTex(
            "0",
            r"\rightarrow",
            "255",
            font_size=58,
        )

        range_group = VGroup(
            limit_title,
            range_math,
        ).arrange(
            DOWN,
            buff=0.4,
        )

        range_group.move_to(
            UP * 0.6
        )

        self.play(
            FadeIn(limit_title),
            Write(range_math),
            run_time=0.8,
        )

        self.wait(0.6)

        eight_bits = code_text(
            "11111111 = 255",
            font_size=36,
        )

        eight_bits.next_to(
            range_math,
            DOWN,
            buff=0.55,
        )

        self.play(
            FadeIn(eight_bits),
            run_time=0.5,
        )

        self.wait(0.7)

        # ----------------------------------------------------
        # MODULO EXPLANATION
        # ----------------------------------------------------

        self.play(
            FadeOut(
                range_group
            ),
            FadeOut(
                eight_bits
            ),
            run_time=0.5,
        )

        overflow_math = MathTex(
            "400",
            r"\bmod",
            "256",
            "=",
            "144",
            font_size=58,
        )

        overflow_math.move_to(
            ORIGIN
        )

        self.play(
            Write(
                overflow_math
            ),
            run_time=0.9,
        )

        wrap_text = Text(
            "The value wraps around.",
            font_size=27,
            color=MUTED,
        )

        wrap_text.next_to(
            overflow_math,
            DOWN,
            buff=0.45,
        )

        self.play(
            FadeIn(
                wrap_text
            ),
            run_time=0.45,
        )

        self.wait(1)

        # ====================================================
        # FINAL TAKEAWAY
        # ====================================================

        self.play(
            FadeOut(
                overflow_math
            ),
            FadeOut(
                wrap_text
            ),
            run_time=0.5,
        )

        final_heading = Text(
            "Left shift",
            font_size=29,
            color=MUTED,
        )

        final_code = code_text(
            "x << n",
            font_size=52,
        )

        normal_rule = MathTex(
            r"\approx",
            "x",
            r"\times",
            "2^n",
            font_size=50,
        )

        final_group = VGroup(
            final_heading,
            final_code,
            normal_rule,
        ).arrange(
            DOWN,
            buff=0.32,
        )

        final_group.move_to(
            UP * 0.45
        )

        self.play(
            FadeIn(
                final_heading
            ),
            FadeIn(
                final_code
            ),
            Write(
                normal_rule
            ),
            run_time=0.8,
        )

        final_note = Text(
            "until the integer runs out of bits",
            font_size=25,
        )

        final_note.next_to(
            final_group,
            DOWN,
            buff=0.55,
        )

        self.play(
            FadeIn(
                final_note
            ),
            run_time=0.5,
        )

        self.wait(0.8)

        final_overflow = Text(
            "Then: overflow.",
            font_size=32,
            weight=BOLD,
            color=DANGER,
        )

        final_overflow.next_to(
            final_note,
            DOWN,
            buff=0.45,
        )

        self.play(
            FadeIn(
                final_overflow,
                shift=UP * 0.08,
            ),
            run_time=0.5,
        )

        self.wait(1.5)