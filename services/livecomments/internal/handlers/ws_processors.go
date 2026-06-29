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

func ChatMessageProcessor(options ProcessorOptions) {
	chatId := options.Ctx.Value("chatId")

	switch options.Message.Action {
	case models.JOIN:
		// Handle join chat logic here
		options.App.GetServerApp().JoinChat(options.Conn, chatId.(string))
	case models.SEND_MESSAGE:
		// Handle send message logic here
		// options.App.GetServerApp().NotifyAll("chat-uuid")
	default:
		options.Errors = append(options.Errors, "Unrecognized action for ChatMessageProcessor")
	}
}

func ErrorProcessor(conn *websocket.Conn, errors []string) {
	if len(errors) > 0 {
		for _, err := range errors {
			conn.WriteJSON(map[string]string{"error": err})
		}
	}
}
