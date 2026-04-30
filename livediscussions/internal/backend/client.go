package backend

import "github.com/gorilla/websocket"

type User struct {
	ID       string `json:"id"`
	Username string `json:"username"`
}

type WebsocketClient struct {
	User User            `json:"user"`
	ID   string          `json:"id"`
	Conn *websocket.Conn `json:"-"`
}

func (c *WebsocketClient) SendJsonMessage(message WebsocketMessage) error {
	return c.Conn.WriteJSON(message)
}

func (c *WebsocketClient) ReadJsonMessage(v any) error {
	return c.Conn.ReadJSON(v)
}

func (c *WebsocketClient) GetClient() *WebsocketClient {
	return c
}

func (c *WebsocketClient) GetUser() *User {
	return &c.User
}

type WebsocketClientInterface interface {
	SendJsonMessage(message WebsocketMessage) error
	ReadJsonMessage(v any) error
	GetUser() *User
	GetClient() *WebsocketClient
}

func NewWebsocketClient(id string, conn *websocket.Conn) WebsocketClientInterface {
	return &WebsocketClient{
		ID:   id,
		Conn: conn,
		User: User{
			ID:       id,
			Username: "",
		},
	}
}

type WebsocketMessage struct {
	Action       string `json:"action"`
	Username     string `json:"username,omitempty"`
	DiscussionId string `json:"discussion_id,omitempty"`
	Message      string `json:"message,omitempty"`
}
