using UnityEngine;
using System.Collections;

using System.Collections.Generic;

public class MainScript : MonoBehaviour {
	GameFlow gameFlow;

	void Start () {
		gameFlow = new GameFlow (gameObject, this);
	}

	void OnGUI() {
		int border = 10;
		GUIStyle style = new GUIStyle (GUIStyle.none);
		style.fontSize = 50;
		style.normal.textColor = Color.white;
		style.alignment = TextAnchor.MiddleCenter;
		GUI.Box (new Rect (border, border, Screen.width - 2 * border, Screen.height - 2 * border),
			gameFlow.StatusMessage, style);
	}

	void Update () {
		gameFlow.Update ();
	}
}
