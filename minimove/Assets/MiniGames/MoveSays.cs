using UnityEngine;
using System.Collections.Generic;

public class MoveSays : MiniGame {
	public MoveSays(GameFlow gameFlow) : base(gameFlow) {
	}

	public override void StartGame() {
		foreach (var player in gameFlow.Players) {
			player.LEDColor = PSMoveColor.getRandomColor();
		}
	}

	public override void ButtonPressed(MovePlayer player, PSMoveButton button) {
		if (PSMoveColor.isColorButton (button)) {
			Color color = PSMoveColor.colorForButton (button);

			if (color == player.LEDColor) {
				gameFlow.endCurrentGame (player);
			} else {
				// TODO: Play "dead" animation
				player.LEDColor = Color.black;
			}
		}
	}

	public override void Update() {
	}
}
