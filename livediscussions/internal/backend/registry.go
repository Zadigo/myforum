package backend

import (
	"fmt"
	"sync"

	"github.com/go-co-op/gocron"
	"github.com/redis/go-redis/v9"
)

type ServerRegistry struct {
	Clients     map[string]*WebsocketClient         `json:"clients"`
	Discussions map[string]DiscussionSpaceInterface `json:"discussions"`
	RedisClient *redis.Client                       `json:"-"`
	PubSub      *redis.PubSub                       `json:"-"`
	scheduler   *gocron.Scheduler                   `json:"-"`
	broadcast   chan WebsocketMessage               `json:"-"`
	mu          sync.Mutex                          `json:"-"`
}

// SetScheduler sets the scheduler for the server registry. This is used for
// scheduling cleanup tasks and other periodic operations.
func (r *ServerRegistry) SetScheduler(scheduler *gocron.Scheduler) {
	r.scheduler = scheduler
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

	// IMPORTANT: Also remove client from any
	// discussions they are part of
	for _, discussion := range r.Discussions {
		discussion.RemoveClient(client)
	}

	return nil
}

// DEPRECATED: This is the old BroadcastMessage function that uses the Golang channel for
// broadcasting messages to clients. It is now replaced by the Redis Pub/Sub mechanism,
// but we keep it here for reference and potential fallback.
func (r *ServerRegistry) BroadcastMessage(message WebsocketMessage) {
	r.broadcast <- message
}

func (r *ServerRegistry) GetRegistry() *ServerRegistry {
	return r
}

// GetDiscussion returns the list of clients in a discussion. If the discussion doesn't exist, it returns nil.
func (r *ServerRegistry) GetDiscussion(discussionId string) (DiscussionSpaceInterface, error) {
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
	GetDiscussion(discussionId string) (DiscussionSpaceInterface, error)
	GetRegistry() *ServerRegistry
	AddDiscussionSpace(discussionSpace DiscussionSpaceInterface) error
}

func NewServerRegistry(redisClient *redis.Client) ServerRegistryInterface {
	return &ServerRegistry{
		Clients:     make(map[string]*WebsocketClient),
		Discussions: make(map[string]DiscussionSpaceInterface),
		broadcast:   make(chan WebsocketMessage, 100),
		RedisClient: redisClient,
	}
}
