using UnityEngine;
using System.Collections.Generic;

public class PSMoveColor {
	private static readonly System.Random rnd = new System.Random();
	private static Dictionary<PSMoveButton, Color> buttonToColor = new Dictionary<PSMoveButton, Color>() {
		{ PSMoveButton.Square, Color.magenta },
		{ PSMoveButton.Triangle, Color.green },
		{ PSMoveButton.Cross, Color.blue },
		{ PSMoveButton.Circle, Color.red },
	};
	private static List<Color> colors;

	static PSMoveColor() {
		colors = new List<Color>();
		foreach (var color in buttonToColor.Values) {
			colors.Add(color);
		}
	}

	public static Color getRandomColor() {
		return colors[rnd.Next(colors.Count)];
	}

	public static bool isColorButton(PSMoveButton button) {
		return buttonToColor.ContainsKey (button);
	}

	public static Color colorForButton(PSMoveButton button) {
		return buttonToColor [button];
	}
}
