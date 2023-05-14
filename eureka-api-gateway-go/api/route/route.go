package route

import (
	"fmt"
	"time"

	"github.com/Ayobami-00/Eureka/bootstrap"
	"github.com/Ayobami-00/Eureka/pkg/auth"
	"github.com/gin-gonic/gin"
)

func Setup(env *bootstrap.Env, timeout time.Duration, gin *gin.Engine) {

	// Auth Service
	authSvc := *auth.RegisterRoutes(gin, env)
	fmt.Println(authSvc)

}
