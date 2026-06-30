package chat

import (
	"context"
	"log"
	"sync/atomic"

	"github.com/Zadigo/livecomments/internal/chat/chats"
	"github.com/Zadigo/livecomments/internal/models"
)

// ChatAApp is the main chat server application that manages
// chat sessions, user interactions, and chat state. It is designed to be independent
// of the main chi server, allowing for flexible deployment and management
// of chat functionality.
type ChatApp struct {
	ctx       context.Context
	Chats     map[string]chats.ChatInterface    `json:"chats"`
	Users     map[string]*chats.WebsocketClient `json:"users"`
	IsRunning atomic.Bool                       `json:"isRunning"`
}

func (c *ChatApp) AddUser(client *chats.WebsocketClient) {
	c.Users[client.User.Id] = client
}

func (c *ChatApp) RemoveUser(client *chats.WebsocketClient) {
	delete(c.Users, client.User.Id)
}

// Create initializes a new chat session based on the provided options.
// It sets up the chat environment, prepares the necessary resources,
// and configures the chat session according to the specified parameters.
func (c *ChatApp) Create(options models.ChatAppOptions) chats.ChatInterface {
	chat := chats.CreateChat(options)
	c.Chats[chat.GetUuid()] = chat
	return chat
}

func (c *ChatApp) GetChat(chatUuid string) chats.ChatInterface {
	return c.Chats[chatUuid]
}

// Start begins the chat application and enters a loop
// to manage chat sessions and user interactions.
func (c *ChatApp) Start() {
	log.Printf("🔵 Starting chat server...")
	c.IsRunning.Store(true)

	for {
		if !c.IsRunning.Load() {
			break
		}
	}
}

func (c *ChatApp) Stop() {
	log.Printf("🔴 Stopping chat server...")
	c.IsRunning.Store(false)
}

// NewChatServer creates a new instance of the chat server application
// based on the specified chat type (standard or extension). This server
// is independent of the main chi server and can be used to manage chat sessions,
// handle player interactions, and maintain chat state.
func NewChatServer(ctx context.Context, baseDir string, options models.ChatAppOptions) *ChatApp {
	return &ChatApp{
		ctx:       ctx,
		Chats:     make(map[string]chats.ChatInterface),
		Users:     make(map[string]*chats.WebsocketClient),
		IsRunning: atomic.Bool{},
	}
}
