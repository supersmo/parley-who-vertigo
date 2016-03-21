using UnityEngine;
using System.Collections;

using System.Collections.Generic;

public class MainScript : MonoBehaviour {
	GameFlow gameFlow;

	void Start () {
		gameFlow = new GameFlow (gameObject, this);
		gameFlow.startCurrentGame ();
	}

	void OnGUI() {
		int border = 10;
		GUI.Box (new Rect (border, border, Screen.width - 2 * border, Screen.height - 2 * border),
			gameFlow.StatusMessage);
	}

	void Update () {
		gameFlow.Update ();
	}
}
