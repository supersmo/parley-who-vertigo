using UnityEngine;
using System.Collections.Generic;

public class GameFlow {
	private static readonly System.Random rnd = new System.Random();
	List<MovePlayer> players = new List<MovePlayer>();
	MiniGame currentGame = null;
	MonoBehaviour behaviour = null;
	int remainingGames = 0;

	public GameFlow(GameObject gameObject, MonoBehaviour behaviour) {
		int count = UniMoveController.GetNumConnected ();
		Debug.Log ("Connected controllers: " + count);

		for (int i = 0; i < count; i++) {
			players.Add(new MovePlayer(this, gameObject, i));
		}

		this.behaviour = behaviour;
		this.remainingGames = GetTunables ().DefaultNumberOfGames;

		SelectNewGame ();
	}

	public void SelectNewGame() {
		Debug.Log("Selecting new game");
		if (remainingGames == 0) {
			Debug.Log ("Session ends");
		} else {
			List<MiniGame> games = new List<MiniGame> ();
			games.Add (new MoveSays (this));
			games.Add (new ShakeIt (this));

			MiniGame candidate = null;
			do {
				candidate = games [rnd.Next (games.Count)];
			} while (!candidate.CanSupportPlayers(players.Count));

			currentGame = candidate;
				
			currentGame.StartGame ();
			remainingGames--;
		}
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

	public TunableVariables GetTunables() {
		return behaviour.GetComponent<TunableVariables> ();
	}

	public void endCurrentGame(MovePlayer winner) {
		endCurrentGame (new List<MovePlayer>() { winner });
	}

	public void endCurrentGame(List<MovePlayer> winners) {
		Debug.Log ("Game ends, winner(s): " + winners);

		foreach (var player in players) {
			player.LEDColor = Color.black;
		}
			
		// Disable access to "old" current game; new current game
		// will be set by the winner player 
		currentGame = null;

		if (winners.Count == 0) {
			SelectNewGame ();
			// TODO: Play "nobody wins" sound
		} else {
			bool first = true;
			foreach (var winner in winners) {
				//winner.LEDColor = Color.white;
				behaviour.StartCoroutine (winner.WinAnimation (GetTunables (), first));
				winner.Score++;
				first = false;
			}
		}
	}

	public List<MovePlayer> Players {
		get { return players; }
	}

	public string StatusMessage {
		get {
			string result = "";
			if (currentGame != null) {
				result += "current game: " + currentGame;
				result += "\n" + currentGame.StatusMessage ();
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
