using UnityEngine;
using System.Collections.Generic;

public class GameFlow {
	List<MovePlayer> players = new List<MovePlayer>();
	MiniGame currentGame = null;
	MonoBehaviour behaviour = null;

	public GameFlow(GameObject gameObject, MonoBehaviour behaviour) {
		int count = UniMoveController.GetNumConnected ();
		Debug.Log ("Connected controllers: " + count);

		for (int i = 0; i < count; i++) {
			players.Add(new MovePlayer(gameObject, i));
		}

		currentGame = new MoveSays (this);
		this.behaviour = behaviour;
	}

	void UpdateControllers() {
		/*
		Color[] colors = { Color.cyan, Color.red, Color.blue, Color.green, Color.magenta };
*/
		foreach (var player in players) {
			// Geht L2, L1, R1, ... (alle PSMoveButton-Werte) durch
			foreach (PSMoveButton button in System.Enum.GetValues(typeof(PSMoveButton))) {
				if (player.move.GetButtonDown (button)) {
					if (currentGame != null) {
						currentGame.ButtonPressed (player, button);
					}
				}
			}

			/*player.LEDColor = colors [player.PlayerNumber % colors.Length];

			if (player.move.GetButtonDown (PSMoveButton.Cross)) {
				Debug.Log ("Button pressed");
				GameObject bling = GameObject.Find ("BlingSound");
				AudioSource blingas = bling.GetComponent<AudioSource> ();

				GameObject go = new GameObject ("HOHO");
				AudioSource src = go.AddComponent<AudioSource> ();
				src.volume = 0.5f;
				src.clip = blingas.clip;
				src.Play ();
			}*/

			player.Update ();
		}
	}

	public void Update () {
		UpdateControllers ();

		if (currentGame != null) {
			currentGame.Update ();
		}
	}

	public void startCurrentGame() {
		currentGame.StartGame ();
	}

	public void endCurrentGame(List<MovePlayer> winners) {
		Debug.Log ("Game ends, winner(s): " + winners);

		foreach (var player in players) {
			player.LEDColor = Color.black;
		}

		foreach (var winner in winners) {
			//winner.LEDColor = Color.white;
			behaviour.StartCoroutine(winner.WinAnimation(behaviour.GetComponent<TunableVariables>()));
			winner.Score++;
		}

		// TODO: Select a new game
		currentGame = null;
	}

	public List<MovePlayer> Players {
		get { return players; }
	}

	public string StatusMessage {
		get {
			string result = "";
			if (currentGame != null) {
				result += "current game: " + currentGame;
			} else {
				result += "no current game";
			}
			foreach (var player in players) {
				result += "\n";
				result += "Player " + (player.PlayerNumber + 1) + ": " + player.Score + " points";
			}
			return result;
		}
	}
}
