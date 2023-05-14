package auth

import (
	"github.com/Ayobami-00/Eureka/bootstrap"
	"github.com/Ayobami-00/Eureka/pkg/auth/routes"
	"github.com/gin-gonic/gin"
)

func RegisterRoutes(r *gin.Engine, env *bootstrap.Env) *ServiceClient {
	svc := &ServiceClient{
		Client: InitServiceClient(env),
	}

	routes := r.Group("/auth")
	routes.POST("/register", svc.Register)
	routes.POST("/login", svc.Login)

	return svc
}

func (svc *ServiceClient) Register(ctx *gin.Context) {
	routes.Register(ctx, svc.Client)
}

func (svc *ServiceClient) Login(ctx *gin.Context) {
	routes.Login(ctx, svc.Client)
}
