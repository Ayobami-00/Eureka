package routes

import (
	"context"
	"net/http"

	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/pkg/auth/pb"
	"github.com/Ayobami-00/Eureka/eureka-api-gateway-go/utils/api_response"
	"github.com/gin-gonic/gin"
)

type RegisterRequestBody struct {
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

func Register(ctx *gin.Context, c pb.AuthServiceClient) {
	reqBody := RegisterRequestBody{}

	if err := ctx.BindJSON(&reqBody); err != nil {
		ctx.JSON(http.StatusBadRequest, api_response.BaseErrorResponse(err.Error()))
		return
	}

	res, _ := c.Register(context.Background(), &pb.RegisterRequest{
		Username: reqBody.Username,
		Email:    reqBody.Email,
		Password: reqBody.Password,
	})

	api_response.Respond(ctx, res)
}
