package backend

import (
	"fmt"
	"sync"

	"github.com/redis/go-redis/v9"
)

type ServerRegistry struct {
	Clients     map[string]*WebsocketClient
	Discussions map[string]*DiscussionSpace
	RedisClient *redis.Client
	broadcast   chan WebsocketMessage
	mu          sync.Mutex
}

func (r *ServerRegistry) AddDiscussionSpace(discussionSpace DiscussionSpaceInterface) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.Discussions[discussionSpace.(*DiscussionSpace).ID] = discussionSpace.(*DiscussionSpace)
	return nil
}

func (r *ServerRegistry) GetClient(client WebsocketClientInterface) (*WebsocketClient, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	c, exists := r.Clients[client.(*WebsocketClient).ID]
	if !exists {
		return nil, fmt.Errorf("Client with ID %s does not exist", client.(*WebsocketClient).ID)
	}

	return c, nil
}

func (r *ServerRegistry) AddClient(client WebsocketClientInterface) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.Clients[client.(*WebsocketClient).ID] = client.(*WebsocketClient)
	return nil
}

func (r *ServerRegistry) RemoveClient(client WebsocketClientInterface) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	delete(r.Clients, client.(*WebsocketClient).ID)
	return nil
}

func (r *ServerRegistry) BroadcastMessage(message WebsocketMessage) {
	r.broadcast <- message
}

func (r *ServerRegistry) GetRegistry() *ServerRegistry {
	return r
}

// GetDiscussion returns the list of clients in a discussion. If the discussion doesn't exist, it returns nil.
func (r *ServerRegistry) GetDiscussion(discussionId string) (*DiscussionSpace, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	discussion, exists := r.Discussions[discussionId]
	if !exists {
		return nil, fmt.Errorf("Discussion with ID %s does not exist", discussionId)
	}

	return discussion, nil
}

type ServerRegistryInterface interface {
	AddClient(client WebsocketClientInterface) error
	GetClient(client WebsocketClientInterface) (*WebsocketClient, error)
	RemoveClient(client WebsocketClientInterface) error
	BroadcastMessage(message WebsocketMessage)
	GetDiscussion(discussionId string) (*DiscussionSpace, error)
	GetRegistry() *ServerRegistry
	AddDiscussionSpace(discussionSpace DiscussionSpaceInterface) error
}

func NewServerRegistry(redisClient *redis.Client) ServerRegistryInterface {
	return &ServerRegistry{
		Clients:     make(map[string]*WebsocketClient),
		Discussions: make(map[string]*DiscussionSpace),
		broadcast:   make(chan WebsocketMessage, 100),
		RedisClient: redisClient,
	}
}
