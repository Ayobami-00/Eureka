package domain

import "github.com/Ayobami-00/Eureka/eureka-api-auth-service-go/utils/methods"

type User struct {
	ID        string `json:"id"`
	Name      string `json:"username"`
	Email     string `json:"email"`
	Password  string `json:"password"`
	CreatedAt int64  `json:"created_at"`
}

func GenerateUserID() string {

	return methods.GenerateRandomID()
}
