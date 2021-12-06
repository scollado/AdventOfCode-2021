from unittest import TestCase

from day02 import Day02, ElvishSubmarine, Command, AimingElvishSubmarine


class TestDay2(TestCase):
    MOVEMENT_AMOUNT = 5
    EXPECTED_RESULT_P1 = 150
    EXPECTED_RESULT_P2 = 900
    COMMANDS = [
        'forward 5',
        'down 5',
        'forward 8',
        'up 3',
        'down 8',
        'forward 2'
    ]

    def test_part_one(self):
        sut = Day02(TestDay2.COMMANDS)
        self.assertEqual(TestDay2.EXPECTED_RESULT_P1, sut.part_one())

    def test_part_two(self):
        sut = Day02(TestDay2.COMMANDS)
        self.assertEqual(TestDay2.EXPECTED_RESULT_P2, sut.part_two())

    def test_elvishsubmarine_should_increase_position_when_command_is_forward(self):
        # Given
        sut = ElvishSubmarine()
        command = Command('forward ' + str(TestDay2.MOVEMENT_AMOUNT))

        # When
        sut.run_command(command)

        # Then
        self.assertEqual(sut.position, TestDay2.MOVEMENT_AMOUNT)

    def test_elvishsubmarine_should_increase_depth_when_command_is_down(self):
        # Given
        sut = ElvishSubmarine()
        command = Command('down ' + str(TestDay2.MOVEMENT_AMOUNT))

        # When
        sut.run_command(command)

        # Then
        self.assertEqual(sut.depth, TestDay2.MOVEMENT_AMOUNT)

    def test_elvishsubmarine_should_decrease_depth_when_command_is_up(self):
        # Given
        sut = ElvishSubmarine()
        sut.depth = TestDay2.MOVEMENT_AMOUNT * 2
        command = Command('up ' + str(TestDay2.MOVEMENT_AMOUNT))

        # When
        sut.run_command(command)

        # Then
        self.assertEqual(sut.depth, TestDay2.MOVEMENT_AMOUNT)

    def test_aimingsubmarine_should_increase_aim_when_command_is_down(self):
        # Given
        sut = AimingElvishSubmarine()
        command = Command('down ' + str(TestDay2.MOVEMENT_AMOUNT))

        # When
        sut.run_command(command)

        # Then
        self.assertEqual(sut.aim, TestDay2.MOVEMENT_AMOUNT)

    def test_aimingsubmarine_should_decrease_aim_when_command_is_up(self):
        # Given
        sut = AimingElvishSubmarine()
        sut.aim = TestDay2.MOVEMENT_AMOUNT
        command = Command('up ' + str(TestDay2.MOVEMENT_AMOUNT))

        # When
        sut.run_command(command)

        # Then
        self.assertEqual(sut.aim, 0)

    def test_aimingsubmarine_should_increase_position_and_depth_when_command_is_forward(self):
        # Given
        starting_aim = 2
        sut = AimingElvishSubmarine()
        sut.aim = starting_aim
        command = Command('forward ' + str(TestDay2.MOVEMENT_AMOUNT))

        # When
        sut.run_command(command)

        # Then
        self.assertEqual(sut.position, TestDay2.MOVEMENT_AMOUNT)
        self.assertEqual(sut.depth, TestDay2.MOVEMENT_AMOUNT * starting_aim)
