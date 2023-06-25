package domain

type Session struct {
	ID           string `json:"id"`
	Name         string `json:"username"`
	RefreshToken string `json:"refresh_token"`
	UserAgent    string `json:"user_agent"`
	ClientIp     string `json:"client_ip"`
	IsBlocked    bool   `json:"is_blocked"`
	ExpiresAt    int64  `json:"expires_at"`
}
