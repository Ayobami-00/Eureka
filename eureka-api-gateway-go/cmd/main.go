package main

import (
	"context"
	"time"

	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/api/route"
	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/bootstrap"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	ginadapter "github.com/awslabs/aws-lambda-go-api-proxy/gin"
	"github.com/gin-gonic/gin"
)

var ginLambda *ginadapter.GinLambda

func main() {

	app := bootstrap.App()

	env := app.Env

	timeout := time.Duration(env.ContextTimeout) * time.Second

	g := gin.Default()

	route.Setup(env, timeout, g)

	if env.AppEnv == "PRODUCTION" {

		gin.SetMode(gin.ReleaseMode)

		ginLambda = ginadapter.New(g)

		lambda.Start(Handler)

	} else {

		g.Run(env.ServerPort)
	}

}

func Handler(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	return ginLambda.ProxyWithContext(ctx, request)
}
