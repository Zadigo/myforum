package handlers

import (
	"net/http"

	"github.com/Zadigo/livecomments/internal/chat/chats"
)

func (g *GenericHandler) CreateChatHandler(w http.ResponseWriter, r *http.Request) {
	g.app.GetServerApp().CreateChat(chats.STANDARD)
}
