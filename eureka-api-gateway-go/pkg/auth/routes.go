package auth

import (
	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/bootstrap"
	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/pkg/auth/routes"
	"github.com/gin-gonic/gin"
)

func RegisterRoutes(r *gin.Engine, env *bootstrap.Env) *ServiceClient {
	svc := &ServiceClient{
		Client: InitServiceClient(env),
	}

	routes := r.Group("/auth")
	routes.POST("/register", svc.Register)
	routes.POST("/login", svc.Login)
	routes.POST("/token", svc.RenewToken)

	return svc
}

func (svc *ServiceClient) Register(ctx *gin.Context) {
	routes.Register(ctx, svc.Client)
}

func (svc *ServiceClient) Login(ctx *gin.Context) {
	routes.Login(ctx, svc.Client)
}

func (svc *ServiceClient) RenewToken(ctx *gin.Context) {
	routes.RenewToken(ctx, svc.Client)
}
