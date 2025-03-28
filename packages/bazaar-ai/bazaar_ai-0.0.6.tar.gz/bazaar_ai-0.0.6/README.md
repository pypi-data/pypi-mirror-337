# 🐪 Bazaar

**Bazaar** is a lightweight, extensible simulation of the *Jaipur* board game, specifically designed for training reinforcement learning (RL) agents. It replicates the core mechanics and strategic depth of the original *Jaipur* game while providing a clean and easy-to-use API for custom agents, facilitating the development of RL environments.

## 🎯 Purpose

The library provides a fully functional, object-oriented implementation of the *Jaipur* game loop with minimal dependencies. It focuses on key aspects of game modeling and reinforcement learning, including:

- **Modeling  Actions and Transitions**: Accurately simulating possible player actions and game state transitions.
- **Enforcing All Game Rules**: Ensures all gameplay mechanics are adhered to.
- **Custom Agent Integration**: Supports easy integration of custom RL agents, enabling researchers to experiment with different strategies and learning techniques.

By providing a well-structured environment, **Bazaar** offers the flexibility and extensibility necessary to build and train RL agents in a dynamic and competitive setting.

---

## 🧠 Why Jaipur?

*Jaipur* is an engaging two-player trading game that makes it an ideal environment for RL research. Here’s why it’s particularly suitable:

- **Small but Rich Action Space**: While the game has a relatively small number of possible actions, these actions lead to complex decision-making and strategic depth.
- **Partial Observability**: Players don’t have access to the full game state at all times, forcing them to make decisions based on incomplete information, simulating real-world uncertainty.
- **Long-term Planning**: Success depends not only on immediate gains but on long-term strategy, perfect for testing agents that need to plan ahead.
- **Fast Episode Turnaround**: The game’s relatively short length makes it ideal for training agents quickly, with fast iterations and short training cycles.

These characteristics make *Jaipur* an excellent environment for RL research.

---

## ⚙️ Features

- ✅ **Complete Implementation of Jaipur Rules**: All major rules of the *Jaipur* board game are faithfully replicated, ensuring accurate game play.
- ✅ **Game State Transition Simulation**: Accurately models state transitions resulting from player actions, maintaining an up-to-date view of the game state.
- ✅ **Easily Serializable State**: The game state can be serialized to facilitate observation modeling for RL agents.
- ✅ **No UI**: This library is designed for programmatic play without any user interface, allowing for faster, automated training and experimentation.

---

## 🚀 Quick Start

To get started with **Bazaar**, simply import the library, set up your traders (agents), and start a game. Here's a minimal example of how to run a basic game between two random traders:

```python
from bazaar_ai.bazaar import BasicBazaar, Trader

trader1 = Trader(seed = 0,
                 name = "Caveman")
trader2 = Trader(seed = 0, 
                 name = "Villager")

traders = {
    trader1.id: trader1,
    trader2.id: trader2
}

game = BasicBazaar(
    seed = 0,
    players = traders,
)

game.play()
```

To implement custom agents, the `Trader` class can be extended.

```python
from bazaar_ai.trader import Trader

class CustomTrader(Trader):
    def __init__(self, seed, name):
        super()__init__(seed, name)
        
        # add additional data
        pass 
            
        
    def select_action(self,
                  actions: list[TraderAction],
                  observation: MarketObservation):
        """
        Method for selecting an action based on the market observation.

        Args:
            actions (list[TraderAction]): The list of actions.
            market_observation (MarketObservation): The current state of the market.

        Returns:
            Action: The selected action.
        """
        
        # choose an action
        # based on the market observation
        
        pass
    
    
    def calculate_reward(self,
                         old_observation: MarketObservation,
                         new_observation: MarketObservation,
                         has_acted: bool,
                         environment_reward: Optional[float]):
        """
        Calculates the reward based on the change in market conditions, the action taken, and any external environment reward.

        Parameters:
        ----------
        old_observation : MarketObservation
            The previous state of the market before the action was taken.

        new_observation : MarketObservation
            The current state of the market after the action is taken.

        has_acted : bool
            A flag indicating whether an action was actually taken. This could influence the reward calculation, as no action may imply no reward.

        environment_reward : Optional[float]
            An optional reward value from the environment. This reward could come from an external system that influences the agent's reward function.

        Returns:
        -------
        float
            The calculated reward, which might take into account the market change, the action, and the environment's reward. 
            This value should be positive or negative based on the desirability of the new market state or the success of the action taken.
        """
        pass

```

