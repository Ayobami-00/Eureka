package main

import (
	"time"

	"github.com/Ayobami-00/Eureka/api/route"
	"github.com/Ayobami-00/Eureka/bootstrap"
	"github.com/gin-gonic/gin"
)

func main() {

	app := bootstrap.App()

	env := app.Env

	timeout := time.Duration(env.ContextTimeout) * time.Second

	gin := gin.Default()

	route.Setup(env, timeout, gin)

}
