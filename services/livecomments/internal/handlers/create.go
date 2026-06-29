package handlers

import (
	"log"
	"net/http"
)

func (g *GenericHandler) CreateChatHandler(w http.ResponseWriter, r *http.Request) {
	// TODO: Implement the logic for creating a chat
	log.Print("CreateChatHandler called")
	// g.app.GetServerApp().CreateChat(games.STANDARD)
	// g.app.GetServerApp().CreateChat(games.EXTENSION)
}
