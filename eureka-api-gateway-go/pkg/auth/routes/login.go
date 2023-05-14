package routes

import (
	"context"
	"net/http"

	"github.com/Ayobami-00/Eureka/pkg/auth/pb"
	"github.com/Ayobami-00/Eureka/utils/api_response"
	"github.com/gin-gonic/gin"
)

type LoginRequestBody struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

func Login(ctx *gin.Context, c pb.AuthServiceClient) {

	reqBody := LoginRequestBody{}

	if err := ctx.BindJSON(&reqBody); err != nil {
		ctx.JSON(http.StatusBadRequest, api_response.BaseErrorResponse(err.Error()))
		return
	}

	res, err := c.Login(context.Background(), &pb.LoginRequest{
		Email:    reqBody.Email,
		Password: reqBody.Password,
	})

	if err != nil {
		ctx.JSON(http.StatusBadGateway, api_response.BaseErrorResponse(err.Error()))
		return
	}

	ctx.JSON(http.StatusOK, &res)

}
