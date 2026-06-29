package handlers

import (
	"context"

	"github.com/Zadigo/livecomments/internal/models"
	"github.com/gorilla/websocket"
)

type ProcessorOptions struct {
	Ctx     context.Context
	App     models.AppInterface
	Conn    *websocket.Conn
	Message models.WebsocketMessage
	Errors  []string
}

// AuthMessageProcessor processes messages that require identification
func AuthMessageProcessor(options ProcessorOptions) {
	switch options.Message.Action {
	case models.MUST_IDENTIFY:
		// Handle identification logic here
	default:
		options.Errors = append(options.Errors, "Unrecognized action for AuthMessageProcessor")
	}
}

func GameMessageProcessor(options ProcessorOptions) {
	gameId := options.Ctx.Value("gameId")

	switch options.Message.Action {
	case models.JOIN:
		// Handle join game logic here
		options.App.GetServerApp().JoinChat(options.Conn, gameId.(string))
	case models.SEND_MESSAGE:
		// Handle start game logic here
		// options.App.GetServerApp().NotifyAll("game-uuid")
	default:
		options.Errors = append(options.Errors, "Unrecognized action for GameMessageProcessor")
	}
}


func ErrorProcessor(conn *websocket.Conn, errors []string) {
	if len(errors) > 0 {
		for _, err := range errors {
			conn.WriteJSON(map[string]string{"error": err})
		}
	}
}
