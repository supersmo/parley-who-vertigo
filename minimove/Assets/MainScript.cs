using UnityEngine;
using System.Collections;

using System.Collections.Generic;

public class MainScript : MonoBehaviour {
	private List<UniMoveController> moves = new List<UniMoveController>();

	void Start () {
		int count = UniMoveController.GetNumConnected ();
		Debug.Log ("Connected controllers: " + count);

		for (int i = 0; i < count; i++) {
			UniMoveController move = gameObject.AddComponent<UniMoveController> ();


			if (!move.Init (i)) {
				Debug.Log ("Failed to init controller#" + i);
			}

			moves.Add (move);
		}
	}

	void Update () {
		//Debug.Log ("Update");

		Color[] colors = { Color.cyan, Color.red, Color.blue, Color.green, Color.magenta };

		for (int i=0; i<moves.Count; i++) {
			var move = moves [i];
			move.SetLED (colors [i % colors.Length]);
		}
	}
}
