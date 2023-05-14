package routes

import (
	"context"
	"net/http"

	"github.com/Ayobami-00/Eureka/pkg/auth/pb"
	"github.com/Ayobami-00/Eureka/utils/api_response"
	"github.com/gin-gonic/gin"
)

type RegisterRequestBody struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

func Register(ctx *gin.Context, c pb.AuthServiceClient) {
	reqBody := RegisterRequestBody{}

	if err := ctx.BindJSON(&reqBody); err != nil {
		ctx.JSON(http.StatusBadRequest, api_response.BaseErrorResponse(err.Error()))
		return
	}

	res, err := c.Register(context.Background(), &pb.RegisterRequest{
		Email:    reqBody.Email,
		Password: reqBody.Password,
	})

	if err != nil {
		ctx.JSON(http.StatusBadGateway, api_response.BaseErrorResponse(err.Error()))
		return
	}

	ctx.JSON(http.StatusCreated, &res)
}
