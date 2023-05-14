package middleware

import (
	"context"
	"net/http"
	"strings"

	"github.com/Ayobami-00/Eureka/pkg/auth"
	"github.com/Ayobami-00/Eureka/pkg/auth/pb"
	"github.com/gin-gonic/gin"
)

type AuthMiddlewareConfig struct {
	svc *auth.ServiceClient
}

func InitAuthMiddleware(svc *auth.ServiceClient) AuthMiddlewareConfig {
	return AuthMiddlewareConfig{svc}
}

func (c *AuthMiddlewareConfig) AuthRequired(ctx *gin.Context) {
	authorizationHeader := ctx.Request.Header.Get("token")

	if authorizationHeader == "" {
		ctx.JSON(http.StatusUnauthorized, gin.H{})
		return
	}

	token := strings.Split(authorizationHeader, "Bearer ")

	if len(token) < 2 {
		ctx.JSON(http.StatusUnauthorized, gin.H{})
		return
	}

	res, err := c.svc.Client.Validate(context.Background(), &pb.ValidateRequest{
		Token: token[1],
	})

	if err != nil || res.Status != http.StatusOK {
		ctx.JSON(http.StatusUnauthorized, gin.H{})
		return
	}

	ctx.Set("userId", res.UserId)

	ctx.Next()
}
