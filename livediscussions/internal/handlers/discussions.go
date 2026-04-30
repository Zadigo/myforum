package handlers

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/Zadigo/livediscussions/internal/backend"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

func authenticationHandler(client backend.WebsocketClientInterface, message backend.WebsocketMessage, serverRegistry backend.ServerRegistryInterface) {
	switch message.Action {
	case "identify":
		username := message.Username
		if username == "" {
			ErrorMessage(client, "Username cannot be empty")
			return
		}

		registeredClient, err := serverRegistry.GetClient(client)
		if err != nil {
			ErrorMessage(client, err.Error())
			return
		}

		registeredClient.User.Username = username
		log.Printf("✅ Client %s identified as %s\n", registeredClient.ID, username)

		registeredClient.SendJsonMessage(backend.WebsocketMessage{
			Action:  "identified",
			Message: fmt.Sprintf("Identification successful as %s", username),
		})

	default:
		// Do something
	}
}

func discussionHandler(client backend.WebsocketClientInterface, message backend.WebsocketMessage, serverRegistry backend.ServerRegistryInterface) {
	switch message.Action {
	case "get_discussions":
		// Do something

	case "send_message":
		// Broadcast message to all clients in the discussion
		discussion, err := serverRegistry.GetDiscussion(message.DiscussionId)
		if err != nil {
			ErrorMessage(client, err.Error())
			return
		}

		discussion.BroadcastMessage(backend.WebsocketMessage{
			Action:  "new_message",
			Message: message.Message,
		})

	case "join_discussion":
		discussionId := message.DiscussionId
		if discussionId == "" {
			ErrorMessage(client, "Discussion ID cannot be empty")
			return
		}

		discussion, err := serverRegistry.GetDiscussion(discussionId)
		if err != nil {
			ErrorMessage(client, err.Error())
			return
		}

		discussion.AddClient(client)
		discussion.BroadcastMessage(backend.WebsocketMessage{
			Action:  "new_client",
			Message: fmt.Sprintf("A new client has joined the discussion %s", client.GetClient().ID),
		})
	default:
		// Do something
	}
}

func LiveDiscussionsHandler(w http.ResponseWriter, r *http.Request, serverRegistry backend.ServerRegistryInterface) {
	conn, err := CustomRequestUpgrader.Upgrade(w, r, nil)
	if err != nil {
		http.Error(w, "Failed to upgrade to websocket", http.StatusInternalServerError)
		return
	}
	defer conn.Close()

	conn.SetReadLimit(1024)
	conn.SetReadDeadline(time.Now().Add(60 * time.Second))

	conn.SetPongHandler(func(string) error {
		conn.SetReadDeadline(time.Now().Add(60 * time.Second))
		return nil
	})

	// Ping ticker: Sends a ping every 30s to keep the connection alive
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()

	go func() {
		for range ticker.C {
			if err := conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}()

	client := backend.NewWebsocketClient(uuid.NewString(), conn)
	err = serverRegistry.AddClient(client)

	defer func() {
		serverRegistry.RemoveClient(client)
		conn.Close()
	}()

	if err != nil {
		log.Println("❌ AddClient error:", err)
		return
	}

	client.SendJsonMessage(backend.WebsocketMessage{
		Action: "must_identify",
	})

	for {
		_, _, err := conn.ReadMessage()

		var message backend.WebsocketMessage
		err = client.ReadJsonMessage(&message)

		if err != nil {
			if IsWebsocketClose(err) {
				log.Println("🔌 Client disconnected:", client.GetClient().ID)
			} else {
				log.Println("❌ Read error:", err)
			}
			break
		}

		authenticationHandler(client, message, serverRegistry)
		discussionHandler(client, message, serverRegistry)
	}
}
