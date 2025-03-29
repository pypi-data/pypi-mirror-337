""":mod:`pokerkit.tests.test_analysis` implements unit tests for
analysis related tools on PokerKit.
"""

from concurrent.futures import ProcessPoolExecutor
from unittest import TestCase, main

from pokerkit.analysis import calculate_equities, parse_range
from pokerkit.hands import StandardHighHand
from pokerkit.utilities import Card, Deck


class HandHistoryTestCase(TestCase):
    def test_parse_range(self) -> None:
        self.assertSetEqual(
            parse_range('JJ'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('JcJd'),
                        Card.parse('JcJh'),
                        Card.parse('JcJs'),
                        Card.parse('JdJh'),
                        Card.parse('JdJs'),
                        Card.parse('JhJs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('AK'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('AcKd'),
                        Card.parse('AcKh'),
                        Card.parse('AcKs'),
                        Card.parse('AdKc'),
                        Card.parse('AdKh'),
                        Card.parse('AdKs'),
                        Card.parse('AhKc'),
                        Card.parse('AhKd'),
                        Card.parse('AhKs'),
                        Card.parse('AsKc'),
                        Card.parse('AsKd'),
                        Card.parse('AsKh'),
                        Card.parse('AcKc'),
                        Card.parse('AdKd'),
                        Card.parse('AhKh'),
                        Card.parse('AsKs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('QJs'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('QcJc'),
                        Card.parse('QdJd'),
                        Card.parse('QhJh'),
                        Card.parse('QsJs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('QTs'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('QcTc'),
                        Card.parse('QdTd'),
                        Card.parse('QhTh'),
                        Card.parse('QsTs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('AKo'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('AcKd'),
                        Card.parse('AcKh'),
                        Card.parse('AcKs'),
                        Card.parse('AdKc'),
                        Card.parse('AdKh'),
                        Card.parse('AdKs'),
                        Card.parse('AhKc'),
                        Card.parse('AhKd'),
                        Card.parse('AhKs'),
                        Card.parse('AsKc'),
                        Card.parse('AsKd'),
                        Card.parse('AsKh'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('JJ+'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('JcJd'),
                        Card.parse('JcJh'),
                        Card.parse('JcJs'),
                        Card.parse('JdJh'),
                        Card.parse('JdJs'),
                        Card.parse('JhJs'),
                        Card.parse('QcQd'),
                        Card.parse('QcQh'),
                        Card.parse('QcQs'),
                        Card.parse('QdQh'),
                        Card.parse('QdQs'),
                        Card.parse('QhQs'),
                        Card.parse('KcKd'),
                        Card.parse('KcKh'),
                        Card.parse('KcKs'),
                        Card.parse('KdKh'),
                        Card.parse('KdKs'),
                        Card.parse('KhKs'),
                        Card.parse('AcAd'),
                        Card.parse('AcAh'),
                        Card.parse('AcAs'),
                        Card.parse('AdAh'),
                        Card.parse('AdAs'),
                        Card.parse('AhAs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('QT+'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('QcTd'),
                        Card.parse('QcTh'),
                        Card.parse('QcTs'),
                        Card.parse('QdTc'),
                        Card.parse('QdTh'),
                        Card.parse('QdTs'),
                        Card.parse('QhTc'),
                        Card.parse('QhTd'),
                        Card.parse('QhTs'),
                        Card.parse('QsTc'),
                        Card.parse('QsTd'),
                        Card.parse('QsTh'),
                        Card.parse('QcTc'),
                        Card.parse('QdTd'),
                        Card.parse('QhTh'),
                        Card.parse('QsTs'),
                        Card.parse('QcJd'),
                        Card.parse('QcJh'),
                        Card.parse('QcJs'),
                        Card.parse('QdJc'),
                        Card.parse('QdJh'),
                        Card.parse('QdJs'),
                        Card.parse('QhJc'),
                        Card.parse('QhJd'),
                        Card.parse('QhJs'),
                        Card.parse('QsJc'),
                        Card.parse('QsJd'),
                        Card.parse('QsJh'),
                        Card.parse('QcJc'),
                        Card.parse('QdJd'),
                        Card.parse('QhJh'),
                        Card.parse('QsJs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('JTs+'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('JcTc'),
                        Card.parse('JdTd'),
                        Card.parse('JhTh'),
                        Card.parse('JsTs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('JTo+'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('JcTd'),
                        Card.parse('JcTh'),
                        Card.parse('JcTs'),
                        Card.parse('JdTc'),
                        Card.parse('JdTh'),
                        Card.parse('JdTs'),
                        Card.parse('JhTc'),
                        Card.parse('JhTd'),
                        Card.parse('JhTs'),
                        Card.parse('JsTc'),
                        Card.parse('JsTd'),
                        Card.parse('JsTh'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('JJ-TT'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('JcJd'),
                        Card.parse('JcJh'),
                        Card.parse('JcJs'),
                        Card.parse('JdJh'),
                        Card.parse('JdJs'),
                        Card.parse('JhJs'),
                        Card.parse('TcTd'),
                        Card.parse('TcTh'),
                        Card.parse('TcTs'),
                        Card.parse('TdTh'),
                        Card.parse('TdTs'),
                        Card.parse('ThTs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('JTs-KQs'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('JcTc'),
                        Card.parse('JdTd'),
                        Card.parse('JhTh'),
                        Card.parse('JsTs'),
                        Card.parse('QcJc'),
                        Card.parse('QdJd'),
                        Card.parse('QhJh'),
                        Card.parse('QsJs'),
                        Card.parse('KcQc'),
                        Card.parse('KdQd'),
                        Card.parse('KhQh'),
                        Card.parse('KsQs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('AsKh'),
            {frozenset(Card.parse('AsKh'))},
        )
        self.assertSetEqual(
            parse_range('2s3s'),
            set(map(frozenset, (Card.parse('2s3s'),))),
        )
        self.assertSetEqual(
            parse_range('4s5h;2s3s'),
            set(map(frozenset, (Card.parse('4s5h'), Card.parse('2s3s')))),
        )
        self.assertSetEqual(
            parse_range('7s8s 27         AK', 'ATs+'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('7s8s'),
                        Card.parse('2c7d'),
                        Card.parse('2c7h'),
                        Card.parse('2c7s'),
                        Card.parse('2d7c'),
                        Card.parse('2d7h'),
                        Card.parse('2d7s'),
                        Card.parse('2h7c'),
                        Card.parse('2h7d'),
                        Card.parse('2h7s'),
                        Card.parse('2s7c'),
                        Card.parse('2s7d'),
                        Card.parse('2s7h'),
                        Card.parse('2c7c'),
                        Card.parse('2d7d'),
                        Card.parse('2h7h'),
                        Card.parse('2s7s'),
                        Card.parse('AcKd'),
                        Card.parse('AcKh'),
                        Card.parse('AcKs'),
                        Card.parse('AdKc'),
                        Card.parse('AdKh'),
                        Card.parse('AdKs'),
                        Card.parse('AhKc'),
                        Card.parse('AhKd'),
                        Card.parse('AhKs'),
                        Card.parse('AsKc'),
                        Card.parse('AsKd'),
                        Card.parse('AsKh'),
                        Card.parse('AcKc'),
                        Card.parse('AdKd'),
                        Card.parse('AhKh'),
                        Card.parse('AsKs'),
                        Card.parse('AcQc'),
                        Card.parse('AdQd'),
                        Card.parse('AhQh'),
                        Card.parse('AsQs'),
                        Card.parse('AcJc'),
                        Card.parse('AdJd'),
                        Card.parse('AhJh'),
                        Card.parse('AsJs'),
                        Card.parse('AcTc'),
                        Card.parse('AdTd'),
                        Card.parse('AhTh'),
                        Card.parse('AsTs'),
                    ),
                ),
            ),
        )
        self.assertSetEqual(
            parse_range('99+', '2h7s'),
            set(
                map(
                    frozenset,
                    (
                        Card.parse('9c9d'),
                        Card.parse('9c9h'),
                        Card.parse('9c9s'),
                        Card.parse('9d9h'),
                        Card.parse('9d9s'),
                        Card.parse('9h9s'),
                        Card.parse('TcTd'),
                        Card.parse('TcTh'),
                        Card.parse('TcTs'),
                        Card.parse('TdTh'),
                        Card.parse('TdTs'),
                        Card.parse('ThTs'),
                        Card.parse('JcJd'),
                        Card.parse('JcJh'),
                        Card.parse('JcJs'),
                        Card.parse('JdJh'),
                        Card.parse('JdJs'),
                        Card.parse('JhJs'),
                        Card.parse('QcQd'),
                        Card.parse('QcQh'),
                        Card.parse('QcQs'),
                        Card.parse('QdQh'),
                        Card.parse('QdQs'),
                        Card.parse('QhQs'),
                        Card.parse('KcKd'),
                        Card.parse('KcKh'),
                        Card.parse('KcKs'),
                        Card.parse('KdKh'),
                        Card.parse('KdKs'),
                        Card.parse('KhKs'),
                        Card.parse('AcAd'),
                        Card.parse('AcAh'),
                        Card.parse('AcAs'),
                        Card.parse('AdAh'),
                        Card.parse('AdAs'),
                        Card.parse('AhAs'),
                        Card.parse('2h7s'),
                    ),
                ),
            ),
        )

    def test_calculate_equities(self) -> None:
        with ProcessPoolExecutor() as executor:
            equities = calculate_equities(
                (parse_range('AsKs'), parse_range('2h2c')),
                (),
                2,
                5,
                Deck.STANDARD,
                (StandardHighHand,),
                sample_count=10000,
                executor=executor,
            )

            self.assertEqual(len(equities), 2)
            self.assertAlmostEqual(sum(equities), 1)

            equities = calculate_equities(
                (parse_range('JsTs'), parse_range('AhAd')),
                Card.parse('9s8s2c'),
                2,
                5,
                Deck.STANDARD,
                (StandardHighHand,),
                sample_count=10000,
                executor=executor,
            )

            self.assertEqual(len(equities), 2)
            self.assertAlmostEqual(sum(equities), 1)

            equities = calculate_equities(
                (parse_range('AKs'), parse_range('22')),
                (),
                2,
                5,
                Deck.STANDARD,
                (StandardHighHand,),
                sample_count=10000,
                executor=executor,
            )

            self.assertEqual(len(equities), 2)
            self.assertAlmostEqual(sum(equities), 1)

            equities = calculate_equities(
                (parse_range('AA'), parse_range('22')),
                (),
                2,
                5,
                Deck.STANDARD,
                (StandardHighHand,),
                sample_count=10000,
                executor=executor,
            )

            self.assertEqual(len(equities), 2)
            self.assertAlmostEqual(sum(equities), 1)

            equities = calculate_equities(
                (
                    parse_range('2h2c'),
                    parse_range('3h3c'),
                    parse_range('AsKs'),
                ),
                Card.parse('QsJsTs'),
                2,
                5,
                Deck.STANDARD,
                (StandardHighHand,),
                sample_count=10000,
                executor=executor,
            )

            self.assertEqual(len(equities), 3)
            self.assertAlmostEqual(sum(equities), 1)
            self.assertAlmostEqual(equities[0], 0)
            self.assertAlmostEqual(equities[1], 0)
            self.assertAlmostEqual(equities[2], 1)

            equities = calculate_equities(
                (
                    parse_range('2h2c'),
                    parse_range('3h3c'),
                    parse_range('AhKh'),
                ),
                Card.parse('3s3d4c'),
                2,
                5,
                Deck.STANDARD,
                (StandardHighHand,),
                sample_count=10000,
                executor=executor,
            )

            self.assertEqual(len(equities), 3)
            self.assertAlmostEqual(sum(equities), 1)
            self.assertAlmostEqual(equities[0], 0)
            self.assertAlmostEqual(equities[1], 1)
            self.assertAlmostEqual(equities[2], 0)

            equities = calculate_equities(
                (parse_range('3d3h'), parse_range('3c3s')),
                Card.parse('Tc8d6h4s'),
                2,
                5,
                Deck.STANDARD,
                (StandardHighHand,),
                sample_count=10000,
                executor=executor,
            )

            self.assertEqual(len(equities), 2)
            self.assertAlmostEqual(sum(equities), 1)
            self.assertAlmostEqual(equities[0], 0.5)
            self.assertAlmostEqual(equities[1], 0.5)


if __name__ == '__main__':
    main()  # pragma: no cover
