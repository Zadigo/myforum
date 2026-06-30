package chats

import "github.com/Zadigo/livecomments/internal/models"

type ChatInterface interface {
	// Start initializes and starts the chat server application.
	// It checks if the chat instance is properly initialized, prepares the chat state,
	// and then starts the chat logic.
	SetOptions(options models.ChatAppOptions)
	GetUuid() string
}
