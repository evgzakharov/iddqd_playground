from statemachine import StateMachine, State


class CarStateDelegate:
    def on_exit_state(self, state):
        print(f"exit {state}")

    def on_enter_state(self, state):
        print(f"enter {state}")


class CarState(StateMachine):
    delegate: CarStateDelegate

    discover = State("Discover", initial=True)
    parking = State("Parking")
    hunting = State("Hunting")

    goHunting = hunting.from_(discover, parking)
    stopMachine = parking.from_(discover, hunting)
    discoverArea = discover.from_(hunting, parking)

    prev_state: State

    def on_exit_state(self, state):
        if self.delegate is not None:
            self.delegate.on_exit_state(state)

    def on_enter_state(self, state):
        if self.delegate is not None:
            self.delegate.on_enter_state(state)
