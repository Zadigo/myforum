package handlers

import (
	"log"
	"net/http"
)

type MessageApi struct{}

func (m *MessageApi) Moderate(w http.ResponseWriter, r *http.Request) {
	log.Print("POST called")
}
