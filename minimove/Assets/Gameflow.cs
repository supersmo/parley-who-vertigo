using UnityEngine;
using System.Collections.Generic;

public class GameFlow {
	private List<MovePlayer> players = new List<MovePlayer>();
	MiniGame currentGame = null;

	public GameFlow(GameObject gameObject) {
		int count = UniMoveController.GetNumConnected ();
		Debug.Log ("Connected controllers: " + count);

		for (int i = 0; i < count; i++) {
			players.Add(new MovePlayer(gameObject, i));
		}
	}

	void UpdateControllers() {
		Color[] colors = { Color.cyan, Color.red, Color.blue, Color.green, Color.magenta };

		foreach (var player in players) {
			player.LEDColor = colors [player.PlayerNumber % colors.Length];

			if (player.move.GetButtonDown (PSMoveButton.Cross)) {
				Debug.Log ("Button pressed");
				GameObject bling = GameObject.Find ("BlingSound");
				AudioSource blingas = bling.GetComponent<AudioSource> ();

				GameObject go = new GameObject ("HOHO");
				AudioSource src = go.AddComponent<AudioSource> ();
				src.volume = 0.5f;
				src.clip = blingas.clip;
				src.Play ();
			}

			player.Update ();
		}
	}

	public void Update () {
		UpdateControllers ();

		if (currentGame != null) {
			currentGame.Update ();
		}
	}

	public void endCurrentGame(int [] winners) {
		// TODO
	}
}
