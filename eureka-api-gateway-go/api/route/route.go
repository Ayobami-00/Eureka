package route

import (
	"time"

	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/bootstrap"
	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/pkg/auth"
	"github.com/gin-gonic/gin"
)

func Setup(env *bootstrap.Env, timeout time.Duration, gin *gin.Engine) {

	// Auth Service
	auth.RegisterRoutes(gin, env)

}
