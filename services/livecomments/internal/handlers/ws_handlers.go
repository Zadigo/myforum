package handlers

import (
	"log"
	"net/http"

	"github.com/Zadigo/livecomments/internal/models"
)

func (g *GenericHandler) JoinChatHandler(w http.ResponseWriter, r *http.Request) {
	log.Print("JoinGameHandler called")

	conn, err := CustomRequestUpgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("❌ Failed to upgrade connection: %v", err)
		http.Error(w, "Failed to upgrade connection", http.StatusInternalServerError)
		return
	}

	WsMiddleware(conn)

	defer func() {
		conn.Close()
	}()

	for {
		var message models.WebsocketMessage
		err = conn.ReadJSON(&message)

		if err != nil {
			log.Println("❌ Read error:", err)
			break
		}

		options := ProcessorOptions{Conn: conn, App: g.app, Message: message, Errors: []string{}}
		AuthMessageProcessor(options)
		ChatMessageProcessor(options)
	}
}
