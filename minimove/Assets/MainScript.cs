using UnityEngine;
using System.Collections;

using System.Collections.Generic;

public class MainScript : MonoBehaviour {
	GameFlow gameFlow;
	int frame = 0;

	void Start () {
		gameFlow = new GameFlow (gameObject);
	}

	void OnGUI() {
		int border = 10;
		GUI.Box (new Rect (border, border, Screen.width-2*border, Screen.height-2*border),
			     "Hello " + frame);
	}

	void Update () {
		//Debug.Log ("Update");

		gameFlow.Update ();

		frame++;
	}
}
