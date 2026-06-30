package chats

import (
	"context"

	"github.com/Zadigo/livecomments/internal/models"
)

type ChatMessage struct {
	Uuid     string `json:"uuid"`
	Parent   string `json:"parent"`
	Username string `json:"username"`
	Message  string `json:"message"`
}

// BaseChat holds the common properties and
// methods for all chat types.
type BaseChat struct {
	Uuid          string
	ctx           context.Context
	users         map[string]*WebsocketClient
	options       models.ChatAppOptions
	messagesQueue chan ChatMessage
}

func (bc *BaseChat) SetOptions(options models.ChatAppOptions) {
	bc.options = options
}

func (bc *BaseChat) GetUuid() string {
	return bc.Uuid
}
