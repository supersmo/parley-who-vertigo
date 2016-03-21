using UnityEngine;
using System.Collections;

public class MainScript : MonoBehaviour {
	private GameObject moveObject = null;
	private UniMoveController move = null;
	private UniMoveController move2 = null;

	// Use this for initialization
	void Start () {
		moveObject = GameObject.Find ("MoveObject");
		move = moveObject.AddComponent<UniMoveController> ();
		move2 = moveObject.AddComponent<UniMoveController> ();

		Debug.Log ("Hello start");
		int count = UniMoveController.GetNumConnected ();
		Debug.Log ("Controllers Connected: " + count);
		if (move.Init (0) && move2.Init(1)) {
			Debug.Log("Initialized successfully");
		} else {
			Debug.Log("Failed to initialize");
		}			
	}
	
	// Update is called once per frame
	void Update () {
		//Debug.Log ("Update");
		move.SetLED(Color.cyan);
		move2.SetLED (Color.red);
	}
}
