package handlers

import (
	"log"
	"net/http"
)

type Message struct{}

func (m *Message) Moderate(w http.ResponseWriter, r *http.Request) {
	log.Print("POST called")
}
