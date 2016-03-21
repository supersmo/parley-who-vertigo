using UnityEngine;
using System.Collections.Generic;

public class MoveSays : MiniGame {
    static Dictionary<PSMoveButton, Color> buttonToColor = new Dictionary<PSMoveButton, Color>() {
		{ PSMoveButton.Square, Color.magenta },
		{ PSMoveButton.Triangle, Color.green },
		{ PSMoveButton.Cross, Color.blue },
		{ PSMoveButton.Circle, Color.red },
	};

	public MoveSays(GameFlow gameFlow) : base(gameFlow) {
	}

	public override void StartGame() {
		System.Random rnd = new System.Random();

		List<Color> colors = new List<Color>();
		foreach (var color in buttonToColor.Values) {
			colors.Add(color);
		}

		foreach (var player in gameFlow.Players) {
			// player.setColorAnimation({Red, 200, Green, 200, ..., player.color})
			player.LEDColor = colors[rnd.Next(colors.Count)];
		}
	}

	public override void ButtonPressed(MovePlayer player, PSMoveButton button) {
		if (buttonToColor.ContainsKey (button)) {
			Color color = buttonToColor [button];
			Debug.Log ("Button Pressed on " + player.PlayerNumber + " : " + button + " -> color: " + color);
			if (color == player.LEDColor) {
				Debug.Log ("YAY!");
				gameFlow.endCurrentGame (new List<MovePlayer>() { player });
			} else {
				Debug.Log ("Nay :/");
			}
		} else {
			Debug.Log ("Ignoring button press: " + button);
		}
	}

	public override void Update() {
		
	}
}
