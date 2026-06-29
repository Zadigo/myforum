package chat

import (
	"context"

	"github.com/Zadigo/livecomments/internal/models"
)

type ChatApp struct {
	ctx          context.Context
	Chat         ChatInterface               `json:"chat"`
	CurrentRound int                         `json:"currentRound"`
	Players      map[string]*WebsocketClient `json:"players"`
}

func (c *ChatApp) AddUser(player *WebsocketClient) error {
	return nil
}

func (c *ChatApp) Create(options models.ChatOptions) {
}
