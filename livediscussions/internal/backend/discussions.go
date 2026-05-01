package backend

import (
	"context"
	"encoding/json"
	"log"
	"sync"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
)

type DiscussionSpace struct {
	ID           string                        `json:"id"`
	Name         string                        `json:"name"`
	Participants []WebsocketClientInterface    `json:"participants"`
	PubSub       *redis.PubSub                 `json:"-"`
	broadcast    chan WebsocketMessage         `json:"-"`
	register     chan WebsocketClientInterface `json:"-"`
	unregister   chan WebsocketClientInterface `json:"-"`
	mu           sync.Mutex                    `json:"-"`
}

func (d *DiscussionSpace) GetID() string {
	return d.ID
}

func (d *DiscussionSpace) AddClient(client WebsocketClientInterface) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	d.Participants = append(d.Participants, client)
	return nil
}

// RemoveClient removes a client from the discussion space. It is important to call
// this when a client disconnects to prevent memory leaks and ensure that the client
// is no longer part of the discussion.
func (d *DiscussionSpace) RemoveClient(client WebsocketClientInterface) error {
	d.mu.Lock()
	defer d.mu.Unlock()

	for i, c := range d.Participants {
		if c.GetClient().ID == client.GetClient().ID {
			d.Participants = append(d.Participants[:i], d.Participants[i+1:]...)
			break
		}
	}
	return nil
}

// DEPRECATED: StartBroadcaster starts a goroutine that listens for messages
// to broadcast to all clients in the discussion, as well as client registration
// and unregistration. This should be called when a new discussion space is created.
func (d *DiscussionSpace) StartBroadcaster() {
	go func() {
		for {
			select {
			case message := <-d.broadcast:
				d.mu.Lock()
				for _, client := range d.Participants {
					client.SendJsonMessage(message)
				}
				d.mu.Unlock()

				// case message := <-d.privateMessages:
				// 	// Handle private messages if needed
				// 	// This can be implemented by including a recipient ID in the message and sending it only to the intended recipient
				// 	recipientID := message.RecipientId
				// 	for _, client := range d.Participants {
				// 		if client.GetClient().ID == recipientID {
				// 			client.SendJsonMessage(message)
				// 			break
				// 		}
				// 	}
			case client := <-d.register:
				d.AddClient(client)
			case client := <-d.unregister:
				d.RemoveClient(client)
			}
		}
	}()
}

func (d *DiscussionSpace) BroadcastMessage(message WebsocketMessage) {
	d.broadcast <- message

	// d.mu.Lock()
	// defer d.mu.Unlock()

	// for _, client := range d.Participants {
	// 	client.SendJsonMessage(message)
	// }
}

// CreateRedisSubscriber creates a Redis Pub/Sub subscriber for the given discussion ID and stores it in the server registry.
func (d *DiscussionSpace) StartBroadcaster2(shutdownContext context.Context, redisClient *redis.Client, serverRegistry ServerRegistryInterface) *redis.PubSub {
	d.mu.Lock()
	defer d.mu.Unlock()

	pubSub := redisClient.Subscribe(context.Background(), "broadcast:"+d.ID)
	if pubSub == nil {
		return nil
	}

	// Start a goroutine to listen for messages on
	// the Redis Pub/Sub channel and broadcast them to all
	// clients in the discussion
	go func() {
	Mainloop:
		for {
			message := pubSub.Channel()

			select {
			case msg := <-message:
				var data WebsocketMessage

				err := json.Unmarshal([]byte(msg.Payload), &data)
				if err != nil {
					continue
				}

				d.mu.Lock()
				for _, client := range d.Participants {
					err := client.SendJsonMessage(WebsocketMessage{
						Action:       "broadcast_message",
						DiscussionId: d.ID,
						Payload:      data,
					})

					if err != nil {
						log.Printf("🟠 Error sending message to client %s: %v", client.GetClient().ID, err)
					}
				}
				d.mu.Unlock()
			case <-shutdownContext.Done():
				log.Printf("🟠 Shutting down broadcaster for discussion %s", d.ID)
				break Mainloop
			}

			// for msg := range message {
			// 	var data WebsocketMessage

			// 	err := json.Unmarshal([]byte(msg.Payload), &data)
			// 	if err != nil {
			// 		continue
			// 	}

			// 	for _, client := range d.Participants {
			// 		client.SendJsonMessage(WebsocketMessage{
			// 			Action:  "new_message",
			// 			Payload: data,
			// 		})
			// 	}
			// }
		}
	}()

	go func() {
		for {
			select {
			case client := <-d.register:
				d.AddClient(client)
			case client := <-d.unregister:
				d.RemoveClient(client)
			}
		}
	}()

	return pubSub
}

func (d *DiscussionSpace) BroadcastMessage2(redisClient *redis.Client, message RedisWebsocketMessage) error {
	data, err := json.Marshal(message)
	if err != nil {
		return err
	}

	cmd := redisClient.Publish(context.Background(), "broadcast:"+d.ID, data)
	return cmd.Err()
}

type DiscussionSpaceInterface interface {
	AddClient(client WebsocketClientInterface) error
	RemoveClient(client WebsocketClientInterface) error
	BroadcastMessage(message WebsocketMessage)
	StartBroadcaster()
	StartBroadcaster2(shutdownContext context.Context, redisClient *redis.Client, serverRegistry ServerRegistryInterface) *redis.PubSub
	BroadcastMessage2(redisClient *redis.Client, message RedisWebsocketMessage) error
	GetID() string
}

// NewDiscussionSpace creates a new discussion space with a unique ID
// and starts its broadcaster goroutine.
func NewDiscussionSpace(name string) DiscussionSpaceInterface {
	ds := &DiscussionSpace{
		ID:           uuid.NewString(),
		Name:         name,
		Participants: []WebsocketClientInterface{},
		broadcast:    make(chan WebsocketMessage, 100),
		register:     make(chan WebsocketClientInterface, 100),
		unregister:   make(chan WebsocketClientInterface, 100),
	}
	ds.StartBroadcaster()
	return ds
}
