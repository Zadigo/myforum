package backend

import "github.com/gorilla/websocket"

type User struct {
	ID       string `json:"id"`
	Username string `json:"username"`
}

type WebsocketClient struct {
	User
	ID   string          `json:"id"`
	Conn *websocket.Conn `json:"-"`
}

type WebsocketClientInterface interface {
	SendJsonMessage(message WebsocketMessage) error
	ReadJsonMessage(v any) error
}

func (c *WebsocketClient) SendJsonMessage(message WebsocketMessage) error {
	return c.Conn.WriteJSON(message)
}

func (c *WebsocketClient) ReadJsonMessage(v any) error {
	return c.Conn.ReadJSON(v)
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
